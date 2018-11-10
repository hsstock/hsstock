import time

from hsstock.common.freqlimit import FreqLimit

DEFAULT_FMT = '[{elapsed:0.8f}s] {name}({args}) -> {result}'

def clock(fmt=DEFAULT_FMT):
    def decorate(func):
        def clocked(*_args):
            t0 = time.time()
            _result = func(*_args)
            elapsed = time.time() - t0
            name = func.__name__
            args = ', '.join(repr(arg) for arg in _args)
            result = repr(_result)
            print(fmt.format(**locals()))
            return _result
        return clocked
    return decorate

def rate_limit(act,retry_count=15,wait=3):
    def decorate(func):
        def rate_limited(*_args):
            freqlimit = FreqLimit()
            _result = freqlimit.rate_limit(act)
            if _result is not True:
                _ret_code, _ret_data = func(*_args)
                return _ret_code, _ret_data
            else:
                for retry in range(1,retry_count,1):
                    time.sleep(wait)
                    print("retry *******{}".format(retry))
                    _result = freqlimit.rate_limit(act)
                    if _result is not True:
                        _ret_code, _ret_data = func(*_args)
                        return _ret_code, _ret_data
                print('rate limited')
                 #result = repr(_ret_code,_ret_data)
                return _result, None
        return rate_limited
    return decorate


def retry(retry_count=5,wait=30):
    def decorate(func):
        def retrying(*_args):
            _ret_code, _ret_data = func(*_args)
            if _ret_code == -1:
                for retry in range(1,retry_count,1):
                    time.sleep(wait)
                    print("retry *******{}".format(retry))
                    _ret_code, _ret_data = func(*_args)
                    if _ret_code == -1:
                        _ret_code, _ret_data = func(*_args)
                    else:
                        return _ret_code, _ret_data
                print('reached maximized retry count')
                return -1,''
            else:
                return _ret_code,_ret_data
        return retrying
    return decorate




def table(table):
    def decorate(kclass):
        old_table


@retry()
def test_retry():
    return -1,''

from hsstock.common.constant import *


if __name__ == '__main__':

    @clock()
    def snooze(seconds):
        time.sleep(seconds)
        return seconds

    for i in range(3):
        snooze(.123)


    test_retry()


