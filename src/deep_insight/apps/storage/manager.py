from deep_insight.apps.storage.drivers.fs import FSDriver
from deep_insight.common.conf import CONF


def get_storage_driver():
    if CONF.storage.driver == "fs":
        return FSDriver()

    raise Exception(f"storage {CONF.storage.driver} is not supported")
