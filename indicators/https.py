#script to check the use of https

#include libs
import sys
sys.path.insert(0, '..')
from include import *

today = date.today()

def get_scheme(url):
    parsed = urlparse(url)
    return parsed.scheme


def https(result_url, hash):
    scheme = get_scheme(result_url)
    module = 'check https'
    value = '0'

    if scheme == 'https':
        value = '1'

    check_evaluations_result(hash, module, value)
