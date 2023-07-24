# 실행방법

<pre><code>1. "/cdk/lib/config/accounts.ts"에서 본인 환경에 맞는 사용자 정보로 변겅
2. "/cdk/lib/config/commons.ts"에서 원하는 이름으로 변경
3. cdk deploy
4. 배포로 생성된 람다함수 이름에 맞게 "/frontend/lambdaTest.py"에서 invoke의 FunctionName 변경
5. main_s3_lambda_cdk.py 실행
</code></pre>
