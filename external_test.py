# this file contains simple examples of how you would use the kontrakto
# module with normal client code.

import kontrakto 

from kontrakto import pre, post, post_arg 

# note - the pre, post, post_arg decorators are enabled by setting
# kontrakto.CONTRACTS_ENABLED to True.  By default CONTRACTS_ENABLED
# is False (which makes the decorators no-ops).
#
# Setting CONTRACTS_ENABLED to True enables these decorators
# for subsequent function definitions in the current module.

kontrakto.CONTRACTS_ENABLED = True 

def run_tests_on_decorated_functions():

    @pre(lambda a, b: a > 0 and b > 0, 'a and b must be positive')
    def target(a, b):
        return a+b

    print('pre, input', (1,2))
    x = target(1,2)
    print('pre, expect 3, got', x)
    print('-')

    try:
        print('pre, input', (-11,2))
        x = target(-11,2)
    except kontrakto.Contract_Error as e:
        print('pre, expect exception:', e)
        print('-')

    @post(lambda v: v>0, 'sum must be positive')
    def target2(a, b):
        return a+b

    print('post, input', (1,2))
    x = target2(1, 2)
    print('post, expect 3, got', x)
    print('-')

    try:
        print('post, input', (-11,2))
        x = target(-11,2)
    except kontrakto.Contract_Error as e:
        print('post, expect exception:', e)
        print('-')

    @post_arg(lambda L: len(L) % 2 == 0, 'list len after call must be even')
    def target3(L):
        if len(L) > 3 and len(L) % 2 == 1:
            L.append(0)

    L = [ 1,2,3,4 ]
    print('post_arg, input L: {}'.format(L))
    target3(L)
    print('post_arg, expect even len, L {} len {}'.format(L,len(L)))
    print('-')

    L = [ 1,2,3,4,5 ]
    print('post_arg, input L: {}'.format(L))
    target3(L)
    print('post_arg, expect even len, L {} len {}'.format(L,len(L)))
    print('-')

    try:
        L = [ 1 ]
        print('post_arg, input L: {}'.format(L))
        target3(L)
        print('post_arg, expect even len, L {} len {}'.format(L,len(L)))
        print('')
    except kontrakto.Contract_Error as e:
        print('post_arg, expect exception:', e)
        print('-')

    # test multiple stacked decorators on one target function.
    @pre(lambda a, _: a > 0, 'a must be positive')
    @pre(lambda _, b: b > 0, 'b must be positive')
    def target4(a, b):
        return a+b

    print('multi, input', (1,2))
    x = target(1,2)
    print('multi, expect 3, got', x)
    print('-')

    try:
        print('multi, input', (-10,2))
        x = target(-10,2)
    except kontrakto.Contract_Error as e:
        print('multi, expect exception:', e)
        print('-')

class Counter(object):
    # note that when we decorate a method, we must include 
    # the class instance itself as an arg to the contract function.

    def __init__(self, val):
        self.val = val 

    @pre(lambda self: self.val > 0, 'counter val must before inc must be greater than zero')
    def inc(self):
        self.val += 1

    @pre(lambda self, ival: (self.val + ival) % 2 == 0,
          'new val after incby must be even')
    def incby(self, ival):
        self.val += ival
    
def run_tests_on_decorated_methods():
    C = Counter(1)
    print('counter C val before inc', C.val)
    C.inc()
    print('counter C val after inc ', C.val)
    print()

    try:
        C2 = Counter(0)
        print('counter C2 val before inc', C2.val)
        C2.inc()
        print('counter C2 val after inc ', C2.val)
    except kontrakto.Contract_Error as e:
        print('expect exception:', e)
    print()

    C3 = Counter(1)
    print('counter C3 val', C3.val)
    C3.inc()
    print('counter C3 val after inc', C3.val)
    C3.incby(2)
    print('counter C3 val after incby', C3.val)
    try:
        C3.incby(3)
        print('counter C3 val after 2nd incby', C3.val)
    except kontrakto.Contract_Error as e:
        print('expect exception:', e)
    print()

# - - - 

if __name__ == '__main__':
    run_tests_on_decorated_functions()
    run_tests_on_decorated_methods()

# end of file
