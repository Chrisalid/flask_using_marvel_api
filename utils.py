
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


def link(ts, public_key, hash_md5):
    ''' Return URL of Marvel API

    Args:
        ts: String
        public_key = String
        hash_md5 = String

    Notes:
        Use ts, public_key and hash_md5 for create
        a URL to make request in Marvel API.
    '''

    base = 'https://gateway.marvel.com'
    req = '/v1/public/characters?name={}&orderBy=name&limit=1'
    url = base+req+'&ts='+ts+'&apikey='+public_key+'&hash='+hash_md5

    return url
