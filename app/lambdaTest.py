import boto3
import io
import pandas as pd
import dotenv
import json

dotenv.load_dotenv(".env",override=True)

BUCKET_NAME = "jiyun-seoul-serverless-keb"

key_name = "moneyflow.csv"

def lambda_addData(file_name,date,type,category,item,amount,note):

    lambda_client = boto3.client('lambda')
    lambda_client.invoke(FunctionName='AccountBook-addData',
                        InvocationType='RequestResponse',
                        Payload=json.dumps({
                            "CRUD" : "CREATE",
                            "filename": file_name,
                            "date" : date,
                            "type":type,
                            "category":category,
                            "item":item,
                            "amount":amount,
                            "note":note
                        })
                    )

def lambda_deleteData(index,file_name):
    lambda_client = boto3.client('lambda')
    lambda_client.invoke(FunctionName='AccountBook-addData',
                        InvocationType='RequestResponse',
                        Payload=json.dumps({
                            "CRUD" : "DELETE",
                            "filename": file_name,
                            "index" : index
                        })
                    )
    
def lambda_updateData(file_name,date,type,category,item,amount,note,index):

    lambda_client = boto3.client('lambda')
    lambda_client.invoke(FunctionName='AccountBook-addData',
                        InvocationType='RequestResponse',
                        Payload=json.dumps({
                            "CRUD" : "UPDATE",
                            "filename": file_name,
                            "date" : date,
                            "type":type,
                            "category":category,
                            "item":item,
                            "amount":amount,
                            "note":note,
                            "index" : index
                        })
                    )
