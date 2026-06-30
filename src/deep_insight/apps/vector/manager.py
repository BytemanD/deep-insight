from deep_insight.apps.vector.drivers.chromadb import ChromadbDriver
from deep_insight.common.conf import CONF


def get_vector_driver():
    if CONF.vector.driver == "chromadb":
        return ChromadbDriver()

    raise Exception(f"{CONF.vector.driver} is not supported")
