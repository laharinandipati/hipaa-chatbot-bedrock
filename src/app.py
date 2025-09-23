import json
import os
import boto3

from masker import mask_phi
from postprocess import restore_placeholders

# Bedrock runtime client
bedrock = boto3.client("bedrock-runtime")

MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-haiku-20240307")
PLACEHOLDER_NAME = os.getenv("PLACEHOLDER_NAME", "[NAME]")
PLACEHOLDER_DATE = os.getenv("PLACEHOLDER_DATE", "[DATE]")

def _invoke_bedrock(prompt: str) -> str:
    """Invoke Bedrock model with a simple prompt. Adjust body according to the model's API."""
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 256,
        "messages": [
            {"role": "user", "content": [{"type": "text", "text": prompt}]}
        ]
    })
    response = bedrock.invoke_model(
        modelId=MODEL_ID,
        contentType="application/json",
        accept="application/json",
        body=body,
    )
    payload = json.loads(response["body"].read())
    # Extract text according to Anthropic response schema
    parts = payload.get("content", [])
    if parts and isinstance(parts, list) and "text" in parts[0]:
        return parts[0]["text"]
    # Fallback for other models/schemas
    return json.dumps(payload)

def lambda_handler(event, context):
    # Example expects API Gateway HTTP API with query string param 'q' OR JSON body { "q": "..." }
    user_input = None
    if event.get("queryStringParameters") and "q" in event["queryStringParameters"]:
        user_input = event["queryStringParameters"]["q"]
    else:
        try:
            body = json.loads(event.get("body") or "{}")
            user_input = body.get("q")
        except json.JSONDecodeError:
            user_input = None

    if not user_input:
        return {"statusCode": 400, "body": json.dumps({"error": "Missing 'q' parameter"})}

    # Mask PHI before sending to LLM
    masked_text, mapping = mask_phi(user_input, name_token=PLACEHOLDER_NAME, date_token=PLACEHOLDER_DATE)

    # Call LLM with masked text
    llm_output = _invoke_bedrock(masked_text)

    # Restore placeholders (only static tokens from mapping)
    final_output = restore_placeholders(llm_output, mapping)

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "masked_input": masked_text,
            "llm_output": llm_output,
            "final_output": final_output
        }),
    }
