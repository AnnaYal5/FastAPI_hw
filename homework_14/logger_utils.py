import logging

logging.basicConfig(
    filename="user_actions.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def log_action(action_type: str, user_info: str):
    logging.info(f"Action: {action_type} | User: {user_info}")
