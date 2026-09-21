"""One-time script to create the ClientPulse table in local DynamoDB."""

import boto3

dynamodb = boto3.resource(
    "dynamodb",
    endpoint_url="http://localhost:8001",
    region_name="us-east-1",
    aws_access_key_id="local",
    aws_secret_access_key="local",
)

table = dynamodb.create_table(
    TableName="ClientPulse",
    KeySchema=[
        {"AttributeName": "PK", "KeyType": "HASH"},
        {"AttributeName": "SK", "KeyType": "RANGE"},
    ],
    AttributeDefinitions=[
        {"AttributeName": "PK", "AttributeType": "S"},
        {"AttributeName": "SK", "AttributeType": "S"},
    ],
    BillingMode="PAY_PER_REQUEST",
)

table.wait_until_exists()
print("Table 'ClientPulse' created successfully.")