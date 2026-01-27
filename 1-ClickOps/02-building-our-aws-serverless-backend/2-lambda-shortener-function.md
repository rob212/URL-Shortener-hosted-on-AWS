# Creating the Lambda Function

In this step, we will create an **AWS Lambda function** that contains the business logic for our URL shortener.

This allows us to:

- Generate unique short codes from long URLs using Base62 conversion
- Write URL mappings to our DynamoDB table
- Return the shortened URL to the user

---

## What we are doing

We will:

1. Create a Lambda function using Python
2. Write the URL shortening logic
3. Configure permissions to access DynamoDB
4. Test the function with sample data

We will achieve this all through the **AWS Management Console**.

---

## Why AWS Lambda?

AWS Lambda is:

- Serverless (no servers to manage)
- Scales automatically
- Pay only for compute time used
- Perfect for event-driven applications
- Easy to integrate with other AWS services

---

## Understanding Our Lambda Function

Our Lambda function will:

1. Receive a POST request containing a long URL
2. Generate a unique short code using Base62 conversion
3. Store the mapping in DynamoDB
4. Return the short code to the caller

**Input example:**

```json
{
  "longUrl": "https://www.example.com/very/long/url/path"
}
```

**Output example:**

```json
{
  "shortCode": "abc123",
  "shortUrl": "https://shorturl.com/abc123"
}
```

---

## Step 1 – Create a Lambda Function

> See [AWS Lambda Docs for further details](https://docs.aws.amazon.com/lambda/latest/dg/getting-started.html)

1. Open the **AWS Management Console**
2. Navigate to **Lambda**
3. Ensure you are in the same region as your DynamoDB table (e.g., `eu-west-2`)
4. Click **Create function**

### Function configuration

- **Function option**:  
  Select **'Author from scratch'**

- **Function name**:  
  Choose a descriptive name, for example:

  `url-shortener-function`

- **Runtime**:  
  Select **'Python 3.12'** (or the latest Python 3.x version available)

- **Architecture**:  
  Keep the default **'x86_64'**

- **Permissions**:  
  Expand the **'Change default execution role'** section
  - Select **'Create a new role with basic Lambda permissions'**

  > 💡 **Note**: This creates an IAM role that allows Lambda to write logs to CloudWatch. We'll add DynamoDB permissions in the next step.

5. Click **Create function**

---

## Step 2 – Add DynamoDB Permissions

Your Lambda function needs permission to read from and write to your DynamoDB table.

1. On your function page, click the **Configuration** tab
2. Click **Permissions** in the left sidebar
3. Under **Execution role**, click the role name (it will look like `url-shortener-function-role-xyz123`)
4. This opens the IAM console in a new tab
5. Click **Add permissions** → **Attach policies**
6. In the search box, type: `DynamoDB`
7. Check the box next to **'AmazonDynamoDBFullAccess'**

   > ⚠️ **Note**: For a production application, you should create a custom policy with minimal permissions (only `PutItem` and `GetItem` for your specific table). For learning purposes, `AmazonDynamoDBFullAccess` is acceptable.

8. Click **Add permissions**
9. Return to the Lambda function tab

---

## Step 3 – Write the Function Code

1. Click the **Code** tab
2. You'll see a code editor with a file called `lambda_function.py`
3. Replace the existing code with the following:

```python
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
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'shortCode': short_code,
                'shortUrl': f'https://<your-domain>/{short_code}'
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
```

4. Click **Deploy** to save your changes

> 💡 **Note**: The `Access-Control-Allow-Origin: '*'` headers are included to enable CORS (Cross-Origin Resource Sharing), which allows your frontend to call this function from a different domain.

---

## Step 4 – Understanding the Code

Let's break down what this code does:

**Base62 Conversion:**

- **`BASE62`**: A string containing all 62 characters (0-9, a-z, A-Z) used for encoding
- **`base62_encode(num)`**: Converts a number to base62 representation
  - Example: `11157` (base 10) → `2TX` (base 62)
  - Uses `divmod()` for efficient division and remainder calculation

**Short Code Generation:**

- **`generate_short_code()`**: Creates a unique identifier
  - Gets current timestamp in microseconds (1/1,000,000 of a second)
  - Converts timestamp to base62
  - Takes last 7 characters to keep URLs short
  - Microsecond precision means collisions are extremely rare

**Main Handler:**

- **`lambda_handler(event, context)`**:
  - Parses the incoming JSON body from API Gateway (created in a subsequent step)
  - Validates that a `longUrl` was provided
  - Generates a unique short code
  - Writes the mapping to DynamoDB
  - Returns the short code to the caller

> 💡 **Note**: The timestamp-based approach increases the likelyhood of uniqueness without needing to check for collisions. Each request gets a different timestamp, resulting in a different short code. This could be improved upon in a production app, but this is not the primary focus of this exercise.

---

## Step 5 – Test the Function

Now let's test our Lambda function to make sure it works:

1. Click the **Test** tab
2. Select **Create new event**
3. **Event name**: Enter `TestShortenUrl`
4. Replace the event JSON with:

```json
{
  "body": "{\"longUrl\": \"https://www.example.com/very/long/url/path\"}"
}
```

5. Click **Save**
6. Click **Test**

### Expected Result

You should see:

- **Execution result**: succeeded (in green)
- **Response**:

```json
{
  "statusCode": 200,
  "headers": {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*"
  },
  "body": "{\"shortCode\": \"j0bjje1\", \"shortUrl\": \"https://shorturl.com/j0bjje1\"}"
}
```

> 💡 **Note**: Your actual `shortCode` will be different as it's based on the current timestamp when you run the test.

---

## Step 6 – Verify Data in DynamoDB

Let's confirm the data was written to DynamoDB:

1. Navigate to **DynamoDB** in the AWS Console
2. Click **Tables** → **url-mappings**
3. Click **Explore table items**
4. You should see your test item with:
   - `shortCode`: (your generated code, e.g., `2aB4xYz`)
   - `longUrl`: `https://www.example.com/very/long/url/path`

---

## Step 7 – Test Multiple Times

To verify that each request generates a unique short code:

1. Go back to the Lambda **Test** tab
2. Click **Test** again (without changing anything)
3. Check the response - you should get a **different** `shortCode`
4. Verify in DynamoDB - you should now have **two** items with different short codes but the same long URL

This demonstrates that our URL shortener allows multiple short URLs for the same long URL, which is useful for tracking different campaigns or sharing contexts.

---

## Understanding What We Built

Your Lambda function is now:

- Successfully generating unique short codes using Base62 conversion
- Using timestamp-based uniqueness (microsecond precision)
- Writing mappings to DynamoDB
- Returning properly formatted responses
- Ready to be connected to API Gateway

In the next step, we'll create an API Gateway endpoint that will trigger this Lambda function when users submit URLs from the frontend.

---

## Troubleshooting

**If you get a permission error:**

- Verify you added the DynamoDB permissions in Step 2
- Check that the table name in the code (`url-mappings`) matches your actual table name

**If the test fails:**

- Check the CloudWatch logs (there's a link in the error message)
- Verify the event JSON is properly formatted
- Make sure you clicked **Deploy** after pasting the code

**If you get the same short code twice:**

- This would be extremely rare with microsecond precision
- Make sure you're using `time.time()` correctly (returns seconds as a float)
- Multiply by 1,000,000 to get microseconds

---

Congratulations! You have successfully created a Lambda function that powers your URL shortener using Base62 conversion.
