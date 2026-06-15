import time

from .client import BotpressClient


class BotpressScanner:
    def __init__(self, target_config: dict):
        self.config = target_config

        self.client = BotpressClient(
            target_config["webhook_id"]
        )

    def validate_target(self) -> bool:
        try:
            self.client.hello()
            return True
        except Exception:
            return False

    def execute_test(
        self,
        vulnerability_id: str,
        attack_id: str,
        test_input: str,
    ):
        start = time.time()

        try:
            user = self.client.connect()

            conversation = self.client.create_conversation(
                user["key"]
            )

            conversation_id = conversation["conversation"]["id"]

            sent_message = self.client.send_message(
                user["key"],
                conversation_id,
                test_input
            )

            message_id = sent_message["message"]["id"]

            bot_response = None

            for _ in range(10):
                time.sleep(2)

                messages = self.client.list_messages(
                    user["key"],
                    conversation_id
                )

                if len(messages.get("messages", [])) > 1:
                    for msg in messages["messages"]:
                        payload = msg.get("payload", {})

                        if (
                            payload.get("type") == "text"
                            and msg["userId"]
                            != user["user"]["id"]
                        ):
                            bot_response = payload.get("text")
                            break

                if bot_response:
                    break

            return {
                "success": bot_response is not None,
                "model_response": bot_response,
                "execution_time_ms": int(
                    (time.time() - start) * 1000
                ),
                "error": None,
                "metadata": {
                    "platform": "botpress",
                    "conversation_id": conversation_id,
                    "message_id": message_id,
                    "delivery_mode": "poll",
                    "vulnerability_id": vulnerability_id,
                    "attack_id": attack_id,
                },
            }

        except Exception as e:
            return {
                "success": False,
                "model_response": None,
                "execution_time_ms": int(
                    (time.time() - start) * 1000
                ),
                "error": str(e),
                "metadata": {
                    "platform": "botpress",
                },
            }

    def reset_conversation(self):
        pass

    def get_platform_metadata(self):
        return {
            "platform": "botpress",
            "webhook_id": self.config["webhook_id"],
        }