import yaml


class AppConfig:
    def __init__(self):
        config_path = r".\config.yaml"
        with open(config_path, 'r') as ymlFile:
            self.cfg = yaml.load(ymlFile, Loader=yaml.FullLoader)

    def get_logs_path(self, path=None, level=None):
        if path:
            return self.cfg['log']['path']
        elif level:
            return self.cfg['log']['level']

    def get_rotaion_retention(self, rotation=None, retention=None):
        if rotation:
            return self.cfg['log']['rotation']
        elif retention:
            return self.cfg['log']['retention']

    def get_mqtt_uri(self):
        return self.cfg["mqtt"]
    def get_mqtt_subscribe_topic(self):
        return self.cfg["mqtt"]['topic']

    def get_mongo_uri(self):
        return self.cfg["mongodb"]

    def get_image_path(self):
        return self.cfg['details']['image']

    def get_gif_path(self):
        return self.cfg['details']['gif']

    def get_video_path(self):
        return self.cfg['details']['video']

    def get_document_path(self):
        return self.cfg['details']['document']

    def get_api_id(self):
        return self.cfg['telegram']['api_id']

    def get_hash_id(self):
        return self.cfg['telegram']['hash_id']
