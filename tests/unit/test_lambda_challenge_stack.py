import aws_cdk as core
import aws_cdk.assertions as assertions

from lambda_challenge.lambda_challenge_stack import LambdaChallengeStack

# example tests. To run these tests, uncomment this file along with the example
# resource in lambda_challenge/lambda_challenge_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = LambdaChallengeStack(app, "lambda-challenge")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
