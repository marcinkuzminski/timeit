import inspect
import linecache
import time
import functools
import pprint

def reset_timeit():
    config = globals()
    if 'timeit_GLOBAL_KEY' in config:
        config['timeit_GLOBAL_KEY'] = None


def init_timeit():
    """
    Initialization function
    """

    config = globals()
    # reset if any globals() are present
    reset_timeit()
    GLOBAL_KEY = config['timeit_GLOBAL_KEY'] = 'timeit__GLOBAL__'
    config['timeit__FUNC'] = []
    config[GLOBAL_KEY] = {}
    config[GLOBAL_KEY]['timeit__stats'] = {
        'total': 0,
        'first_line': None,
        'last_line': 0
    }
    config[GLOBAL_KEY]['timeit__start'] = time.time()
    config[GLOBAL_KEY]['timeit__start_int'] = 0


def timeit_stamp(frame=None, show_stats=False):
    """
    Usage::

         timeit_stamp(inspect.currentframe())

    :param frame:
    :param show_stats:
    """
    config = globals()
    GLOBAL_KEY = config['timeit_GLOBAL_KEY']

    t = time.time() - config[GLOBAL_KEY]['timeit__start']
    stats = config[GLOBAL_KEY]['timeit__stats']
    callable_ = linecache.getline(__file__, inspect.getlineno(frame))
    lineno = inspect.getlineno(frame)

    print '\t *** tracepoint at line: %s %.3f|%s' % (lineno, t,
                                                     callable_.strip())

    if (stats['total'] < t):
        stats['total'] = t
        stats['last_line'] = lineno
    if stats['first_line'] is None:
        stats['first_line'] = lineno

    config[GLOBAL_KEY]['timeit__start_int'] = time.time()
    if show_stats:
        print stats


#==============================================================================
# decorator
#==============================================================================
def timeit(key=None):
    def decorator(method):
        argspec = inspect.getargspec(method)
        config = globals()
        GLOBAL_KEY = config['timeit_GLOBAL_KEY']

        @functools.wraps(method)
        def wrapper(*args, **kwargs):
            func_spec = {
                'id': id(method),
                'method': method,
                'argspec': argspec,
            }
            config['timeit__FUNC_CURRENT'] = func_spec['id']
            print '\t *** Measuring function %s' % str(method)
            ts = time.time()
            result = method(*args, **kwargs)
            te = time.time()
            func_total = te - ts
            func_spec['execution_time'] = func_total
            config['timeit__FUNC'].append(func_spec)
            print ('\t *** method: "%r" total: %2.2f sec args:(%r, %r)  \n') % (
               method.__name__, func_total, args, kwargs,
            )
            print pprint.pformat(config[GLOBAL_KEY]['timeit__stats'])
            print pprint.pformat(config['timeit__FUNC'])
            return result
        return wrapper
    return decorator


if __name__ == '__main__':
    init_timeit()

    print 'aloha !'

    @timeit()
    def func():
        print 'a'
        timeit_stamp(inspect.currentframe())
        time.sleep(1)
        timeit_stamp(inspect.currentframe())
        time.sleep(2)
        timeit_stamp(inspect.currentframe())
        print 'b'

    @timeit()
    def func2():
        print 'a'
        timeit_stamp(inspect.currentframe())
        time.sleep(3)
        timeit_stamp(inspect.currentframe())
        time.sleep(4)
        timeit_stamp(inspect.currentframe())
        print 'b'

    func()
    func2()
