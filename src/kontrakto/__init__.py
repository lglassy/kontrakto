"""simple implementation of 'design-by-contract' contracts"""

# This module defines 3 decorators: @pre, @post, and @post_arg.
# For example uses of these decorators, see the code in 
# kontrakto.self_test module.  You can run the self test with 
# the command:
#
#     python3 -m kontrakto.self_test 
#
# @pre(fn, msg) runs fn before the decorated function, and 
# raises an exception if fn fails (returns False) when run 
# on the decorated function's arguments.
# 
# @post(fn, msg) runs fn after the decorated function, and 
# raises an exception if fn fails (returns False) when run 
# on the decorated function's return values.
#
# @post_arg(fn, msg) runs fn after the decorated function, and 
# raises an exception if fn fails (returns False) when run 
# on the decorated function's arguments.  Use @post_arg
# instead of @post if you have a function that modifies its 
# arguments.

# standard modules

import functools
import os
import sys

# module-level constants 

__copyright__ = "Copyright (C) 2017 Lou Glassy"
__license__   = "Apache 2.0"
__version__   = "0.1"

# set CONTRACTS_ENABLED to True in client code to use this module.

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

# end of file
