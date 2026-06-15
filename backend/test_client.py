from app.connector.client import BotpressClient

client = BotpressClient(
    "d140b3e1-2fa4-4a87-8ea5-00fc2cc97d80"
)

print(client.hello())