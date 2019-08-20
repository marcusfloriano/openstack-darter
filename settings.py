
from darter import DarterUtil

config = DarterUtil().get_config("redis")

REDIS_URL = "redis://%s:%s/%s" % (config["host"], config["port"], config["queue"])

# Queues to listen on
QUEUES = ['high']
