import requests
import logging

def send_error_notification(webhook_url, error_buffer):
    payload = {"errors": error_buffer}
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(webhook_url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        logging.info(f"Sent {len(error_buffer)} notifications successfully.")
    except requests.RequestException as e:
        logging.error(f"Failed to send notifications: {e}")