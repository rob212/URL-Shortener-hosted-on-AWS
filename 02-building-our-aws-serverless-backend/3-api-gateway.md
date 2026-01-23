# Creating the API Gateway

In this step, we will create an **AWS API Gateway** that acts as the HTTP endpoint for our URL shortener.

This allows us to:

- Receive POST requests from our frontend
- Trigger our Lambda function with the request data
- Return the shortened URL back to the user
- Enable secure communication between frontend and backend

---

## What we are doing

We will:

1. Create an HTTP API in API Gateway
2. Configure a POST route to trigger our Lambda function
3. Enable CORS to allow requests from our frontend
4. Test the API endpoint
5. Get the API URL to use in our frontend

We will achieve this all through the **AWS Management Console**.

---

## Why API Gateway?

API Gateway is:

- A fully managed service for creating APIs
- Highly scalable and secure
- Easy to integrate with Lambda
- Handles CORS, authentication, and throttling
- Perfect for serverless applications

---

## Understanding the Request Flow

Here's how a request will flow through our system:

1. User enters a long URL in the frontend and clicks the "Shorten URL" button
2. JavaScript `fetch()` sends a POST request to API Gateway
3. API Gateway triggers our Lambda function
4. Lambda generates a short code and stores it in DynamoDB
5. Lambda returns the short code to API Gateway
6. API Gateway returns the response to the frontend
7. Frontend displays the shortened URL

---

## Step 1 – Create an HTTP API

> See [AWS API Gateway Docs for further details](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api.html)

1. Open the **AWS Management Console**
2. Navigate to **API Gateway**
3. Ensure you are in the same region as your Lambda function (e.g., `eu-west-2`)
4. Click **Create API**

### Choose API Type

You'll see several options. We want **HTTP API**:

- Locate the **HTTP API** section (not REST API)
- Click **Build** under HTTP API

> 💡 **Note**: HTTP APIs are simpler, faster, and cheaper than REST APIs. They're perfect for our use case where we just need to trigger a Lambda function.

---

## Step 2 – Configure Integrations

On the "Create HTTP API" page:

1. **API name**: Enter `url-shortener-api`
2. **IP address type**: keep the default of **IPv4**
3. Under **Integrations**, click **Add integration**
4. Select **Lambda** from the dropdown
5. **Lambda function**: Select your function `url-shortener-function` from the dropdown (via your Lambda's _arn_ (Amazon Resource Name)). Keep the version at **2.0**
6. Click **Next**

> 💡 **Note**: This automatically creates the connection between API Gateway and your Lambda function.

---

## Step 3 – Configure Routes

On the "Configure routes" page:

1. Click the **Add route** button
2. Click the **Method** dropdown and select **POST**
3. Click the **Resource path** field and populate it with: `/shorten`
4. Click the **Integration target** dropdown and select `url-shortener-function' (the name of our lamdba function)
5. Click **Next**

> 💡 **Note**: The route `/shorten` is the endpoint path. Your full API URL will be: `https://your-api-id.execute-api.region.amazonaws.com/shorten`

---

## Step 4 – Define Stages

On the "Define stages" page:

1. **Stage name**: Keep the default `$default`
2. **Auto-deploy**: Keep this **enabled** (checked)
3. Click **Next**

> 💡 **Note**: Auto-deploy means any changes to your API will automatically be deployed. This is convenient for development.

---

## Step 5 – Review and Create

1. Review your settings:
   - API name: `url-shortener-api`
   - Integration: Lambda function `url-shortener-function`
   - Route: `POST /shorten`
   - Stage: `$default`
2. Click **Create**

---

## Step 6 – Enable CORS

CORS (Cross-Origin Resource Sharing) allows your frontend (hosted on CloudFront) to make requests to your API (hosted on a different domain).

1. In your newly created API, click on **CORS** in the left sidebar
2. Click **Configure**
3. Under **Access-Control-Allow-Origin**, enter our CloudFront distribution domain name. Ensure you prepend this with `https://` (e.g. `https://<distribution-id>.cloudfront.net`)
   > ⚠️ **Note**: You will need to navigate to the CloudFront console to find this.
4. click the associated **Add** button
5. Under **Access-Control-Allow-Headers**, add `content-type` and click the associated **Add** button
6. Under **Access-Control-Allow-Methods**, ensure these are selected:
   - `GET`
   - `POST`
   - `OPTIONS`

   > 💡 **Note**: 'OPTIONS' is needed for the CORS preflight request made automatically by our web browser

7. Click **Save**

> 💡 **Note**: CORS errors are one of the most common issues when connecting frontends to APIs. These settings tell browsers it's safe to make requests from your frontend to this API.

---

## Step 7 – Get Your API URL

Now we need to find the URL to call our API:

1. Click on **Stages** in the left sidebar
2. Click on **$default**
3. You'll see **Invoke URL** at the top - it will look like:

   `https://abc123xyz.execute-api.eu-west-2.amazonaws.com`

4. **Copy this URL** - you'll need it for testing and for your frontend

Your full API endpoint will be:

```
https://abc123xyz.execute-api.eu-west-2.amazonaws.com/shorten
```

> 💡 **Note**: The `/shorten` path is added to the invoke URL because that's the route we configured in Step 3.

---

## Step 8 – Test the API

Let's test our API to make sure it works:

### Option 1: Test with curl (if you have terminal access)

Open your terminal and run:

```bash
curl -X POST https://YOUR-INVOKE-URL/shorten \
  -H "Content-Type: application/json" \
  -d '{"longUrl": "https://www.example.com/test"}'
```

Replace `YOUR-INVOKE-URL` with your actual invoke URL.

### Option 2: Test with Postman or similar tool

1. Open Postman (or any API testing tool)
2. Create a new **POST** request
3. URL: `https://YOUR-INVOKE-URL/shorten`
4. Headers: `Content-Type: application/json`
5. Body (raw JSON):

```json
{
  "longUrl": "https://www.example.com/test"
}
```

6. Click **Send**

### Expected Response

You should receive:

```json
{
  "shortCode": "2aB4xYz",
  "shortUrl": "https://shorturl.com/2aB4xYz"
}
```

---

## Step 9 – Verify API Gateway is hitting our Lambda function (Optional)

We can see detailed request logs via **CloudWatch**:

1. Navigate to **CloudWatch** in the AWS Console
2. Expand **Logs** and click **Log Management**
3. Find `/aws/apigateway/url-shortener-api`
4. You can see detailed request/response logs here following our successful test of calling our API Gateway

> ⚠️ **Note**: Our Lambda automatically logs to CloudWatch, this is sufficient for our needs in this exercise. If you wish specific API Gateway logs you need to enable them specifically in the CloudWatch console.

---

## Understanding What We Built

Your API Gateway is now:

- Accepting POST requests at `/shorten`
- Passing the request body to your Lambda function
- Returning the Lambda response to the caller
- Handling CORS so your frontend can call it
- Ready to be integrated into your HTML page

In the next step, we'll update our frontend `index.html` to call this API and display the shortened URLs to users.

---

## Important: Save Your API URL

Make sure you have your full API endpoint URL saved:

```
https://YOUR-API-ID.execute-api.YOUR-REGION.amazonaws.com/shorten
```

You'll need this in the next step when we connect the frontend!

---

## Troubleshooting

**If you get CORS errors:**

- Verify you enabled CORS in Step 6
- Check that `Access-Control-Allow-Origin` is set correctly. If you are having trouble you can allow all access with `*` (not advised for production apps)
- Make sure `POST` and `OPTIONS` methods are allowed

**If you get a 403 Forbidden error:**

- Check that your route is configured correctly (`POST /shorten`)
- Verify the Lambda integration is connected
- Ensure your Lambda has the correct permissions

**If you get a 500 Internal Server Error:**

- The issue is likely in your Lambda function
- Check CloudWatch logs for the Lambda function
- Verify the Lambda can write to DynamoDB

**If the request times out:**

- Check that your Lambda function is in the same region as API Gateway
- Verify the Lambda execution role has proper permissions
- Check CloudWatch logs for errors

---

Congratulations! You have successfully created an API Gateway that connects your frontend to your Lambda function.
