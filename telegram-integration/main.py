import time
from asyncio.log import logger

from mqtt_client import MqttConnector


def start_running():
    try:
        # global thread_list
        thread_ = MqttConnector()
        # thread_ = multiprocessing.Process(target=thread_.start_subscribing,
        #                                   name=f'cloud_publish/{industry.get("client_id")}')
        thread_.start_subscribing()
        #     thread_list.append(thread_)
        # for thread_ in thread_list:
        #     thread_.join()
    except Exception as e:
        print(logger.error(f'Got Exception is {e}'))


if __name__ == '__main__':
    start_running()
    print("service is running")
    while True:
        time.sleep(1)
        pass
