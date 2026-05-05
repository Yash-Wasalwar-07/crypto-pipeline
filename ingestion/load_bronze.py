# ingestion/load_bronze.py

import os
from datetime import datetime, timezone
from azure.storage.filedatalake import DataLakeServiceClient
from dotenv import load_dotenv

load_dotenv()

def get_adls_client():
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    return DataLakeServiceClient.from_connection_string(connection_string)

def upload_to_bronze(local_file_path: str) -> str:
    client = get_adls_client()
    container_name = os.getenv("AZURE_CONTAINER_NAME", "bronze")

    # Build remote path: bronze/crypto/year=2026/month=05/day=05/filename.json
    now = datetime.now(timezone.utc)
    remote_path = (
        f"crypto/"
        f"year={now.strftime('%Y')}/"
        f"month={now.strftime('%m')}/"
        f"day={now.strftime('%d')}/"
        f"{os.path.basename(local_file_path)}"
    )

    file_system_client = client.get_file_system_client(container_name)
    file_client = file_system_client.get_file_client(remote_path)

    with open(local_file_path, "rb") as f:
        data = f.read()
        file_client.upload_data(data, overwrite=True)

    print(f"✅ Uploaded to Bronze: {container_name}/{remote_path}")
    return remote_path

if __name__ == "__main__":
    # Find the latest raw file
    raw_dir = "data/raw"
    files = sorted(os.listdir(raw_dir))
    if not files:
        print("❌ No raw files found. Run fetch_crypto.py first.")
        exit(1)

    latest_file = os.path.join(raw_dir, files[-1])
    print(f"Uploading {latest_file} to Azure Data Lake Bronze layer...")
    upload_to_bronze(latest_file)