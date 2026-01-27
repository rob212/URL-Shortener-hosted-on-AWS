import json
import boto3
import time

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('url-mappings')

# Base62 characters for encoding
BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def base62_encode(num):
    """Convert a number to base62 string"""
    if num == 0:
        return BASE62[0]
    
    result = []
    while num:
        num, remainder = divmod(num, 62)
        result.append(BASE62[remainder])
    
    return ''.join(reversed(result))

def generate_short_code():
    """Generate a unique short code using timestamp-based Base62 conversion"""
    # Use current timestamp in microseconds for uniqueness
    # This ensures each call generates a different code
    timestamp_us = int(time.time() * 1_000_000)
    
    # Convert to base62 and take last 7 characters to keep URLs short
    short_code = base62_encode(timestamp_us)
    
    return short_code[-7:]

def lambda_handler(event, context):
    """Main Lambda handler function"""
    
    try:
        # Parse the incoming request body
        body = json.loads(event.get('body', '{}'))
        long_url = body.get('longUrl')
        
        # Validate input
        if not long_url:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': 'longUrl is required'
                })
            }
        
        # Generate unique short code
        short_code = generate_short_code()
        
        # Store in DynamoDB
        table.put_item(
            Item={
                'shortCode': short_code,
                'longUrl': long_url
            }
        )
        
        # Return success response
        # NOTE to update your shortUrl with your API Gateway Invoke URL
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'shortCode': short_code,
                'shortUrl': f'https://r6rxczcb99.execute-api.eu-west-2.amazonaws.com/{short_code}/{short_code}'
            })
        }
        
    except Exception as e:
        # Handle errors
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': 'Internal server error'
            })
        }