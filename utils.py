def find_first_diff(a, b):
    """
    Find index where b first differs from a. If b is a substring
    of a, there is no practical difference, just return the  length of a.
    """

    i = 0
    n = len(a)
    m = len(b)
    while i < n and i < m:

        if a[i] != b[i]:
            return i
        i += 1
    
    # By default, the first diff is just after the end of a
    return n