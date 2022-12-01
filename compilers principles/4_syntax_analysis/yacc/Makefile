calculator: lex.yy.c parser.tab.c calculator.c
	cc -o $@ calculator.c parser.tab.c

lex.yy.c: flex.l
	flex flex.l

parser.tab.c: parser.y
	bison -d parser.y

clean:
	@rm -f lex.yy.c
	@rm -f parser.tab.c
	@rm -f calculator