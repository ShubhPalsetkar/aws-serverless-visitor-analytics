import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("VisitorAnalytics")

def lambda_handler(event, context):
    try:
        response = table.update_item(
            Key={"id": "homepage"},
            UpdateExpression="ADD visit_count :inc",
            ExpressionAttributeValues={":inc": Decimal(1)},
            ReturnValues="UPDATED_NEW"
        )

        visit_count = int(response["Attributes"]["visit_count"])

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "message": "Visitor count updated successfully",
                "visit_count": visit_count
            })
        }

    except Exception as error:
        print("Error:", str(error))

        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "message": "Error updating visitor count",
                "error": str(error)
            })
        }