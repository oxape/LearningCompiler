import os
import argparse
import uuid
from pathlib import Path
from graphviz import Graph, Digraph
from functools import wraps


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
    # with open(lexis, 'r', encoding='utf-8') as fp:
    #     for line in iter(lambda: fp.readline(), ''):
    #         print(f'{line.strip()}', end='\n')
    #         line = line.strip()
    #         parser = RegExParser(line)
    #         root = parser.parse()
    #         root.draw()
    #         break

    # with open(file_path, 'r', encoding='utf-8') as fp:
    #     for chunk in iter(lambda: fp.read(128), ''):
    #         print(f'{chunk}', end='')
    print(f'### output end ###')