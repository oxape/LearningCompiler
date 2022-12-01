#include <stdio.h>
#include "translator.tab.c"


int main(void)
{
//  extern int yyparse(void);
    // yydebug=1;
    yyparse();
    return 0;
}