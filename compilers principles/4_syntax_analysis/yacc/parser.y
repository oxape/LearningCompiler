%{
#include <ctype.h>
#include <stdio.h>
#include "lex.yy.c"

#define YYSTYPE int

int yylval;

void yyerror(const char* msg) {printf("%s", msg);}
int yywrap(){return 1;} //一些库的实现没有自带默认的yywrap和main，需要自己实现


%}

%token NUMBER

%%
lines   : lines expr '\n'         { printf("%d\n", $2); }
        | lines '\n'
        |
        ;

expr    : expr '+' term      { $$ = $1 + $3; }
        | term
        ;

term    : term '*' factor   { $$ = $1 * $3; }
        | factor
        ;

factor  : '(' expr ')'      { $$ = $2; }
        | NUMBER
        ;

%%