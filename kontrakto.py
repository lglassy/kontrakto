"""simple implementation of 'design-by-contract' contracts"""

# This module defines 3 decorators: @pre, @post, and @post_arg.
# For example uses of these decorators, see the self_test function 
# in this module.
#
# @pre(fn, msg) runs before the decorated function, and 
# raises an exception if fn fails (returns False) when run 
# on the decorated function's arguments.
# 
# @post(fn, msg) runs after the decorated function, and 
# raises an exception if fn fails (returns False) when run 
# on the decorated function's return values.
#
# @post_arg(fn, msg) runs after the decorated function, and 
# raises an exception if fn fails (returns False) when run 
# on the decorated function's arguments.  @post_arg is used 
# when you want to test a postcondition on a function whose 
# main effect is to modify its arguments.

# standard modules

import functools
import os
import sys

# module-level constants 

__copyright__ = "Copyright (C) 2017 Lou Glassy"
__license__ = "Apache 2.0"
__version__ = "0.1"

# user should set CONTRACTS_ENABLED to True in client code
# when using this module.

CONTRACTS_ENABLED = False

# - - - 

class Contract_Error(Exception):
    def __init__(self, ctype, message):
        self.message = '{}: {}'.format(ctype, message)
    def __str__(self):
        return self.message

# - - - 

def pre(pre_fn, failure_message):
    if CONTRACTS_ENABLED:
        def contract_decorator(wrapped_fn):
            @functools.wraps(wrapped_fn)
            def fn_wrapper(*args, **kwargs):
                if pre_fn(*args, **kwargs): # precondition ok
                    return wrapped_fn(*args, **kwargs)
                else:
                    raise Contract_Error('@pre', failure_message)
            return fn_wrapper
        return contract_decorator
    else:
        def passthrough(wrapped_fn):
            return wrapped_fn
        return passthrough

# - - - 

def post(post_fn, failure_message):
    if CONTRACTS_ENABLED:
        def contract_decorator(wrapped_fn):
            @functools.wraps(wrapped_fn)
            def fn_wrapper(*args, **kwargs):
                results = wrapped_fn(*args, **kwargs)
                if post_fn(results): # postcondition ok
                    return results
                else:
                    raise Contract_Error('@post', failure_message)
            return fn_wrapper
        return contract_decorator
    else:
        def passthrough(wrapped_fn):
            return wrapped_fn
        return passthrough

# - - - 

def post_arg(post_fn, failure_message):
    if CONTRACTS_ENABLED:
        def contract_decorator(wrapped_fn):
            @functools.wraps(wrapped_fn)
            def fn_wrapper(*args, **kwargs):
                results = wrapped_fn(*args, **kwargs)
                if post_fn(*args, **kwargs): # postcondition ok
                    return results
                else:
                    raise Contract_Error('@post_arg', failure_message)
            return fn_wrapper
        return contract_decorator
    else:
        def passthrough(wrapped_fn):
            return wrapped_fn
        return passthrough

# - - - 

def self_test(test):

    global CONTRACTS_ENABLED 
    if 'CONTRACTS_ENABLED' in os.environ:
        CONTRACTS_ENABLED = True 

    if test == 'pre':
        @pre(lambda a, b: a > 0 and b > 0, 'a and b must be positive')
        def target(a, b):
            return a+b

        print('target(1,2)  ', target(1,2))
        print('target(-10,2)', target(-10, 2))

    if test == 'post':
        @post(lambda v: v>0, 'sum must be positive')
        def target(a, b):
            return a+b

        print('target(1,2)  ', target(1,2))
        print('target(-10,2)', target(-10, 2))

    if test == 'post_arg':
        @post_arg(lambda L: len(L) % 2 == 0, 'list len after call must be even')
        def target(L):
            if len(L) > 3 and len(L) % 2 == 1:
                L.append(0)

        L = [ 1,2,3,4 ]
        print('test 1: L: {}'.format(L))
        target(L)
        print('len L', len(L))
        print('')
        L = [ 1,2,3,4,5 ]
        print('test 2: L: {}'.format(L))
        target(L)
        print('len L', len(L))
        print('')
        L = [ 1 ]
        print('test 3: L: {}'.format(L))
        target(L)
        print('len L', len(L))
        print('')

    if test == 'multi':
        # test multiple stacked decorators on one target function.
        @pre(lambda a, _: a > 0, 'a must be positive')
        @pre(lambda _, b: b > 0, 'b must be positive')
        def target(a, b):
            return a+b

        print('target(1,2)  ', target(1,2))
        print('target(-10,2)', target(-10, 2))
# - - - 

if __name__ == '__main__':

    if len(sys.argv) == 1:
        m = """
usage: {} TEST, where TEST is one of:
pre		- testing @pre
post		- testing @post
post_arg 	- testing @post_arg
multi		- testing multiple 'stacked' decorators
""".format(sys.argv[0])
        print(m)
        sys.exit(1)

    # run one of the simple self tests.

    self_test(sys.argv[1])

# end of file
