import sys

class SyntaxError(Exception):
    pass

class Parser:
    def __init__(self):
        self.lookahead = sys.stdin.read(1)

    def expr(self):
        self.term()
        while True:
            if self.lookahead == '+':
                self.match('+')
                self.expr() #这里为自己修改后支持*
                sys.stdout.write('+')
            elif self.lookahead == '-':
                self.match('-')
                self.expr() #这里为自己修改后支持*
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
            raise SyntaxError('syntax error')

    def match(self, t):
        if self.lookahead == t:
            self.lookahead = sys.stdin.read(1)
        else:
            raise SyntaxError('syntax error')

class Postfix(object):
    @classmethod
    def main(cls):
        parser = Parser()
        parser.expr()
        sys.stdout.write('\n')


if __name__ == '__main__':
    Postfix.main()

