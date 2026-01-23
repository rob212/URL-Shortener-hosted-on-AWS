# Hosting the Frontend with Amazon S3

In this step, we will host our static website using **Amazon S3** so that it can be accessed publicly over the internet via a Cloudfront distribution we will create in a subsequent step.

This allows us to:

- Serve our `index.html` file from AWS
- Access the site via a public URL
- Prepare the frontend to call our backend APIs later

---

## What we are doing

We will:

1. Create an S3 bucket
2. Upload our `index.html` file
3. Access the site via an AWS-provided URL

We will achieve this all through the **AWS Management Console**.

---

## Why Amazon S3?

Amazon S3 is:

- Extremely cheap
- Highly durable
- Simple to configure
- Ideal for static assets

---

## Step 1 – Create an S3 bucket

> See [AWS S3 Docs for further details](https://docs.aws.amazon.com/AmazonS3/latest/userguide/GetStartedWithS3.html#creating-bucket)

1. Open the **AWS Management Console**
2. Navigate to **S3**
3. Ensure you are in the desired Region for your bucket, for latency purposes, choose a region close to you (for example `eu-west-2`)
4. Click **Create bucket**

### Bucket configuration

- **Bucket type**:
  'General purpose'

- **Bucket name**:  
  Choose a globally unique name, for example:

`url-shortener-frontend-<your-name>`

- **Object Ownership**:
  Choose the recommended 'ACLs disabled'

- **Block Public Access settings for this bucket**
  Keep the default 'Block _all_ public access' checked.

  > ⚠️ **Note**: it is a valid options to host a static website directly from a publicly accessible S3, however, this violates AWS Burner account terms of service.

  We will thefore keep the S3 bucket that hosts our `index.html` private and make this accessible via a Cloudfront distribution in a later step.

- **Bucket Versioning**
  Keep the disabled

- **Default encryption**
  Keep these options as their defaults

---

## Step 2 – Upload the website file

1. Open your newly created bucket
2. Click **Upload**
3. Click **Add files**
4. Select your `index.html` file
5. Click **Upload**

Once uploaded, you should see `index.html` listed in the bucket.

---

Congratulations, you have successfully created an S3 bucket and used it to store your website content.
