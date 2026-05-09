import json
import os
from typing import List

def search_internal_codebase(query: str) -> List[dict]:
    """
    Mock MCP Tool: Searches local codebase for architectural patterns.
    In a real scenario, this would use 'grep' or a vector search over the repo.
    """
    # Simulated search results
    codebase_knowledge = [
        {
            "file": "services/payment/config.java",
            "snippet": "public class PaymentConfig { private String encryptionKeyId = 'alias/default'; }",
            "hint": "Uses default KMS alias. Recommendation: Switch to CMK for HIPAA."
        },
        {
            "file": "infrastructure/terraform/vpc.tf",
            "snippet": "resource 'aws_vpc' 'main' { cidr_block = '10.0.0.0/16' }",
            "hint": "VPC CIDR found. Ensure subnets are isolated."
        }
    ]
    
    # Simple keyword filter for the mock
    results = [res for res in codebase_knowledge if query.lower() in res["snippet"].lower() or query.lower() in res["hint"].lower()]
    return results if results else [{"status": "No patterns found for query."}]

if __name__ == "__main__":
    # Test the mock tool
    print(json.dumps(search_internal_codebase("encryption"), indent=2))
