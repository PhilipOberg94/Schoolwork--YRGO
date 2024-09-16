import time

def ctime(simplified=True, printable=True):
    def decorator(f):
        sec = None
        def timeit():
            st_time = time.time()
            f()
            end_time = time.time()
            sec = end_time - st_time
            if printable == True:
                if simplified == True:
                    print(f'Function \"{f.__name__}\" took {sec:.2f} seconds.')
                else:
                    print(f'Function \"{f.__name__}\" took {sec} seconds.')
            return sec
        return timeit
    return decorator

if __name__ == '__main__':
    raise Exception('You need to import the library, not run the module.')