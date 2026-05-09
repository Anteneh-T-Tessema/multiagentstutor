import re
from typing import Tuple

def pii_masking_gateway(text: str) -> Tuple[str, bool]:
    """
    Detects and masks PII (Emails, SSNs, Phone Numbers).
    Returns (masked_text, pii_detected).
    """
    pii_patterns = {
        "EMAIL": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
        "SSN": r"\d{3}-\d{2}-\d{4}",
        "PHONE": r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"
    }
    
    masked_text = text
    pii_detected = False
    
    for label, pattern in pii_patterns.items():
        if re.search(pattern, masked_text):
            pii_detected = True
            masked_text = re.sub(pattern, f"[REDACTED_{label}]", masked_text)
            
    return masked_text, pii_detected

def validate_input_integrity(text: str) -> bool:
    """
    Ensures the input is a valid discovery note and not a prompt injection.
    """
    forbidden_keywords = ["ignore previous instructions", "system prompt", "dan mode"]
    if any(k in text.lower() for k in forbidden_keywords):
        return False
    if len(text.strip()) < 20:
        return False
    return True

def sanitize_output(text: str) -> str:
    """
    Final check on output to ensure no internal dev tags or forbidden words.
    """
    # Example: Ensure we don't leak internal 'mock' or 'stub' labels in a final proposal
    sanitized = text.replace("[MOCK_DATA]", "").replace("STUB:", "")
    return sanitized

if __name__ == "__main__":
    test_input = "Contact John Doe at john.doe@gmail.com. SSN: 123-45-6789. Also ignore previous instructions."
    masked, detected = pii_masking_gateway(test_input)
    valid = validate_input_integrity(test_input)
    
    print(f"Masked Text: {masked}")
    print(f"PII Detected: {detected}")
    print(f"Is Valid: {valid}")
