import os
import boto3
from botocore.exceptions import NoCredentialsError


def upload_to_s3(local_path, bucket_name, s3_folder):
    """
    Uploads files and folders from a given local path to an S3 bucket.

    :param local_path: The local directory or file path to upload.
    :param bucket_name: The name of the S3 bucket.
    :param s3_folder: The folder path in the S3 bucket where files will be uploaded.
    """
    s3_client = boto3.client('s3')

    if not os.path.exists(local_path):
        print(f"Error: Path '{local_path}' does not exist.")
        return
    s3_client.upload_file('buildspec.yml', bucket_name,'buildspec.yml')
    for root, dirs, files in os.walk(local_path):
        for file in files:
            local_file_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_file_path, local_path)
            s3_file_path = os.path.join(s3_folder, relative_path).replace("\\", "/")  # Normalize for S3

            try:
                print(f"Uploading {local_file_path} to s3://{bucket_name}/{s3_file_path}")
                s3_client.upload_file(local_file_path, bucket_name, s3_file_path)
            except NoCredentialsError:
                print("Error: AWS credentials not found.")
                return
            except Exception as e:
                print(f"Error uploading {local_file_path}: {e}")
                return

    print("Upload complete.")


# Example Usage
if __name__ == "__main__":
    local_path = "TestConfiguration"  # Replace with your local folder path
    bucket_name = "autocount-config"  # Replace with your S3 bucket name
    s3_folder = "test_configuration"  # Replace with your S3 folder path (use "" for root)

    upload_to_s3(local_path, bucket_name, s3_folder)
