# Connecting the Frontend to the Backend

In this step, we will update our **frontend HTML page** to call our API Gateway endpoint and display the shortened URLs to users.

This allows us to:

- Submit long URLs from the browser
- Call our API Gateway endpoint using JavaScript
- Display the generated short URL to the user
- Complete the full URL shortener workflow

---

## What we are doing

We will:

1. Update our `index.html` with JavaScript to call the API
2. Add the API Gateway invoke URL to our code
3. Handle the API response and display the short URL
4. Upload the updated file to S3
5. Test the complete application end-to-end

We will achieve this all through the **AWS Management Console** and a text editor.

---

## Understanding the Frontend Flow

Here's what happens when a user shortens a URL:

1. User enters a long URL in the input field
2. User clicks the "Shorten" button
3. JavaScript captures the button click
4. JavaScript sends a POST request to API Gateway with the long URL
5. API Gateway triggers Lambda
6. Lambda generates a short code and stores it in DynamoDB
7. Lambda returns the short code to API Gateway
8. API Gateway returns the response to the frontend
9. JavaScript displays the shortened URL to the user

---

## Step 1 – Get Your API Gateway Invoke URL

Before we update the HTML, we need to get the API endpoint URL:

1. Open the **AWS Management Console**
2. Navigate to **API Gateway**
3. Click on your API: `url-shortener-api`
4. Click **Stages** in the left sidebar
5. Click **$default**
6. Copy the **Invoke URL** (it looks like: `https://abc123xyz.execute-api.eu-west-2.amazonaws.com`)
7. Your full endpoint will be this URL + `/shorten`

**Example full endpoint:**

```
https://abc123xyz.execute-api.eu-west-2.amazonaws.com/shorten
```

Keep this URL handy - you'll need it in the next step!

---

## Step 2 – Create the Updated HTML

Open your text editor and edit our `index.html` with the following code:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>URL Shortener</title>
    <style>
      body {
        font-family: Arial, sans-serif;
        max-width: 600px;
        margin: 50px auto;
        padding: 20px;
        background-color: #f5f5f5;
      }
      .container {
        background-color: white;
        padding: 30px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
      }
      h1 {
        color: #333;
        text-align: center;
      }
      input[type="text"] {
        width: 100%;
        padding: 12px;
        margin: 10px 0;
        border: 1px solid #ddd;
        border-radius: 4px;
        box-sizing: border-box;
        font-size: 14px;
      }
      button {
        width: 100%;
        padding: 12px;
        background-color: #007bff;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
        font-size: 16px;
        margin-top: 10px;
      }
      button:hover {
        background-color: #0056b3;
      }
      button:disabled {
        background-color: #ccc;
        cursor: not-allowed;
      }
      .result {
        margin-top: 20px;
        padding: 15px;
        background-color: #e7f3ff;
        border-radius: 4px;
        display: none;
      }
      .result.show {
        display: block;
      }
      .result.error {
        background-color: #ffe7e7;
      }
      .short-url {
        font-weight: bold;
        color: #007bff;
        word-break: break-all;
      }
      .error-message {
        color: #d8000c;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <h1>URL Shortener</h1>
      <p>Enter a long URL below to create a shortened version:</p>

      <input
        type="text"
        id="longUrl"
        placeholder="https://example.com/very/long/url/path"
        aria-label="Long URL input"
      />

      <button id="shortenBtn" onclick="shortenUrl()">Shorten URL</button>

      <div id="result" class="result"></div>
    </div>

    <script>
      // Replace this with your actual API Gateway invoke URL
      const API_ENDPOINT =
        "https://YOUR-INVOKE-URL-HERE.execute-api.YOUR-REGION.amazonaws.com/shorten";

      async function shortenUrl() {
        const longUrlInput = document.getElementById("longUrl");
        const resultDiv = document.getElementById("result");
        const button = document.getElementById("shortenBtn");

        // Get the long URL from input
        const longUrl = longUrlInput.value.trim();

        // Validate input
        if (!longUrl) {
          showError("Please enter a URL");
          return;
        }

        // Basic URL validation
        if (!isValidUrl(longUrl)) {
          showError(
            "Please enter a valid URL (must start with http:// or https://)",
          );
          return;
        }

        // Disable button and show loading state
        button.disabled = true;
        button.textContent = "Shortening...";
        resultDiv.className = "result";
        resultDiv.textContent = "";

        try {
          // Make POST request to API Gateway
          const response = await fetch(API_ENDPOINT, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ longUrl: longUrl }),
          });

          // Parse the response
          const data = await response.json();

          if (response.ok) {
            // Success - display the short URL
            showSuccess(data.shortCode, data.shortUrl);
          } else {
            // API returned an error
            showError(data.error || "Failed to shorten URL");
          }
        } catch (error) {
          // Network error or other issue
          console.error("Error:", error);
          showError("Failed to connect to the server. Please try again.");
        } finally {
          // Re-enable button
          button.disabled = false;
          button.textContent = "Shorten URL";
        }
      }

      function showSuccess(shortCode, shortUrl) {
        const resultDiv = document.getElementById("result");
        resultDiv.className = "result show";
        resultDiv.innerHTML = `
                <p>✅ Success! Your shortened URL:</p>
                <p class="short-url">${shortUrl}</p>
                <p style="font-size: 12px; color: #666; margin-top: 10px;">
                    Short code: <strong>${shortCode}</strong>
                </p>
            `;
      }

      function showError(message) {
        const resultDiv = document.getElementById("result");
        resultDiv.className = "result show error";
        resultDiv.innerHTML = `
                <p class="error-message">❌ ${message}</p>
            `;
      }

      function isValidUrl(string) {
        try {
          const url = new URL(string);
          return url.protocol === "http:" || url.protocol === "https:";
        } catch (_) {
          return false;
        }
      }
    </script>
  </body>
</html>
```

---

## Step 3 – Update the API Endpoint

In the HTML code you just copied, find this line:

```javascript
const API_ENDPOINT =
  "https://YOUR-INVOKE-URL-HERE.execute-api.YOUR-REGION.amazonaws.com/shorten";
```

Replace it with your actual API Gateway invoke URL from Step 1.

**Example:**

```javascript
const API_ENDPOINT =
  "https://abc123xyz.execute-api.eu-west-2.amazonaws.com/shorten";
```

> ⚠️ **Important**: Make sure to include `/shorten` at the end of the URL!

Save the file.

---

## Step 4 – Understanding the JavaScript Code

Let's break down what this code does:

**API Configuration:**

- `API_ENDPOINT` - Your API Gateway URL that we'll send requests to

**`shortenUrl()` function:**

- Gets the URL from the input field
- Validates that it's not empty and is a valid URL
- Disables the button and shows "Shortening..." (prevents double-clicks)
- Uses `fetch()` to make a POST request to API Gateway
- Sends the long URL in the request body as JSON
- Handles the response and displays the short URL

**`showSuccess()` function:**

- Displays the shortened URL in a blue box
- Shows the short code for reference

**`showError()` function:**

- Displays error messages in a red box
- Handles validation errors and API errors

**`isValidUrl()` function:**

- Checks that the input is a valid URL
- Ensures it starts with `http://` or `https://`

---

## Step 5 – Upload the Updated File to S3

Now we need to replace the old `index.html` with our new version:

1. Open the **AWS Management Console**
2. Navigate to **S3**
3. Click on your bucket: `url-shortener-frontend-<your-name>`
4. Select the existing `index.html` file (check the box next to it)
5. Click **Delete** and confirm
6. Click **Upload**
7. Click **Add files**
8. Select your updated `index.html` file
9. Click **Upload**

> 💡 **Note**: We delete the old file first to ensure there are no conflicts. Alternatively, you could just upload the new file and it will overwrite the old one.

---

## Step 6 – Clear CloudFront Cache (Important!)

CloudFront caches files, so it might still serve the old version of your `index.html`. We need to clear the cache:

1. Navigate to **CloudFront** in the AWS Console
2. Click on your distribution
3. Click the **Invalidations** tab
4. Click **Create invalidation**
5. In the **Object paths** field, enter: `/index.html`
6. Click **Create invalidation**
7. Wait 1-2 minutes for the invalidation to complete (status will change from "In Progress" to "Completed")

> 💡 **Note**: An invalidation tells CloudFront to fetch the latest version of the file from S3 instead of using the cached version.

---

## Step 7 – Test Your Complete Application

Now let's test everything end-to-end:

1. Open your **CloudFront distribution URL** in a browser
   - Find this in CloudFront → Your distribution → Distribution domain name
   - It looks like: `https://d1a2b3c4d5e6f7.cloudfront.net`

2. You should see your URL shortener page with:
   - A heading "URL Shortener"
   - An input field
   - A "Shorten URL" button

3. Enter a long URL (e.g., `https://www.example.com/very/long/url/path/to/something`)

4. Click **Shorten URL** (or press Enter)

5. You should see:
   - The button briefly shows "Shortening..."
   - A success message appears in a blue box
   - Your shortened URL is displayed (e.g., `https://yourdomain.com/2aB4xYz`)
   - The short code is shown below

---

## Step 8 – Test Error Handling

Let's verify error handling works:

**Test 1: Empty input**

1. Leave the input field empty
2. Click "Shorten URL"
3. You should see: "❌ Please enter a URL" in a red box

**Test 2: Invalid URL**

1. Enter: `not-a-valid-url`
2. Click "Shorten URL"
3. You should see: "❌ Please enter a valid URL..." in a red box

**Test 3: Valid URL**

1. Enter: `https://www.google.com`
2. Click "Shorten URL"
3. You should see a success message with a short URL

---

## Step 9 – Verify Data in DynamoDB

Let's confirm the data is being stored:

1. Navigate to **DynamoDB** in the AWS Console
2. Click **Tables** → **url-mappings**
3. Click **Explore table items**
4. You should see entries for each URL you shortened
5. Each entry should have:
   - `shortCode`: (e.g., `2aB4xYz`)
   - `longUrl`: (the URL you entered)

---

## Step 10 – Open Browser Developer Tools (Learning)

To see what's happening behind the scenes:

1. In your browser, press **F12** (or right-click → Inspect)
2. Click the **Network** tab
3. Enter a URL and click "Shorten URL"
4. You'll see the network requests:
   - **OPTIONS** request to your API (the CORS preflight)
   - **POST** request to your API with the long URL
   - The response with the short code

5. Click the **Console** tab
   - If there are any errors, they'll appear here
   - This is invaluable for debugging

> 💡 **Note**: This is a technique to debug frontend issues. If something doesn't work, check the Console for JavaScript errors and the Network tab for API errors.

---

## Understanding What We Built so far

Our URL shortener application is now:

- ✅ Accepting user input from a web page
- ✅ Validating URLs client-side
- ✅ Sending POST requests to API Gateway
- ✅ Triggering Lambda to generate short codes
- ✅ Storing mappings in DynamoDB
- ✅ Displaying results to users
- ✅ Handling errors gracefully

**The architecture so far:**

```
User Browser (CloudFront/S3)
    ↓ POST request
API Gateway
    ↓ Invoke
Lambda Function
    ↓ Write
DynamoDB
```

---

## Why the Short URLs Don't Redirect Yet

If you try clicking on your shortened URL (e.g., `https://d11xc5qvo3ejev.cloudfront.net/je5UWgw`), you'll get a **403 Forbidden** error.

**This is expected!** We've only built the **URL shortening** part of the application. To make the URLs actually redirect, we would need to add:

1. A second Lambda function to handle redirects
2. An API Gateway GET endpoint that accepts the short code
3. Logic to look up the short code in DynamoDB and redirect users

**What's missing:**

- ❌ Redirect users when they visit short URLs

For now, you can verify your short codes work by checking DynamoDB - the mappings are stored correctly, we just haven't built the redirect handler yet.

## Troubleshooting

**If you see "Failed to connect to the server":**

- Check that you updated `API_ENDPOINT` with your actual API URL
- Verify the URL includes `/shorten` at the end
- Make sure CORS is enabled in API Gateway (especially the OPTIONS method)
- Open browser DevTools → Console to see the exact error

**If you get a CORS error in the browser console:**

- Go to API Gateway → CORS settings
- Verify `Access-Control-Allow-Origin` is your CloudFront Distribution domain name prepend with 'https'. Alternatively set to allow everything: `*`
- Verify `Access-Control-Allow-Methods` includes `POST` and `OPTIONS`
- Verify `Access-Control-Allow-Headers` includes `content-type`
- Save the settings and wait a minute for changes to propagate

**If the page doesn't update after uploading:**

- Create a CloudFront invalidation for `/index.html`
- Wait 1-2 minutes for the invalidation to complete
- Try a hard refresh in your browser (Ctrl+Shift+R or Cmd+Shift+R)

**If you get "Please enter a valid URL":**

- Make sure your URL starts with `http://` or `https://`
- Example: `https://www.example.com` (not just `www.example.com`)

**If nothing happens when you click the button:**

- Open browser DevTools (F12) → Console tab
- Look for JavaScript errors
- Check that you saved the HTML file after updating the API_ENDPOINT
