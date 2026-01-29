# AWS URL Shortener – Learning Project

This repository contains a step-by-step learning exercise designed to help Software Engineers understand core AWS services by building a **simple URL shortener**.

---

## Who this is for

- Junior Software Engineers learning AWS
- Engineers new to serverless architectures
- Anyone who wants hands-on, practical AWS experience
- Teams looking for a shared reference project

This is **not** a production-ready system. It is a learning tool.

---

## How to use this repository

Work through the repository **in order**:

1. Start with the introduction:

   - `00-introduction/1-problem-statement.md`
   - `00-introduction/2-learning-goals.md`
   - `00-introduction/3-high-level-design.md`

2. Then complete **Building our Frontend**:
   - `01-building-our-frontend/1-building-the-website.md`
   - `01-building-our-frontend/2-s3-bucket-web-hosting.md`
   - `01-building-our-frontend/3-cloudfront-distribution.md`

3. Finally **Building our AWS Serverless Backend**:
   - `02-building-our-aws-serverless-backend/1-dynamodb-table.md`
   - `02-building-our-aws-serverless-backend/2-lambda-shortener-function.md`
   - `02-building-our-aws-serverless-backend/3-api-gateway.md`
   - `02-building-our-aws-serverless-backend/4-connecting-frontend-backed.md`
   - `02-building-our-aws-serverless-backend/5-lambda-for-redirection.md`

Each iteration:

- Explains the architecture
- Walks through AWS Console setup step-by-step

---

## Important learning principles for this iteration of the challenge

- All AWS resources are created **manually via the AWS Management Console**
- The focus is on **understanding AWS services**
- Simplicity is preferred over best practices in early iterations

---

## Cost awareness

Learners should always:

- Delete resources when finished
- Monitor AWS billing dashboards
- Understand which services incur costs
