# AWS URL Shortener – CDK Edition
This repository contains the second iteration of our URL Shortener project. In this phase, we transition from manual configuration (ClickOps) to Infrastructure as Code (IaC) using the AWS Cloud Development Kit (CDK) in Python.

The goal is to recreate the exact same serverless architecture from Iteration 1, but entirely through code that can be deployed, updated, and destroyed with a single command.

---

## Who this is for

Engineers who have completed the "ClickOps" iteration of this project.

Developers familiar with Python who want to treat infrastructure as software.

Cloud Engineers looking to understand the abstraction layers of the AWS CDK.

---

## How to use this repository

Work through the following modules in order to set up your environment and build the stack:

1. Environment & Tooling

    - 00-introduction/the-iac-mindset.md – Why we move away from the Console.

    - 00-introduction/pre-requisites.md – Installing Node.js, AWS CLI, and CDK.

    - 00-introduction/authentication.md – Connecting your terminal to AWS.

2. Initializing the Project

    - 01-initialization/cdk-init.md – Scaffolding the Python project and understanding the directory structure.

    - 01-initialization/the-bootstrap.md – Preparing your AWS account for CDK.

3. Defining Resources (The Code)

    - 02-resources/dynamodb-table.md – Defining stateful resources.

    - 02-resources/lambda-functions.md – Packaging code and managing environment variables.

    - 02-resources/api-gateway.md – Creating the interface and routing.

    - 02-resources/s3-cloudfront.md – Hosting the frontend and OAC permissions.

4. Deployment & Lifecycle

    - 03-deployment/synth-and-deploy.md – Turning Python into CloudFormation.

    - 03-deployment/clean-up.md – How to properly destroy resources to avoid costs.

---

## Important learning principles for this iteration

* **Abstraction over Manual Entry:** We use high-level "Constructs" to handle complex configurations (like IAM policies) automatically.

- **Repeatability:** The goal is to be able to delete everything and redeploy an identical environment in minutes.

- **Version Control:** Your infrastructure is now "text," meaning it can be tracked in Git just like your application code.

- **The "Grant" Pattern:** We replace manual IAM Role creation with CDK’s simplified permission methods (e.g., table.grant_read_write(function)).

---

### Cost awareness

While the services used (S3, Lambda, DynamoDB) remain within the AWS Free Tier for low usage, keep in mind:

- **CDK Bootstrapping:** Creates a small S3 bucket for staging; this is negligible in cost but should be noted.

- **Orphaned Resources:** Always run cdk destroy when finished. If you manually delete items in the console that were created by CDK, your "Stack" may become out of sync (Drift).