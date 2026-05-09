import json
from typing import Dict

def check_data_governance_rules(region: str, compliance_standard: str) -> Dict:
    """
    Mock MCP Tool: Checks specific cloud governance rules for a region and standard.
    In a real scenario, this would query a live AWS/Azure policy API.
    """
    rules = {
        "us-east-1": {
            "HIPAA": {
                "status": "Warning",
                "reason": "Encryption at rest must use customer-managed keys (CMK).",
                "action_required": "Enable AWS KMS with CMK."
            },
            "SOC2": {
                "status": "Passed",
                "reason": "Region meets all audit requirements.",
                "action_required": "None"
            }
        },
        "eu-central-1": {
            "GDPR": {
                "status": "Passed",
                "reason": "Data residency compliant.",
                "action_required": "Ensure Data Processing Agreement (DPA) is signed."
            }
        }
    }
    
    # Return specific rule or a default "Manual Review"
    return rules.get(region, {}).get(compliance_standard, {
        "status": "Manual Review Required",
        "reason": f"No automated rules found for {region}/{compliance_standard}",
        "action_required": "Contact Security & Compliance Team."
    })

if __name__ == "__main__":
    # Test the mock tool
    print(json.dumps(check_data_governance_rules("us-east-1", "HIPAA"), indent=2))
