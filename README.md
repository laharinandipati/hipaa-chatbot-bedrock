# HIPAA-Compliant Chatbot (AWS Lambda + Amazon Bedrock)

This is a minimal example project demonstrating a HIPAA-friendly chatbot architecture using:
- AWS API Gateway -> AWS Lambda (pre-process: PHI scrubbing)
- Amazon Bedrock (LLM inference) with masked input
- AWS Lambda (post-process: placeholder restore)


## Features
- Simple PHI masking (dates, first names) in `src/masker.py`
- Lambda handler in `src/app.py`
- Unit tests for masking logic
- AWS SAM template for local testing & deployment
- Example API Gateway event to test locally

## Quick Start

### Prerequisites
- Python 3.11+
- AWS CLI configured (`aws configure`)
- AWS SAM CLI: https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html

### Setup
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Deploy (SAM)
```bash
sam deploy --guided
```
Follow the prompts to create a new stack and grant Bedrock access to the Lambda role (see IAM notes below).

## Environment Variables
- `BEDROCK_MODEL_ID` (e.g., `anthropic.claude-3-haiku-20240307`)
- Optional: `PLACEHOLDER_NAME`, `PLACEHOLDER_DATE` to customize masking tokens.

## IAM / Permissions
- The Lambda execution role must have `bedrock:InvokeModel` permission for the chosen model.
- Consider adding VPC, KMS CMK, and CloudWatch logs policies as required by your environment.
- For compliance, log redaction is recommended before printing any user content.

## DISCLAIMER
This sample is for educational purposes only. You are responsible for ensuring HIPAA compliance for your environment, data handling, and logging practices.
