from aws_cdk import (
    App,
    Stack,
    aws_s3 as s3,
    aws_lambda as _lambda,
    aws_dynamodb as dynamodb,
    RemovalPolicy
)

class Prog8860Stack(Stack):

    def __init__(self, scope: App, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create S3 Bucket
        s3.Bucket(self,
                  "MyBucket",
                  bucket_name="prog8860assign2alfred",
                  versioned=True,
                  removal_policy=RemovalPolicy.DESTROY)

        # Create DynamoDB Table
        table = dynamodb.Table(self,
                               "MyTable",
                               table_name="prog8860assign2alfred",
                               partition_key={"name": "id", "type": dynamodb.AttributeType.STRING},
                               removal_policy=RemovalPolicy.DESTROY)

        # Create Lambda Function
        lambda_function = _lambda.Function(self,
                                           "MyLambda",
                                           function_name="prog8860assign2alfred",
                                           runtime=_lambda.Runtime.PYTHON_3_9,
                                           handler="index.handler",
                                           code=_lambda.Code.from_asset("lambda"))

app = App()
Prog8860Stack(app, "Prog8860Stack")
app.synth()
