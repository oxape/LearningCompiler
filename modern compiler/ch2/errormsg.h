#ifndef FA657786_9282_408E_B5A0_4D548D21C474
#define FA657786_9282_408E_B5A0_4D548D21C474

extern bool EM_anyErrors;

void EM_newline(void);

extern int EM_tokPos;

void EM_error(int, string,...);
void EM_impossible(string,...);
void EM_reset(string filename);

#endif /* FA657786_9282_408E_B5A0_4D548D21C474 */
