"""
order-service — a small Lambda that prices an incoming order.

Deployed to AWS Lambda; logs to CloudWatch. Monitored by the Patchwork
incident-response agent.
"""
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """Price an order from the request body.

    Expected body: {"user_id": str, "item": str, "quantity": int, "unit_price": number}
    Returns the line total.
    """
    body = event.get("body", {})
    if isinstance(body, str):
        body = json.loads(body)

    user_id = body["user_id"]
    item = body["item"]

    # BUG: assumes "quantity" is always present. Real-world callers sometimes
    # omit it (e.g. a "save for later" action), which raises KeyError and 500s.
    quantity = body["quantity"]
    unit_price = body["unit_price"]

    total = quantity * unit_price
    logger.info("Priced order for user=%s item=%s total=%s", user_id, item, total)

    return {
        "statusCode": 200,
        "body": json.dumps({"user_id": user_id, "item": item, "total": total}),
    }
