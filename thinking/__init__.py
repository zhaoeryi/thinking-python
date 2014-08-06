from __future__ import print_function

import logging.config
#from oslo.config import cfg

print("package ", __file__, "is loaded")

# see example at: nova\openstack\common\log.py
log_config = "/home/zhyizhyi/workspace/stack/thinking-python/thinking/logging.conf"
if log_config:
    logging.config.fileConfig(log_config)

logger = logging.getLogger("thinking")
#CONF = cfg.CONF
#CONF(args=['--config-file', '/home/zhyizhyi/workspace/stack/thinking-python/thinking/thinking.conf'])
