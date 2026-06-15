import httpx


class BotpressClient:
    def __init__(self, webhook_id: str):
        self.webhook_id = webhook_id
        self.base_url = f"https://chat.botpress.cloud/{webhook_id}"

        self.client = httpx.Client(
            timeout=30
        )

    def hello(self):
        r = self.client.get(
            f"{self.base_url}/hello"
        )
        r.raise_for_status()

        return r.text

    def connect(self):
        r = self.client.post(
            f"{self.base_url}/users",
            json={
                "name": "Wingback Test User"
            }
        )

        print("STATUS:", r.status_code)
        print("BODY:", r.text)

        r.raise_for_status()

        return r.json()

    def create_conversation(
        self,
        user_key: str,
    ):
        r = self.client.post(
            f"{self.base_url}/conversations",
            headers={
                "x-user-key": user_key
            },
            json={
                "body": {}
            }
        )

        print("STATUS:", r.status_code)
        print("BODY:", r.text)

        r.raise_for_status()

        return r.json()

    def send_message(
        self,
        user_key: str,
        conversation_id: str,
        text: str,
    ):
        r = self.client.post(
            f"{self.base_url}/messages",
            headers={
                "x-user-key": user_key
            },
            json={
                "payload": {
                    "type": "text",
                    "text": text
                },
                "conversationId": conversation_id
            }
        )

        print("SEND STATUS:", r.status_code)
        print("SEND BODY:", r.text)

        r.raise_for_status()

        return r.json()

    def list_messages(
        self,
        user_key: str,
        conversation_id: str,
    ):
        r = self.client.get(
            f"{self.base_url}/conversations/{conversation_id}/messages",
            headers={
                "x-user-key": user_key
            }
        )

        print("LIST STATUS:", r.status_code)
        print("LIST BODY:", r.text)

        r.raise_for_status()

        return r.json()
