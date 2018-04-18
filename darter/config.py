
import os
import yaml

UNIX_CONFIG_HOME = os.path.join(os.path.expanduser(os.path.join('~', '.config')), 'darter')
UNIX_SITE_CONFIG_HOME = '/etc/darter'


CONFIG_SEARCH_PATH = [
    os.getcwd(),
    UNIX_CONFIG_HOME, UNIX_SITE_CONFIG_HOME
]


YAML_SUFFIXES = ('.yaml', '.yml')


CONFIG_FILES = [
    os.path.join(d, 'darter' + s)
    for d in CONFIG_SEARCH_PATH
    for s in YAML_SUFFIXES
]


class DarterConfig:

    def __init__(self):
        self.filelist = CONFIG_FILES
        self.config_filename, self.darter_config = self._load()

    def get(self, key):
        if key in self.darter_config:
            return self.darter_config[key]
        else:
            raise KeyError("Key for % config not exists" % self.config_filename)

    def _load(self):
        for path in self.filelist:
            if os.path.exists(path):
                with open(path, 'r') as f:
                    return path, yaml.safe_load(f)
        return None, {}
