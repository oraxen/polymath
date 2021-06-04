import os
import toml
import shutil
import utils


class Config:

    def extract(self, file_name, template_name):
        config_file = utils.get_path(file_name)
        if not os.path.isfile(config_file):
            self.configured = False
            print(f"config {file_name} doesn't exist, copying template!")
            shutil.copyfile(utils.get_path(template_name), config_file)
        return config_file


class TomlConfig(Config):
    def __init__(self, file_name, template_name):
        self.configured = True
        config_file = self.extract(file_name, template_name)
        self.load(config_file)

    def load(self, config_file):
        self._config = toml.load(config_file)

    def __getitem__(self, key):
        return self._config[key]