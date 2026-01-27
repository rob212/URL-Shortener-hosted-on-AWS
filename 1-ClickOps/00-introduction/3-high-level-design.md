## Back of the envelope estimates

When designing a system, architectural desicisions should factor in capacity needs, availability, scalability and fault tolerance. This goes beyond the scope of this exercise. But here is a quick run down of a possible calculation that would aid in decision making to ensure we select appropriate services to be part of our solution.

Assumptions:

- Write operations: 10 million URLs are generated per day.

- Write operations per second: 10 million / 24 _(hrs)_ /3600 _(seconds)_ = 116

- Read operations: Assuming ratio of read operation to write operation is 10:1, read operation per second: 116 \* 10 = 1,160

- Assuming the URL shortener service will run for 10 years, this means we must support 10 million _ 365 _ 10 = 36.5 billion records.

- Assume average URL length is 100.

Storage requirement over 10 years: 36.5 billion \* 100 bytes = **3.65 TB**

---

## API Endpoints

> If you are unfamiliar with restful API see this tutorial: https://www.restapitutorial.com/

We need two API endpoints:

1. **URL shortener** - To create a new short URL, a client will send a POST request containing one parameter; the original long URL.

```
POST api/v1/shorten

- request parameter: {longUrl: longURLString}
- return: shortURL
```

2. **URL redirecting** - To redirect a short URL to the corresponding long URL, a client sends a GET request.

```
GET api/v1/{shortCode}

- return longURL for HTTP redirection
```

## AWS Architecture

![AWS Architecture](./../docs/url_shortener_serverless_architecture.svg)
