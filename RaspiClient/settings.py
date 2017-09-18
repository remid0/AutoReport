SEVER_ADDRESS = 'http://127.0.0.1:8000/'

# Load local settings
try:
    # pylint: disable=line-too-long,unused-wildcard-import,wildcard-import,wrong-import-position
    from local_settings import *
except ImportError:
    pass
