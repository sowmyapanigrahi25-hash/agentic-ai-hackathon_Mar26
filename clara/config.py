import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

# Required environment variables
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
COMPLIANCE_KB_ID = os.getenv('COMPLIANCE_KB_ID')
BEDROCK_MODEL_ID = os.getenv('BEDROCK_MODEL_ID', 'anthropic.claude-3-7-sonnet-20250219')

# Agent thresholds (hardcoded constants)
CONFIDENCE_THRESHOLD = 0.5
RISK_SCORE_THRESHOLD = 0.85
SLA_BREACH_HOURS = 72


def validate_config():
    """
    Validates that all required configuration variables are set.
    Raises ValueError if any required variable is missing.
    """
    missing_vars = []
    
    if not S3_BUCKET_NAME:
        missing_vars.append('S3_BUCKET_NAME')
    
    if not COMPLIANCE_KB_ID:
        missing_vars.append('COMPLIANCE_KB_ID')
    
    if missing_vars:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing_vars)}\n"
            f"Please set these variables in your environment or create a .env file.\n"
            f"Example .env file:\n"
            f"  S3_BUCKET_NAME=your-bucket-name\n"
            f"  AWS_REGION=us-east-1\n"
            f"  COMPLIANCE_KB_ID=your-kb-id\n"
            f"  BEDROCK_MODEL_ID=anthropic.claude-3-7-sonnet-20250219"
        )
    
    print("✓ Configuration validated successfully")
    print(f"  S3 Bucket: {S3_BUCKET_NAME}")
    print(f"  AWS Region: {AWS_REGION}")
    print(f"  Compliance KB ID: {COMPLIANCE_KB_ID}")
    print(f"  Bedrock Model: {BEDROCK_MODEL_ID}")
    print(f"  Confidence Threshold: {CONFIDENCE_THRESHOLD}")
    print(f"  Risk Score Threshold: {RISK_SCORE_THRESHOLD}")
    print(f"  SLA Breach Hours: {SLA_BREACH_HOURS}")


if __name__ == '__main__':
    validate_config()
