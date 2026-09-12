from pathlib import Path
import requests

download_dir=Path(__file__).parent / "CSVfiles"
download_dir.mkdir(parents=True, exist_ok=True)

urls = [
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/N0CceRlquaf9q85PK759WQ/regression-dataset.csv",
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/7J73m6Nsz-vmojwab91gMA/classification-dataset.csv",
]

for url in urls:
    file_path = download_dir / url.split("/")[-1]

    response = requests.get(url)
    response.raise_for_status()

    file_path.write_bytes(response.content)
    print(f"Downloaded: {file_path}")