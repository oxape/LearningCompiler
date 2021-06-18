import argparse
import prettytable as pt
import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from syntax_analysis.firstfollow import parse_file
from syntax_analysis.firstfollow import first_and_follow
from syntax_analysis.firstfollow import ListAndSet
from syntax_analysis.firstfollow import epsilon


def get_las_from_dict(d, key):
    las = d.get(key, None)
    if las is None:
        las = ListAndSet()
        d[key] = las
    return las


def build_predictive_map(file_path):
    rules = parse_file(file)
    first_dict, follow_dict, nonterminals, terminals = first_and_follow(rules)
    predictive_map = {}
    print('############ build_predictive_map ############')
    for s, l in rules:
        s_map = predictive_map.get(s, None)
        if s_map is None:
            s_map = {}
            predictive_map[s] = s_map
        production = f'{s} -> {" ".join(l)}'
        # print(f'{s} -> {" ".join(l)}')
        end = 0
        for index, e in enumerate(l):
            for se in first_dict[e].list:
                if se == epsilon:
                    continue
                las = get_las_from_dict(s_map, se)
                las.list.append(production)
                las.set.add(production)
            if epsilon not in first_dict[e].set:
                break
            end = index+1
        if end == len(l):
            for se in follow_dict[s].list:
                las = get_las_from_dict(s_map, se)
                las.list.append(production)
                las.set.add(production)
    field_names = [' ']
    field_names.extend(["id", "+", "*", "(", ")", "$"])
    tb = pt.PrettyTable(field_names)
    for nt in ['E', "E'", "T", "T'", "F"]:
        columns = [nt]
        s_map = predictive_map.get(nt, None)
        for t in ["id", "+", "*", "(", ")", "$"]:
            las = s_map.get(t, None)
            if las is None:
                columns.append(' ')
            else:
                columns.append("\n".join(las.list))
        tb.add_row(columns)
    print(tb)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='calculating first, follow and predict sets for the grammar.')
    parser.add_argument('file', type=str, nargs='+', help='input file')

    args = parser.parse_args()
    print(args.file)
    for file in args.file:
        build_predictive_map(file)
