"""
Edit Distance -> int
    number of transformations to actions cost to convert string1 to string2
    actions: * insertion -> 1
             * deletion -> 1
             * substitution -> 1
"""
def memo(func):
    memo = {}
    def inner(*args, **kargs):
        if args in memo:
            return memo[args]
        memo[args] = func(*args)
        print(memo)
        return memo[args]
    return inner

@memo
def edit_distance(string1, string2):
    """
    :param string1: string,
    :param string2: string,
    :return:
    """
    if len(string1) == 0 and len(string2) == 0:
        return 0
    if len(string1) == 0 or len(string2) == 0:
        return abs(len(string1) - len(string2))

    c1, c2 = string1[-1], string2[-1]

    if c1 == c2:
        return edit_distance(string1[:-1], string2[:-1]) + 0
    else:
        return min(
            edit_distance(string1, string2[:-1]) + 1,   # insert 1 char to str1
            edit_distance(string1[:-1], string2) + 1,   # delete 1 char from str1
            edit_distance(string1[:-1], string2[:-1]) + 2   # substitute 1 char in str1 (assume 2 actions for sub)
        )