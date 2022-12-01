#ifndef C92AF802_4A66_4786_A039_BEFC76F15AB2
#define C92AF802_4A66_4786_A039_BEFC76F15AB2

//这里考虑支持unicode，token值使用负数避免和unicode有效值冲突，这样一些标点符号可以直接返回unicode值作为token值

#define TOKEN_EOF       -1
#define STRING          -258
#define INT             -259

#endif /* C92AF802_4A66_4786_A039_BEFC76F15AB2 */
