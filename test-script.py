import inspect

def test_function():
    print("These are the locals:", inspect.currentframe().f_back.f_locals.copy())
    print("These are the globals:", inspect.currentframe().f_back.f_globals.copy())
    print('test_function() was called')


def fx():
    a = 2
    test_function()
    print("fx() was called")

def main():
    a = 1
    fx()


main()


