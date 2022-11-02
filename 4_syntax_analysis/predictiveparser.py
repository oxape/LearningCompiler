import argparse
import sys
import os
from tabulate import tabulate
import logging

# 编译原理  4.4.3 生成LL(1)文法对应的预测分析表

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from firstfollow import parse_file
from firstfollow import first_and_follow
from firstfollow import ListAndSet
from firstfollow import epsilon


logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


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
    for s, l in rules:
        logging.info(f'{s} -> {" ".join(l)}')
    logging.info('############ build_predictive_map ############')
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
                logging.info("FIRST  [{0} {1}] = {2}".format(s, se, production))
            if epsilon not in first_dict[e].set:
                break
            end = index+1
        if end == len(l):
            for se in follow_dict[s].list:
                las = get_las_from_dict(s_map, se)
                las.list.append(production)
                las.set.add(production)
                logging.info("FOLLOW [{0} {1}] = {2}".format(s, se, production))
    field_names = [' ']
    header = []
    terminals.remove(epsilon)
    header.extend(terminals)
    header.append("$")
    field_names.extend(header)
    table = [field_names]
    for nt in nonterminals:
        columns = [nt]
        s_map = predictive_map.get(nt, None)
        for t in header:
            las = s_map.get(t, None)
            if las is None:
                columns.append(' ')
            else:
                columns.append("\n".join(las.list))
        table.append(columns)
    logging.info(tabulate(table, headers='firstrow', tablefmt='grid'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='calculating first, follow and predict sets for the grammar.')
    parser.add_argument('file', type=str, nargs='+', help='input file')

    args = parser.parse_args()
    logging.info(args.file)
    for file in args.file:
        build_predictive_map(file)
