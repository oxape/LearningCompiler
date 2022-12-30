import os
import argparse
import uuid
from pathlib import Path
from graphviz import Graph, Digraph
from functools import wraps
from tabulate import tabulate
from collections import OrderedDict

func_count_dict = {}

def FnLogging(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        global func_count_dict
        local_count = func_count_dict.get(fn.__name__, 1)
        func_count_dict[fn.__name__] = local_count+1
        # print(f'{fn.__name__} {local_count} enter')
        ret = fn(*args)
        # print(f'{fn.__name__} {local_count} exit')
        return ret
    return wrapper


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
        g.render(filename='tmp/g.gv', view=True)

    @classmethod
    def _build_graph(cls, g, node):
        g.node(node.uuid, label=node.op, fontcolor='black')
        for child in node.children:
            ASTNode._build_graph(g, child)
            g.edge(node.uuid, child.uuid, color='black')


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

    # 实现<RE>	::=	<union>
    @FnLogging
    def regex(self):
        union = self.union()
        return union

    # 实现<union>	::=	<concatenation> "|" <union> | <concatenation>
    @FnLogging
    def union(self):
        concatenation = self.concatenation()
        while self.more() and self.peek() == '|':
            self.eat('|')
            union = self.union()
            concatenation = ASTNode('|', concatenation, union)
        return concatenation

    # 实现<concatenation>	::=	<basic-RE> <concatenation> | <basic-RE>
    @FnLogging
    def concatenation(self):
        basic_regex = self.basic_regex()
        # 判断peek属于basic_regex follow，这里一定要判断好，后面如果是'|'和')'需要返回交给上层解析
        while self.more() and self.peek() != '|' and self.peek() != ')':
            # 这里和文法略微不一样，按照文法这里应该是concatenation = self.concatenation()
            basic_regex_next = self.basic_regex()
            basic_regex = ASTNode('·', basic_regex, basic_regex_next)
        return basic_regex

    # 实现<basic-RE>	::=	<elementary-RE> "*" | <elementary-RE>
    @FnLogging
    def basic_regex(self):
        elementary_regex_first = self.elementary_regex()
        if self.more() and self.peek() == '*':
            self.eat('*')
            return ASTNode('*', elementary_regex_first)
        else:
            return elementary_regex_first
    
    # 实现<elementary-RE>	::=	<group> | <char>
    @FnLogging
    def elementary_regex(self):
        if self.peek() == '(':
            return self.group()
        else:
            return self.char()

    # 实现<group>	::=	"(" <RE> ")"
    @FnLogging
    def group(self):
        self.eat('(')
        r = self.regex()
        self.eat(')')
        return r

    # 实现<char>	::=	any non metacharacter | "\" metacharacter
    @FnLogging
    def char(self):
        if self.peek() == '\\':
            self.eat('\\')
            esc = self.next()
            return ASTNode(esc)
        else:
            return ASTNode(self.next())


class NFA:
    '''
        nfa = {状态集, 字母表, 转移函数, 初始状态, 接收状态}

        nfa_state_map = {
            1: {a: set({3}), b: set({2})},
            2: {a: set({4}), b: set({5, 6})}
        }
    '''
    Ɛ = -1 # Ɛ边为-1
    def __init__(self, astree): #从正则表达式的语法树构建NFA
        self.astree = astree
        self.nfa_state_map = {}
        self.final_state_set = set()
        self.letter_set = set()
        self.start = -1
        self.state = -1 # 这样初始状态就会从0开始
        self.op_construct_method = {
            '|': self.construct_union,
            '·': self.construct_cat,
            '*': self.construct_closure,
        }

    def new_state(self):
        self.state += 1
        return self.state

    def add_transition(self, from_sate, to_sate, edge):
        to_state_dict = self.nfa_state_map.get(from_sate, None)
        if to_state_dict is None:
            self.nfa_state_map[from_sate] = {}
        to_state_dict = self.nfa_state_map[from_sate]
        edge_dict = to_state_dict.get(edge, None)
        if edge_dict is None:
            to_state_dict[edge] = {to_sate}
        else:
            to_state_dict[edge].add(to_sate)
        if self.nfa_state_map.get(to_sate, None) is None:
            self.nfa_state_map[to_sate] = {}
    
    def construct_nfa(self):
        node = self.astree
        op_set = {'|', '·', '*'}
        if node.op in op_set:
            self.start, _ = self.construct(node)
        else:
            raise ValueError(f'op {node.op} unexpected')

    def construct(self, node):
        construction = self.op_construct_method.get(node.op, None)
        if construction is not None:
            return construction(node)
        else:
            return self.construct_letter(node)

    def construct_union(self, node):
        start_state = self.new_state() # start_state = self.new_state() 必须放在开始位置
        next_state0, final_state0 = self.construct(node.children[0])
        next_state1, final_state1 = self.construct(node.children[1])
        self.add_transition(start_state, next_state0, self.Ɛ)
        self.add_transition(start_state, next_state1, self.Ɛ)
        final_state = self.new_state() # final_state = self.new_state() 必须放在结束位置
        self.add_transition(final_state0, final_state, self.Ɛ)
        self.add_transition(final_state1, final_state, self.Ɛ)
        self.final_state_set.remove(final_state0)
        self.final_state_set.remove(final_state1)
        self.final_state_set.add(final_state)
        return start_state, final_state

    def construct_cat(self, node):
        next_state0, _ = self.construct(node.children[0])
        '''
        由于每个构造方法start_state = self.new_state()都在开始位置，
        final_state = self.new_state() 必须放在结束位置
        这里self.state -= 1可以让next_state1等于final_state0这样就避免合并状态的操作
        '''
        self.state -= 1
        next_state1, final_state1 = self.construct(node.children[1])
        self.final_state_set.remove(next_state1)
        self.final_state_set.add(final_state1)
        return next_state0, final_state1

    def construct_closure(self, node):
        start_state = self.new_state() # start_state = self.new_state() 必须放在开始位置
        next_state0, final_state0 = self.construct(node.children[0])
        final_state = self.new_state() # final_state = self.new_state() 必须放在结束位置
        self.add_transition(final_state0, final_state, self.Ɛ)
        self.add_transition(start_state, next_state0, self.Ɛ)
        self.add_transition(final_state0, next_state0, self.Ɛ)
        self.add_transition(start_state, final_state, self.Ɛ)
        self.final_state_set.remove(final_state0)
        self.final_state_set.add(final_state)
        return start_state, final_state

    def construct_letter(self, node):
        start_state = self.new_state() # start_state = self.new_state() 必须放在开始位置
        final_state = self.new_state() # final_state = self.new_state() 必须放在结束位置
        self.add_transition(start_state, final_state, node.op)
        self.final_state_set.add(final_state)
        self.letter_set.add(node.op)
        return start_state, final_state

    def match(self, s):
        pass

    def draw(self):
        if len(self.nfa_state_map) == 0:
            raise SyntaxError('need construct_nfa before draw')
        dg = Digraph(format='png')
        dg.attr(rankdir='LR', size='8,5')
        self.state_record_set = {self.start}
        dg.node(str(self.start), str(self.start), fontcolor='black')
        for edge in self.nfa_state_map[self.start]:
            state_set = self.nfa_state_map[self.start][edge]
            for to_state in state_set:
                NFA._build_graph(dg, self.state_record_set, self.nfa_state_map, self.final_state_set, to_state) #构建子节点
                edge_label = edge
                if edge == -1:
                    edge_label = 'Ɛ'
                dg.edge(str(self.start), str(to_state), label=edge_label, color='black') #连接
                # print(f'{self.start} -{edge_label}-> {to_state}')
        dg.render(filename='tmp/nfa.gv', view=True)

    @classmethod
    def _build_graph(cls, dg, record_set, state_map, final_set, state):
        if state in record_set:
            return
        record_set.add(state)
        if state in final_set:
            dg.node(str(state), label=str(state), fontcolor='black', shape='doublecircle')
        else:
            dg.node(str(state), label=str(state), fontcolor='black')
        for edge in state_map[state]:
            state_set = state_map[state][edge]
            for to_state in state_set:
                NFA._build_graph(dg, record_set, state_map, final_set, to_state) #构建子节点
                edge_label = edge
                if edge == -1:
                    edge_label = 'Ɛ'
                dg.edge(str(state), str(to_state), label=edge_label, color='black') #连接
                # print(f'{state} -{edge_label}-> {to_state}')

class DFA:
    '''
        dfa = {状态集, 字母表, 转移函数, 初始状态, 接收状态}

        dfa_state_map = {
            1: {a: 3, b: 2},
            2: {a: 4, b: 5}
        }
    '''
    Ɛ = -1 # Ɛ边为-1
    def __init__(self):
        self.nfa_states_map = OrderedDict() # 每个key是NFA中的一个状态集
        self.nfa_ss2s_map = {} # 每个NFA状态集映射一个DFA状态
        self.dfa_state_map = {} # DFA状态沿着边到DFA状态
        self.final_state_set = set()
        self.letter_set = set()
        self.start = -1
        self.state = ord('A') # 这样初始状态就会从0开始

    def new_state(self):
        new_state = chr(self.state)
        self.state += 1
        return new_state

    def nfa2dfa(self, nfa):
        def closure(nfa_state_map, T):
            stack = list(T)
            closure_set = set(T)
            while len(stack) > 0:
                t = stack.pop()
                state_set = nfa_state_map[t].get(self.Ɛ, None)
                if state_set is None:
                    continue
                for u in state_set:
                    if u not in closure_set:
                        closure_set.add(u)
                        stack.append(u)
            return closure_set

        def move(nfa_state_map, T, edge):
            move_set = set()
            for t in T:
                state_set = nfa_state_map[t].get(edge, None)
                if state_set is None:
                    continue
                for u in state_set:
                    if u not in move_set:
                        move_set.add(u)
            return move_set
        
        self.letter_set = set(nfa.letter_set)
        t0 = closure(nfa.nfa_state_map, {nfa.start})
        t0 = frozenset(t0)
        mark_set = set()
        Dstates = list([t0])
        while len(Dstates) > 0:
            ts = Dstates.pop(0) #Dstates相当于一个FIFO队列
            if ts in mark_set:
                continue
            mark_set.add(ts)
            if self.nfa_states_map.get(ts, None) is None:
                if self.nfa_ss2s_map.get(ts, None) is None:
                    self.nfa_ss2s_map[ts] = self.new_state()
                self.nfa_states_map[ts] = {}
                self.dfa_state_map[self.nfa_ss2s_map[ts]] = {}
            for letter in nfa.letter_set:
                U = closure(nfa.nfa_state_map, move(nfa.nfa_state_map, ts, letter))
                U = frozenset(U)
                if U not in Dstates: # 这里没有不能使用frozenset作为key判断not in时，可以将set中元素排序后变成字符串作为key
                    Dstates.append(U)
                if self.nfa_ss2s_map.get(U, None) is None:
                    self.nfa_ss2s_map[U] = self.new_state()
                self.nfa_states_map[ts][letter] = U
                self.dfa_state_map[self.nfa_ss2s_map[ts]][letter] = self.nfa_ss2s_map[U]
        # print(self.nfa_ss2s_map)
        # print(self.dfa_state_map)
    
    def print_table(self):
        headers = ['NFA states', 'DFA states']
        letter_list = list(self.letter_set)
        letter_list.sort()
        headers.extend(letter_list)
        table = [headers]
        for nfa_states, value in self.nfa_states_map.items():
            rows = [list(nfa_states)]
            rows.append(self.nfa_ss2s_map[nfa_states])
            for letter in letter_list:
                to_states = value.get(letter, None)
                if to_states is None:
                    continue
                rows.append(self.nfa_ss2s_map[to_states])
            table.append(rows)
        print(tabulate(table, tablefmt='grid'))


def RegExParserTest():
    parser = RegExParser('(a|b)*abb')
    # parser = RegExParser('(a|bb)*abb')
    root = parser.parse()
    # root.draw()
    nfa = NFA(root)
    nfa.construct_nfa()
    # nfa.draw()
    dfa = DFA()
    dfa.nfa2dfa(nfa)
    dfa.print_table()

if __name__ == '__main__':
    os.chdir(Path(__file__).parent)
    print(Path(__file__).parent)

    RegExParserTest()
