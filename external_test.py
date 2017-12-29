# this file is a simple example of how you would use 
# kontrakto from normal client code.

import kontrakto 

from kontrakto import pre, post, post_arg 

# note - the pre, post, post_arg decorators are enabled by setting
# kontrakto.CONTRACTS_ENABLED to True.  By default CONTRACTS_ENABLED
# is False (which makes the decorators no-ops).
#
# Setting CONTRACTS_ENABLED to True enables these decorators
# for subsequent function definitions in the current module.

kontrakto.CONTRACTS_ENABLED = True 

def run_tests():

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

# - - - 

if __name__ == '__main__':
    run_tests()

# end of file
