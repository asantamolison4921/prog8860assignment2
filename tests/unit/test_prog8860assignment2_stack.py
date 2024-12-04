import aws_cdk as core
import aws_cdk.assertions as assertions

from prog8860assignment2.prog8860assignment2_stack import Prog8860Assignment2Stack

# example tests. To run these tests, uncomment this file along with the example
# resource in prog8860assignment2/prog8860assignment2_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = Prog8860Assignment2Stack(app, "prog8860assignment2")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
