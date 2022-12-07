import os
import argparse
from pathlib import Path
from graphviz import Graph
import uuid

dfa_state_map = {}
dfa_next_state_map = {}
dfa_final_state_set = {}

class ParseRegError(Exception):
    pass

class ASTNode:

    def __init__(self, op, *args):
        self.op = op
        self.children = [*args]
        self.uuid = str(uuid.uuid4())

    def draw(self):
        g = Graph(format='png')
        g.node(self.uuid, label=self.op, fontcolor='black')
        for child in self.children:
            ASTNode._build_graph(g, child) #构建子节点
            g.edge(self.uuid, child.uuid, color='black') #连接
        g.render(filename='tmp/g', view=True)

    @classmethod
    def _build_graph(cls, g, node):
        g.node(node.uuid, label=node.op, fontcolor='black')
        for child in node.children:
            ASTNode._build_graph(g, child)
            g.edge(node.uuid, child.uuid, color='black')

'''
    <regex>	::=	<term> '|' <regex> |  <term>
    <term>	::=	<factor> <term> | Ɛ
    <factor> ::= <base> '*' | Ɛ
    <base>	::= <char> | '\' <char> | '(' <regex> ')'
'''

class RegExParser:

    def __init__(self, input):
        self.input = input

    def peek(self):
        return self.input[0]

    def eat(self, c):
        if self.peek() == c:
            self.input = self.input[1:]
        else:
            raise ParseRegError("Expected: " + c + "; got: " + self.peek())

    def next(self):
        c = self.peek()
        self.eat(c)
        return c

    def more(self):
        return len(self.input) > 0

    def parse(self):
        return self.regex()

    def regex(self):
        term = self.term()

        if self.more() and self.peek() == '|':
            self.eat('|')
            regex = self.regex()
            return ASTNode('|', term, regex)
        else:
            return term

    def term(self):
        factor = self.factor()
        #判断peek不属于term follow
        while self.more() and self.peek() != ')' and self.peek() != '|':
            nextFactor = self.factor()
            return ASTNode('·', factor,nextFactor)
        return factor

    def factor(self):
        base = self.base()
        if self.more() and self.peek() == '*':
            self.eat('*')
            base = ASTNode('*', base)
        return base

    def base(self):
        if self.peek() == '(':
            self.eat('(')
            r = self.regex()
            self.eat(')')
            return r
        elif self.peek() == '\\':
            self.eat('\\')
            esc = self.next()
            return ASTNode(esc)
        else:
            return ASTNode(self.next())

def get_character():
    pass

def get_token():
    pass

if __name__ == '__main__':
    os.chdir(Path(__file__).parent)
    print(Path(__file__).parent)

    parser = argparse.ArgumentParser('lexer preprocess')
    parser.add_argument('file_path', type=str)
    parser.add_argument('--lexis', type=str, required=True)
    
    args = parser.parse_args()
    file_path = args.file_path
    lexis = args.lexis
    print(f'file_path = {args.file_path}')
    print(f'lexis = {args.lexis}')
    print(f'### args end ###')
    with open(lexis, 'r', encoding='utf-8') as fp:
        for line in iter(lambda: fp.readline(), ''):
            print(f'{line.strip()}', end='\n')
            line = line.strip()
            parser = RegExParser(line)
            root = parser.parse()
            root.draw()
            break

    # with open(file_path, 'r', encoding='utf-8') as fp:
    #     for chunk in iter(lambda: fp.read(128), ''):
    #         print(f'{chunk}', end='')
    print(f'### output end ###')