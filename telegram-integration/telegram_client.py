import time
import json

from loguru import logger
from telethon import TelegramClient

from app_config import AppConfig

app_conf = AppConfig()
# api_id = 22241399
# api_hash = '5d8a24d581e2c1d3c97d06c36e516b19'
# phone_number = '8050675891'
# user_ids = ['@chini_23','@sandy6255']
api_id = app_conf.get_api_id()
api_hash = app_conf.get_hash_id()

client = TelegramClient('session_name', api_id, api_hash)


# _json = {
#     "phone_no": 8050675891,
#    "tel_username": "@chini_23",
#    "type": "DirectNotification",
#    "action": "Login",
#    "service": "Theiox_api",
#    "data": {
#        "message": "535171 is your Theiox Verification code for Signin. This code is valid till 2023-11-08 13:00:00. Elmeasure"
#    }
# }

def send_telegram_message(message):
    parsed_message = json.loads(message)
    with TelegramClient("session_name", api_id, api_hash) as client:
        client.loop.run_until_complete(client.send_message(parsed_message['phone_no'], parsed_message['data'].get('message')))



async def send_message_async(message, phone_number=None):
    try:
        logger.info("Connecting to Telegram...")
        await client.connect()

        tel_parm = json.loads(message.payload.decode())
        phone_no = tel_parm.get("phone_no")
        user_id = json.loads(message.payload.decode()).get('tel_username')

        if not await client.is_user_authorized():
            logger.info("Authorization required. Sending code request...")
            await client.send_code_request(phone_number)

            logger.info("Signing in...")
            code = input('Enter the code: ')
            await client.sign_in(phone_number, code)

        # Send a message
        logger.info("Sending a message...")
        await client.send_message(user_id, message)
        time.sleep(1)

        # Send a photo
        logger.info("Sending a photo...")
        photo_path = app_conf.get_image_path()
        await client.send_file(user_id, file=photo_path, caption='Here is a photo!')
        time.sleep(1)

        # Send a GIF
        logger.info("Sending a GIF...")
        gif_path = app_conf.get_gif_path()
        await client.send_file(user_id, file=gif_path, caption='Here is a GIF!')
        time.sleep(1)

        # Send a video
        logger.info("Sending a video...")
        video_path = app_conf.get_video_path()
        await client.send_file(user_id, file=video_path, caption='Here is a video!')
        time.sleep(1)

        # Send an Excel file or any other document
        logger.info("Sending a document...")
        document_path = app_conf.get_document_path()
        await client.send_file(user_id, file=document_path, caption='Here is a document!')
        time.sleep(1)

        logger.info("Messages, photo, GIF, video, and document sent successfully.")
    except Exception as e:
        logger.error(f"Failed to send messages or files. Error: {e}")
    finally:
        logger.info("Disconnecting from Telegram...")
        client.disconnect()

# async def send_to_multiple_users(user_ids):
#     for user_id in user_ids:
#        await send_telegram_message(user_id)


# with client:
#    client.loop.run_until_complete(send_to_multiple_users(user_ids))
