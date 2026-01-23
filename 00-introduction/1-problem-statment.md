# Problem Statement

The goal of this project is to build a **simple URL shortener** using AWS services.

A URL shortener takes a long URL such as:

`https://www.example.com/some/very/long/path?with=query&parameters=true`

And it turns it into a shorter URL such as:

`https://shorturl.com/abc123`

When a user visits the shortened URL, they are redirected to the original long URL.

---

## Functional requirements

The system must:

1. Provide a web page where a user can submit a URL via a form
2. Generate a shortened version of that URL
3. Store the relationship between the original URL and the shortened URL
4. Allow users to visit the shortened URL and be redirected to the original URL

---

## Out of scope

The system does **not** need to:

- Authenticate users
- Validate URLs thoroughly
- Handle high traffic
- Prevent abuse
- Support custom domains
- Be production-ready

These concerns are deliberately deferred so that learning can focus on **core AWS concepts first**.

---

#### Prerequisites

1. An AWS account
2. Code editor
3. Basic understanding a programming concepts

### Task overview

1. Build a web page with a form with an input field for a URL and a button to submit this, hosted on AWS.
2. Create an endpoint that submits the URL to be shortened and returns this to the user. The original and shortened URLs should be stored in a database
3. Create a second endpoint that accepts a shortened URL, returns it from the database, and directs the user to it.
