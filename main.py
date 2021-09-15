import sys
import re

config = {
    'path_separator': '/',
    'pattern_separator': ',',
    'wildcard': '*'
}


def main():
    """ File Main Function"""

    if(sys.stdin.isatty()):
        print("No hay ningún archivo (input) especificado! (ᵔᴥᵔ)")
        return

    is_first_line = True
    n, m = 0, 0
    patterns = []

    for line in sys.stdin:
        is_numeric = line.strip().isnumeric()

        if(is_first_line):
            n = int(line.strip())
            is_first_line = False
        elif(is_numeric):
            m = int(line.strip())

        if((n > 0) and not (is_numeric)):
            patterns.append(line.strip())
            n -= 1

        if((m > 0) and not (is_numeric)):
            path = line.strip()
            path = path.strip(config['path_separator'])
            path = path.split(config['path_separator'])
            best_matching_pattern = find_pattern(path, patterns)
            print(best_matching_pattern)
            m -= 1


def find_pattern(path, patterns):
    """
    Find the best pattern from a list that matches the path.
    param path: list - path from which will be found the best pattern
    param patterns: list - list of patterns that can match (or not) the path
    return: string - The best matching pattern otherwise 'NO MATCH' if no one was found
    """
    regular_expression = get_regular_expression(path)
    results = get_patterns_that_match(regular_expression, patterns)
    if(len(results) > 1):
        best_matching_pattern = check_best_matching_pattern(results)
    elif(len(results) == 1):
        best_matching_pattern = results[0]
    else:
        best_matching_pattern = 'NO MATCH'

    return best_matching_pattern


def get_regular_expression(path):
    """
    Get the regular expression (RE) from a path
    param path: list - path from which will be found the RE
    return: string - The RE from the path
    """
    regular_expression = ""
    for item in path:
        if(item == path[-1]):
            regular_expression += "("+item+"$|[*]$)"
        else:
            regular_expression += "("+item+"|[*])"

    return regular_expression


def get_patterns_that_match(regular_expression, patterns):
    """
    Get the patterns that match a regular expression (RE)
    param regular_expression: string - RE from a path
    param patterns: list - list of patterns that can match (or not) the RE
    return: list - The list of patterns that match the RE
    """
    results = []
    for pattern in patterns:
        pattern_clean = pattern.replace(config['pattern_separator'], '')
        match = re.match(regular_expression, pattern_clean)

        if(bool(match)):
            results.append(pattern)

    return results


def check_best_matching_pattern(results):
    """
    Check the best matching pattern from a list of pattern results
    param results: list - Patterns list from which will be found the best pattern
    return: string - The best matching pattern
    """
    filtered = []
    lesser = float('inf')

    for item in results:
        current = item.count(config['wildcard'])
        if(current < lesser):
            lesser = current
            filtered = []

        if(current == lesser):
            filtered.append(item)

    if(len(filtered) > 1):
        best_matching_pattern = check_tie(filtered)
    else:
        best_matching_pattern = filtered[0]

    return best_matching_pattern


def check_tie(results):
    """
    Check the best pattern if a tie exists
    param results: list - Patterns list from which will be found the best pattern
    return: string - The best matching pattern
    """
    best_pattern = ''
    greater_rate = 0
    for item in results:
        rate = 0
        for index, value in enumerate(item.split(config['pattern_separator'])):
            if(value == config['wildcard']):
                rate += index

        if(rate > greater_rate):
            greater_rate = rate
            best_pattern = item

    return best_pattern


if __name__ == '__main__':
    main()
