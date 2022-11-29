"""
使用前需要建议先消除文法中的左递归，也许可以处理左递归，但也可能发生什么一些我也无法预测的事情
"""
import argparse
import logging

epsilon = '\u0190'
dollar = '\u0024'
start = ''


class ParseError(Exception):
    pass


class Parser:
    def __init__(self, buffer):
        self.buffer = buffer
        self.length = len(self.buffer)
        self.next = 0

    def production(self):
        if len(self.buffer) == 0:
            return None
        if self.buffer.startswith('#'):
            return None
        left = self.nonterminal()
        self.match_space()
        self.match('-')
        if self.next >= self.length:
            raise ParseError('syntax error')
        self.match('>')
        sysmbols = []
        productions = []
        self.match_space()
        while self.next < self.length:
            right = self.symbol()
            if right == '|':
                productions.append((left, sysmbols))
                sysmbols = []
            else:
                sysmbols.append(right)
            if self.next >= self.length:
                break
            self.match_space()
            if self.next >= self.length:
                break
            if self.buffer[self.next] == '.':
                break
        productions.append((left, sysmbols))
        return productions

    def nonterminal(self):
        start_index = self.next
        if not self.buffer[self.next].isalpha():
            raise ParseError('syntax error')
        self.next += 1
        while self.next < self.length:
            if self.buffer[self.next].isspace() or self.buffer[self.next] == '.':
                break
            else:
                self.next += 1
        return self.buffer[start_index:self.next]

    def symbol(self):
        start = self.next
        while self.next < self.length:
            if self.buffer[self.next].isspace() or self.buffer[self.next] == '.':
                break
            else:
                self.next += 1
        return self.buffer[start:self.next]

    def match(self, t):
        if self.buffer[self.next] == t:
            self.next += 1
        else:
            raise ParseError('syntax error')

    def match_space(self):
        while self.next < self.length:
            if self.buffer[self.next].isspace():
                self.next += 1
            else:
                break


class ListAndSet:
    def __init__(self):
        self.list = []
        self.set = set()


def first(s, rules, terminal_set, first_dict):
    las = first_dict.get(s, None)
    if las is not None:
        return
    las = ListAndSet()
    # 下面一句放在这里和上面的first_dict是否存在过放入一起可以处理左递归
    first_dict[s] = las
    if s in terminal_set:
        las.list.append(s)
        las.set.add(s)
        first_dict[s] = las
        return
    logging.debug(f'^^^^^^^^^^^^{s}^^^^^^^^^^^^')
    for t, l in rules:
        if t != s:
            continue
        logging.debug(f'    process {t} -> {" ".join(l)} -- for {s}')
        end = 0
        for index, e in enumerate(l):
            if e == epsilon:
                if len(l) == 1:
                    first(e, rules, terminal_set, first_dict)
                    for se in first_dict[e].list:
                        if se not in las.set:
                            logging.debug(f'1 add {se} to FIRST({s})')
                            las.list.append(se)
                            las.set.add(se)
            else:
                first(e, rules, terminal_set, first_dict)
                for se in first_dict[e].list:
                    if se == epsilon:
                        continue
                    if se not in las.set:
                        logging.debug(f'2 add {se} to FIRST({s})')
                        las.list.append(se)
                        las.set.add(se)
                if epsilon not in first_dict[e].set:
                    break
            end = index+1
        if end == len(l):
            if epsilon in first_dict[l[-1]].set:
                if epsilon not in las.set:
                    logging.info(f'3 add {epsilon} to FIRST({s})')
                    las.list.append(epsilon)
                    las.set.add(epsilon)
    logging.debug(f'------------{s}------------')


def follow(s, rules, terminal_set, first_dict, follow_dict, second=False):
    las = follow_dict.get(s, None)
    if not second:
        if las is not None:
            return
        las = ListAndSet()
        global start
        if s == start:
            las.list.append(dollar)
            las.set.add(dollar)
        follow_dict[s] = las
    else:
        if las is None:
            return
    logging.debug(f'^^^^^^^^^^^^{s}^^^^^^^^^^^^')
    for t, l in rules:
        logging.debug(f'    process {t} -> {" ".join(l)} -- for {s}')
        for index, e in enumerate(l):
            if e == s:
                if index+1 < len(l):
                    for se in first_dict[l[index+1]].list:
                        if se != epsilon and se not in las.set:
                            logging.debug(f'1 add {se} to FOLLOW({s})')
                            las.list.append(se)
                            las.set.add(se)
                end = index+1
                for i, se in enumerate(l[index+1:]):
                    if epsilon not in first_dict[se].set:
                        break
                    end = index+1+i+1
                """
                这里处理的情况是 A -> a B X1 X2 X3 ... Xn
                上述产生式的右侧 X1 ~ Xn的FIRST集合都包含Ɛ，FOLLOW(A)是FOLLOW(B)的子集
                """
                if end == len(l):
                    if t == s:
                        continue
                    if not second:
                        follow(t, rules, terminal_set, first_dict, follow_dict, second)
                    for se in follow_dict[t].list:
                        if se not in las.set:
                            logging.debug(f'2 add {se} to FOLLOW({s})')
                            las.list.append(se)
                            las.set.add(se)
    logging.debug(f'------------{s}------------')


def first_and_follow(rules):
    if len(rules) == 0:
        return
    nonterminal_set = set()
    nonterminals = []
    terminal_set = set()
    terminals = []
    first_dict = {}
    follow_dict = {}
    unprocessed_nonterminal_set = set()
    global start
    start = rules[0][0]
    for s, l in rules:
        if s not in nonterminal_set:
            nonterminal_set.add(s)
            nonterminals.append(s)
    for s, l in rules:
        for e in l:
            if e not in nonterminal_set and e not in terminal_set:
                terminal_set.add(e)
                terminals.append(e)
    unprocessed_nonterminal_set.update(nonterminals)
    for s, l in rules:
        logging.debug(f'{s} -> {" ".join(l)}')
    logging.debug(nonterminals)
    logging.debug(terminals)
    logging.debug(f'############first############')
    for s in nonterminals:
        first(s, rules, terminal_set, first_dict)
    for s in terminals:
        first(s, rules, terminal_set, first_dict)
    logging.debug(f'############follow############')
    logging.debug(f'start = {start}')
    logging.debug(f'############   1   ############')
    for s in nonterminals:
        follow(s, rules, terminal_set, first_dict, follow_dict, set())
    # 第二遍主要扫描有右递归的产生式
    logging.debug(f'############   2   ############')
    for s in nonterminals:
        follow(s, rules, terminal_set, first_dict, follow_dict, nonterminals)
    maxlen = 0
    for s in nonterminals:
        if len(s) > maxlen:
            maxlen = len(s)
    follow_len = len("FOLLOW()")
    maxlen += follow_len
    for s in nonterminals:
        logging.debug('{0:<{width}} {1} {{ {2} }}'.format("FIRST("+s+")", "=", " ".join(first_dict[s].list), width=maxlen))
    for s in nonterminals:
        logging.debug('{0:<{width}} {1} {{ {2} }}'.format("FOLLOW("+s+")", "=", " ".join(follow_dict[s].list), width=maxlen))
    return first_dict, follow_dict, nonterminals, terminals


def parse_line(line):
    line = line.strip()
    p = Parser(line)
    return p.production()


def parse_file(file_path):
    rules = []
    with open(file_path) as f:
        for line in f:
            rule = parse_line(line)
            if rule is None:
                continue
            rules.extend(rule)
    for s, l in rules:
        if len(l) == 0:
            l.append(epsilon)
    return rules


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='calculating first, follow and predict sets for the grammar.')
    parser.add_argument('file', type=str, nargs='+', help='input file')

    args = parser.parse_args()
    logging.info(args.file)
    for file in args.file:
        rules = parse_file(file)
        first_and_follow(rules)
