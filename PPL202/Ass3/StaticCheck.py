from abc import ABC, abstractmethod, ABCMeta
from dataclasses import dataclass
from typing import List, Tuple
from AST import *
from Visitor import *
from StaticError import *
from functools import *


class Type(ABC):
    __metaclass__ = ABCMeta
    pass


class Prim(Type):
    __metaclass__ = ABCMeta
    pass


class NumberType(Prim):
    pass


class StringType(Prim):
    pass


class BoolType(Prim):
    pass


class VoidType(Type):
    pass


# class NoneType(Type):
#   pass

# I added NoneType here!


class NoneType(Type):
    pass

# @dataclass
# class ArrayType(Type):
#     dimen: List[int]
#     eletype: Type

# It should be List[expr]?


@dataclass
class ArrayType(Type):
    dimen: List[int]
    eletype: Type


@dataclass
class MType:
    intype: List[Type]
    restype: Type


@dataclass
class Symbol:
    name: str
    mtype: Type


class StaticChecker(BaseVisitor):
    def __init__(self, ast):
        self.ast = ast
        self.global_envi = [
            Symbol("read", MType([], StringType())),
            Symbol("print", MType([StringType()], VoidType())),
            Symbol("printSLn", MType([StringType()], VoidType()))]

    def setTypeVariable(self, env, targetName, targetType):

        targetScope = None
        param = None
        for scopes in env:
            flag = False
            for decl in scopes:
                if decl.name == targetName and type(decl.mtype) != MType:
                    decl.mtype = targetType
                    targetScope = scopes
                    param = decl
                    flag = True
                    break
            if flag: break
        #Kiem tra bien co phai la parameter hay khong
        if targetScope == env[-3]:
            for decl in env[-1]:
                if type(decl.mtype) == MType and decl.name == env[-2][0].name:
                    if targetScope.index(param) + 1 <= len(decl.mtype.intype):
                        decl.mtype.intype[targetScope.index(param)] = param.mtype
                        break

    def check(self):
        return self.visit(self.ast, self.global_envi)

    def visitProgram(self, ast, c):
        names = list(map(lambda x: x.name, c))
        funcList = []
        globalScope = [c]
        for decl in ast.decl:
            if type(decl) == VarDecl:
                newDecl = self.visit(decl, globalScope)
                if newDecl.name in names:
                    raise Redeclared(Variable(), newDecl.name)
                names += [newDecl.name]
                globalScope[0] += [newDecl]

                continue

            if type(decl) == ConstDecl:
                newDecl = self.visit(decl, globalScope)
                if newDecl.name in names:
                    raise Redeclared(Constant(), newDecl.name)
                names += [newDecl.name]
                globalScope[0] += [newDecl]
                continue

            if type(decl) == FuncDecl:
                if decl.name.name in names:
                    raise Redeclared(Function(), decl.name.name)
                names += [decl.name.name]
            listParamType = list(map(lambda x: NoneType(), decl.param))
            globalScope[0] += [Symbol(decl.name.name, MType(listParamType, NoneType()))]
            funcList += [decl]

        if "main" not in names:
            raise NoEntryPoint()

        for funcDecl in funcList:
            self.visit(funcDecl, globalScope)

    def visitVarDecl(self,ast,c):
        if not ast.varDimen:
            if ast.varInit != None:
                typ = self.visit(ast.varInit, c)
                typInit = self.visit(ast.typ, c)
                if type(typInit) != NoneType and type(typ) != type(typInit):
                    raise TypeMismatchInStatement(ast)
            else:
                typ = self.visit(ast.typ, c)

            if type(typ) == ArrayType:
                raise TypeMismatchInStatement(ast)
            return Symbol(ast.variable.name,typ)          
        else: 
            if ast.varInit != None:
                typ = self.visit(ast.varInit, c)
                typInit = self.visit(ast.typ, c)
                if type(typInit) != NoneType and type(typ) != type(typInit):
                    raise TypeMismatchInStatement(ast)
            else:
                typ = self.visit(ast.typ, c)
            if type(typ) == NoneType:
                return Symbol(ast.variable.name, ArrayType(ast.varDimen,typ))
            elif type(typ) != ArrayType:
                raise TypeMismatchInStatement(ast)
            return Symbol(ast.variable.name,typ)

    def visitConstDecl(self,ast,c):
        if not ast.constDimen:
            typ = self.visit(ast.constInit,c)
            typInit = self.visit(ast.typ, c)
            if type(typInit) != NoneType and type(typ) != type(typInit):
                raise TypeMismatchInStatement(ast)
            if type(typ) == ArrayType:
                raise TypeMismatchInStatement(ast)
            return Symbol(ast.constant.name,typ)
        else: 
            typ = self.visit(ast.constInit,c)
            typInit = self.visit(ast.typ, c)
            if type(typInit) != NoneType and type(typ) != type(typInit):
                raise TypeMismatchInStatement(ast)          
            if type(typ) != ArrayType:
                raise TypeMismatchInStatement(ast)
            return Symbol(ast.constant.name,typ)

    def visitFuncDecl(self,ast,c):
        innerScope = [[]] + [[Symbol(ast.name.name,MType([],NoneType()))]] + c
        funcDecl = None
        for decl in innerScope[-1]:
            if decl.name == ast.name.name:
                funcDecl = decl
                break

        names = []
        listParamType = []
        for index in range(len(ast.param)):
            newDecl = self.visit(ast.param[index],innerScope)
            if newDecl.name in names:
                raise Redeclared(Parameter(),newDecl.name)
            names = names + [newDecl.name]
            if type(newDecl.mtype) == NoneType or type(newDecl.mtype)== NoneType:
                newDecl.mtype = funcDecl.mtype.intype[index]
            listParamType.append(newDecl.mtype)
            innerScope[0] = innerScope[0] + [newDecl]

        varList = []
        stmtList = []
        for decl in ast.body:
            if type(decl) == VarDecl:
                varList += [decl]
            else:
                stmtList += [decl]

        for var in varList:
            newDecl = self.visit(var,innerScope)
            if newDecl.name in names:
                raise Redeclared(Variable(),newDecl.name)
            names = names + [newDecl.name]
            innerScope[0] = innerScope[0] + [newDecl]

        listrestype = []
        for stmt in stmtList:
            listrestype += self.visit(stmt,innerScope)
            if type(funcDecl.mtype.restype) == NoneType and listrestype:
                if type(listrestype[0][0]) == NoneType:
                    raise TypeCannotBeInferred(listrestype[0][1])
                funcDecl.mtype.restype = listrestype[0][0]
        for restype in listrestype:
            if type(funcDecl.mtype.restype) != type(restype[0]):
                raise TypeMismatchInStatement(restype[1])

    def visitBinaryOp(self,ast,c):
        if ast.op in ['+.']:
        # except string type and return string type
            left = self.visit(ast.left, c)
            if type(ast.left) == CallExpr and type(left) == TypeCannotBeInferred:
                raise TypeCannotBeInferred(ast)
            typeLeft = type(left)
            if typeLeft == NoneType and type(ast.left) == CallExpr:
                for decl in c[-1]:
                    if decl.name == ast.left.method.name:
                        decl.mtype.restype = StringType()
                        break
                typeLeft = type(StringType())
            if typeLeft == NoneType and type(ast.left) == Id:
                self.setTypeVariable(c, ast.left.name, StringType())
                typeLeft = type(StringType())

            right = self.visit(ast.right, c)
            if type(ast.right) == CallExpr and type(right) == TypeCannotBeInferred:
                raise TypeCannotBeInferred(ast)
            typeRight = type(right)
            if typeRight == NoneType and type(ast.right) == CallExpr:
                for decl in c[-1]:
                    if decl.name == ast.right.method.name:
                        decl.mtype.restype = StringType()
                        break
                typeRight = type(StringType())
            if typeRight == NoneType and type(ast.right) == Id:
                self.setTypeVariable(c, ast.right.name, StringType())
                typeRight = type(StringType())

            if typeLeft != StringType or typeRight != StringType:
                raise TypeMismatchInExpression(ast)
            return StringType()         
        # if ast.op in ['==.']:
        # except string type and return bool type
        if ast.op in ['==.']:

            left = self.visit(ast.left, c)
            if type(ast.left) == CallExpr and type(left) == TypeCannotBeInferred:
                raise TypeCannotBeInferred(ast)
            typeLeft = type(left)
            if typeLeft == NoneType and type(ast.left) == CallExpr:
                for decl in c[-1]:
                    if decl.name == ast.left.method.name:
                        decl.mtype.restype = StringType()
                        break
                typeLeft = type(StringType())
            if typeLeft == NoneType and type(ast.left) == Id:
                self.setTypeVariable(c, ast.left.name, StringType())
                typeLeft = type(StringType())

            right = self.visit(ast.right, c)
            if type(ast.right) == CallExpr and type(right) == TypeCannotBeInferred:
                raise TypeCannotBeInferred(ast)
            typeRight = type(right)
            if typeRight == NoneType and type(ast.right) == CallExpr:
                for decl in c[-1]:
                    if decl.name == ast.right.method.name:
                        decl.mtype.restype = StringType()
                        break
                typeRight = type(StringType())
            if typeRight == NoneType and type(ast.right) == Id:
                self.setTypeVariable(c, ast.right.name, StringType())
                typeRight = type(StringType())

            if typeLeft != StringType or typeRight != StringType:
                raise TypeMismatchInExpression(ast)
            return BoolType()  

        # if ast.op in ['+','-','*','/','%']:
        # except number and return number type
        if ast.op in ['+','-','*','/','%']:

            left = self.visit(ast.left, c)
            if type(ast.left) == CallExpr and type(left) == TypeCannotBeInferred:
                raise TypeCannotBeInferred(ast)
            typeLeft = type(left)
            if typeLeft == NoneType and type(ast.left) == CallExpr:
                for decl in c[-1]:
                    if decl.name == ast.left.method.name:
                        decl.mtype.restype = NumberType()
                        break
                typeLeft = type(NumberType())
            if typeLeft == NoneType and type(ast.left) == Id:
                self.setTypeVariable(c, ast.left.name, NumberType())
                typeLeft = type(NumberType())

            right = self.visit(ast.right, c)
            if type(ast.right) == CallExpr and type(right) == TypeCannotBeInferred:
                # print('on here')
                raise TypeCannotBeInferred(ast)
            typeRight = type(right)
            if typeRight == NoneType and type(ast.right) == CallExpr:
                for decl in c[-1]:
                    if decl.name == ast.right.method.name:
                        decl.mtype.restype = NumberType()
                        break
                typeRight = type(NumberType())
            if typeRight == NoneType and type(ast.right) == Id:
                self.setTypeVariable(c, ast.right.name, NumberType())
                typeRight = type(NumberType())

            if typeLeft != NumberType or typeRight != NumberType:
                raise TypeMismatchInExpression(ast)
            return NumberType()         
        # if ast.op in ['==','!=','>','<','<=','>=']:
        #except number and return bool type
        if ast.op in ['==','!=','>','<','<=','>=']:

            left = self.visit(ast.left, c)
            if type(ast.left) == CallExpr and type(left) == TypeCannotBeInferred:
                raise TypeCannotBeInferred(ast)
            typeLeft = type(left)
            if typeLeft == NoneType and type(ast.left) == CallExpr:
                for decl in c[-1]:
                    if decl.name == ast.left.method.name:
                        decl.mtype.restype = NumberType()
                        break
                typeLeft = type(NumberType())
            if typeLeft == NoneType and type(ast.left) == Id:
                self.setTypeVariable(c, ast.left.name, NumberType())
                typeLeft = type(NumberType())

            right = self.visit(ast.right, c)
            if type(ast.right) == CallExpr and type(right) == TypeCannotBeInferred:
                raise TypeCannotBeInferred(ast)
            typeRight = type(right)
            if typeRight == NoneType and type(ast.right) == CallExpr:
                for decl in c[-1]:
                    if decl.name == ast.right.method.name:
                        decl.mtype.restype = NumberType()
                        break
                typeRight = type(NumberType())
            if typeRight == NoneType and type(ast.right) == Id:
                self.setTypeVariable(c, ast.right.name, NumberType())
                typeRight = type(NumberType())

            if typeLeft != NumberType or typeRight != NumberType:
                raise TypeMismatchInExpression(ast)
            return BoolType()       
        # if ast.op in ['&&', '||']:
        #except bool and return bool type
        if ast.op in ['&&', '||']:

            left = self.visit(ast.left, c)
            if type(ast.left) == CallExpr and type(left) == TypeCannotBeInferred:
                raise TypeCannotBeInferred(ast)
            typeLeft = type(left)
            if typeLeft == NoneType and type(ast.left) == CallExpr:
                for decl in c[-1]:
                    if decl.name == ast.left.method.name:
                        decl.mtype.restype = BoolType()
                        break
                typeLeft = type(BoolType())
            if typeLeft == NoneType and type(ast.left) == Id:
                self.setTypeVariable(c, ast.left.name, BoolType())
                typeLeft = type(BoolType())

            right = self.visit(ast.right, c)
            if type(ast.right) == CallExpr and type(right) == TypeCannotBeInferred:
                raise TypeCannotBeInferred(ast)
            typeRight = type(right)
            if typeRight == NoneType and type(ast.right) == CallExpr:
                for decl in c[-1]:
                    if decl.name == ast.right.method.name:
                        decl.mtype.restype = BoolType()
                        break
                typeRight = type(BoolType())
            if typeRight == NoneType and type(ast.right) == Id:
                self.setTypeVariable(c, ast.right.name, BoolType())
                typeRight = type(BoolType())

            if typeLeft != BoolType or typeRight != BoolType:
                raise TypeMismatchInExpression(ast)
            return BoolType()   

    def visitUnaryOp(self,ast,c):
        # if ast.op in ['!']:
        # except bool and return bool type
        if ast.op in ['!']:
            expr = self.visit(ast.body, c)
            if type(ast.body) == CallExpr and type(expr) == TypeCannotBeInferred:
                return TypeCannotBeInferred(ast)
            typexpr = type(expr)
            if type(ast.body) == CallExpr and typexpr == NoneType:
                for decl in param[-1]:
                    if decl.name == ast.body.method.name:
                        decl.mtype.restype = BoolType()
                        break
                typexpr = type(BoolType())
            if type(ast.body) == Id and typexpr == NoneType:
                self.setTypeVariable(c,ast.body.name,BoolType())
                typexpr = type(BoolType())
            if typexpr != BoolType:
                raise TypeMismatchInExpression(ast)
            return BoolType()
        # if ast.op in ['-']:
        # except number and return number type
        if ast.op in ['-']:
            expr = self.visit(ast.body, c)
            if type(ast.body) == CallExpr and type(expr) == TypeCannotBeInferred:
                return TypeCannotBeInferred(ast)
            typexpr = type(expr)
            if type(ast.body) == CallExpr and typexpr == NoneType:
                for decl in param[-1]:
                    if decl.name == ast.body.method.name:
                        decl.mtype.restype = NumberType()
                        break
                typexpr = type(NumberType())
            if type(ast.body) == Id and typexpr == NoneType:
                self.setTypeVariable(c, ast.body.name,NumberType())
                typexpr = type(NumberType())
            if typexpr != NumberType:
                raise TypeMismatchInExpression(ast)
            return NumberType()

    def visitId(self,ast,c):
        for scopes in c:
            for decl in scopes:
                if decl.name == ast.name and type(decl.mtype) != MType:
                    return decl.mtype
        raise Undeclared(Identifier(),ast.name)
        
    def visitAssign(self,ast,c):
        lhs = self.visit(ast.lhs, c)
        rhs = self.visit(ast.rhs, c)
        if type(lhs) == VoidType or type(rhs) == VoidType:
            raise TypeMismatchInStatement(ast)
        if type(rhs) == TypeCannotBeInferred:
            raise TypeCannotBeInferred(ast)
        if type(lhs) == NoneType and type(rhs) == NoneType:
            raise TypeCannotBeInferred(ast)
        elif type(lhs) == NoneType:
            self.setTypeVariable(c, ast.lhs.name, rhs)
        elif type(rhs) == NoneType:
            if type(ast.rhs) == Id:
                self.setTypeVariable(c, ast.rhs.name, lhs)
            elif type(ast.rhs) == CallExpr:
                for decl in c[-1]:
                    if decl.name == ast.rhs.method.name:
                        decl.mtype.restype = lhs
                        break
        else:
            if type(lhs) != type(rhs):
                raise TypeMismatchInStatement(ast)
        return []

    def visitCallStmt(self,ast,c):
        funcDecl = None
        for decl in c[-1]:
            if decl.name == ast.method.name:
                if type(decl.mtype) != MType:
                    raise Undeclared(Function(),decl.name)
                else:
                    funcDecl = decl
                    break
        if funcDecl == None:
            raise Undeclared(Function(),ast.method.name)
        if len(funcDecl.mtype.intype) != len(ast.param):
            raise TypeMismatchInStatement(ast)
        for i in range(len(ast.param)):
            typparam = self.visit(ast.param[i], c)
            if type(funcDecl.mtype.intype[i]) == NoneType and type(self.visit(ast.param[i], c)) == NoneType:
                raise TypeCannotBeInferred(ast)
            if type(funcDecl.mtype.intype[i]) == NoneType:
                funcDecl.mtype.intype[i] = self.visit(ast.param[i], c)

                if funcDecl.name == c[-2][0].name:
                    c[-3][i].mtype = funcDecl.mtype.intype[i]

            if type(typparam) == NoneType and type(ast.param[i])==Id:
                for scopes in c:
                    flag = False
                    for decl in scopes:
                        if type(decl.mtype) != MType and decl.name == ast.param[i].name:
                            decl.mtype = funcDecl.mtype.intype[i]
                            flag = True
                    if flag:
                        break
                typparam = funcDecl.mtype.intype[i]
                
            if type(typparam) == NoneType and type(ast.param[i]) == CallExpr:
                for decl in c[-1]:
                    if decl.name == ast.param[i].method.name:
                        decl.mtype.restype = funcDecl.mtype.intype[i]
                        break
                typparam = funcDecl.mtype.intype[i]
            if type(funcDecl.mtype.intype[i]) != type(typparam):
                raise TypeMismatchInStatement(ast)  
        # if type(funcDecl.mtype.restype) == NoneType:
        #   funcDecl.mtype.restype = VoidType()
        return []

    def visitBreak(self,ast,c):
        return []

    def visitContinue(self,ast,c):
        return []

    def visitReturn(self,ast,c):
        if ast.expr !=None:
            return [(self.visit(ast.expr, c),ast)]
        return [(VoidType(),ast)]


    def visitCallExpr(self,ast,c):
        funcDecl = None
        for decl in c[-1]:
            if decl.name == ast.method.name:
                if type(decl.mtype) != MType:
                    raise Undeclared(Function(), decl.name)
                else:
                    funcDecl = decl
                    break
        if funcDecl == None:
            raise Undeclared(Function(), ast.method.name)
        if len(funcDecl.mtype.intype) != len(ast.param):
            raise TypeMismatchInExpression(ast)

        for i in range(len(ast.param)):
            typparam = self.visit(ast.param[i], c)
            if type(funcDecl.mtype.intype[i]) == NoneType and type(typparam) == NoneType:
                # print('here')
                return TypeCannotBeInferred(ast)
            elif type(funcDecl.mtype.intype[i]) == NoneType:
                funcDecl.mtype.intype[i] = typparam
                if funcDecl.name == c[-2][0].name:
                    c[-3][i].mtype = funcDecl.mtype.intype[i]
            elif type(typparam) == NoneType and type(ast.param[i])==Id:
                for scopes in c:
                    flag = False
                    for decl in scopes:
                        if type(decl.mtype) != MType and decl.name == ast.param[i].name:
                            decl.mtype = funcDecl.mtype.intype[i]
                            flag = True
                    if flag:
                        break
                typparam = funcDecl.mtype.intype[i]
            elif type(typparam) == NoneType and type(ast.param[i]) == CallExpr:
                for decl in c[-1]:
                    if decl.name == ast.param[i].method.name:
                        decl.mtype.restype = funcDecl.mtype.intype[i]
                        break
                typparam = funcDecl.mtype.intype[i]
            if type(funcDecl.mtype.intype[i]) != type(typparam):
                raise TypeMismatchInExpression(ast)
        # print(funcDecl)
        return funcDecl.mtype.restype

    def visitArrayAccess(self,ast,c):
        arr = self.visit(ast.arr, c)
        idx = []
        for i in range(len(ast.idx)):
            idx += [self.visit(ast.idx[i], c)]
        if type(arr) != ArrayType: 
            raise TypeMismatchInExpression(ast)
        if len(idx) != len(arr.dimen): 
            raise TypeMismatchInExpression(ast)
        return arr.eletype

    def visitJSONAccess(self,ast,c):
        arr = self.visit(ast.arr, c)
        idx = []
        for i in range(len(ast.idx)):
            idx += [self.visit(ast.idx[i], c)]
        if type(arr) != JSONType: 
            raise TypeMismatchInExpression(ast)
        return arr.eletype

    def visitIf(self,ast,c):
        listRestype = []
        for ifstmt in ast.ifthenStmt:
            innerScope = [[]] + c
            typexpr = self.visit(ifstmt[0],innerScope)
            if type(typexpr) == NoneType and type(ifstmt[0]) == Id:
                self.setTypeVariable(c, ifstmt[0].name, BoolType())
                typexpr = BoolType()
            if type(ifstmt[0]) == CallExpr:
                if type(typexpr) == TypeCannotBeInferred:
                    raise TypeCannotBeInferred(ast)
                if type(typexpr) == NoneType:
                    for decl in innerScope[-1]:
                        if decl.name == ifstmt[0].method.name:
                            decl.mtype.restype = BoolType()
                            break
                    typexpr = BoolType()
            if type(typexpr) != BoolType:
                raise TypeMismatchInStatement(ast)
            names = []
            varList = []
            stmtList = []
            for decl in ifstmt[1]:
                if type(decl) == VarDecl:
                    varList += [decl]
                else:
                    stmtList += [decl]
            for var in varList:
                newDecl = self.visit(var, innerScope)
                if newDecl.name in names:
                    raise Redeclared(Variable(), newDecl.name)
                names.append(newDecl.name)
                innerScope[0] += [newDecl]
            for stmt in stmtList:
                listRestype += self.visit(stmt, innerScope)

        if ast.elseStmt:
            innerScope = [[]] + c
            names = []
            varList = []
            stmtList = []
            for decl in ifstmt[1]:
                if type(decl) == VarDecl:
                    varList += [decl]
                else:
                    stmtList += [decl]
            for var in varList:
                newDecl = self.visit(var, innerScope)
                if newDecl.name in names:
                    raise Redeclared(Variable(), newDecl.name)
                names.append(newDecl.name)
                innerScope[0] += [newDecl]
            for stmt in stmtList:
                listRestype += self.visit(stmt, innerScope)
    
        return listRestype

    def visitForIn(self,ast,c):
        # print(ast)
        listRestype = []
        if type(ast.idx1) != Id:
            raise TypeMismatchInStatement(ast)
        expr = self.visit(ast.expr, c)
        typexpr = type(expr)
        # print(typexpr)
        if typexpr != ArrayType:
            # print('here')
            raise TypeMismatchInStatement(ast)
        if ast.body != None:
            innerScope = [[]] + c
            names = []
            varList = []
            stmtList = []
            for decl in ast.body:
                if type(decl) == VarDecl:
                    varList += [decl]
                else:
                    stmtList += [decl]
            for var in varList:
                newDecl = self.visit(var, innerScope)
                if newDecl.name in names:
                    raise Redeclared(Variable(), newDecl.name)
                names.append(newDecl.name)
                innerScope[0] += [newDecl]
            for stmt in stmtList:
                listRestype += self.visit(stmt, innerScope)
    
        return listRestype

    def visitForOf(self,ast,c):
        listRestype = []
        if type(ast.idx1) != Id:
            raise TypeMismatchInStatement(ast)
        expr = self.visit(ast.expr, c)
        typexpr = type(expr)
        if typexpr != JSONType:
            raise TypeMismatchInStatement(ast)
        if ast.body != None:
            innerScope = [[]] + c
            names = []
            varList = []
            stmtList = []
            for decl in ast.body:
                if type(decl) == VarDecl:
                    varList += [decl]
                else:
                    stmtList += [decl]
            for var in varList:
                newDecl = self.visit(var, innerScope)
                if newDecl.name in names:
                    raise Redeclared(Variable(), newDecl.name)
                names.append(newDecl.name)
                innerScope[0] += [newDecl]
            for stmt in stmtList:
                listRestype += self.visit(stmt, innerScope)
    
        return listRestype

    def visitWhile(self,ast,c):
        listRestype = []
        exp = self.visit(ast.exp, c)
        typexp = type(exp)
        if type(ast.exp) == Id and typexp == NoneType:
            self.setTypeVariable(c, ast.exp.name, BoolType())
            typexp = type(BoolType())
        if type(ast.exp) == CallExpr:
            if type(exp) == TypeCannotBeInferred:
                raise TypeCannotBeInferred(ast)
            if type(exp) == NoneType:
                for decl in c[-1]:
                    if decl.name == ast.exp.method.name:
                        decl.mtype.restype = BoolType()
                        break
                typexp = type(BoolType())
        if typexp != BoolType:
            raise TypeMismatchInStatement(ast)  
        if ast.sl != None:
            innerScope = [[]] + c
            names = []
            varList = []
            stmtList = []
            for decl in ast.sl:
                if type(decl) == VarDecl:
                    varList += [decl]
                else:
                    stmtList += [decl]
            for var in varList:
                newDecl = self.visit(var, innerScope)
                if newDecl.name in names:
                    raise Redeclared(Variable(), newDecl.name)
                names.append(newDecl.name)
                innerScope[0] += [newDecl]
            for stmt in stmtList:
                listRestype += self.visit(stmt, innerScope)
    
        return listRestype
    
    def visitNumberLiteral(self, ast, c):
        return NumberType()

    def visitIntLiteral(self, ast, c):
        return NumberType()

    def visitBooleanLiteral(self, ast, c):
        return BoolType()
    
    def visitStringLiteral(self, ast, c):
        return StringType()

    def visitArrayLiteral(self, ast, c):
        return ArrayType([len(ast.value)],self.visit(ast.value[0],c))

    def visitJSONLiteral(self,ast,c):
        return JSONType()

    def visitNumberType(self, ast, c):
        return NumberType()
    
    def visitBooleanType(self, ast, c):
        return BoolType()
    
    def visitStringType(self, ast, c):
        return StringType()

    def visitJSONType(self, ast, c):
        return JSONType()

    def visitNoneType(self, ast, c):
        return NoneType()

    def visitVoidType(self,ast,c):
        return VoidType()





