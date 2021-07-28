grammar CSEL;

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

program: decleration+ EOF;
decleration: varDecl | constDecl | functionDecl ;

exp: exp1 (STRINGPLUS | STRINGCOM ) exp1 | exp1 ;  

exp1: exp2 (EQUAL | NOTEQUAL | LESS | GREATER | LESSEQ | GREATEREQ ) exp2 | exp2 ;

exp2: exp2 (AND | OR) exp3 | exp3 ;

exp3: exp3 (ADD | SUB) exp4 | exp4 ;

exp4: exp4 (MUL | DIV | MOD) exp5 | exp5;

exp5: NOT exp5 | exp6 ;

exp6: SUB exp6 | exp7 ;

exp7:  exp8 (index | key) | exp8 ;

exp8: funcCall | exp9 ;

exp9: '(' exp ')' | operand ;

operand: funcCall | IdWithDollar | IdWithoutDollar | NUMBERLIT | STRINGLIT | boolean | json | array;

index: '[' expList ']' ;
key: ('{' exp '}')+ ;

varDecl: LET initVarDecl (',' initVarDecl)* ';' ;

constDecl: CONSTANT initConDecl (',' initConDecl)* ';' ;

initConDecl: IdWithDollar ('[' expList ']')? (':' typeLit)? ('=' exp) ;

initVarDecl: IdWithoutDollar ('[' expList ']')? (':' typeLit)? ('=' exp)? ;

typeLit: NUMBER | STRING | BOOLEAN | JSON ;

expList: exp (',' exp)* ;

// function decleration

functionDecl: FUNCTION IdWithoutDollar parameters '{' stmtList '}' ;

para:  IdWithoutDollar ('[' expList? ']')? ;

parameters: '(' (para (',' para)*)? ')' ;

//Assignment statement
assStmt: exp7 '=' exp ';';

// if else statement

ifElseStmt: IF '(' exp ')' '{' stmtList '}' elseIfStmt*? elseStmt? ;

elseIfStmt: ELIF '(' exp ')' '{' stmtList '}' ;

elseStmt: ELSE '{' stmtList '}';

// For statement

forIn: FOR IdWithoutDollar IN exp '{' stmtList '}' ;

forOf: FOR IdWithoutDollar OF exp '{' stmtList '}' ;

// While statement

whileStmt: WHILE '(' exp ')' '{' stmtList '}' ;

// Break statement

breakStmt: BREAK ';' ;

// Continue statement

continueStmt: CONTINUE ';' ;

// Call statement

callStmt: CALL '(' IdWithoutDollar  ',' '[' expList? ']' ')' ';' ;

// functionCall


funcCall: CALL '(' IdWithoutDollar  ',' '[' expList? ']' ')' ;

// return statement

returnStmt: RETURN (exp)? ';';

stmt: assStmt | ifElseStmt | forIn | forOf | whileStmt | breakStmt | continueStmt | callStmt | returnStmt | varDecl | constDecl ;

stmtList: stmt* ;

// Lexer Part
WS : [ \t\r\n]+ -> skip ; // skip spaces, tabs, newlines
// Comment

COMMENT: '##' .*? '##' -> skip;

// Identifier
IdWithDollar: '$'[a-z]([a-zA-Z0-9_])* ;
IdWithoutDollar: ([a-z])([a-zA-Z0-9_])* ;

// Keywords

BREAK: 'Break' ;
WHILE: 'While' ;
LET: 'Let' ;
NUMBER: 'Number' ;
CONSTANT: 'Constant' ;
CONTINUE: 'Continue' ;
FOR: 'For' ;
TRUE: 'True' ;
BOOLEAN: 'Boolean' ;
IF: 'If' ;
OF: 'Of' ;
FALSE: 'False' ;
STRING: 'String' ;
ELIF: 'Elif' ;
IN: 'In' ;
CALL: 'Call' ;
JSON: 'JSON' ;
ELSE: 'Else' ;
FUNCTION: 'Function' ;
RETURN: 'Return' ;
ARRAY: 'Array' ;

// Operators

ADD: '+' ;
SUB: '-' ;
MUL: '*' ;
DIV: '/' ;
MOD: '%' ;
NOT: '!' ;
AND: '&&' ;
OR: '||' ;
EQUAL: '==' ;
NOTEQUAL: '!=' ;
GREATER: '>' ;
LESS: '<' ;
GREATEREQ: '>=' ;
LESSEQ: '<=' ;
STRINGPLUS: '+.' ;
STRINGCOM: '==.' ;

// Seperators

SEPERATORS: '(' | ')' | '[' | ']' | ':' | '.' | ';' | '{' | '}' ;



fragment INTLIT: [0-9]+ ;

fragment INTPART: ['-']?INTLIT ;
fragment DECIMALPART: '.' INTLIT? ;
fragment EXPONENTPART: [eE][+-]? INTLIT ;

NUMBERLIT: INTPART | INTPART DECIMALPART | INTPART EXPONENTPART | INTPART DECIMALPART EXPONENTPART;

boolean: TRUE | FALSE ;

arrayElement: NUMBERLIT | STRINGLIT | boolean | json | array;

array: '[' arrayElement (',' arrayElement)* ']' ;

jsonElement: IdWithoutDollar ':' arrayElement;

json: '{' jsonElement (',' jsonElement)* '}' ;


STRINGLIT: '"' STRING_CHAR* '"'
    {
        y = str(self.text)
        self.text = y[1:-1]
    } ;

UNCLOSE_STRING: '"' STRING_CHAR* ( ESC_SEQ | '<EOF>' )?
    {
        y = str(self.text)
        raise UncloseString(y[1:])
    }
    ;


ILLEGAL_ESCAPE: '"' STRING_CHAR* ESC_ILLEGAL
    {
        raise IllegalEscape(self.text[1:])
    };

ERROR_CHAR: .
    {
        raise ErrorToken(self.text)
    };
UNTERMINATED_COMMENT: '##' .*?;

fragment STRING_CHAR: ~[\b\t\n\f\r\\'"] | ESC_SEQ | '\'"'  ;

fragment ESC_SEQ: '\\' [btnfr'\\];

fragment ESC_ILLEGAL: '\\' ~[btnfr'\\] | '\'' ~["] ;





