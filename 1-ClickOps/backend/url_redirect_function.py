import json
import boto3

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('url-mappings')

def lambda_handler(event, context):
    """
    Lambda function to handle URL redirects.
    Receives a short code, looks it up in DynamoDB, and returns a redirect.
    """

    try:
        # Extract the short code from the path parameters
        # API Gateway sends this as event['pathParameters']['shortCode']
        short_code = event.get('pathParameters', {}).get('shortCode')

        # Validate that we received a short code
        if not short_code:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    'error': 'Short code is required'
                })
            }

        # Look up the short code in DynamoDB
        response = table.get_item(
            Key={
                'shortCode': short_code
            }
        )

        # Check if the short code exists
        if 'Item' not in response:
            # Short code not found - return 404
            return {
                'statusCode': 404,
                'headers': {
                    'Content-Type': 'text/html'
                },
                'body': '''
                    <html>
                        <body>
                            <h1>404 - Short URL Not Found</h1>
                            <p>This shortened URL does not exist or may have expired.</p>
                        </body>
                    </html>
                '''
            }

        # Extract the long URL from the DynamoDB response
        long_url = response['Item']['longUrl']

        # Return a 302 redirect to the long URL
        return {
            'statusCode': 302,
            'headers': {
                'Location': long_url
            },
            'body': ''
        }

    except Exception as e:
        # Handle any errors
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'error': 'Internal server error'
            })
        }