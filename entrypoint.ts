import { APIGatewayProxyEvent, APIGatewayProxyResult } from 'aws-lambda';
import { SQSClient, SendMessageRequest, SendMessageCommand } from "@aws-sdk/client-sqs";

/**
 *
 * Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format
 * @param {Object} event - API Gateway Lambda Proxy Input Format
 *
 * Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
 * @returns {Object} object - API Gateway Lambda Proxy Output Format
 *
 */

export const lambdaHandler = async (event: APIGatewayProxyEvent): Promise<APIGatewayProxyResult> => {
    try {
        const client = new SQSClient({region: "eu-central-1"})
        const input: SendMessageRequest = {
            QueueUrl: process.env.WORKER_QUEUE,
            MessageBody: "Hallo test"
        }
        const command = new SendMessageCommand(input);
        const response = await client.send(command);
        return {
            statusCode: 200,
            body: JSON.stringify({
                message: JSON.stringify(response),
            }),
        };
    } catch (err) {
        console.log(err);
        return {
            statusCode: 500,
            body: JSON.stringify({
                message: 'some error happened',
            }),
        };
    }
};