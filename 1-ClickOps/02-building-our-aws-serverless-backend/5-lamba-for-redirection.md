# URL Redirection

In this step, we will complete our URL shortener by adding **redirection functionality** so that when users visit a shortened URL, they are automatically redirected to the original long URL.

This allows us to:

- Handle requests to shortened URLs (e.g., `/je5UWgw`)
- Look up the short code in DynamoDB
- Redirect users to the original long URL
- Complete the full URL shortener workflow

---

## What we are doing

We will:

1. Create a new Lambda function to handle redirects
2. Add a GET route to API Gateway that accepts short codes
3. Configure the Lambda to look up URLs in DynamoDB
4. Return HTTP redirects to users
5. Test the complete redirect flow

We will achieve this all through the **AWS Management Console**.

---

## Understanding the Redirect Flow

Here's what happens when a user visits a shortened URL:

1. User clicks or visits: `https://<your-domain>/je5UWgw`
2. API Gateway captures the request with short code `je5UWgw`
3. API Gateway triggers the redirect Lambda function
4. Lambda queries DynamoDB for short code `je5UWgw`
5. Lambda retrieves the original long URL
6. Lambda returns a 302 redirect response
7. User's browser automatically redirects to the long URL

---

## Current vs. Complete Architecture

**What we have now:**

```
User → CloudFront → index.html → API Gateway (POST /shorten) → Lambda → DynamoDB
```

**What we're adding:**

```
User → API Gateway (GET /{shortCode}) → Redirect Lambda → DynamoDB → 302 Redirect
```

---

## Step 1 – Create the Redirect Lambda Function

1. Open the **AWS Management Console**
2. Navigate to **Lambda**
3. Ensure you are in the same region as your other resources (e.g., `eu-west-2`)
4. Click **Create function**

### Function configuration

- **Function option**:  
  Select **'Author from scratch'**

- **Function name**:  
  `url-redirect-function`

- **Runtime**:  
  Select **'Python 3.12'** (or the latest Python 3.x version available)

- **Architecture**:  
  Keep the default **'x86_64'**

- **Permissions**:  
  Expand the **'Change default execution role'** section
  - Select **'Create a new role with basic Lambda permissions'**

5. Click **Create function**

---

## Step 2 – Add DynamoDB Permissions

Just like with our first Lambda function, this one needs permission to read from DynamoDB:

1. On your function page, click the **Configuration** tab
2. Click **Permissions** in the left sidebar
3. Under **Execution role**, click the role name (it will look like `url-redirect-function-role-xyz123`)
4. This opens the IAM console in a new tab
5. Click **Add permissions** → **Attach policies**
6. In the search box, type: `DynamoDB`
7. Check the box next to **'AmazonDynamoDBReadOnlyAccess'**

   > 💡 **Note**: We only need read access for this function since it's just looking up URLs, not creating them.

8. Click **Add permissions**
9. Return to the Lambda function tab

---

## Step 3 – Write the Redirect Function Code

1. Click the **Code** tab
2. Replace the existing code in `lambda_function.py` with:

```python
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
```

3. Click **Deploy** to save your changes

---

## Step 4 – Understanding the Redirect Code

Let's break down what this code does:

**Extracting the Short Code:**

- `event['pathParameters']['shortCode']` - API Gateway passes the URL path parameter here
- Example: For URL `/je5UWgw`, the short code is `je5UWgw`

**Looking Up in DynamoDB:**

- `table.get_item()` - Retrieves a single item by primary key
- `Key={'shortCode': short_code}` - Looks up using the short code
- `response['Item']` - Contains the item if found

**Handling Different Cases:**

- **Short code not found**: Returns 404 with a friendly HTML message
- **Short code found**: Returns 302 redirect with the `Location` header
- **Error**: Returns 500 with error message

**HTTP 302 Redirect:**

- Status code `302` means "Found" (temporary redirect)
- The `Location` header tells the browser where to redirect
- The browser automatically follows the redirect

> 💡 **Note**: We use 302 (temporary) instead of 301 (permanent) because URLs might be reused or deleted. In production, you might use 301 for better SEO.

---

## Step 5 – Test the Redirect Lambda

Let's test the function before connecting it to API Gateway:

1. Click the **Test** tab
2. Click **Create new event**
3. **Event name**: Enter `TestRedirect`
4. Replace the event JSON with:

```json
{
  "pathParameters": {
    "shortCode": "je5UWgw"
  }
}
```

> 💡 **Note**: Replace `je5UWgw` with an actual short code from your DynamoDB table. You can find these by going to DynamoDB → url-mappings → Explore table items.

5. Click **Save**
6. Click **Test**

### Expected Result

You should see:

```json
{
  "statusCode": 302,
  "headers": {
    "Location": "https://www.example.com/very/long/url/path"
  },
  "body": ""
}
```

The `Location` header should contain the original long URL you stored!

---

## Step 6 – Add GET Route to API Gateway

Now we need to add a new route to our existing API Gateway:

1. Navigate to **API Gateway** in the AWS Console
2. Click on your existing API: `url-shortener-api`
3. Click **Routes** in the left sidebar
4. Click **Create**

### Route configuration

- **Method**: Select **GET** from the dropdown
- **Resource path**: Enter `/{shortCode}`

  > 💡 **Note**: The curly braces `{}` make this a **path parameter**. Anything after the `/` will be captured as the short code. For example: `/je5UWgw` → shortCode = "je5UWgw"

5. Click **Create**

---

## Step 7 – Attach Lambda Integration to GET Route

Now we need to connect this route to our redirect Lambda:

1. You should see your new route: **GET /{shortCode}**
2. Click on the route to select it
3. Click **Attach integration**
4. Click **Create and attach an integration**

### Integration configuration

- **Integration type**: Select **Lambda function**
- **AWS Region**: Select the Region our Lambda is deployed to (e.g., `eu-west-2`)
- **Lambda function**: Select `url-redirect-function` from the dropdown
- **Invoke permissions**: This will be automatically configured

5. Click **Create**

---

## Step 8 – Deploy the Changes

Since we have auto-deploy enabled, the changes should deploy automatically.

Your API is now ready to handle both URL shortening AND redirection!

---

## Step 9 – Update the Shorten Lambda to Return API Gateway URLs

Now that we have a working redirect endpoint, we should update our original Lambda function to return API Gateway URLs instead of CloudFront URLs:

1. Navigate to **Lambda**
2. Click on `url-shortener-function` (your original Lambda)
3. Click the **Code** tab
4. Find this line:

```python
'shortUrl': f'https://d11xc5qvo3ejev.cloudfront.net/{short_code}'
```

5. Replace it with your API Gateway invoke URL:

```python
'shortUrl': f'https://YOUR-API-ID.execute-api.YOUR-REGION.amazonaws.com/{short_code}'
```

**Example:**

```python
'shortUrl': f'https://abc123xyz.execute-api.eu-west-2.amazonaws.com/{short_code}'
```

> 💡 **Note**: Do NOT include `/shorten` in this URL. The short code is accessed directly at the root level (e.g., `/je5UWgw`).

6. Click **Deploy**

### Why Use API Gateway URLs Instead of CloudFront URLs?

When we were using CloudFront URLs (`https://d11xc5qvo3ejev.cloudfront.net/{shortCode}`), CloudFront would try to serve that path as a **file from your S3 bucket**.

- CloudFront looks for a file called `je5UWgw` in your S3 bucket
- That file doesn't exist (it's just a record in DynamoDB)
- CloudFront returns 403 Forbidden

#### Why API Gateway URLs work:

API Gateway URLs (`https://abc123xyz.execute-api.eu-west-2.amazonaws.com/{shortCode}`) route to your **redirect Lambda function**.

- API Gateway captures the path /{shortCode}
- Triggers your redirect Lambda
- Lambda looks it up in DynamoDB
- Returns a 302 redirect
- User gets redirected to the long URL ✅

#### Could we keep using CloudFront?

Yes, but it would require additional configuration involving **CloudFront Behaviours**, **Lambda@Edge** or **CloudFront Functions**. These options add complexity and are out of scope for our needs.

---

## Step 10 – Test the Complete Flow

Now let's test everything end-to-end:

### Test 1: Create a Short URL

1. Go to your CloudFront URL (your frontend)
2. Enter a long URL: `https://docs.aws.amazon.com/lambda/latest/dg/python-handler.html`
3. Click **Shorten URL**
4. You should see a short URL like: `https://abc123xyz.execute-api.eu-west-2.amazonaws.com/je5UWgw`

### Test 2: Test the Redirect

Either click on the short URL link or:

1. **Copy the shortened URL** from the frontend
2. **Open a new browser tab**
3. **Paste the shortened URL** and press Enter
4. You should be **automatically redirected** to ` https://docs.aws.amazon.com/lambda/latest/dg/python-handler.html`!

🎉 **Success!** Your URL shortener now fully works!

---

## Step 11 – Test Edge Cases

Let's verify error handling works:

**Test 1: Non-existent short code**

1. Visit: `https://YOUR-API-URL.amazonaws.com/invalid999`
2. You should see: "404 - Short URL Not Found"

**Test 2: Multiple different URLs**

1. Create short URLs for different websites
2. Test that each one redirects to the correct destination
3. Verify in DynamoDB that all mappings are stored correctly

---

## Understanding What We Built

Your complete URL shortener now has:

✅ **URL Shortening**

- User submits long URL via frontend
- Lambda generates short code
- Stores mapping in DynamoDB
- Returns API Gateway URL

✅ **URL Redirection**

- User visits short URL
- API Gateway captures short code
- Lambda looks up in DynamoDB
- Returns 302 redirect to long URL
- Browser automatically redirects user

**Complete Architecture:**

```
Frontend (CloudFront/S3)
    ↓ POST /shorten
API Gateway
    ↓ Invoke
Shorten Lambda → DynamoDB (write)
    ↓ Return short URL

User clicks short URL
    ↓ GET /{shortCode}
API Gateway
    ↓ Invoke
Redirect Lambda → DynamoDB (read)
    ↓ 302 Redirect
Browser → Long URL
```

---

## Why the URLs Are Long

You might notice that your "shortened" URLs are actually quite long:

```
https://abc123xyz.execute-api.eu-west-2.amazonaws.com/je5UWgw
```

This is because we're using the **API Gateway domain**, which is lengthy. In a production URL shortener, you would typically:

1. Purchase a short domain name (e.g., `go.link`, `s.hrt`, `yourname.io`)
2. Configure it to point to your API Gateway
3. This would give you truly short URLs like: `https://go.link/je5UWgw`

However, the **core functionality** you've built is exactly the same as production URL shorteners - only the domain differs. The architecture, logic, and AWS services are production-ready!

---

## Troubleshooting

**If the redirect doesn't work:**

- Verify the GET route is configured: `GET /{shortCode}` (with curly braces)
- Check that the redirect Lambda is attached to the GET route
- Verify DynamoDB permissions on the redirect Lambda
- Check CloudWatch logs for the redirect Lambda
- Ensure the short code exists in DynamoDB

**If you get "Short code is required" error:**

- The URL path might be incorrect
- Try: `https://your-api-url.com/je5UWgw` (no trailing slash)
- Verify the route is `/{shortCode}` not `/shortCode`

**If you get 404 "Short URL Not Found":**

- The short code doesn't exist in DynamoDB
- Check DynamoDB → url-mappings → Explore table items
- Verify you're using an actual short code from the table

**If redirect is slow:**

- First redirect might be slower (Lambda cold start ~1-2 seconds)
- Subsequent redirects should be fast (<100ms)
- This is normal behavior for serverless functions

**If you see the old CloudFront URLs:**

- Verify you updated the `url-shortener-function` Lambda in Step 9
- Make sure you clicked **Deploy** after making changes
- Create a new short URL to test (old ones still use CloudFront URLs)

---

## Optional Enhancements

Now that you have a fully functional URL shortener, you could add:

1. **Analytics**: Track click counts and timestamps for each short URL
2. **Expiration**: Add TTL (Time To Live) to DynamoDB to auto-delete old URLs
3. **Custom short codes**: Let users choose their own short codes instead of auto-generated ones
4. **Authentication**: Require login to create short URLs (using AWS Cognito)
5. **Dashboard**: Create an admin page to view all your short URLs and their stats
6. **QR codes**: Generate QR codes for shortened URLs
7. **Link preview**: Show a preview page before redirecting (security feature)
8. **Rate limiting**: Prevent abuse by limiting how many URLs can be created
9. **Custom domain**: Purchase a short domain to make URLs truly short
10. **Infrastructure as Code**: Best practice is to have reproducable infrastructure managed in code

---

Congratulations! You now have a complete, working URL shortener with both creation and redirection capabilities!

## What You've Learned

In this step, you learned:

- How to create Lambda functions that handle HTTP redirects
- How to use API Gateway path parameters (`{shortCode}`)
- How to query DynamoDB using `get_item()`
- How HTTP redirects work (302 status code + Location header)
- How to handle different response types (JSON vs HTML vs Redirect)
- How to connect multiple Lambda functions to the same API Gateway
- The difference between 301 (permanent) and 302 (temporary) redirects
- How serverless architectures can handle production workloads

Your URL shortener implements the same core functionality as industry services like Bitly, TinyURL, and others. The only difference is they use custom domains to make the URLs shorter!
