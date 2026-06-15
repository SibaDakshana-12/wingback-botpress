import time

from app.connector.client import BotpressClient

client = BotpressClient(
    "d140b3e1-2fa4-4a87-8ea5-00fc2cc97d80"
)

user = client.connect()

conversation = client.create_conversation(
    user["key"]
)

conversation_id = conversation["conversation"]["id"]

client.send_message(
    user["key"],
    conversation_id,
    "hello"
)

for i in range(10):
    print(f"\nTRY {i+1}")

    time.sleep(2)

    messages = client.list_messages(
        user["key"],
        conversation_id
    )

    print(messages)

    if len(messages.get("messages", [])) > 1:
        print("BOT REPLIED!")
        break