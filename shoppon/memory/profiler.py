from memory_profiler import profile


@profile
def foo():
    return [i for i in range(1000000)]


foo()
