#1711376
from CSELVisitor import CSELVisitor
from CSELParser import CSELParser
from AST import *
from functools import *


class ASTGeneration(CSELVisitor):
    def visitProgram(self, ctx: CSELParser.ProgramContext):
        return Program(list(reduce(lambda x, y: x+y, [self.visit(t) for t in ctx.decleration()], [])))

    def visitDeclaration(self, ctx: CSELParser.DeclerationContext):
        #decleration: varDecl | constDecl | functionDecleration ;
        return self.visit(ctx.getChild(0))

    def visitVarDecl(self, ctx: CSELParser.VarDeclContext):
        # varDecl: LET initVarDecl (',' initVarDecl)* ';' ;
        return list(map(lambda x: self.visit(x), ctx.initVarDecl()))
        # return [self.visit(x) for x in ctx.initVarDecl()]

    def visitInitVarDecl(self, ctx: CSELParser.InitVarDeclContext):
        # initVarDecl: IdWithoutDollar ('[' expList ']')? (':' typeLit)? ('=' exp)? ;

        dimen = self.visit(ctx.expList()) if ctx.expList() else []
        typ = self.visit(ctx.typeLit()) if ctx.typeLit() else NoneType()
        init = self.visit(ctx.exp()) if ctx.exp() else None
        return VarDecl(Id(ctx.IdWithoutDollar().getText()), dimen, typ, init)

    def visitConstDecl(self, ctx: CSELParser.ConstDeclContext):
        # constDecl: CONSTANT initConDecl (',' initConDecl)* ';' ;
        # return [self.visit(x) for x in ctx.initConDecl()]
        return list(map(lambda x: self.visit(x), ctx.initConDecl()))

    def visitInitConDecl(self, ctx: CSELParser.InitConDeclContext):
        # initConDecl: IdWithDollar ('[' expList ']')? (':' typeLit)? ('=' exp) ;
        dimen = self.visit(ctx.expList()) if ctx.expList() else []
        typ = self.visit(ctx.typeLit()) if ctx.typeLit() else NoneType()
        return ConstDecl(Id(ctx.IdWithDollar().getText()), dimen, typ, self.visit(ctx.exp()))

    def visitExpList(self,ctx: CSELParser.ExpListContext):
    	return list(map(lambda x: self.visit(x),ctx.exp()))

    def visitTypeLit(self, ctx: CSELParser.TypeLitContext):
        #typeLit: NUMBER | STRING | BOOLEAN | JSON ;
        if ctx.NUMBER():
            return NumberType()
        elif ctx.STRING():
            return StringType()
        elif ctx.BOOLEAN():
            return BooleanType()
        return JSONType()

    def visitFunctionDecl(self, ctx: CSELParser.FunctionDeclContext):
        # functionDecl: FUNCTION IdWithoutDollar parameters '{' varDecl* constDecl* stmtList '}' ;
        name = Id(ctx.IdWithoutDollar().getText())
        para = self.visit(ctx.parameters()) if ctx.parameters() else []
        body = self.visit(ctx.stmtList())
        return [FuncDecl(name, para, body)]
        # not sure why we need to return list, find out later on.

    def visitParameters(self, ctx: CSELParser.ParametersContext):
        # parameters: '(' (para (',' para)*)? ')' ;
        return list(map(lambda x: self.visit(x), ctx.para()))

    def visitPara(self, ctx: CSELParser.ParaContext):
        # para:  IdWithoutDollar ('[' (expList)? ']')? ;
        var = Id(ctx.IdWithoutDollar().getText())
        dimen = self.visit(ctx.expList()) if ctx.expList() else []
        return VarDecl(var, dimen, NoneType(), None)

    def visitArrayElement(self, ctx: CSELParser.ArrayElementContext):
        #arrayElement: NUMBERLIT | STRINGLIT | boolean | json | array;
        if ctx.NUMBERLIT():
            return NumberLiteral(float(ctx.NUMBERLIT().getText()))
        elif ctx.STRINGLIT():
            return StringLiteral(str(ctx.STRINGLIT().getText()))
        elif ctx.boolean():
            return BooleanLiteral(ctx.boolean().getText())
        elif ctx.json():
            return self.visit(ctx.json())
        elif ctx.array():
            return self.visit(ctx.array())

    def visitArray(self, ctx: CSELParser.ArrayContext):
        # array: '[' arrayElement (',' arrayElement)* ']' ;
        return ArrayLiteral(list(map(lambda x: self.visit(x), ctx.arrayElement())))

    def visitJson(self, ctx: CSELParser.JsonContext):
        # json: '{' jsonElement (',' jsonElement)* '}' ;
        jList = []
        for x in ctx.jsonElement():
            jList += self.visit(x)
        return JSONLiteral(jList)

    def visitJsonElement(self, ctx: CSELParser.JsonElementContext):
        # jsonElement: IdWithoutDollar ':' arrayElement;
        return [(Id(ctx.IdWithoutDollar().getText()), self.visit(ctx.arrayElement()))]

    def visitExp(self, ctx: CSELParser.ExpContext):
        # exp: exp1 (STRINGPLUS | STRINGCOM ) exp1 | exp1 ;
        if ctx.getChildCount() == 1:
            return self.visit(ctx.exp1(0))
        elif ctx.STRINGPLUS():
            return BinaryOp(ctx.STRINGPLUS().getText(), self.visit(ctx.exp1(0)), self.visit(ctx.exp1(1)))
        elif ctx.STRINGCOM():
            return BinaryOp(ctx.STRINGCOM().getText(), self.visit(ctx.exp1(0)), self.visit(ctx.exp1(1)))

    def visitExp1(self, ctx: CSELParser.Exp1Context):
        # exp1: exp2 (EQUAL | NOTEQUAL | LESS | GREATER | LESSEQ | GREATEREQ ) exp2 | exp2;

        if ctx.getChildCount() == 1:
            return self.visit(ctx.exp2(0))
        elif ctx.EQUAL():
            return BinaryOp(ctx.EQUAL().getText(), self.visit(ctx.exp2(0)), self.visit(ctx.exp2(1)))
        elif ctx.NOTEQUAL():
            return BinaryOp(ctx.NOTEQUAL().getText(), self.visit(ctx.exp2(0)), self.visit(ctx.exp2(1)))
        elif ctx.LESS():
            return BinaryOp(ctx.LESS().getText(), self.visit(ctx.exp2(0)), self.visit(ctx.exp2(1)))
        elif ctx.GREATER():
            return BinaryOp(ctx.GREATER().getText(), self.visit(ctx.exp2(0)), self.visit(ctx.exp2(1)))
        elif ctx.LESSEQ():
            return BinaryOp(ctx.LESSEQ().getText(), self.visit(ctx.exp2(0)), self.visit(ctx.exp2(1)))
        elif ctx.GREATEREQ():
            return BinaryOp(ctx.GREATEREQ().getText(), self.visit(ctx.exp2(0)), self.visit(ctx.exp2(1)))

    def visitExp2(self, ctx: CSELParser.Exp2Context):
        # exp2: exp2 (AND | OR) exp3 | exp3;

        if ctx.getChildCount() == 1:
            return self.visit(ctx.exp3())
        elif ctx.AND():
            return BinaryOp(ctx.AND().getText(), self.visit(ctx.exp2()), self.visit(ctx.exp3()))
        elif ctx.OR():
            return BinaryOp(ctx.OR().getText(), self.visit(ctx.exp2()), self.visit(ctx.exp3()))

    def visitExp3(self, ctx: CSELParser.Exp3Context):
        # exp3: exp3 (ADD | SUB) exp4 | exp4;
        if ctx.getChildCount() == 1:
            return self.visit(ctx.exp4())
        elif ctx.ADD():
            return BinaryOp(ctx.ADD().getText(), self.visit(ctx.exp3()), self.visit(ctx.exp4()))
        elif ctx.SUB():
            return BinaryOp(ctx.SUB().getText(), self.visit(ctx.exp3()), self.visit(ctx.exp4()))

    def visitExp4(self, ctx: CSELParser.Exp4Context):
        # exp4: exp4 (MUL | DIV | MOD) exp5 | exp5;
        if ctx.getChildCount() == 1:
            return self.visit(ctx.exp5())
        elif ctx.MUL():
            return BinaryOp(ctx.MUL().getText(), self.visit(ctx.exp4()), self.visit(ctx.exp5()))
        elif ctx.DIV():
            return BinaryOp(ctx.DIV().getText(), self.visit(ctx.exp4()), self.visit(ctx.exp5()))
        elif ctx.MOD():
            return BinaryOp(ctx.MOD().getText(), self.visit(ctx.exp4()), self.visit(ctx.exp5()))

    def visitExp5(self, ctx: CSELParser.Exp5Context):
        # exp5: NOT exp5 | exp6;
        if ctx.getChildCount() == 1:
            return self.visit(ctx.exp6())
        elif ctx.NOT():
            return UnaryOp(ctx.NOT().getText(), self.visit(ctx.exp5()))

    def visitExp6(self, ctx: CSELParser.Exp6Context):
        # exp6: SUB exp6 | exp7;
        if ctx.getChildCount() == 1:
            return self.visit(ctx.exp7())
        elif ctx.SUB():
            return UnaryOp(ctx.SUB().getText(), self.visit(ctx.exp6()))

    def visitExp7(self, ctx: CSELParser.Exp7Context):
        #exp7:  exp8 (index | key) | exp8 ;
        if ctx.getChildCount()==1:
            return self.visit(ctx.exp8())
        elif ctx.index():
            indexOp = self.visit(ctx.index())
            return ArrayAccess(self.visit(ctx.exp8()),indexOp) 
        keyOp = self.visit(ctx.key())
        return JSONAccess(self.visit(ctx.exp8()),keyOp)

    def visitIndex(self,ctx: CSELParser.IndexContext):
        #index: '[' expList ']' ;
        return self.visit(ctx.expList())

    def visitKey(self,ctx: CSELParser.KeyContext):
        #key: ('[' exp ']')+ ;
        llist=list(map(lambda x: self.visit(x),ctx.exp()))
        return llist


    def visitExp8(self, ctx: CSELParser.Exp8Context):
        #exp8: funcCall | exp9;
        if ctx.funcCall():
            return self.visit(ctx.funcCall())
        return self.visit(ctx.exp9())

    def visitExp9(self, ctx: CSELParser.Exp9Context):
        # exp9: '(' exp ')' | operand;
        if ctx.exp():
            return self.visit(ctx.exp())
        return self.visit(ctx.operand())

    def visitOperand(self, ctx: CSELParser.OperandContext):
        #operand: funcCall | IdWithDollar | IdWithoutDollar | NUMBERLIT | STRINGLIT | boolean | json | array;
        if ctx.funcCall():
            return self.visit(ctx.funcCall())
        elif ctx.IdWithDollar():
            return Id(ctx.IdWithDollar().getText())
        elif ctx.IdWithoutDollar():
            return Id(ctx.IdWithoutDollar().getText())
        elif ctx.NUMBERLIT():
            return NumberLiteral(float(ctx.NUMBERLIT().getText()))
        elif ctx.STRINGLIT():
            return StringLiteral(str(ctx.STRINGLIT().getText()))
        elif ctx.boolean():
            return BooleanLiteral(ctx.boolean().getText())
        elif ctx.json():
            return self.visit(ctx.json())
        elif ctx.array():
            return self.visit(ctx.array())

    def visitAssStmt(self, ctx: CSELParser.AssStmtContext):
        # assStmt: exp7 '=' exp ';';
        return Assign(self.visit(ctx.exp7()),self.visit(ctx.exp()))



    """ifElseStmt: IF '(' exp ')' '{' stmtList '}' elseIfStmt*? elseStmt? ;
       elseIfStmt: ELIF '(' exp ')' '{' stmtList '}' ;
       elseStmt: ELSE '{' stmtList '}';"""

    def visitIfElseStmt(self, ctx: CSELParser.IfElseStmtContext):
        exp = self.visit(ctx.exp())
        stmtList = self.visit(ctx.stmtList())
        ifList = [(exp, stmtList)]
        elseIf = [self.visit(x) for x in ctx.elseIfStmt()
                  ] if ctx.elseIfStmt() else []
        elseStmt = self.visit(ctx.elseStmt()) if ctx.elseStmt() else []
        return If(ifList+elseIf, elseStmt)

    def visitElseIfStmt(self, ctx: CSELParser.ElseIfStmtContext):
        exp = self.visit(ctx.exp())
        stmtList = self.visit(ctx.stmtList())
        return (exp, stmtList)

    def visitElseStmt(self, ctx: CSELParser.ElseStmtContext):
        return self.visit(ctx.stmtList())

    def visitForIn(self, ctx: CSELParser.ForInContext):
        # forIn: FOR IdWithoutDollar IN exp '{' stmtList '}' ;
        var = Id(ctx.IdWithoutDollar().getText())
        exp = self.visit(ctx.exp())
        body = self.visit(ctx.stmtList())
        return ForIn(var, exp, body)

    def visitForOf(self, ctx: CSELParser.ForOfContext):
        # forIn: FOR IdWithoutDollar OF exp '{' stmtList '}' ;
        var = Id(ctx.IdWithoutDollar().getText())
        exp = self.visit(ctx.exp())
        body = self.visit(ctx.stmtList())
        return ForOf(var, exp, body)

    def visitWhileStmt(self, ctx: CSELParser.WhileStmtContext):
        # whileStmt: WHILE '(' exp ')' '{' stmtList '}' ;
        exp = self.visit(ctx.exp())
        stmtList = self.visit(ctx.stmtList())
        return While(exp, stmtList)

    def visitBreakStmt(self, ctx: CSELParser.BreakStmtContext):
        # breakStmt: BREAK ';' ;
        return Break()

    def visitContinueStmt(self, ctx: CSELParser.ContinueStmtContext):
        # continueStmt: CONTINUE ';' ;
        return Continue()

    def visitReturnStmt(self, ctx: CSELParser.ReturnStmtContext):
        # returnStmt: RETURN (exp)? ';';
        exp = self.visit(ctx.exp()) if ctx.exp() else None
        return Return(exp)

    def visitCallStmt(self, ctx: CSELParser.CallStmtContext):
        # callStmt: CALL '(' IdWithoutDollar  ',' '[' expList? ']' ')' ';' ;
        name = Id(ctx.IdWithoutDollar().getText())
        llist = self.visit(ctx.expList()) if ctx.expList() else []
        return CallStmt(name, llist)

    def visitFuncCall(self, ctx: CSELParser.FuncCallContext):
        # funcCall: CALL '(' IdWithoutDollar  ',' '[' expList? ']' ')' ;
        name = Id(ctx.IdWithoutDollar().getText())
        llist = self.visit(ctx.expList()) if ctx.expList() else []
        return CallExpr(name, llist)

    def visitStmt(self, ctx: CSELParser.StmtContext):
        #stmt: assStmt | ifElseStmt | forIn | forOf | whileStmt | breakStmt | continueStmt
        # | callStmt | returnStmt | varDecl | constantDecl ;
        if ctx.assStmt():
            return self.visit(ctx.assStmt())
        elif ctx.ifElseStmt():
            return self.visit(ctx.ifElseStmt())
        elif ctx.forIn():
            return self.visit(ctx.forIn())
        elif ctx.forOf():
            return self.visit(ctx.forOf())
        elif ctx.whileStmt():
            return self.visit(ctx.whileStmt())
        elif ctx.breakStmt():
            return self.visit(ctx.breakStmt())
        elif ctx.continueStmt():
            return self.visit(ctx.continueStmt())
        elif ctx.callStmt():
            return self.visit(ctx.callStmt())
        elif ctx.returnStmt():
            return self.visit(ctx.returnStmt())
        elif ctx.varDecl():
            return self.visit(ctx.varDecl())[0]
        elif ctx.constDecl():
            return self.visit(ctx.constDecl())[0]

    def visitStmtList(self, ctx: CSELParser.StmtListContext):
        # stmtList: stmt* ;
        return list(map(lambda x: self.visit(x), ctx.stmt())) if ctx.stmt() else []
        # return [self.visit(x) for x in ctx.stmt()]
        
