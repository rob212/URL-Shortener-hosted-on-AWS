# Creating the DynamoDB Table

In this step, we will create a **DynamoDB table** to store the mappings between long URLs and their shortened versions.

This allows us to:

- Store URL mappings persistently
- Retrieve shortened URLs quickly
- Scale automatically as our application grows

---

## What we are doing

We will:

1. Create a DynamoDB table
2. Configure the primary key structure
3. Understand the data model for our URL shortener

We will achieve this all through the **AWS Management Console**.

---

## Why Amazon DynamoDB?

Amazon DynamoDB is:

- Fully managed (no servers to maintain)
- Highly scalable
- Fast and predictable performance
- Pay-per-use with generous free tier
- Perfect for key-value lookups like URL mappings

---

## Understanding Our Data Model

Our table will store two main pieces of information:

- **shortCode** (Primary Key): The unique identifier for the shortened URL (e.g., `abc123`)
- **longUrl**: The original URL that we want to shorten

**Example item:**

```json
{
  "shortCode": "abc123",
  "longUrl": "https://www.example.com/very/long/url/path"
}
```

When a user visits `shorturl.com/abc123`, we'll look up `abc123` in the table and redirect them to the `longUrl`.

---

## Step 1 – Create a DynamoDB Table

> See [AWS DynamoDB Docs for further details](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/getting-started-step-1.html)

1. Open the **AWS Management Console**
2. Navigate to **DynamoDB**
3. Ensure you are in the same region as our S3 bucket (e.g. `eu-west-2`)
4. Click **Create table**

### Table configuration

- **Table name**:  
  Choose a descriptive name, for example:

  `url-mappings`

- **Partition key**:  
  Enter: `shortCode`  
  Type: `String`

  > 💡 **Note**: The partition key is how DynamoDB will uniquely identify each URL mapping. Since we're using Base62 conversion in our Lambda function, each `shortCode` will be unique.

- **Sort key**:  
  Leave this blank (not needed for our use case)

  > 💡 **Note**: Unlike traditional SQL databases, DynamoDB doesn't require you to define all columns (attributes) upfront. We only need to define the primary key (`shortCode`). Other attributes like `longUrl` can be added when we insert items into the table from our Lambda function.

- **Table settings**:  
  Keep the default **'Default settings'** selected

  This will:
  - Use **On-demand** capacity mode (pay only for what you use)
  - Enable encryption at rest
  - Create with recommended settings for most applications

  > 💡 **Alternative**: If you expect consistent, predictable traffic, you could choose **'Customize settings'** and select **Provisioned** capacity mode. For this beginner project, **On-demand** is simpler and more cost-effective.

5. Click **Create table**

---

## Step 2 – Wait for Table Creation

The table creation process typically takes less than a minute.

1. You'll see the table status as **"Creating"**
2. Wait until the status changes to **"Active"**
3. Once active, your table is ready to use

---

## Step 3 – Verify Your Table

1. Click on your table name (`url-mappings`) to view its details
2. Review the **Settings** tab to see:
   - Partition key (`shortCode`)
   - Item count (currently 0)
   - Table size (currently 0 bytes)

---

## Understanding What We Built

Your DynamoDB table is now ready to:

- Accept write requests from your Lambda function when a user submits a long URL
- Return the original long URL when someone accesses a shortened link
- Scale automatically as your application grows

In the next step, we'll create a Lambda function that will write to this table and generate the Base62 short codes.

---

## Optional: Manually Test Your Table

If you want to verify everything is working before moving on:

1. In your table, click the **"Explore table items"** button
2. Click **"Create item"**
3. Add the following:
   - `shortCode`: `test123`
   - Click **"Add new attribute"** → **String**
   - Attribute name: `longUrl`
   - Value: `https://www.example.com`
4. Click **"Create item"**

You should now see one item in your table. You can delete this test item before proceeding.

---

Congratulations! You have successfully created a DynamoDB table to store our URL mappings.
