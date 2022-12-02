## 需要实现

1. 从正则表达式构造NFA
3. NFA转DFA
2. 输入缓存

4. NFA模拟
5. 求闭包
6. 从正则表达式构造DFA
7. 最小化DFA

## 支持的正则表达式
1. a
2. a|b
3. ab
4. a*
5. a?
6. a+
7. [ab]
8. [^ab]
9. [a-zA-Z]
10. [^a-zA-Z]

## 实现一个词法分析器
1. 可以使用文件的方式，编写每个token的模式和token值
2. 识别token后返回token值和text

### 实现
因为要识别最的长匹配(同时匹配所有的词法模式，找到一个最长的匹配)，所以状态机只要在当前状态对当前输入字符有出口状态就一直前进，直到到达停滞状态，回退到最近一次的接收状态(目前猜测对于现代多数语言，只需要回退一个字符)，需要一个last_final(最近一次进入的接收转态)，input_position_at_last_final(最后一次进入接收状态时的字符读入位置)，lexeme_begin(最后识别token时字符读入位置结尾)。lexeme_begin和input_position_at_last_final之间就是最后一次识别的词素

举例对于"s=ab+mn*xy;"，识别mn的时刻。

<style>
    table {
        width: 100%;
        border-collapse: collapse;
        border-spacing: 0;
        border: 3px solid;
        empty-cells: show;
    }
</style>

<table>
    <tr>
        <th>s</th>
        <th>=</th>
        <th>ab</th>
        <th>+</th>
        <th>mn</th>
        <th>*</th>
        <th>xy</th>
        <th>;</th>
    </tr>
    <tr>
        <td colspan="4">最后一次识别的token(+号)</td>
        <td colspan="2">最近进入接收状态位置是读入n后</td>
        <td colspan="1">读入*号后状态机进入停滞状态</td>
        <td colspan="1"> </td>
        <td colspan="1"> </td>
    </tr>
</table>


