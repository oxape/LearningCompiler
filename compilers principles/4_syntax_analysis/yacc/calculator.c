#include <stdio.h>
#include "parser.tab.h"

extern int yyparse(void);

int main(void)
{
//  extern int yyparse(void);
    // yydebug=1;
    yyparse();
    return 0;
}