myc: lexer.o
	cc -g -o lextest driver.o lex.yy.o errormsg.o util.o

lexer.o: lexer.c
	cc -g -c driver.c

clean: 
	rm -f lexer.o