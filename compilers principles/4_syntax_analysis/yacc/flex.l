%{
extern int yylval;
%}

number      [0-9]+\.?
%%
[ ]          {}
{number}    {sscanf(yytext, "%d", &yylval);
                return NUMBER; }
\n|.        {return yytext[0];}
%%