//MSSV: 1812228

grammar BKIT;

@lexer::header {
from lexererr import *
}

@lexer::members {
def emit(self):
    tk = self.type
    result = super().emit()
    if tk == self.UNCLOSE_STRING:       
        raise UncloseString(result.text)
    elif tk == self.ILLEGAL_ESCAPE:
        raise IllegalEscape(result.text)
    elif tk == self.ERROR_CHAR:
        raise ErrorToken(result.text)
    elif tk == self.UNTERMINATED_COMMENT:
        raise UnterminatedComment()
    else:
        return result;
}

options{
	language=Python3;
}

program  : declaration+ EOF ;

declaration: var_declare | func_decalre;


//function_call
func_call: IDENTIFIER '(' (expr (',' expr)*)?  ')' ;


expr: expr1 (GREATER_INT| GREATER_EQ_INT|LESS_INT|LESS_EQ_INT|EQ_INT|N_EQ_INT|GREATER_FLOAT|GREATER_EQ_FLOAT|LESS_FLOAT|LESS_EQ_INT|EQ_FLOAT) expr1 | expr1;
expr1: expr1 (AND_OP|OR_OP) expr2 | expr2;
expr2: expr2 (ADD_INT|ADD_FLOAT|SUB_INT|SUB_FLOAT) expr3 | expr3;
expr3: expr3 (MUL_INT|MUL_FLOAT|DIV_INT|DIV_FLOAT|REMAIN_INT) expr4 |expr4;
expr4: NOT_OP expr4|expr5;
expr5: (SUB_INT|SUB_FLOAT) expr5|expr6;
expr6: expr7 ('[' expr ']')+ | expr7;
expr7: func_call | expr8 ;
expr8: '(' expr ')' | operand;

operand: IDENTIFIER | INTLIT | FLOATLIT | STRINGLIT | BOOLLIT | array ; 

//var declaration
var_init: IDENTIFIER ('['INTLIT']'('['INTLIT']')*)? ('=' array_element)? ;

var_declare: VAR ':' var_init (',' var_init)*  ';' ;

param_element: IDENTIFIER ('['INTLIT']'('['INTLIT']')*)?;
param_list: param_element(','param_element)*;

//function declaration
func_decalre: FUNCTION ':' IDENTIFIER
                (PARAMETER ':' param_list)?
                BODY ':'
                var_declare*?
                stmt_list
                ENDBODY '.';

//assignment statement
ass_stmt: (IDENTIFIER | expr6) '=' expr ';';


elif_stmt : ELSEIF expr THEN stmt_list;
//if_else statement
if_else_stmt: IF expr THEN var_declare*? stmt_list
            elif_stmt*
            (ELSE var_declare*? stmt_list)?
            ENDIF '.';

//for statement
for_stmt: FOR '(' IDENTIFIER '=' expr ',' expr ',' expr ')' DO var_declare*? stmt_list
            ENDFOR '.';


//while statement
while_stmt: WHILE expr DO var_declare*? stmt_list ENDWHILE '.';

//do while statment
do_while_stmt: DO var_declare*? stmt_list WHILE expr ENDDO '.';

//break statement
break_stmt: BREAK ';';

//continue statement
continue_stmt: CONTINUE ';';

//call statement
call_stmt: IDENTIFIER '(' (expr (',' expr)*)?  ')' ';';

//return statement
return_stmt: RETURN (expr)? ';';

stmt: if_else_stmt|while_stmt|do_while_stmt|ass_stmt|call_stmt|return_stmt|break_stmt|continue_stmt|for_stmt;

stmt_list: (stmt)*;


array_element: INTLIT|STRINGLIT|BOOLLIT|FLOATLIT| array;

array: '{' (array_element (',' array_element)*)? '}' ;


//fragment Number and character
fragment DIGIT: [0-9];
fragment LOWERCASE: [a-z];
fragment UPPERCASE: [A-Z];
fragment UNDERSCORES: '_';

//Display identifier
IDENTIFIER: LOWERCASE (LOWERCASE | UPPERCASE | UNDERSCORES | DIGIT)* ;

//Display Keywords
//KEYWORDS: 'Body' | 'Break' | 'Continue' | 'Do'
//        | 'Else' | 'ElseIf' | 'EndBody' | 'EndIf'
//        | 'EndFor' | 'EndWhile' | 'For' | 'Function' 
//        | 'If' | 'Parameter' | 'Return' | 'Then'
//        | 'Var' | 'While'
//        | 'EndDo' ;

BODY: 'Body';
BREAK: 'Break';
CONTINUE: 'Continue';
DO: 'Do';
ELSE: 'Else';
ELSEIF: 'ElseIf';
ENDBODY: 'EndBody';
ENDIF: 'EndIf';
ENDFOR: 'EndFor';
ENDWHILE: 'EndWhile';
FOR: 'For';
FUNCTION: 'Function';
IF: 'If';
PARAMETER: 'Parameter';
RETURN: 'Return';
THEN: 'Then';
VAR: 'Var';
WHILE: 'While';
ENDDO: 'EndDo';


//Integer Operator
ADD_INT: '+';
SUB_INT: '-';
MUL_INT: '*';
DIV_INT: '\\';
REMAIN_INT: '%' ;
EQ_INT: '==';
N_EQ_INT: '!=';
LESS_INT: '<';
GREATER_INT: '>';
LESS_EQ_INT: '<=';
GREATER_EQ_INT: '>=';

//Floating point Operator
ADD_FLOAT: '+.';
SUB_FLOAT: '-.';
MUL_FLOAT: '*.';
DIV_FLOAT: '\\.';
EQ_FLOAT: '=/=';
LESS_FLOAT: '<.';
GREATER_FLOAT: '>.';
LESS_EQ_FLOAT: '<=.';
GREATER_EQ_FLOAT: '>=.';

AND_OP: '&&';
OR_OP: '||';
NOT_OP: '!';

//Display integer number
//DECIMAL: [1-9] DIGIT* | '0' ;
//OCTAL: ('0o'|'0O') [1-7] [0-7]*;
//HEXADECIMAL: ('0X'|'0x') ([1-9] | [A-F]) (DIGIT | [A-F])*;
INTLIT: [1-9] DIGIT* | '0' | (('0o'|'0O') [1-7] [0-7]*) | (('0X'|'0x') ([1-9] | [A-F]) (DIGIT | [A-F])*);


//Display floating point number
//INT_PART: DIGIT+;
//DEC_PART: '.' DIGIT*;
//EXP_PART: [eE] [+-]? DIGIT+;
FLOATLIT: DIGIT+ (('.'DIGIT* ([eE] [+-]? DIGIT+)?) | ([eE] [+-]? DIGIT+));

//Display Boolean literal
BOOLLIT: 'True' | 'False';


SEPARATOR: '(' | ')'| '[' | ']' |':' | '.' | ','| ';' | '{' |'}';




WS : [ \t\r\n]+ -> skip ; // skip spaces, tabs, newlines

fragment BSP: '\\b';
fragment FF: '\\f';
fragment CR: '\\r';
fragment NEWLINE: '\\n';
fragment TAB: '\\t';
fragment SQUOTE: '\\\'';
fragment DQUOTE: '\\"';
fragment BSL:'\\''\\';

SIN_CMT: '**' .*? '**' -> skip ;

UNCLOSE_STRING: '"' STRING_CHAR* ( ESC_SEQ | '<EOF>' )?
	{
		y = str(self.text)
		raise UncloseString(y[1:])
	}
	;

//Display String literal
STRINGLIT: '"' STRING_CHAR* '"'
    {
        y = str(self.text)
        self.text = y[1:-1]
    } ;

ILLEGAL_ESCAPE: '"' STRING_CHAR* ESC_ILLEGAL
    {
        raise IllegalEscape(self.text[1:])
    };

ERROR_CHAR: .
    {
        raise ErrorToken(self.text)
    };
UNTERMINATED_COMMENT: '**' .*?;

fragment STRING_CHAR: ~[\b\t\n\f\r\\'"] | ESC_SEQ | '\'"'  ;

fragment ESC_SEQ: '\\' [btnfr'\\];

fragment ESC_ILLEGAL: '\\' ~[btnfr'\\] | '\'' ~["] ;
