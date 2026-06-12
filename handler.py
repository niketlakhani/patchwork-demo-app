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

    user_id    = body.get("user_id")
    item       = body.get("item")
    quantity   = body.get("quantity")
    unit_price = body.get("unit_price")

    missing = [f for f in ("user_id", "item", "quantity", "unit_price") if body.get(f) is None]
    if missing:
        logger.warning("Bad request — missing required fields: %s", missing)
        return {
            "statusCode": 400,
            "body": json.dumps({"error": f"Missing required fields: {missing}"}),
        }

    total = quantity * unit_price
    logger.info("Priced order for user=%s item=%s total=%s", user_id, item, total)

    return {
        "statusCode": 200,
        "body": json.dumps({"user_id": user_id, "item": item, "total": total}),
    }
