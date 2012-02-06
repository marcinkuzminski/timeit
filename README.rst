Timeit is a simple set of functions for measuring execution time for python functions.

timeit can use tracepoints to measure each step time, and display summary at the end:

example::

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
        
        
gives such output::

    aloha !
         *** Measuring function <function func at 0x26625f0>
    a
         *** tracepoint at line: 106 0.000|timeit_stamp(inspect.currentframe())
         *** tracepoint at line: 108 1.001|timeit_stamp(inspect.currentframe())
         *** tracepoint at line: 110 3.003|timeit_stamp(inspect.currentframe())
    b
         *** method: "'func'" total: 3.00 sec args:((), {})  

    {'first_line': 106, 'last_line': 110, 'total': 3.0032649040222168}
    [{'argspec': ArgSpec(args=[], varargs=None, keywords=None, defaults=None),
      'execution_time': 3.0032460689544678,
      'id': 40248816,
      'method': <function func at 0x26625f0>}]
         *** Measuring function <function func2 at 0x26626e0>
    a
         *** tracepoint at line: 116 3.004|timeit_stamp(inspect.currentframe())
         *** tracepoint at line: 118 6.006|timeit_stamp(inspect.currentframe())
         *** tracepoint at line: 120 10.007|timeit_stamp(inspect.currentframe())
    b
         *** method: "'func2'" total: 7.00 sec args:((), {})  

    {'first_line': 106, 'last_line': 120, 'total': 10.00725793838501}
    [{'argspec': ArgSpec(args=[], varargs=None, keywords=None, defaults=None),
      'execution_time': 3.0032460689544678,
      'id': 40248816,
      'method': <function func at 0x26625f0>},
     {'argspec': ArgSpec(args=[], varargs=None, keywords=None, defaults=None),
      'execution_time': 7.003587007522583,
      'id': 40249056,
      'method': <function func2 at 0x26626e0>}]