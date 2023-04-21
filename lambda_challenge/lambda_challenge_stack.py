from aws_cdk import (
    # Duration,
    Stack,
    Tags,
    aws_lambda,
    aws_apigateway,
    aws_sqs,
    aws_lambda_event_sources,
    aws_lambda_nodejs,
    aws_s3 as s3,
)
from constructs import Construct


class LambdaChallengeStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        queue = aws_sqs.Queue(self, "worker-queue")
        handler = aws_lambda_nodejs.NodejsFunction(
            self,
            "manager",
            entry="entrypoint.ts",
            handler="lambdaHandler",
            deps_lock_file_path="yarn.lock",
            runtime=aws_lambda.Runtime.NODEJS_18_X,
            environment=dict(WORKER_QUEUE=queue.queue_url),
        )
        queue.grant_send_messages(handler)

        workers = aws_lambda.Function(
            self,
            "workerX",
            runtime=aws_lambda.Runtime.NODEJS_18_X,
            code=aws_lambda.Code.from_asset("workers"),
            handler="example.main",
        )
        queue.grant_consume_messages(workers)

        workers.add_event_source(
            aws_lambda_event_sources.SqsEventSource(
                queue, max_concurrency=2, batch_size=1
            )
        )

        api = aws_apigateway.RestApi(
            self,
            "telephone-game-api",
            rest_api_name="Telephone game",
            description="This api handles strings like the children game telephone",
        )

        entrypoint_integration = aws_apigateway.LambdaIntegration(
            handler, request_templates={"application/json": '{ "statusCode": "200" }'}
        )

        api.root.add_method("GET", entrypoint_integration)
