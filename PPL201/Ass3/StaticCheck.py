
"""
 * @author nhphung
"""
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
class IntType(Prim):
    pass
class FloatType(Prim):
    pass
class StringType(Prim):
    pass
class BoolType(Prim):
    pass
class VoidType(Type):
    pass
class Unknown(Type):
    pass

@dataclass
class ArrayType(Type):
    dimen:List[int]
    eletype: Type

@dataclass
class MType:
    intype:List[Type]
    restype:Type

@dataclass
class Symbol:
    name: str
    mtype:Type

class StaticChecker(BaseVisitor):
    def __init__(self,ast):
        self.ast = ast
        self.global_envi = [
Symbol("int_of_float",MType([FloatType()],IntType())),
Symbol("float_of_int",MType([IntType()],FloatType())),
Symbol("int_of_string",MType([StringType()],IntType())),
Symbol("string_of_int",MType([IntType()],StringType())),
Symbol("float_of_string",MType([StringType()],FloatType())),
Symbol("string_of_float",MType([FloatType()],StringType())),
Symbol("bool_of_string",MType([StringType()],BoolType())),
Symbol("string_of_bool",MType([BoolType()],StringType())),
Symbol("read",MType([],StringType())),
Symbol("printLn",MType([],VoidType())),
Symbol("printStr",MType([StringType()],VoidType())),
Symbol("printStrLn",MType([StringType()],VoidType()))]

    def findAndSetTypeForVariable(self,environment,targetName,targetType):
        targetscopes = None
        param = None
        for scopes in environment:
            flag = False
            for decl in scopes:
                if decl.name == targetName and type(decl.mtype) != MType:
                    decl.mtype = targetType
                    targetscopes = scopes
                    param = decl
                    flag = True
                    break
            if flag: break
        #Kiem tra bien co phai la parameter hay khong
        if targetscopes == environment[-3]:
            for decl in environment[-1]:
                if type(decl.mtype) == MType and decl.name == environment[-2][0].name:
                    if targetscopes.index(param) + 1 <= len(decl.mtype.intype):
                        decl.mtype.intype[targetscopes.index(param)] = param.mtype
                        break

   
    def check(self):
        return self.visit(self.ast,self.global_envi)

    def visitProgram(self, ast, param):
        names =  list(map(lambda x: x.name,param))
        funclist = []
        globalscope = [param]
        for decl in ast.decl:
            if type(decl) == VarDecl:
                newdecl = self.visit(decl,globalscope)
                if newdecl.name in names:
                    raise Redeclared(Variable(),newdecl.name)
                names = names + [newdecl.name]
                globalscope[0] = globalscope[0] + [newdecl]
                continue
            if type(decl) == FuncDecl:
                if decl.name.name in names:
                    raise Redeclared(Function(),decl.name.name)
                names = names + [decl.name.name]
                lstparamtyp = list(map(lambda x: Unknown(),decl.param))
                globalscope[0] = globalscope[0] + [Symbol(decl.name.name,MType(lstparamtyp,Unknown()))]
                funclist = funclist + [decl]
        if "main" not in names:
            raise NoEntryPoint()
        for funcdecl in funclist:
            self.visit(funcdecl,globalscope)

    
    """wrong here"""
    def visitVarDecl(self, ast, param):
        if not ast.varDimen:
            typ = self.visit(ast.varInit,param) if ast.varInit != None else Unknown()
            if type(typ) == ArrayType:
                raise TypeMismatchInStatement(ast)
            return Symbol(ast.variable.name,typ)
        else:
            typ = self.visit(ast.varInit,param) if ast.varInit != None else Unknown()
            if type(typ) == Unknown:
                return Symbol(ast.variable.name,ArrayType(ast.varDimen,typ))
            elif type(typ) != ArrayType:
                raise TypeMismatchInStatement(ast)
            return Symbol(ast.variable.name,typ)
    
    """wrong here"""
    def visitFuncDecl(self, ast, param):
        innerscope = [[]] + [[Symbol(ast.name.name,MType([],Unknown()))]] + param
        fdecl = None
        for decl in innerscope[-1]:
            if decl.name == ast.name.name:
                fdecl = decl
                break
        #innerscope[1] = innerscope[1] + [Symbol(ast.name.name,MType([],Unknown()))]
        #innerscope[0] = 
        names = []
        listParamType = []
        for index in range(len(ast.param)):
            newdecl = self.visit(ast.param[index],innerscope)
            if newdecl.name in names:
                raise Redeclared(Parameter(),newdecl.name)
            names = names + [newdecl.name]
            if type(newdecl.mtype) == Unknown:
                newdecl.mtype = fdecl.mtype.intype[index]
            listParamType.append(newdecl.mtype)
            innerscope[0] = innerscope[0] + [newdecl]


        for vardecl in ast.body[0]:
            newdecl = self.visit(vardecl,innerscope)
            if newdecl.name in names:
                raise Redeclared(Variable(),newdecl.name)
            names = names + [newdecl.name]
            innerscope[0] = innerscope[0] + [newdecl]

        funcdecl = None
        for decl in innerscope[-1]:
            if decl.name == ast.name.name:
                funcdecl = decl
                break

        #funcdecl = None
        listrestype = []
        for stmt in ast.body[1]:
            listrestype = listrestype + self.visit(stmt,innerscope)
            if type(funcdecl.mtype.restype) == Unknown and listrestype:
                if type(listrestype[0][0]) == Unknown:
                    raise TypeCannotBeInferred(listrestype[0][1])
                funcdecl.mtype.restype = listrestype[0][0]

        for restype in listrestype:
            if type(funcdecl.mtype.restype) != type(restype[0]):
                raise TypeMismatchInStatement(restype[1])
    
    def visitBinaryOp(self, ast, param):
        if ast.op in ["+","-","*","\\","%"]:
            left = self.visit(ast.left,param)
            if type(ast.left) == CallExpr and type(left) == TypeCannotBeInferred:
                return TypeCannotBeInferred(ast)
            typleft = type(left)
            if typleft == Unknown and type(ast.left) == CallExpr:
                for decl in param[-1]:
                    if decl.name == ast.left.method.name:
                        decl.mtype.restype = IntType()
                        break
                typleft = type(IntType())
            if typleft == Unknown and type(ast.left) == Id:
                self.findAndSetTypeForVariable(param,ast.left.name,IntType())
                typleft = type(IntType())
            
            right = self.visit(ast.right,param)
            if type(ast.right) == CallExpr and type(right) == TypeCannotBeInferred:
                return TypeCannotBeInferred(ast)
            typright = type(right)
            if typright == Unknown and type(ast.right) == CallExpr:
                for decl in param[-1]:
                    if decl.name == ast.right.method.name:
                        decl.mtype.restype = IntType()
                        break
                typright = type(IntType())
            if typright == Unknown and type(ast.right) == Id:
                self.findAndSetTypeForVariable(param,ast.right.name,IntType())
                typright = type(IntType())
            
            if typleft != IntType or typright != IntType:
                raise TypeMismatchInExpression(ast)
            return IntType()

        if ast.op in ["+.","-.","*.","\\."]:
            left = self.visit(ast.left,param)
            if type(ast.left) == CallExpr and type(left) == TypeCannotBeInferred:
                return TypeCannotBeInferred(ast)
            typleft = type(left)
            if typleft == Unknown and type(ast.left) == CallExpr:
                for decl in param[-1]:
                    if decl.name == ast.left.method.name:
                        decl.mtype.restype = FloatType()
                        break
                typleft = type(FloatType())
            if typleft == Unknown and type(ast.left) == Id:
                self.findAndSetTypeForVariable(param,ast.left.name,FloatType())
                typleft = type(FloatType())
            
            right = self.visit(ast.right,param)
            if type(ast.right) == CallExpr and type(right) == TypeCannotBeInferred:
                return TypeCannotBeInferred(ast)
            typright = type(right)
            if typright == Unknown and type(ast.right) == CallExpr:
                for decl in param[-1]:
                    if decl.name == ast.right.method.name:
                        decl.mtype.restype = FloatType()
                        break
                typright = type(FloatType())
            if typright == Unknown and type(ast.right) == Id:
                self.findAndSetTypeForVariable(param,ast.right.name,FloatType())
                typright = type(FloatType())
            
            if typleft != FloatType or typright != FloatType:
                raise TypeMismatchInExpression(ast)
            return FloatType()

        if ast.op in ["==","!=","<",">",">=","<="]:
            left = self.visit(ast.left,param)
            if type(ast.left) == CallExpr and type(left) == TypeCannotBeInferred:
                return TypeCannotBeInferred(ast)
            typleft = type(left)
            if typleft == Unknown and type(ast.left) == CallExpr:
                for decl in param[-1]:
                    if decl.name == ast.left.method.name:
                        decl.mtype.restype = IntType()
                        break
                typleft = type(IntType())
            if typleft == Unknown and type(ast.left) == Id:
                self.findAndSetTypeForVariable(param,ast.left.name,IntType())
                typleft = type(IntType())
            
            right = self.visit(ast.right,param)
            if type(ast.right) == CallExpr and type(right) == TypeCannotBeInferred:
                return TypeCannotBeInferred(ast)
            typright = type(right)
            if typright == Unknown and type(ast.right) == CallExpr:
                for decl in param[-1]:
                    if decl.name == ast.right.method.name:
                        decl.mtype.restype = IntType()
                        break
                typright = type(IntType())
            if typright == Unknown and type(ast.right) == Id:
                self.findAndSetTypeForVariable(param,ast.right.name,IntType())
                typright = type(IntType())
            
            if typleft != IntType or typright != IntType:
                raise TypeMismatchInExpression(ast)
            return BoolType()

        if ast.op in [">.","<.","*>=.","<=.","=/="]:
            left = self.visit(ast.left,param)
            if type(ast.left) == CallExpr and type(left) == TypeCannotBeInferred:
                return TypeCannotBeInferred(ast)
            typleft = type(left)
            if typleft == Unknown and type(ast.left) == CallExpr:
                for decl in param[-1]:
                    if decl.name == ast.left.method.name:
                        decl.mtype.restype = FloatType()
                        break
                typleft = type(FloatType())
            if typleft == Unknown and type(ast.left) == Id:
                self.findAndSetTypeForVariable(param,ast.left.name,FloatType())
                typleft = type(FloatType())

            right = self.visit(ast.right,param)
            if type(ast.right) == CallExpr and type(right) == TypeCannotBeInferred:
                return TypeCannotBeInferred(ast)
            typright = type(right)
            if typright == Unknown and type(ast.right) == CallExpr:
                for decl in param[-1]:
                    if decl.name == ast.right.method.name:
                        decl.mtype.restype = FloatType()
                        break
                typright = type(FloatType())
            if typright == Unknown and type(ast.right) == Id:
                self.findAndSetTypeForVariable(param,ast.right.name,FloatType())
                typright = type(FloatType())
            
            if typleft != FloatType or typright != FloatType:
                raise TypeMismatchInExpression(ast)
            return BoolType()
        
        if ast.op in ["||","&&"]:
            left = self.visit(ast.left,param)
            if type(ast.left) == CallExpr and type(left) == TypeCannotBeInferred:
                return TypeCannotBeInferred(ast)
            typleft = type(left)
            if typleft == Unknown and type(ast.left) == CallExpr:
                for decl in param[-1]:
                    if decl.name == ast.left.method.name:
                        decl.mtype.restype = BoolType()
                        break
                typleft = type(BoolType())
            if typleft == Unknown and type(ast.left) == Id:
                self.findAndSetTypeForVariable(param,ast.left.name,BoolType())
                typleft = type(BoolType())

            right = self.visit(ast.right,param)
            if type(ast.right) == CallExpr and type(right) == TypeCannotBeInferred:
                return TypeCannotBeInferred(ast)
            typright = type(right)
            if typright == Unknown and type(ast.right) == CallExpr:
                for decl in param[-1]:
                    if decl.name == ast.right.method.name:
                        decl.mtype.restype = BoolType()
                        break
                typright = type(BoolType())
            if typright == Unknown and type(ast.right) == Id:
                self.findAndSetTypeForVariable(param,ast.right.name,BoolType())
                typright = type(BoolType())
            
            if typleft != BoolType or typright != BoolType:
                raise TypeMismatchInExpression(ast)
            return BoolType()
    
    def visitUnaryOp(self, ast, param):
        if ast.op in ["-"]:
            expr = self.visit(ast.body,param)
            if type(ast.body) == CallExpr and type(expr) == TypeCannotBeInferred:
                return TypeCannotBeInferred(ast)
            typexpr = type(expr)
            if type(ast.body) == CallExpr and typexpr == Unknown:
                for decl in param[-1]:
                    if decl.name == ast.body.method.name:
                        decl.mtype.restype = IntType()
                        break
                typexpr = type(IntType())
            if type(ast.body) == Id and typexpr == Unknown:
                self.findAndSetTypeForVariable(param,ast.body.name,IntType())
                typexpr = type(IntType())
            if typexpr != IntType:
                raise TypeMismatchInExpression(ast)
            return IntType()
        if ast.op in ["-."]:
            expr = self.visit(ast.body,param)
            if type(ast.body) == CallExpr and type(expr) == TypeCannotBeInferred:
                return TypeCannotBeInferred(ast)
            typexpr = type(expr)
            if type(ast.body) == CallExpr and typexpr == Unknown:
                for decl in param[-1]:
                    if decl.name == ast.body.method.name:
                        decl.mtype.restype = FloatType()
                        break
                typexpr = type(FloatType())
            if type(ast.body) == Id and typexpr == Unknown:
                self.findAndSetTypeForVariable(param,ast.body.name,FloatType())
                typexpr = type(FloatType())
            if typexpr != FloatType:
                raise TypeMismatchInExpression(ast)
            return FloatType()
        if ast.op in ["!"]:
            expr = self.visit(ast.body,param)
            if type(ast.body) == CallExpr and type(expr) == TypeCannotBeInferred:
                return TypeCannotBeInferred(ast)
            typexpr = type(expr)
            if type(ast.body) == CallExpr and typexpr == Unknown:
                for decl in param[-1]:
                    if decl.name == ast.body.method.name:
                        decl.mtype.restype = BoolType()
                        break
                typexpr = type(BoolType())
            if type(ast.body) == Id and typexpr == Unknown:
                self.findAndSetTypeForVariable(param,ast.body.name,BoolType())
                typexpr = type(BoolType())
            if typexpr != BoolType:
                raise TypeMismatchInExpression(ast)
            return BoolType()
    
    def visitCallExpr(self, ast, param):
        funcdecl = None
        for decl in param[-1]:
            if decl.name == ast.method.name:
                if type(decl.mtype) != MType:
                    raise Undeclared(Function(),decl.name)
                else:
                    funcdecl = decl
                    break
        if funcdecl == None:
            raise Undeclared(Function(),ast.method.name)
        if len(funcdecl.mtype.intype) != len(ast.param):
            raise TypeMismatchInExpression(ast)

        for i in range(len(ast.param)):
            typparam = self.visit(ast.param[i],param)
            if type(funcdecl.mtype.intype[i]) == Unknown and type(typparam) == Unknown:
                return TypeCannotBeInferred(ast)
            elif type(funcdecl.mtype.intype[i]) == Unknown:
                funcdecl.mtype.intype[i] = typparam
                if funcdecl.name == param[-2][0].name:
                    param[-3][i].mtype = funcdecl.mtype.intype[i]
            elif type(typparam) == Unknown and type(ast.param[i])==Id:
                for scopes in param:
                    flag = False
                    for decl in scopes:
                        if type(decl.mtype) != MType and decl.name == ast.param[i].name:
                            decl.mtype = funcdecl.mtype.intype[i]
                            flag = True
                    if flag:
                        break
                typparam = funcdecl.mtype.intype[i]
            elif type(typparam) == Unknown and type(ast.param[i]) == CallExpr:
                for decl in param[-1]:
                    if decl.name == ast.param[i].method.name:
                        decl.mtype.restype = funcdecl.mtype.intype[i]
                        break
                typparam = funcdecl.mtype.intype[i]
            if type(funcdecl.mtype.intype[i]) != type(typparam):
                raise TypeMismatchInExpression(ast)
        return funcdecl.mtype.restype
    
    def visitId(self, ast, param):
        for scopes in param:
            for decl in scopes:
                if decl.name == ast.name and type(decl.mtype) != MType:
                    return decl.mtype
        raise Undeclared(Identifier(),ast.name)
    
    def visitArrayCell(self, ast, param):
        return None
    
    def visitAssign(self, ast, param):
        rhs = self.visit(ast.rhs,param)
        lhs = self.visit(ast.lhs,param)
        if type(lhs) == VoidType or type(rhs) == VoidType:
            raise TypeMismatchInStatement(ast)
        if type(rhs) == TypeCannotBeInferred:
            raise TypeCannotBeInferred(ast)
        if type(lhs) == Unknown and type(rhs) == Unknown:
            raise TypeCannotBeInferred(ast)
        elif type(lhs) == Unknown:
            self.findAndSetTypeForVariable(param,ast.lhs.name,rhs)
        elif type(rhs) == Unknown:
            if type(ast.rhs) == Id:
                self.findAndSetTypeForVariable(param,ast.rhs.name,lhs)
            elif type(ast.rhs) == CallExpr:
                for decl in param[-1]:
                    if decl.name == ast.rhs.method.name:
                        decl.mtype.restype = lhs
                        break
        else:
            if type(lhs) != type(rhs):
                raise TypeMismatchInStatement(ast)

        return []

    
    def visitIf(self, ast, param):
        listrestype = []
        for ifstmt in ast.ifthenStmt:
            innerscope = [[]] + param
            typexpr = self.visit(ifstmt[0],innerscope)
            if type(typexpr) == Unknown and type(ifstmt[0]) == Id:
                self.findAndSetTypeForVariable(param,ifstmt[0].name,BoolType())
                typexpr = BoolType()
            if type(ifstmt[0]) == CallExpr:
                if type(typexpr) == TypeCannotBeInferred:
                    raise TypeCannotBeInferred(ast)
                if type(typexpr) == Unknown:
                    for decl in innerscope[-1]:
                        if decl.name == ifstmt[0].method.name:
                            decl.mtype.restype = BoolType()
                            break
                    typexpr = BoolType()
            if type(typexpr) != BoolType:
                raise TypeMismatchInStatement(ast)
            names = []
            for vardecl in ifstmt[1]:
                newdecl = self.visit(vardecl,innerscope)
                if newdecl.name in names:
                    raise Redeclared(Variable(),newdecl.name)
                names.append(newdecl.name)
                innerscope[0] = innerscope[0] + [newdecl]
            for stmt in ifstmt[2]:
                listrestype = listrestype + self.visit(stmt,innerscope)
        if ast.elseStmt:
            innerscope = [[]] + param
            names = []
            for vardecl in ast.elseStmt[0]:
                newdecl = self.visit(vardecl,innerscope)
                if newdecl.name in names:
                    raise Redeclared(Variable(),newdecl.name)
                names.append(newdecl.name)
                innerscope[0] = innerscope[0] + [newdecl]
            for stmt in ast.elseStmt[1]:
                listrestype = listrestype + self.visit(stmt,innerscope)
    
        return listrestype
                
    
    def visitFor(self, ast, param):
        idx1 = self.visit(ast.idx1,param)
        typidx1 = type(idx1)
        if type(ast.idx1) == Id and typidx1 == Unknown:
            self.findAndSetTypeForVariable(param,ast.idx1.name,IntType())
            typidx1 = type(IntType())
        if typidx1 != IntType:
            raise TypeMismatchInStatement(ast)
        
        expr1 = self.visit(ast.expr1,param)
        typexpr1 = type(expr1)
        if type(ast.expr1) == Id and typexpr1 == Unknown:
            self.findAndSetTypeForVariable(param,ast.expr1.name,IntType())
            typexpr1 = type(IntType())
        if type(ast.expr1) == CallExpr:
            if type(expr1) == TypeCannotBeInferred:
                raise TypeCannotBeInferred(ast)
            if type(expr1) == Unknown:
                for decl in param[-1]:
                    if decl.name == ast.expr1.method.name:
                        decl.mtype.restype = IntType()
                        break
                typexpr1 = type(IntType())
        if typexpr1 != IntType:
            raise TypeMismatchInStatement(ast)

        expr2 = self.visit(ast.expr2,param)
        typexpr2 = type(expr2)
        if type(ast.expr2) == Id and typexpr2 == Unknown:
            self.findAndSetTypeForVariable(param,ast.expr2.name,BoolType())
            typexpr2 = type(BoolType())
        if type(ast.expr2) == CallExpr:
            if type(expr2) == TypeCannotBeInferred:
                raise TypeCannotBeInferred(ast)
            if type(expr2) == Unknown:
                for decl in param[-1]:
                    if decl.name == ast.expr2.method.name:
                        decl.mtype.restype = BoolType()
                        break
                typexpr2 = type(BoolType())
        if typexpr2 != BoolType:
            raise TypeMismatchInStatement(ast)

        expr3 = self.visit(ast.expr3,param)
        typexpr3 = type(expr3)
        if type(ast.expr3) == Id and typexpr3 == Unknown:
            self.findAndSetTypeForVariable(param,ast.expr2.name,IntType())
            typexpr3 = type(IntType())
        if type(ast.expr3) == CallExpr:
            if type(expr3) == TypeCannotBeInferred:
                raise TypeCannotBeInferred(ast)
            if type(expr3) == Unknown:
                for decl in param[-1]:
                    if decl.name == ast.expr3.method.name:
                        decl.mtype.restype = IntType()
                        break
                typexpr3 = type(IntType())
        if typexpr3 != IntType:
            raise TypeMismatchInStatement(ast)
        
        innerscope = [[]] + param
        names = []
        for vardecl in ast.loop[0]:
            newdecl = self.visit(vardecl,innerscope)
            if newdecl in names:
                raise Redeclared(Variable(),newdecl.name)
            names.append(newdecl.name)
            innerscope[0] = innerscope[0] + [newdecl]
        listrestype = []
        for stmt in ast.loop[1]:
            listrestype = listrestype + self.visit(stmt,innerscope)
        return listrestype

    
    def visitContinue(self, ast, param):
        return []
    
    def visitBreak(self, ast, param):
        return []
    
    def visitReturn(self, ast, param):
        return [(VoidType(),ast)] if ast.expr == None else [(self.visit(ast.expr,param),ast)]
    
    def visitDowhile(self, ast, param):
        innerscope = [[]] + param
        names = []
        for vardecl in ast.sl[0]:
            newdecl = self.visit(vardecl,innerscope)
            if newdecl in names:
                raise Redeclared(Variable(),newdecl.name)
            names.append(newdecl.name)
            innerscope[0] = innerscope[0] + [newdecl]
        listrestype = []
        for stmt in ast.sl[1]:
            listrestype = listrestype + self.visit(stmt,innerscope)
        for funcdecl in param[-1]:
            if funcdecl.name == param[-2][0].name and listrestype:
                if type(funcdecl.mtype.restype) == Unknown:
                    if type(listrestype[0][0]) != Unknown:
                        funcdecl.mtype.restype = listrestype[0][0]
                    if type(listrestype[0][0]) == Unknown:
                        raise TypeCannotBeInferred(listrestype[0][1])
                    break

        exp = self.visit(ast.exp,param)
        typexp = type(exp)
        if type(ast.exp) == Id and typexp == Unknown:
            self.findAndSetTypeForVariable(param,ast.exp.name,BoolType())
            typexp = type(BoolType())
        if type(ast.exp) == CallExpr:
            if type(exp) == TypeCannotBeInferred:
                raise TypeCannotBeInferred(ast)
            if type(exp) == Unknown:
                for decl in innerscope[-1]:
                    if decl.name == ast.exp.method.name:
                        decl.mtype.restype = BoolType()
                        break
                typexp = type(BoolType())
        if typexp != BoolType:
            raise TypeMismatchInStatement(ast)
        return listrestype

    def visitWhile(self, ast, param):
        exp = self.visit(ast.exp,param)
        typexp = type(exp)
        if type(ast.exp) == Id and typexp == Unknown:
            self.findAndSetTypeForVariable(param,ast.exp.name,BoolType())
            typexp = type(BoolType())
        if type(ast.exp) == CallExpr:
            if type(exp) == TypeCannotBeInferred:
                raise TypeCannotBeInferred(ast)
            if type(exp) == Unknown:
                for decl in param[-1]:
                    if decl.name == ast.exp.method.name:
                        decl.mtype.restype = BoolType()
                        break
                typexp = type(BoolType())
        if typexp != BoolType:
            raise TypeMismatchInStatement(ast)
        
        innerscope = [[]] + param
        names = []
        for vardecl in ast.sl[0]:
            newdecl = self.visit(vardecl,innerscope)
            if newdecl in names:
                raise Redeclared(Variable(),newdecl.name)
            names.append(newdecl.name)
            innerscope[0] = innerscope[0] + [newdecl]
        listrestype = []
        for stmt in ast.sl[1]:
            listrestype = listrestype + self.visit(stmt,innerscope)
        return listrestype

    def visitCallStmt(self, ast, param):
        funcdecl = None
        for decl in param[-1]:
            if decl.name == ast.method.name:
                if type(decl.mtype) != MType:
                    raise Undeclared(Function(),decl.name)
                else:
                    funcdecl = decl
                    break
        if funcdecl == None:
            raise Undeclared(Function(),ast.method.name)
        if len(funcdecl.mtype.intype) != len(ast.param):
            raise TypeMismatchInStatement(ast)
        for i in range(len(ast.param)):
            typparam = self.visit(ast.param[i],param)
            if type(funcdecl.mtype.intype[i]) == Unknown and type(self.visit(ast.param[i],param)) == Unknown:
                raise TypeCannotBeInferred(ast)
            if type(funcdecl.mtype.intype[i]) == Unknown:
                funcdecl.mtype.intype[i] = self.visit(ast.param[i],param)
                if funcdecl.name == param[-2][0].name:
                    param[-3][i].mtype = funcdecl.mtype.intype[i]
            elif type(typparam) == Unknown and type(ast.param[i])==Id:
                for scopes in param:
                    flag = False
                    for decl in scopes:
                        if type(decl.mtype) != MType and decl.name == ast.param[i].name:
                            decl.mtype = funcdecl.mtype.intype[i]
                            flag = True
                    if flag:
                        break
                typparam = funcdecl.mtype.intype[i]
            elif type(typparam) == Unknown and type(ast.param[i]) == CallExpr:
                for decl in param[-1]:
                    if decl.name == ast.param[i].method.name:
                        decl.mtype.restype = funcdecl.mtype.intype[i]
                        break
                typparam = funcdecl.mtype.intype[i]
            if type(funcdecl.mtype.intype[i]) != type(typparam):
                raise TypeMismatchInStatement(ast)  
        if type(funcdecl.mtype.restype) == Unknown:
            funcdecl.mtype.restype = VoidType()
        return []
        
    
    def visitIntLiteral(self, ast, param):
        return IntType()
    
    def visitFloatLiteral(self, ast, param):
        return FloatType()
    
    def visitBooleanLiteral(self, ast, param):
        return BoolType()
    
    def visitStringLiteral(self, ast, param):
        return StringType()

    def visitArrayLiteral(self, ast, param):
        return ArrayType([len(ast.value)],self.visit(ast.value[0],param))