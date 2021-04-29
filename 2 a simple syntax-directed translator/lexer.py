import sys

# 编译原理  2.6.5 词法分析器


class Tag:
    NUM = 256
    ID = 257
    TRUE = 258
    FALSE = 259


class Token:
    def __init__(self, tag: int):
        print(tag)
        self.tag = tag


class Num(Token):
    def __init__(self, v: int):
        super().__init__(Tag.NUM)
        self.value = v


class Word(Token):

    def __init__(self, t: int, s: str):
        super().__init__(t)
        self.lexeme = s


class Lexer:
    line = 1
    peek = ''
    words = dict()

    def __init__(self):
        self.reverve(Word(Tag.TRUE, 'true'))
        self.reverve(Word(Tag.FALSE, 'false'))

    def reverve(self, w: Word):
        self.words[w.lexeme] = w

    def scan(self) -> Token:
        while True:
            self.peek = sys.stdin.read(1)
            if self.peek == ' ' or self.peek == '\t':
                continue
            elif self.peek == '\n':
                self.line += 1
            else:
                break
        if self.peek.isdigit():
            v = 0
            while True:
                v = v*10 + int(self.peek)
                self.peek = sys.stdin.read(1)
                if not self.peek.isdigit():
                    break
            return Num(v)
        if self.peek.isalpha():
            b = bytearray()
            while True:
                b.extend(self.peek.encode('utf-8'))
                self.peek = sys.stdin.read(1)
                if not self.peek.isalnum():
                    break
            s = b.decode('utf-8')
            w = self.words.get(s, None)
            if w is not None:
                return w
            w = Word(Tag.ID, s)
            self.words[s] = w
            return w
        t = Token(ord(self.peek[0]))
        self.peek = ' '
        return t


if __name__ == '__main__':
    lexer = Lexer()
    lexer.scan()
