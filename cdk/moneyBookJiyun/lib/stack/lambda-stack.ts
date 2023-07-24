import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as s3 from 'aws-cdk-lib/aws-s3';
import { getAccountUniqueName } from "../config/accounts";
import { MoneyBookJiyunStackProps } from "../money_book_jiyun-stack";
import { SYSTEM_NAME } from "../config/commons";
import { PythonFunction, PythonLayerVersion } from '@aws-cdk/aws-lambda-python-alpha';
import { Runtime, LayerVersion } from 'aws-cdk-lib/aws-lambda';
import * as path from "path";
import { ManagedPolicy, Role, ServicePrincipal, CompositePrincipal, PolicyDocument, PolicyStatement, Effect } from "aws-cdk-lib/aws-iam";
import { Timeout } from 'aws-cdk-lib/aws-stepfunctions';

export class MoneyBookLambdaStack extends cdk.Stack {

    constructor(scope: Construct, id: string, props: MoneyBookJiyunStackProps) {
        super(scope, id, props);

        const lambdaRole = new Role(this, `${SYSTEM_NAME}-lambda-role`, {
            roleName: `${getAccountUniqueName(props.context)}-lambda-role`,
            assumedBy: new CompositePrincipal(
                new ServicePrincipal('lambda.amazonaws.com'),
            ),
            managedPolicies: [
                ManagedPolicy.fromAwsManagedPolicyName('service-role/AWSLambdaBasicExecutionRole'),
                ManagedPolicy.fromAwsManagedPolicyName('AmazonS3FullAccess'),
            ]
            
        })

        // index.py -> lambda_handler
        //
        new PythonFunction(this, `${SYSTEM_NAME}-handle-file`, {
            functionName: `${getAccountUniqueName(props.context)}-handle-file`,
            entry: path.join(__dirname, '../../../../app/backend/handle-file'),
            index: 'handle-file.py',
            runtime: Runtime.PYTHON_3_10,
            role: lambdaRole,
            environment: {
                'BUCKET_NAME': props.s3Stack!.bucket.bucketName,
            },
            timeout: cdk.Duration.seconds(10),
            memorySize: 256,
            handler: "lambda_handler",
            layers: [LayerVersion.fromLayerVersionArn(this,"pandasLayer-handle-file",
                "arn:aws:lambda:ap-northeast-2:336392948345:layer:AWSSDKPandas-Python310:3" )],
            
        })
        new PythonFunction(this, `${SYSTEM_NAME}-read-csv`, {
            functionName: `${getAccountUniqueName(props.context)}-read-csv`,
            entry: path.join(__dirname, '../../../../app/backend/read-csv'),
            index: 'read-csv.py',
            runtime: Runtime.PYTHON_3_10,
            role: lambdaRole,
            environment: {
                'BUCKET_NAME': props.s3Stack!.bucket.bucketName,
            },
            timeout: cdk.Duration.seconds(10),
            memorySize: 256,
            handler: "lambda_handler",
            layers: [LayerVersion.fromLayerVersionArn(this,"pandasLayer-read-csv",
            "arn:aws:lambda:ap-northeast-2:336392948345:layer:AWSSDKPandas-Python310:3" )],
        })
    }
}