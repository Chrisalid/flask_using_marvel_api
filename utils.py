
import time
from decouple import config
from hashlib import md5


def hashcode():
    ''' Variables Used for API Consumption

    Notes:
        The variables above are the variables
        used to consume the Marvel API
'''

    ts = str(time.time())
    PRIVATE_KEY = config('PRIVATE_KEY')
    public_key = '869987b325cf1b23991e5babc934e8e7'

    join_string = bytes(ts+PRIVATE_KEY+public_key, 'utf-8')

    hash = md5(join_string)

    hash_md5 = hash.hexdigest()

    return ts, public_key, hash_md5
