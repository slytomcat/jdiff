#!/usr/bin/python3
""" Finds and print out the difference between two json files
ignoring the order of items in arrays and objects
"""
import argparse
import json


def print_(to_print):
    """ print string without new line """
    print(to_print, end="")


KEEP_ARRAYS_ORDER: bool
S4 = "    "


def multi_line(item):
    """ returns True when item should be printed on several lines"""
    return isinstance(item, (list, dict)) and len(item) > 0


def multi_lines(item_a, item_b):
    """ returns True when items diff should be printed on several lines"""
    return (
        multi_line(item_a) or
        multi_line(item_b)) and type(item_a) is type(item_b)


def print_item(prefix, item):
    """ Prints the whole item with specified prefix """
    if isinstance(item, (list, dict)):
        for row in json.dumps(item, sort_keys=True, indent=4).split('\n'):
            print_(F"{prefix}{row}")
    else:
        print_(json.dumps(item))


def print_item_prefixed(prefix, item):
    """ Prints prefix and then the whole item with specified prefix """
    print_(prefix)
    print_item(prefix, item)


def print_comma(yes):
    """ Prints comma if yes = True and always return True"""
    if yes:
        print_(",")
    return True


def item_hash(obj):
    """ Returns hash string for list, dict, str, bool, int, float and None """
    obj_type = type(obj).__name__[0]
    if obj_type == "d":  # dict
        return "d"+(
            "".join([F"{k}{item_hash(obj[k])}" for k in sorted(obj.keys())]))
    if obj_type == "l":  # list
        return "l"+("".join(sorted([item_hash(i) for i in obj])))
    if obj_type == "N":  # None type - nill in json
        return "N"
    if obj_type == "b":  # bool
        return "bT" if obj else "bF"
    # str, int or float)
    return obj_type+str(obj)


def print_diff(prefix, item_a, item_b, keep_arr_order):
    """ Finds and prints differences between two json items"""
    prefix = prefix+S4
    type_a = type(item_a)
    if type_a is not type(item_b):
        print_item(F"\n- {prefix}", item_a)
        print_item(F"\n+ {prefix}", item_b)
    elif type_a is dict:
        print_obj_diff(prefix, item_a, item_b, keep_arr_order)
    elif type_a is list:
        print_arr_diff(prefix, item_a, item_b, keep_arr_order)
    elif item_a == item_b:   # both items are not list or dict
        print_(json.dumps(item_a))
    else:
        print_(F'\n- {prefix}{json.dumps(item_a)},')
        print_(F'\n+ {prefix}{json.dumps(item_b)}')


def print_obj_diff(prefix, item_a, item_b, keep_arr_order):
    """ print diff between two objects """
    print_("{")
    if len(item_a) + len(item_b) == 0:
        print_("}")
        return
    minus = item_a.keys() - item_b.keys()
    equal = set(item_a.keys()).intersection(item_b.keys())
    comma = False
    for k in sorted(set(item_a.keys()).union(item_b.keys())):
        comma = print_comma(comma)
        sign = ' ' if k in equal else ("-" if k in minus else "+")
        pre = F'\n{sign} {prefix+S4}'
        print_(F'{pre}"{k}": ')
        if sign == ' ':
            if multi_lines(item_a[k], item_b[k]):
                print_(pre+S4)
            print_diff(prefix+S4, item_a[k], item_b[k], keep_arr_order)
        else:
            print_item(pre+S4, item_a[k] if sign == '-' else item_b[k])
    print_(F"\n  {prefix}" + "}")


def print_arr_items(prefix, items):
    """ print array items """
    for item in items:
        print_item(prefix, item)


def print_arr_item_diff(prefix, item_a, item_b):
    """ print diff between two array items """
    if item_hash(item_a) == item_hash(item_b):
        print_item_prefixed(F'\n  {prefix}', item_a)
    else:
        print_item_prefixed(F'\n- {prefix}', item_a)
        print_item_prefixed(F'\n+ {prefix}', item_b)


def print_arr_diff(prefix, item_a, item_b, keep_arr_order):
    """ print diff between two arrays """
    print_("[")
    if len(item_a) + len(item_b) == 0:
        print_("]")
        return
    if keep_arr_order:
        print_arr_diff_ordered(prefix+S4, item_a, item_b)
    else:
        print_arr_diff_unordered(prefix+S4, item_a, item_b)
    print_(F"\n  {prefix}" + "]")


def print_arr_diff_ordered(prefix, item_a, item_b):
    """ print diff between arrays items keeping the arrays order """
    if len(item_a) == len(item_b):
        for i, a_ith in enumerate(item_a):
            print_arr_item_diff(prefix, a_ith, item_b[i])
    else:
        if len(item_a) > len(item_b):
            bigger = item_a
            smaller = item_b
            rest = "+"
        else:
            bigger = item_b
            smaller = item_a
            rest = "-"
        for i in range(len(smaller)):
            print_arr_item_diff(prefix, item_a[i], item_b[i])
        for i in range(len(smaller), len(bigger)):
            print_item(F'{rest} {prefix}', item_a)


def print_arr_diff_unordered(prefix, item_a, item_b):
    """ print diff between arrays items ignoring the arrays order """
    hashed = {item_hash(i): i for i in item_a}
    hashed_b = {item_hash(i): i for i in item_b}
    a_set = set(hashed.keys())
    common_set = a_set.intersection(hashed_b.keys())
    hashed.update(hashed_b)
    del hashed_b
    comma = False
    for val in sorted(hashed.keys()):
        comma = print_comma(comma)
        sign = " " if val in common_set else ("-" if val in a_set else "+")
        pre = F'\n{sign} {prefix}'
        print_(pre)
        print_item(pre, hashed[val])


def init():
    """ Initialize parameters"""
    parser = argparse.ArgumentParser()
    parser.add_argument("in_file", type=str, help="first file")
    parser.add_argument("out_file", type=str, help="second file")
    parser.add_argument("--keep_arrays_order", "-o",
                        default=False, action="store_true",
                        help="Don't ignore arrays order",)
    args = parser.parse_args()
    return args.in_file, args.out_file, args.keep_arrays_order


def main():
    """ main routine """
    file_a, file_b, keep_arr_order = init()
    with open(file_a) as file_r:
        json_a = json.load(file_r)
    with open(file_b) as file_r:
        json_b = json.load(file_r)
    print_("  " if type(json_a) is type(json_b) else "")
    print_diff("", json_a, json_b, keep_arr_order)
    print_("\n")


if __name__ == "__main__":
    main()
