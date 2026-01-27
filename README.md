# AWS Learning: The URL Shortener Journey

This repository is a practical learning path to develop your AWS skills. W 
We  will build, tear down, and rebuild a **URL Shortener** multiple times, evolving the architecture and deployment methodology in each iteration.

The goal is to gain experience with a variety of AWS services, infrastructure patterns, and the trade-offs between different cloud strategies.

---

## The Learning Path

We purposefully build the same URL Shortener application in each stage to ensure we focus our attention of the AWS specific elements, minimising the overhead of a variety of web applications to learn about.

### 📂 [1-ClickOps](./1-ClickOps)
**Focus:** Mental Models & Service Fundamentals.
- **Architecture:** Serverless (S3, CloudFront, Lambda, API Gateway, DynamoDB).
- **Method:** Manual configuration via the AWS Management Console.
- **Goal:** Understand how services connect and function without the abstraction of code.

### 📂 [2-CDK](./2-CDK)
**Focus:** Infrastructure as Code (IaC).
- **Architecture:** Serverless (Identical to Iteration 1).
- **Method:** AWS Cloud Development Kit (CDK) in Python.
- **Goal:** Learn to version, deploy, and manage infrastructure using software engineering principles.

### 📂 3-Containers (Coming Soon)
**Focus:** Orchestration & Compute abstraction.
- **Architecture:** Moving logic from Lambda to Fargate/ECS.
- **Method:** Dockerization and Load Balancing.

### 📂 4-EC2 (Coming Soon)
**Focus:** Redundancy, Load Balancing and VPC management
- **Architecture:** EC2 Auto-scaling groups, VPCs and Load Balancers.

---

## Core Philosophy

1.  **Architecture over Syntax:** We focus on *why* a service is chosen and *how* it talks to others.
2.  **Repeatability:** By the end of the CDK phase, you should be able to deploy a full stack in minutes.
3.  **Cost Awareness:** Every exercise is designed to stay within the **AWS Free Tier** where possible.
4.  **Mentor-Led:** Each folder contains step-by-step guides, architectural diagrams, and "Expert Tips" to avoid common pitfalls.

---

## Prerequisites

Before starting any iteration, ensure you have an active **AWS Account**. Follow the instructions within the specific iteration folders to set up your local environment.

---

