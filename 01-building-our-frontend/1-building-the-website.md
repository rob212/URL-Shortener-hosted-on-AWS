# Building the Frontend – A Simple Static Website

In this step, we will build the **simplest possible frontend** for our URL shortener.

The goal is **not** to learn frontend frameworks, styling, or UX design.  
The goal is to create a minimal web page that allows us to interact with AWS services.

---

## What we are building

We will create a **single static HTML page** that:

- Contains an input field for a long URL
- Contains a button to submit that URL
- Displays the shortened URL returned by our backend

There will be:

- No styling
- No frameworks
- No build tools
- No authentication
- No client-side validation

This is intentional.

---

## Technology choice

We will use:

- Plain **HTML**
- A small amount of **JavaScript**
- No external dependencies

This allows us to:

- Run the site locally by opening a file
- Upload it directly to an S3 bucket
- Avoid any build or deployment steps

---

## Creating the HTML file

Create a new file called:

`index.html`

> I have included a small amount of inline CSS purely to improve readability. Styling is not a learning goal of this exercise and can be ignored entirely when focusing on AWS

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
      // Replace this with your API Gateway endpoint
      const API_ENDPOINT = "REPLACE_WITH_API_GATEWAY_URL/shorten";

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
                 <a href="${shortUrl}" class="short-url" target="_blank">${shortUrl}</a>
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

### Understanding what this page does

At a high level:

1. The user enters a long URL
2. The browser sends a POST request to an API
3. The API returns a shortened URL
4. The page displays the result

This page has **no knowledge of AWS**.It only knows how to make an HTTP request, this seperation of concerns is important as a means to build a decoupled system.

---

## Running the site locally

You can run this page locally by double-clicking the index.html in you mac finder.

When running locally, the page may fail when you submit the form due to **CORS** (Cross-Origin Resources Sharing). Handling CORS is a backend responsibility and something we will address when configuring our API Gateway.

---

## Next steps

We now have a simple frontend running locally on our machine contained entirely in our `index.html` file. Next we will upload this file to an AWS S3 bucket with 'static website hosting' enabled without any build steps and it will run as a static website that wll be accessible via an AWS-hosted URL.
