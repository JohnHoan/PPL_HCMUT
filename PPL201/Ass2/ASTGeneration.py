from BKITVisitor import BKITVisitor
from BKITParser import BKITParser
from AST import *
from functools import*


class ASTGeneration(BKITVisitor):
    def visitProgram(self,ctx:BKITParser.ProgramContext):
        llist = []
        # if ctx.var_declare():
        #     for i in ctx.var_declare():
        #         llist = llist + self.visit(i)
        llist = reduce(lambda arr, ele: arr + self.visit(ele),ctx.var_declare(),[]) if ctx.var_declare() else []
        # if ctx.func_declare():
        #     for i in ctx.func_declare():
        #         llist = llist + self.visit(i)
        llist = (llist + reduce(lambda arr,ele: arr + self.visit(ele),ctx.func_declare(),[])) if ctx.func_declare() else llist

        return Program(llist)

    def visitVar_init(self, ctx:BKITParser.Var_initContext):
        if ctx.getChildCount() == 1:
            return VarDecl(Id(ctx.IDENTIFIER().getText()),[],None)
        if ctx.INTLIT():
            varDimen = [int(x.getText(),0) for x in ctx.INTLIT()]
            varInit = self.visit(ctx.array_element()) if ctx.array_element() else None
            return VarDecl(Id(ctx.IDENTIFIER().getText()),varDimen,varInit)
        else:
            return VarDecl(Id(ctx.IDENTIFIER().getText()),[],self.visit(ctx.array_element()))
    
    def visitVar_declare(self, ctx:BKITParser.Var_declareContext):
        return list(map(lambda x: self.visit(x),ctx.var_init()))
    
    def visitParam_element(self, ctx:BKITParser.Param_elementContext):
        if ctx.INTLIT():
            varDimen = [int(x.getText(),0) for x in ctx.INTLIT()]
            return VarDecl(Id(ctx.IDENTIFIER().getText()),varDimen,None)
        return VarDecl(Id(ctx.IDENTIFIER().getText()),[],None)

    def visitParam_list(self, ctx:BKITParser.Param_listContext):
        return list(map(lambda x: self.visit(x),ctx.param_element()))
    
    def visitFunc_declare(self, ctx:BKITParser.Func_declareContext):
        name = Id(ctx.IDENTIFIER().getText())
        lparam = self.visit(ctx.param_list()) if ctx.param_list() else []
        body = ([],[])
        if ctx.var_declare():
            res = []
            for i in ctx.var_declare():
                res += self.visit(i)
            body = (res,self.visit(ctx.stmt_list()))
        else:
            body = ([], self.visit(ctx.stmt_list()))
        return [FuncDecl(name,lparam,body)]
    
    
    def visitArray_element(self,ctx:BKITParser.Array_elementContext):
        if ctx.array():
            return self.visit(ctx.array())
        elif ctx.INTLIT():
            return IntLiteral(int(ctx.INTLIT().getText(),0))
        elif ctx.FLOATLIT():
            return FloatLiteral(float(ctx.FLOATLIT().getText()))
        elif ctx.STRINGLIT():
            return StringLiteral(str(ctx.STRINGLIT().getText()))
        elif ctx.BOOLLIT():
            return BooleanLiteral((ctx.BOOLLIT().getText()))  


    def visitArray(self, ctx:BKITParser.ArrayContext):
        return ArrayLiteral(list(map(lambda x: self.visit(x),ctx.array_element())))
    

    def visitExpr(self, ctx:BKITParser.ExprContext):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expr1(0))
        if ctx.GREATER_INT():
            return BinaryOp(ctx.GREATER_INT().getText(),self.visit(ctx.expr1(0)),self.visit(ctx.expr1(1)))
        if ctx.GREATER_EQ_INT():
            return BinaryOp(ctx.GREATER_EQ_INT().getText(),self.visit(ctx.expr1(0)),self.visit(ctx.expr1(1)))
        if ctx.LESS_INT():
            return BinaryOp(ctx.LESS_INT().getText(),self.visit(ctx.expr1(0)),self.visit(ctx.expr1(1)))
        if ctx.LESS_EQ_INT():
            return BinaryOp(ctx.LESS_EQ_INT().getText(),self.visit(ctx.expr1(0)),self.visit(ctx.expr1(1)))
        if ctx.EQ_INT():
            return BinaryOp(ctx.EQ_INT().getText(),self.visit(ctx.expr1(0)),self.visit(ctx.expr1(1)))
        if ctx.N_EQ_INT():
            return BinaryOp(ctx.N_EQ_INT().getText(),self.visit(ctx.expr1(0)),self.visit(ctx.expr1(1)))
        if ctx.GREATER_FLOAT():
            return BinaryOp(ctx.GREATER_FLOAT().getText(),self.visit(ctx.expr1(0)),self.visit(ctx.expr1(1)))
        if ctx.GREATER_EQ_FLOAT():
            return BinaryOp(ctx.GREATER_EQ_FLOAT().getText(),self.visit(ctx.expr1(0)),self.visit(ctx.expr1(1)))
        if ctx.LESS_FLOAT():
            return BinaryOp(ctx.LESS_FLOAT().getText(),self.visit(ctx.expr1(0)),self.visit(ctx.expr1(1)))
        if ctx.LESS_EQ_FLOAT():
            return BinaryOp(ctx.LESS_EQ_FLOAT().getText(),self.visit(ctx.expr1(0)),self.visit(ctx.expr1(1)))
        if ctx.EQ_FLOAT():
            return BinaryOp(ctx.EQ_FLOAT().getText(),self.visit(ctx.expr1(0)),self.visit(ctx.expr1(1)))

    def visitExpr1(self, ctx:BKITParser.Expr1Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expr2())
        if ctx.AND_OP():
            return BinaryOp(ctx.AND_OP().getText(),self.visit(ctx.expr1()),self.visit(ctx.expr2()))
        if ctx.OR_OP():
            return BinaryOp(ctx.OR_OP().getText(),self.visit(ctx.expr1()),self.visit(ctx.expr2()))


    
    def visitExpr2(self, ctx:BKITParser.Expr2Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expr3())
        if ctx.ADD_INT():
            return BinaryOp(ctx.ADD_INT().getText(),self.visit(ctx.expr2()),self.visit(ctx.expr3()))
        if ctx.ADD_FLOAT():
            return BinaryOp(ctx.ADD_FLOAT().getText(),self.visit(ctx.expr2()),self.visit(ctx.expr3()))
        if ctx.SUB_INT():
            return BinaryOp(ctx.SUB_INT().getText(),self.visit(ctx.expr2()),self.visit(ctx.expr3()))
        if ctx.SUB_FLOAT():
            return BinaryOp(ctx.SUB_FLOAT().getText(),self.visit(ctx.expr2()),self.visit(ctx.expr3()))
    
    def visitExpr3(self, ctx:BKITParser.Expr3Context):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.expr4())
        if ctx.MUL_INT():
            return BinaryOp(ctx.MUL_INT().getText(),self.visit(ctx.expr3()),self.visit(ctx.expr4()))
        if ctx.MUL_FLOAT():
            return BinaryOp(ctx.MUL_FLOAT().getText(),self.visit(ctx.expr3()),self.visit(ctx.expr4()))
        if ctx.DIV_INT():
            return BinaryOp(ctx.DIV_INT().getText(),self.visit(ctx.expr3()),self.visit(ctx.expr4()))
        if ctx.DIV_FLOAT():
            return BinaryOp(ctx.DIV_FLOAT().getText(),self.visit(ctx.expr3()),self.visit(ctx.expr4()))
        if ctx.REMAIN_INT():
            return BinaryOp(ctx.REMAIN_INT().getText(),self.visit(ctx.expr3()),self.visit(ctx.expr4()))


    def visitExpr4(self, ctx:BKITParser.Expr4Context):
        if ctx.expr5():
            return self.visit(ctx.expr5())
        return UnaryOp(ctx.NOT_OP().getText(), self.visit(ctx.expr4()))
    
    def visitExpr5(self, ctx:BKITParser.Expr5Context):
        if ctx.expr6():
            return self.visit(ctx.expr6())
        else:
            if ctx.SUB_INT():
                return UnaryOp(ctx.SUB_INT().getText(), self.visit(ctx.expr5()))
            return UnaryOp(ctx.SUB_FLOAT().getText(), self.visit(ctx.expr5()))
    
    

    """wrong here"""
    def visitExpr6(self, ctx:BKITParser.Expr6Context):
        if ctx.expr():
            llist = list(map(lambda x: self.visit(x),ctx.expr()))
            return ArrayCell(self.visit(ctx.expr7()),llist)
        return self.visit(ctx.expr7())

    
    def visitExpr7(self, ctx:BKITParser.Expr7Context):
        if ctx.func_call():
            return self.visit(ctx.func_call())
        return self.visit(ctx.expr8())
    
    def visitExpr8(self, ctx:BKITParser.Expr8Context):
        if ctx.operand():
            return self.visit(ctx.operand())
        return self.visit(ctx.expr())
    
    def visitOperand(self,ctx:BKITParser.OperandContext):
        if ctx.IDENTIFIER():
            return Id(ctx.IDENTIFIER().getText())
        elif ctx.INTLIT():
            return IntLiteral(int(ctx.INTLIT().getText(),0))
        elif ctx.FLOATLIT():
            return FloatLiteral(float(ctx.FLOATLIT().getText()))
        elif ctx.STRINGLIT():
            return StringLiteral(str(ctx.STRINGLIT().getText()))
        elif ctx.BOOLLIT():
            return BooleanLiteral((ctx.BOOLLIT().getText()))
        elif ctx.array():
            return self.visit(ctx.array())

    def visitBreak_stmt(self, ctx:BKITParser.Break_stmtContext):
        return Break()

    def visitContinue_stmt(self, ctx:BKITParser.Continue_stmtContext):
        return Continue()

    def visitReturn_stmt(self, ctx:BKITParser.Return_stmtContext):
        return Return(self.visit(ctx.expr())) if ctx.expr() else Return(None)

    def visitFunc_call(self, ctx:BKITParser.Func_callContext):
        llist = [self.visit(x) for x in ctx.expr()]
        return CallExpr(Id(ctx.IDENTIFIER().getText()),llist) if llist else CallExpr(Id(ctx.IDENTIFIER().getText()),[])

    def visitCall_stmt(self, ctx:BKITParser.Call_stmtContext):
        llist = [self.visit(x) for x in ctx.expr()]
        return CallStmt(Id(ctx.IDENTIFIER().getText()),llist) if llist else CallStmt(Id(ctx.IDENTIFIER().getText()),[])
    
    def visitAss_stmt(self, ctx:BKITParser.Ass_stmtContext):
        if ctx.IDENTIFIER():
            return Assign(Id(ctx.IDENTIFIER().getText()),self.visit(ctx.expr(0)))
        if ctx.expr7():
            llist = list(map(lambda x: self.visit(x),ctx.expr()))
            return Assign(ArrayCell(self.visit(ctx.expr7()),llist[:-1]),llist[-1])

    
    def visitIf_else_stmt(self, ctx:BKITParser.If_else_stmtContext):
        expr = self.visit(ctx.expr())
        varlist = []
        if ctx.var_declare():
            for i in ctx.var_declare():
                varlist = varlist + self.visit(i)

        stmtlist = self.visit(ctx.stmt_list())
        iflist = [(expr,varlist,stmtlist)]
        elseiflist = [self.visit(i) for i in ctx.else_if_stmt()] if ctx.else_if_stmt() else []
        elstmt = self.visit(ctx.else_stmt()) if ctx.else_stmt() else ([],[])
        return If(iflist+elseiflist,elstmt)

    def visitElse_if_stmt(self, ctx:BKITParser.Else_if_stmtContext):
        expr = self.visit(ctx.expr())
        varlist = []
        if ctx.var_declare():
            for i in ctx.var_declare():
                varlist = varlist + self.visit(i)

        stmtlist = self.visit(ctx.stmt_list())
        return (expr,varlist,stmtlist)


    def visitElse_stmt(self, ctx:BKITParser.Else_stmtContext):
        varlist = []
        if ctx.var_declare():
            for i in ctx.var_declare():
                varlist = varlist + self.visit(i)

        stmtlist = [self.visit(i) for i in ctx.stmt()]
        return (varlist,stmtlist)

    def visitFor_stmt(self, ctx:BKITParser.For_stmtContext):
        idx = Id(ctx.IDENTIFIER().getText())
        expr1 = self.visit(ctx.expr(0))
        expr2 = self.visit(ctx.expr(1))
        expr3 = self.visit(ctx.expr(2))
        var_list = []
        if ctx.var_declare():
            for i in ctx.var_declare():
                var_list = var_list + self.visit(i)
        loop = (var_list,self.visit(ctx.stmt_list()))
        return For(idx,expr1,expr2,expr3,loop)

    def visitWhile_stmt(self, ctx:BKITParser.While_stmtContext):
        expr = self.visit(ctx.expr())
        var_list = []
        if ctx.var_declare():
            for i in ctx.var_declare():
                var_list = var_list + self.visit(i)
        tup = (var_list,self.visit(ctx.stmt_list()))
        return While(expr,tup)

    def visitDo_while_stmt(self, ctx:BKITParser.Do_while_stmtContext):
        expr = self.visit(ctx.expr())
        var_list = []
        if ctx.var_declare():
            for i in ctx.var_declare():
                var_list = var_list + self.visit(i)
        tup = (var_list,self.visit(ctx.stmt_list()))
        return Dowhile(tup,expr)
    
    def visitStmt(self, ctx:BKITParser.StmtContext):
        if ctx.if_else_stmt():
            return self.visit(ctx.if_else_stmt())
        if ctx.while_stmt():
            return self.visit(ctx.while_stmt())
        if ctx.do_while_stmt():
            return self.visit(ctx.do_while_stmt())
        if ctx.ass_stmt():
            return self.visit(ctx.ass_stmt())
        if ctx.call_stmt():
            return self.visit(ctx.call_stmt())
        if ctx.return_stmt():
            return self.visit(ctx.return_stmt())
        if ctx.break_stmt():
            return self.visit(ctx.break_stmt())
        if ctx.continue_stmt():
            return self.visit(ctx.continue_stmt())
        if ctx.for_stmt():
            return self.visit(ctx.for_stmt())

    def visitStmt_list(self, ctx:BKITParser.Stmt_listContext):
        return list(map(lambda x: self.visit(x),ctx.stmt())) if ctx.stmt() else []     