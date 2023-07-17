import boto3
import io
import pandas as pd
from botocore.client import Config

ACCESS_KEY_ID = "AKIA3ZCOMZWK26LTZAN4"
ACCESS_SECRET_KEY = "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"
BUCKET_NAME = "jiyun-seoul-serverless-keb"

key_name = "moneyflow.csv"

s3 = boto3.client('s3',
    aws_access_key_id=ACCESS_KEY_ID,
    aws_secret_access_key=ACCESS_SECRET_KEY)

#READ
obj = s3.get_object(
    Bucket=BUCKET_NAME,
    Key=key_name
)

df = pd.read_csv(io.BytesIO(obj["Body"].read()), index_col=0)
print(df)
# #WRITE
# s3.put_object(
#     Body=df.to_csv().encode(),
#     Bucket=BUCKET_NAME,
#     KEY=key_name
# )

