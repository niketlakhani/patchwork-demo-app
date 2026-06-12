# order-service (Patchwork demo app)

A tiny AWS Lambda that prices an incoming order. Deployed to AWS, logs to CloudWatch,
and monitored by the **Patchwork** autonomous incident-response agent.

When an unhandled error reaches CloudWatch, Patchwork diagnoses it, writes a fix, and
opens a pull request against this repo.

## Endpoint contract

`POST` with JSON body:

```json
{ "user_id": "u-1", "item": "widget", "quantity": 3, "unit_price": 9.99 }
```

Returns the line total.
