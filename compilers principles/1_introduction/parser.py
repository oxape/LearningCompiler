import sys

# 编译原理  2.4.2 预测分析法  2.5 简单表达式的翻译器


class ParseSyntaxError(Exception):
    pass


class Parser:
    def __init__(self):
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


class Postfix(object):
    @classmethod
    def main(cls):
        parser = Parser()
        parser.expr()
        sys.stdout.write('\n')


if __name__ == '__main__':
    while True:
        try:
            Postfix.main()
        except KeyboardInterrupt:
            print('Keyboard interrupt in main')
            break


