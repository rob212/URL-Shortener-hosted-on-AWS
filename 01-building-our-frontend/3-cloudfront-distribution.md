# Making your frontend publicly accessible via CloudFront

In this step, we will create an AWS CloudFront distribution in order to make our website publicly accessible on the web.

CloudFront is a content delivery network (CDN) that enables you to deliver static or dynamic web content worldwide through a network of data centres called "edge locations".

When an end user navigates our site, their request is routed to the edge location nearest to them geographically, with the intention of providing the lowest latency for the user. CloudFront takes care of replicating our static site `index.html` and delivering it across it's edge locations.

In addition to reduced latency, serving our site through CloudFront, as opposed to a publicly available S3 bucket also ensures we can keep our S3 bucket private.

---

## What we are doing

We will:

1. Create a CloudFront distribution with our S3 bucket as the origin.
2. Set our webpage as the default root object in our CloudFront distribution.
3. Review our updated S3 bucket policy to allow CloudFront to access it.

We will achieve this all through the **AWS Management Console**.

---

## Step 1 – Create a CloudFront distribution

1. Open the **AWS Management Console**
2. Navigate to **CloudFront**
3. Click **Create distribution**
4. Select the 'Free' plan

> Note: CloudFront is a _global_ AWS service, so you do not need to select a Region as we did for our S3 bucket.

### Distribution configuration

- **Choose a plan**:
  Select the 'Free' plan

- **Distribution name**:  
  Choose a distribution name, for example:

`url-shortener-cdn-<your-name>`

- **Distribution type**
  'Single website or app

- **Origin type**:
  'Amazon S3'

- **Origin - S3 origin**
  Either type in your S3 bucket name or select it via 'Browse S3'

- **Settings**
  Keep 'Allow private S3 bucket access to CloudFront' checked. This will automativally update the S3 bucket policy on our bucket to allow our CloudFront distribution to access it.

  > ⚠️ **Note**: we also have the ability to manually update the S3 bucket policy within the S3 console. I advise to take a look at the policy changes that have been implemented for us for your learning.

- **Origin settings**
  Use recommended origin settings

- **Cache settings**
  Use recommended cache settings tailored to serving S3 content

- **Enable security - Web Application Firewall (WAF)**
  leave disabled

### Step 2 - Set our webpage as the default root object in our CloudFront distribution.

We now need to define the default root object which is our `index.html` file. If we don't do this, requests to the root of our distribution pass to our origin server, in our instance our S3 bucket. This will result in an 'HTTP 403 - Forbidden' error due to the configuration of our bucket.

**In order to set the default root object in our CloudFront distribution**

1. In the CloudFront console click on your distribution ID to open it
2. Click the 'General' tab (should be selected by default)
3. In the 'Settings' section, click the 'Edit' button
4. Scroll down until you find the **Default root object** field and enter `index.html`
5. Save the changes

### Step 3 - Review our S3 bucket permission change

Navigate to your S3 bucket and look at the 'Bucket policy' under the 'Permissions' tab. It should have been updated to something resembling:

```
{
    "Version": "2008-10-17",
    "Id": "PolicyForCloudFrontPrivateContent",
    "Statement": [
        {
            "Sid": "AllowCloudFrontServicePrincipal",
            "Effect": "Allow",
            "Principal": {
                "Service": "cloudfront.amazonaws.com"
            },
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::<your-s3-bucket-name>/*",
            "Condition": {
                "ArnLike": {
                    "AWS:SourceArn": "arn:aws:cloudfront::182090060122:distribution/<your-CloudFront-distribution-ID>"
                }
            }
        }
    ]
}
```

### Confirm your static website is publicly accessible

Once your changes propogate (should only take a few seconds) navigate to your 'Distribution domain name' in your web browser of choice.

You can find this in the CloudFront 'Dashboard' in the AWS Management Console.

E.g: d11xc5qvo3ejev.cloudfront.net
