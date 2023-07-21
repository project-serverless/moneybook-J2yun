import io
import pandas as pd
import json

def lambda_handler(event, context):
    session = boto3.Session()
    s3 = session.client('s3')
    filename = event["filename"]
    obj = s3.get_object(
        Bucket="jiyun-seoul-serverless-keb",
        Key=filename
        )
    df = pd.read_csv(io.BytesIO(obj["Body"].read()), index_col=0)
    print(df)
    #TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps(f'{filename} is load!!'),
    }