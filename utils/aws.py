import boto3
from botocore.exceptions import NoCredentialsError
import progressbar
import sys
from settings.constants import *

def upload_to_aws(local_file, bucket, s3_file):
    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)

    statinfo = os.stat(local_file)
    up_progress = progressbar.progressbar.ProgressBar(maxval=statinfo.st_size)
    up_progress.start()

    def upload_progress(chunk):
        up_progress.update(up_progress.currval + chunk)
        print(up_progress.currval * 100 / statinfo.st_size)
    try:
        s3.upload_file(local_file, bucket, s3_file, Callback=upload_progress)
        print("Upload Successful")
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False