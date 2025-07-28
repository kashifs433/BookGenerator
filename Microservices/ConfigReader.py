import os
import yaml

loaded_configs = {}

class ConfigReader():

    @staticmethod
    def find_config_file(config_file_name):

        config_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Config'))
        ConfigFilePath = os.path.join(config_dir, config_file_name)
        if not os.path.exists(ConfigFilePath+".yaml"):
            return None
        else:
            return ConfigFilePath+".yaml"

    @staticmethod
    def get_value(config_file_name, *keys):

        if config_file_name not in loaded_configs:
            file_path = ConfigReader.find_config_file(config_file_name)

            if file_path:
                with open(file_path, "r") as file:
                    loaded_configs[config_file_name] = yaml.safe_load(file) or {}
            else:
                raise ValueError(f"Config file '{config_file_name}.yaml' not found in '{config_dir}' or its subdirectories")


        config_data = loaded_configs.get(config_file_name, {})
        for key in keys:
            config_data = config_data.get(key)
            if config_data is None:
                return None
        return config_data

