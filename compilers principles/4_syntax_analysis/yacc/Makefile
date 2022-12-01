calculator: lex.yy.c translator.tab.c calculator.c
	cc -o $@ calculator.c

lex.yy.c: flex.l
	flex flex.l

translator.tab.c: translator.y
	bison translator.y

clean:
	@rm -f lex.yy.c
	@rm -f translator.tab.c
	@rm -f calculator