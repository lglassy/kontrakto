# this file is a simple example of how you would use 
# kontrakto from normal client code.

import kontrakto 

from kontrakto import pre, post, post_arg 

# note - to enable contracts you must set kontrakto.CONTRACTS_ENABLED
# to True, and you must do this before using @pre, @post, @post_arg
# decorators.  if you do set CONTRACTS_ENABLED to True, then these 
# decorators act as no-ops.  There is a likely still a small runtime 
# cost for such no-op decorators.

kontrakto.CONTRACTS_ENABLED = True 

def run_tests():

    @pre(lambda a, b: a > 0 and b > 0, 'a and b must be positive')
    def target(a, b):
        return a+b

    x = target(1,2)
    print('pre, expect 3, got', x)

    try:
        x = target(-11,2)
    except kontrakto.Contract_Error as e:
        print('pre, expect exception:', e)

    @post(lambda v: v>0, 'sum must be positive')
    def target2(a, b):
        return a+b

    x = target2(1, 2)
    print('post, expect 3, got', x)

    try:
        x = target(-11,2)
    except kontrakto.Contract_Error as e:
        print('post, expect exception:', e)


    @post_arg(lambda L: len(L) % 2 == 0, 'list len after call must be even')
    def target3(L):
        if len(L) > 3 and len(L) % 2 == 1:
            L.append(0)

    L = [ 1,2,3,4 ]
    print('post_arg, target3 test 1: L: {}'.format(L))
    target3(L)
    print('len L', len(L))
    print('')
    L = [ 1,2,3,4,5 ]
    print('post_arg, target3 test 2: L: {}'.format(L))
    target3(L)
    print('len L', len(L))
    print('')
    try:
        L = [ 1 ]
        print('post_arg, target3 test 3: L: {}'.format(L))
        target3(L)
        print('len L', len(L))
        print('')
    except kontrakto.Contract_Error as e:
        print('post_arg, expect exception:', e)

    # test multiple stacked decorators on one target function.
    @pre(lambda a, _: a > 0, 'a must be positive')
    @pre(lambda _, b: b > 0, 'b must be positive')
    def target4(a, b):
        return a+b

    print('multi, target4(1,2)  ', target(1,2))
    try:
        print('multi, target4(-10,2)', target(-10, 2))
    except kontrakto.Contract_Error as e:
        print('multi, expect exception:', e)

# - - - 

if __name__ == '__main__':
    run_tests()

# end of file
