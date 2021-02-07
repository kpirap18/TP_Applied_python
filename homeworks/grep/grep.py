import argparse
import sys
import re
from collections import deque


def output(line):
    print(line)


def output_line(line, line_number=False, match=True):
    """
    Adds to line proper leading symbols if needed
    Keyword arguments:
        line(str):        line to output
        line_number(int): should be line numbered
        match(bool):      if current line satisfy pattern (":" or "-" will be added)
    Returns:
    """
    if line_number and match:
        output(str(line_number) + ':' + line)
    elif line_number:
        output(str(line_number) + '-' + line)
    else:
        output(line)


def count(lines, regularexp, invert=False):
    """
    Count lines matches regularexp.
    Args:
        lines(iterable):      lines to process
        regularexp(SRE_Pattern):  regularexp to check
        invert(bool):         invert regularexp match
    Returns:
        Number of lines matching regularexp
    """
    counter = 0
    for line in lines:
        line = line.rstrip()
        if bool(regularexp.search(line)) != invert:
            counter += 1
    return counter


def out_match(lines, regularexp, invert=False, line_number=False):
    """
    Outputs lines matching regularexp
    Args:
        lines(iterable):     lines to process
        regularexp(SRE_Pattern): regularexp to check
        invert(bool):        invert regularexp match
        line_number(bool):   number lines
    Returns:
    """
    idx = 0
    for line in lines:
        idx += 1
        line = line.rstrip()
        if bool(regularexp.search(line)) != invert:
            output_line(line, idx if line_number else False)


def out_match_context(lines, regularexp, before, after,
                      invert=False, line_number=False):
    """
    Outputs lines matching regularexp with context __after__ and __before__
    Args:
        lines(iterable):    lines to process
        regularexp(SRE_Pattern):regularexp to check
        before(int):        context before
        after(int):         context after
        invert(int):        invert regularexp match
        line_number(bool):  number lines
    Returns:
    """
    idx = 0
    deq = deque(maxlen=before)
    to_print_after = 0
    for line in lines:
        line = line.rstrip()
        idx += 1

        if bool(regularexp.search(line)) != invert:
            to_print_after = after
            while deq:
                linet = deq.popleft()
                output_line(linet[0], linet[1] if line_number else False, False)
            output_line(line, idx if line_number else False)
        elif to_print_after:
            output_line(line, idx if line_number else False, False)
            to_print_after -= 1
        else:
            deq.append((line, idx))


def grep(lines, params):
    regularexp = params.pattern.replace('?', '.').replace('*', '.*')
    regularexp = re.compile(regularexp, re.I if params.ignore_case else 0)
    if params.count:
        result = count(lines, regularexp, params.invert)
        output(str(result))

    elif params.context or params.after_context or params.before_context:
        before = max(params.context, params.before_context)
        after = max(params.context, params.after_context)
        out_match_context(lines, regularexp, before, after,
                          params.invert, params.line_number)

    else:
        out_match(lines, regularexp, params.invert, params.line_number)


def parse_args(args):
    parser = argparse.ArgumentParser(description='This is a simple grep on python')
    parser.add_argument(
        '-v',
        action="store_true",
        dest="invert",
        default=False,
        help='Selected lines are those not matching pattern.')
    parser.add_argument(
        '-i',
        action="store_true",
        dest="ignore_case",
        default=False,
        help='Perform case insensitive matching.')
    parser.add_argument(
        '-c',
        action="store_true",
        dest="count",
        default=False,
        help='Only a count of selected lines is written to standard output.')
    parser.add_argument(
        '-n',
        action="store_true",
        dest="line_number",
        default=False,
        help='Each output line is preceded by its relative line number in the file, starting at line 1.')
    parser.add_argument(
        '-C',
        action="store",
        dest="context",
        type=int,
        default=0,
        help='Print num lines of leading and trailing context surrounding each match.')
    parser.add_argument(
        '-B',
        action="store",
        dest="before_context",
        type=int,
        default=0,
        help='Print num lines of trailing context after each match')
    parser.add_argument(
        '-A',
        action="store",
        dest="after_context",
        type=int,
        default=0,
        help='Print num lines of leading context before each match.')
    parser.add_argument('pattern', action="store", help='Search pattern. Can contain magic symbols: ?*')
    return parser.parse_args(args)


def main():
    params = parse_args(sys.argv[1:])
    grep(sys.stdin, params)


if __name__ == '__main__':
    main()