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

def rate_limit(act):
    def decorate(func):
        def rate_limited(*_args):
            freqlimit = FreqLimit()
            _result = freqlimit.rate_limit(act)
            if _result is not True:
                _ret_code, _ret_data = func(*_args)
            else:
                print('rate limited')
            #result = repr(_ret_code,_ret_data)
            return _ret_code,_ret_data
        return rate_limited
    return decorate

if __name__ == '__main__':

    @clock()
    def snooze(seconds):
        time.sleep(seconds)
        return seconds

    for i in range(3):
        snooze(.123)

