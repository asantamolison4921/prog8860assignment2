from aws_cdk import (
    App,
    Stack,
    pipelines,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as cpactions,
    aws_s3 as s3,
    aws_lambda as _lambda,
    aws_dynamodb as dynamodb,
    RemovalPolicy,
    Stage,
    SecretValue
)
from constructs import Construct

class Prog8860Stack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
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

class MyPipelineStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Define the source action
        source_output = codepipeline.Artifact()
        source_action = cpactions.GitHubSourceAction(
            action_name="GitHub_Source",
            owner="asantamolison4921",
            repo="prog8860assignment2",
            output=source_output,
            branch="main",
            oauth_token=SecretValue.secrets_manager("prog8860assignment2token")
        )

        # Define the build action
        build_output = codepipeline.Artifact()
        build_action = cpactions.CodeBuildAction(
            action_name="CodeBuild",
            project=pipelines.CodeBuildStep("BuildProject",
                                            input=source_output,
                                            commands=[
                                                "npm install -g aws-cdk",
                                                "pip install -r requirements.txt",
                                                "cdk synth"
                                            ]),
            input=source_output,
            outputs=[build_output]
        )

        # Define the pipeline
        pipeline = pipelines.CodePipeline(self, "Pipeline",
                                          pipeline_name="MyPipeline",
                                          synth=pipelines.ShellStep("Synth",
                                                                    input=source_output,
                                                                    commands=[
                                                                        "npm install -g aws-cdk",
                                                                        "pip install -r requirements.txt",
                                                                        "cdk synth"
                                                                    ]))

        # Add stages to the pipeline
        pipeline.add_stage(Prog8860Stage(self, "Deploy"))

class Prog8860Stage(Stage):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        Prog8860Stack(self, "Prog8860Stack")

app = App()
MyPipelineStack(app, "MyPipelineStack")
app.synth()
