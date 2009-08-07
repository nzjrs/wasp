def linspace(xmin, xmax, N):
    """
    Return a list of N linearly spaced floats in
    the range [xmin,xmax], i.e. including the endpoints
    """
    if N==1: return [xmax]
    dx = (xmax-xmin)/(N-1)
    return [xmin] + [xmin + (dx*float(i)) for i in range(1,N)]
