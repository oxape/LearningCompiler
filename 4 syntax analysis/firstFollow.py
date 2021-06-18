"""
使用前需要建议先消除文法中的左递归，也许可以处理左递归，但也可能发生什么一些我也无法预测的事情
"""
import argparse

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
        start = self.next
        if not self.buffer[self.next].isalpha():
            raise ParseError('syntax error')
        self.next += 1
        while self.next < self.length:
            if self.buffer[self.next].isspace() or self.buffer[self.next] == '.':
                break
            else:
                self.next += 1
        return self.buffer[start:self.next]

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
    print(f'^^^^^^^^^^^^{s}^^^^^^^^^^^^')
    for t, l in rules:
        if t != s:
            continue
        print(f'    process {t} -> {" ".join(l)} -- for {s}')
        end = 0
        for index, e in enumerate(l):
            if e == epsilon:
                if len(l) == 1:
                    first(e, rules, terminal_set, first_dict)
                    for se in first_dict[e].list:
                        if se not in las.set:
                            print(f'1 add {se} to FIRST({s})')
                            las.list.append(se)
                            las.set.add(se)
            else:
                first(e, rules, terminal_set, first_dict)
                for se in first_dict[e].list:
                    if se == epsilon:
                        continue
                    if se not in las.set:
                        print(f'2 add {se} to FIRST({s})')
                        las.list.append(se)
                        las.set.add(se)
                if epsilon not in first_dict[e].set:
                    break
            end = index
        if end+1 == len(l):
            if epsilon in first_dict[l[-1]].set:
                if epsilon not in las.set:
                    print(f'3 add {epsilon} to FIRST({s})')
                    las.list.append(epsilon)
                    las.set.add(epsilon)
    print(f'------------{s}------------')


def follow(s, rules, terminal_set, first_dict, follow_dict, second=False):
    las = follow_dict.get(s, None)
    if not second:
        if las is not None:
            return
        las = ListAndSet()
        if s == start:
            las.list.append(dollar)
            las.set.add(dollar)
        follow_dict[s] = las
    else:
        if las is None:
            return
    print(f'^^^^^^^^^^^^{s}^^^^^^^^^^^^')
    for t, l in rules:
        print(f'    process {t} -> {" ".join(l)} -- for {s}')
        for index, e in enumerate(l):
            if e == s:
                if index+1 < len(l):
                    for se in first_dict[l[index+1]].list:
                        if se != epsilon and se not in las.set:
                            print(f'1 add {se} to FOLLOW({s})')
                            las.list.append(se)
                            las.set.add(se)
                end = index
                for i, se in enumerate(l[index+1:]):
                    if epsilon not in first_dict[se].set:
                        break
                    end = i
                if end + 1 == len(l):
                    if t == s:
                        continue
                    if not second:
                        follow(t, rules, terminal_set, first_dict, follow_dict, second)
                    for se in follow_dict[t].list:
                        if se not in las.set:
                            print(f'2 add {se} to FOLLOW({s})')
                            las.list.append(se)
                            las.set.add(se)
    print(f'------------{s}------------')


def first_and_follow(rules):
    nonterminal_set = set()
    nonterminals = []
    terminal_set = set()
    terminals = []
    first_dict = {}
    follow_dict = {}
    unprocessed_nonterminal_set = set()
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
        print(f'{s} -> {" ".join(l)}')
    print(nonterminals)
    print(terminals)
    print(f'############first############')
    for s in nonterminals:
        first(s, rules, terminal_set, first_dict)
    for s in terminals:
        first(s, rules, terminal_set, first_dict)
    print(f'############follow############')
    print(f'start = {start}')
    print(f'############   1   ############')
    for s in nonterminals:
        follow(s, rules, terminal_set, first_dict, follow_dict, set())
    # 第二遍主要扫描有右递归的产生式
    print(f'############   2   ############')
    for s in nonterminals:
        follow(s, rules, terminal_set, first_dict, follow_dict, nonterminals)
    for s in nonterminals:
        print(f'FIRST({s}) -> {{{" ".join(first_dict[s].list)}}}')
    for s in nonterminals:
        print(f'FOLLOW({s}) -> {{{" ".join(follow_dict[s].list)}}}')


def parse_line(line):
    line = line.strip()
    p = Parser(line)
    return p.production()


def parse_file(file_path):
    rules = []
    with open(file_path) as f:
        for line in f:
            rules.extend(parse_line(line))
    for s, l in rules:
        if len(l) == 0:
            l.append(epsilon)
    return rules


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='calculating first, follow and predict sets for the grammar.')
    parser.add_argument('file', type=str, nargs='+', help='input file')

    args = parser.parse_args()
    print(args.file)
    for file in args.file:
        rules = parse_file(file)
        first_and_follow(rules)
