# Copyright (C) 2018-2026 by xcentaurix
# License: GNU General Public License v3.0


import os
from enigma import loadPNG
from Components.config import config
from .Debug import logger
from .ServiceUtils import getPicon as getEnigmaPicon


def getPicon(service_ref):
    """The picon of a service: from the plugin's picon directory if it has one for the service reference
    (<picon dir>/1_0_19_2855_401_1_C00000_0_0_0.png), else the one Enigma2's own picon lookup finds."""
    picon_dir = config.plugins.tvmagazinecockpit.piconspath.value
    if picon_dir and service_ref:
        path = os.path.join(picon_dir, service_ref.rstrip(":").replace(":", "_") + ".png")
        if os.path.isfile(path):
            logger.debug("picon: %s", path)
            return loadPNG(path)
    return getEnigmaPicon(service_ref)
