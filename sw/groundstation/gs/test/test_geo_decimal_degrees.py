import doctest

import gs.geo.decimaldegrees as decimaldegrees

# Run doctest
def _test():
    return doctest.testmod(decimaldegrees)

if __name__ == "__main__":
    _test()
