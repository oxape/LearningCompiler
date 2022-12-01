import argparse

def get_character():
    pass

def get_token():
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser('lexer preprocess')
    parser.add_argument('file_path', type=str, nargs='?', default='')
    
    version = 0x01020000

    args = parser.parse_args()
    file_path = args.file_path
    print(f'file_path = {args.file_path}')
    print(f'### args end ###')
    with open(file_path, 'r', encoding='utf-8') as fp:
        for chunk in iter(lambda: fp.read(128), ''):
            print(f'{chunk}', end='')
    print(f'### output end ###')