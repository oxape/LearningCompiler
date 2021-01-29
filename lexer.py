import sys

class Tag:
    NUM = 256
    ID = 257
    TRUE = 258
    FALSE = 259

class Token:
    def __init__(self, tag: int):
        self.tag = tag

class Number(Token):
    def __init__(self, v: int):
        super().__init__(Tag.NUM)
        self.value = v

class Word(Token):
    def __init__(self, t: int, s:str):
        super().__init__(t)
        self.lexeme = s

class Lexer:
    line = 1
    peek = ''
    words = dict()
    def __init__(self):
        super.__init__()

    def reverve(self, w:Word):
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
            pass


if __name__ == '__main__':
    pass