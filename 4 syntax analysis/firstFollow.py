import argparse


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
            right = self.sysmbol()
            if right == '|':
                productions.append((left, sysmbols))
                sysmbols = []
            else:
                sysmbols.append(right)
            if self.next >= self.length:
                break
            self.match_space()
        productions.append((left, sysmbols))
        return productions

    def nonterminal(self):
        start = self.next
        if not self.buffer[self.next].isalpha():
            raise ParseError('syntax error')
        self.next += 1
        while self.next < self.length:
            if self.buffer[self.next].isspace():
                break
            else:
                self.next += 1
        return self.buffer[start:self.next]

    def sysmbol(self):
        start = self.next
        while self.next < self.length:
            if self.buffer[self.next].isspace():
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


def parse_line(line):
    line = line.strip()
    p = Parser(line)
    return p.production()


def parse_file(file_path):
    rules = []
    with open(file_path) as f:
        for line in f:
            rules.extend(parse_line(line))
    print(rules)
    for s, l in rules:
        print(f'{s} -> {" ".join(l)}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='calculating first, follow and predict sets for the grammar.')
    parser.add_argument('file', type=str, nargs='+', help='input file')

    args = parser.parse_args()
    print(args.file)
    for file in args.file:
        parse_file(file)
