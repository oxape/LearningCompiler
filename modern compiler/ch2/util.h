#ifndef CF4738BD_C2FB_4199_A631_5C5C0B3D0A58
#define CF4738BD_C2FB_4199_A631_5C5C0B3D0A58

#include <assert.h>

typedef char *string;
typedef char bool;

#define TRUE 1
#define FALSE 0

void *checked_malloc(int);
string String(char *);

typedef struct U_boolList_ *U_boolList;
struct U_boolList_ {bool head; U_boolList tail;};
U_boolList U_BoolList(bool head, U_boolList tail);


#endif /* CF4738BD_C2FB_4199_A631_5C5C0B3D0A58 */
