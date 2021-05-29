import argparse


class ParseError(Exception):
    pass


class Parser:
    def __init__(self, ):
        self.lookahead = sys.stdin.read(1)

    def expr(self):
        self.term()
        while True:
            if self.lookahead == '+':
                self.match('+')
                # 这里为自己修改后支持*
                self.expr()
                sys.stdout.write('+')
            elif self.lookahead == '-':
                self.match('-')
                # 这里为自己修改后支持*
                self.expr()
                sys.stdout.write('-')
            elif self.lookahead == '*':
                self.match('*')
                self.term()
                sys.stdout.write('*')
            else:
                return

    def term(self):
        if self.lookahead.isdigit():
            sys.stdout.write(self.lookahead)
            self.match(self.lookahead)
        else:
            raise ParseSyntaxError('syntax error')

    def match(self, t):
        if self.lookahead == t:
            self.lookahead = sys.stdin.read(1)
        else:
            raise ParseSyntaxError('syntax error')


def parse_line(line):
    line = line.strip()
    print(line)
    for

def parse_file(file_path):
    rules = []
    with open(file_path) as f:
        for line in f:
            parse_line(line)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='calculating first, follow and predict sets for the grammar.')
    parser.add_argument('file', type=str, nargs='+', help='input file')

    args = parser.parse_args()
    print(args.file)
    for file in args.file:
        parse_file(file)
