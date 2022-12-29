
## 小任务

### 1. 实现一个正则表达式引擎

#### 步骤
1. 从一个正则表达式文法开始
2. 消除左递归
3. 使用递归下降法，构建语法分析树
4. 从语法分析树构建NFA
5. NFA

## 第3章需要实现

1. 从正则表达式构造NFA(算法3.23 page117)

    关键步骤需要构造语法分析树

2. NFA转DFA(算法3.20 page113)
4. NFA模拟(算法3.22 page115)
3. 输入缓存
5. 求闭包
6. 从正则表达式构造DFA
7. 最小化DFA

## 正则表达式的文法

### 文法
参考1:https://matt.might.net/articles/parsing-regex-with-recursive-descent/

参考2:https://www2.cs.sfu.ca/~cameron/Teaching/384/99-3/regexp-plg.html

    <RE>	::=	<union> | <simple-RE>
    <union>	::=	<RE> "|" <simple-RE>
    <simple-RE>	::=	<concatenation> | <basic-RE>
    <concatenation>	::=	<simple-RE> <basic-RE>
    <basic-RE>	::=	<star> | <plus> | <elementary-RE>
    <star>	::=	<elementary-RE> "*"
    <plus>	::=	<elementary-RE> "+"
    <elementary-RE>	::=	<group> | <any> | <eos> | <char> | <set>
    <group>	::=	"(" <RE> ")"
    <any>	::=	"."
    <eos>	::=	"$"
    <char>	::=	any non metacharacter | "\" metacharacter
    <set>	::=	<positive-set> | <negative-set>
    <positive-set>	::=	"[" <set-items> "]"
    <negative-set>	::=	"[^" <set-items> "]"
    <set-items>	::=	<set-item> | <set-item> <set-items>
    <set-items>	::=	<range> | <char>
    <range>	::=	<char> "-" <char>

参考了参考1的代码，使用了参考2的文法改成未扩展的正则表达式

    <RE>	::=	<union> | <simple-RE>
    <union>	::=	<RE> "|" <simple-RE>
    <simple-RE>	::=	<concatenation> | <basic-RE>
    <concatenation>	::=	<simple-RE> <basic-RE>
    <basic-RE>	::=	<star> | <elementary-RE>
    <star>	::=	<elementary-RE> "*"
    <elementary-RE>	::=	<group> | <char>
    <group>	::=	"(" <RE> ")"
    <char>	::=	any non metacharacter | "\" metacharacter

### 消除左递归

    <RE>	::=	<union>
    <union>	::=	<concatenation> "|" <union> | <concatenation>
    <concatenation>	::=	<basic-RE> <concatenation> | <basic-RE>
    <basic-RE>	::=	<elementary-RE> "*" | <elementary-RE>
    <elementary-RE>	::=	<group> | <char>
    <group>	::=	"(" <RE> ")"
    <char>	::=	any non metacharacter | "\" metacharacter

### 实现

使用递归下降分析正则表达式，首先需要消除左递归

## 支持的正则表达式
1. a
2. a|b
3. ab
4. a*
5. (a|b)
6. a?
7. a+
8. [ab]
9. [^ab]
10. [a-zA-Z]
11. [^a-zA-Z]
12. \\

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


### 3.8.2 基于NFA的模式匹配
词法模拟器基于NFA的模式匹配，从它的输入中lexemeBegin所指的位置开始读取输入，当它在输入中向前移动forword指针时，它在每个位置上根据算法3.22计算当前的状态集。

在这个模拟NFA运行的过程中，最终会到达一个<strong>没有后续状态</strong>的输入点。那时，不可能有<strong>任何更长的输入前缀</strong>使得这个NFA到达某个接受状态，此后的状态集将一直为空。于是，我们就可以判定最长前缀(与某个模式匹配的词素)是什么。

我们沿着状态集的顺序回头寻找，直到找到一个包含一个或多个接受状态的集合位置。如果集合中有多个接受状态，我们就选择和在Lex程序中位置最靠前的模式相关联的那个接受状态$p_i$。我们将forward指针移回到词素末尾，同时执行与$p_i$相关联的动作$A_i$。

### 3.8.3 词法分析器使用的DFA
另一种体系结构和Lex的输出相似，它使用算法3.20中的子集构造法将表示所有模式的NFA转换为等价的DFA。在DFA的每个状态中，如果该状态包含一个或多个NFA的接收状态，那么就要确定哪些模式的接受状态出现在此DFA状态中，并找出第一个这样的模式。然后将该模式作为这个DFA状态的输出。

在词法分析器中，我们使用DFA的方法与使用NFA的方法很类似。我们模拟这个DFA的运行，直到在某一点上没有后续状态为止(严格地说应该是下一个状态为$\varnothing$，即对应于空的NFA的状态集合的死状态)。此时我们回头查找我们进入过的状态序列，一旦找到接收状态就执行与状态对应的模式关联的动作


## 实现方法
1. 递归预测分析法
2. 非递归的预测分析法

    通过维护栈而不是递归调用隐式地维护栈