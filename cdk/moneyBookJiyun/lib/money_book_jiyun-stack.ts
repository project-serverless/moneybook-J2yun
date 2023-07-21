import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { Account } from "./config/accounts";
import { MoneyBookS3Stack } from './stack/s3-stack';
import { MoneyBookLambdaStack } from './stack/lambda-stack';
import { SYSTEM_NAME } from "./config/commons";
// import * as sqs from 'aws-cdk-lib/aws-sqs';

export interface MoneyBookJiyunStackProps extends cdk.StackProps {
  context: Account
  s3Stack?: MoneyBookS3Stack
}

export class MoneyBookJiyunStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: MoneyBookJiyunStackProps) {
    super(scope, id, props);

    const s3Stack = new MoneyBookS3Stack(this, `${SYSTEM_NAME}-s3Stack`, props);
    props.s3Stack = s3Stack;

    new MoneyBookLambdaStack(this, `${SYSTEM_NAME}-lambdaStack`, props);
  }
}
