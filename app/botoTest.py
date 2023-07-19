import boto3
import io
import pandas as pd

# ACCESS_KEY_ID
# ACCESS_SECRET_KEY
# BUCKET_NAME
key_name = "moneyflow.csv"

class CSV():
    def __init__(self):
        self.s3 = boto3.client('s3',
            aws_access_key_id=ACCESS_KEY_ID,
            aws_secret_access_key=ACCESS_SECRET_KEY)

    #READ
    def read(self):
        self.obj = self.s3.get_object(
            Bucket=BUCKET_NAME,
            Key=key_name
        )
        df = pd.read_csv(io.BytesIO(self.obj["Body"].read()), index_col=0)
        
        return df

    # #WRITE
    def write(self,df):
        self.s3.put_object(
            Body=df.to_csv().encode(),
            Bucket=BUCKET_NAME,
            Key=key_name
        )

