import ssl
import sys
import traceback
import paho.mqtt.client as mqtt
from loguru import logger
from app_config import AppConfig
from meta_log import all_logs_config
from telegram_client import send_telegram_message

all_logs_config()
app_config = AppConfig()
service_name = None


class MqttConnector:
    def __init__(self):
        try:
            self.main_topics_subscribe = [(app_config.get_mqtt_subscribe_topic(), 0)]
            self.qos = app_config.get_mqtt_uri()["qos"]
            self.mqtt_client = mqtt.Client()
        except Exception as e:
            logger.error(f'Got Exception is {e}')

    def on_connect(self, client, userdata, flag, rc):
        try:
            logger.info(f'Connected to broker- {self.mqtt_client.is_connected()}')
            if rc == 0:
                print("Connected to broker")
                self.mqtt_client.subscribe(app_config.get_mqtt_subscribe_topic())
                print(self.main_topics_subscribe)

                logger.info(f"{self.main_topics_subscribe} topic has been subscribed")
            else:
                self.mqtt_client.unsubscribe(self.main_topics_subscribe)
                print(self.main_topics_subscribe)
        except Exception as e:
            traceback.print_exc()
            logger.error(f'Connection Exception is {e}')

    def on_message(self, client, userdata, message):
        try:
            logger.debug(f"msg has been arrived from collector service {message}")
            send_telegram_message(message.payload.decode())
        except Exception as e:
            logger.error(f'Got Exception is {e}')

    def start_subscribing(self):
        try:
            logger.debug(f'Subscribing to {self.main_topics_subscribe}')
            if self.mqtt_client:
                self.mqtt_client.on_connect = self.on_connect
                self.mqtt_client.on_message = self.on_message
                certificate = None
                tls_port = app_config.get_mqtt_uri()["tls_port"]
                is_tls_ = app_config.get_mqtt_uri()["is_tls"]
                broker_addr, port = app_config.get_mqtt_uri()["host"], tls_port if is_tls_ else \
                    app_config.get_mqtt_uri()["port"]
                self.mqtt_client.connect(broker_addr, port, app_config.get_mqtt_uri()["keep_alive"])
                self.mqtt_client.loop_forever()

        except Exception as e:
            logger.error(f'Got Exception is {e}')
