import os
from pathlib import Path
import boto3

def download_model_from_s3():
    model_env_path = os.getenv("LOCAL_MODEL_PATH")
    if model_env_path:
        local_path = Path(model_env_path)
    else:
        local_path = Path(__file__).parent.joinpath("models", "pawpredict_model.keras")

    # Ensure directory exists
    local_path.parent.mkdir(parents=True, exist_ok=True)

    # If model already exists, reuse it
    if local_path.exists():
        print("Model already exists locally.")
        return str(local_path)

    bucket = os.getenv("S3_BUCKET")
    key = os.getenv("S3_MODEL_KEY")
    if not bucket or not key:
        print("S3_BUCKET or S3_MODEL_KEY not set in environment. Skipping S3 download.")
        return str(local_path)

    print("Downloading model from S3...")
    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-east-1"),
    )

    s3.download_file(
        bucket,
        key,
        str(local_path)
    )

    print("Model downloaded successfully.")
    return str(local_path)
