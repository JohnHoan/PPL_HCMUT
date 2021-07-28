import unittest
from TestUtils import TestChecker
from StaticError import *
from AST import *

class CheckSuite(unittest.TestCase):
    
    def test00(self):
        input = Program([VarDecl(Id("x"),[],None),VarDecl(Id("x"),[],None)])
        expect = str(Redeclared(Variable(),"x"))
        self.assertTrue(TestChecker.test(input,expect,400))

    def test01(self):
        input = Program([
            VarDecl(Id("main"),[],None),
            FuncDecl(Id("main"),[],([],[]))
        ])
        expect = str(Redeclared(Function(),"main"))
        self.assertTrue(TestChecker.test(input,expect,401))

    def test02(self):
        input = Program([
            FuncDecl(Id("main"),[
                VarDecl(Id("x"),[],None),
                VarDecl(Id("x"),[],None)
            ],([],[]))
        ])
        expect = str(Redeclared(Parameter(),"x"))
        self.assertTrue(TestChecker.test(input,expect,402))
    
    def test03(self):
        input = Program([
            FuncDecl(Id("main"),[
                VarDecl(Id("x"),[],None),
                VarDecl(Id("y"),[],None),
                VarDecl(Id("x"),[],None)
            ],([],[]))
        ])
        expect = str(Redeclared(Parameter(),"x"))
        self.assertTrue(TestChecker.test(input,expect,403))

    def test04(self):
        input = Program([
            FuncDecl(Id("main"),[],([],[])),
            FuncDecl(Id("main"),[],([],[]))
        ])
        expect = str(Redeclared(Function(),"main"))
        self.assertTrue(TestChecker.test(input,expect,404))

    def test05(self):
        input = Program([
            VarDecl(Id("x"),[],None),
            FuncDecl(Id("main"),[
                VarDecl(Id("x"),[],None)
            ],([],[])),
            FuncDecl(Id("main"),[],([],[]))
        ])
        expect = str(Redeclared(Function(),"main"))
        self.assertTrue(TestChecker.test(input,expect,405))
    
    def test06(self):
        input = Program([
            FuncDecl(Id("main"),[],([],[
                Return(IntLiteral(2))
            ])),
            FuncDecl(Id("main"),[],([],[]))
        ])
        expect = str(Redeclared(Function(),"main"))
        self.assertTrue(TestChecker.test(input,expect,406))
    
    def test07(self):
        input = Program([
            FuncDecl(Id("foo"),[VarDecl(Id("x"),[],None)],([],[])),
            FuncDecl(Id("main"),[],([
                VarDecl(Id("x"),[],None),
                VarDecl(Id("y"),[],None)
            ],[
                Assign(Id("x"),BinaryOp("+",Id("x"),CallExpr(Id("foo"),[Id("y")])))
            ]))
        ])
        expect = str(TypeCannotBeInferred(Assign(Id("x"),BinaryOp("+",Id("x"),CallExpr(Id("foo"),[Id("y")])))))
        self.assertTrue(TestChecker.test(input,expect,407))
    
    def test08(self):
        input = Program([
            FuncDecl(Id("foo"),[],([],[])),
            FuncDecl(Id("foo1"),[],([],[]))
        ])
        expect = str(NoEntryPoint())
        self.assertTrue(TestChecker.test(input,expect,408))

    def test09(self):
        input = """
            Function: main
            Body:
                Var: a;
                a = foo;
            EndBody.
            Function: foo
            Parameter: x
            Body:
                Return x + 5;
            EndBody.
        """
        expect = str(Undeclared(Identifier(),"foo"))
        self.assertTrue(TestChecker.test(input,expect,409))

    def test10(self):
        input = """
            Function: main
            Body:
                Var: a;
                a = 1 + foo(3.5);
            EndBody.
            Function: foo
            Parameter: x
            Body:
                Return x + 5;
            EndBody.
        """
        expect = str(TypeMismatchInExpression(BinaryOp("+",Id("x"),IntLiteral(5))))
        self.assertTrue(TestChecker.test(input,expect,410))
    
    def test11(self):
        input = """
            Function: main
            Body:
            EndBody.
            Function: factorial
            Parameter: n
            Body:
                If True Then Return 1;
                Else Return 1.0; 
                EndIf.
            EndBody.
        """
        expect = str(TypeMismatchInStatement(Return(FloatLiteral(1.0))))
        self.assertTrue(TestChecker.test(input,expect,411))

    def test12(self):
        input = """
            Function: main
            Body:
            EndBody.
            Function: factorial
            Parameter: n
            Body:
                If n <= 1 Then Return 1;
                Else Return n *. factorial(n-1); 
                EndIf.
            EndBody.
        """
        expect = str(TypeMismatchInExpression(BinaryOp("*.",Id("n"),CallExpr(Id("factorial"),[BinaryOp("-",Id("n"),IntLiteral(1))]))))
        self.assertTrue(TestChecker.test(input,expect,412))

    def test13(self):
        input = """
            Function: factorial
            Parameter: n
            Body:
                If n <= 1 Then Return 1;
                Else Return n * factorial(n-1); 
                EndIf.
            EndBody.
            Function: main
            Body:
                Return factorial(5) -. 2.0;
            EndBody.
        """
        expect = str(TypeMismatchInExpression(BinaryOp("-.",CallExpr(Id("factorial"),[IntLiteral(5)]),FloatLiteral(2.0))))
        self.assertTrue(TestChecker.test(input,expect,413))

    def test14(self):
        input = """
            Function: factorial
            Parameter: n
            Body:
                If n <= 1 Then Return n * factorial(n-1);
                Else Return 1; 
                EndIf.
            EndBody.
            Function: main
            Body:
                Return factorial(5) -. 2.0;
            EndBody.
        """
        expect = str(TypeMismatchInExpression(BinaryOp("-.",CallExpr(Id("factorial"),[IntLiteral(5)]),FloatLiteral(2.0))))
        self.assertTrue(TestChecker.test(input,expect,414))

    def test15(self):
        input = """
            Function: factorial
            Parameter: n
            Body:
                If n <= 1 Then Return n * factorial(n-1);
                Else Return 1; 
                EndIf.
            EndBody.
            Function: main
            Body:
                Return factorial1(5) -. 2.0;
            EndBody.
        """
        expect = str(Undeclared(Function(),"factorial1"))
        self.assertTrue(TestChecker.test(input,expect,415))

    def test16(self):
        input = """
            Function: factorial
            Parameter: n
            Body:
                If n <= 1 Then Return n * factorial(n-1);
                Else Return 1; 
                EndIf.
            EndBody.
            Function: main
            Body:
                Return factorial1 -. 2.0;
            EndBody.
        """
        expect = str(Undeclared(Identifier(),"factorial1"))
        self.assertTrue(TestChecker.test(input,expect,416))

    def test17(self):
        input = """
            Var: n = 1;
            Function: factorial
            Body:
                If n <= 1 Then Return 1;
                Else Return 1; 
                EndIf.
            EndBody.
            Function: main
            Body:
                Return factorial1 -. 2.0;
            EndBody.
        """
        expect = str(Undeclared(Identifier(),"factorial1"))
        self.assertTrue(TestChecker.test(input,expect,417))
    
    def test18(self):
        input = """
            Var: n = 1;
            Function: factorial
            Body:
                If n <=. 1 Then Return 1;
                Else Return 1; 
                EndIf.
            EndBody.
            Function: main
            Body:
            EndBody.
        """
        expect = str(TypeMismatchInExpression(BinaryOp("<=.",Id("n"),IntLiteral(1))))
        self.assertTrue(TestChecker.test(input,expect,418))

    def test19(self):
        input = """
            Var: x = 10.0;
            Function: factorial
            Parameter: n
            Body:
                If n <= 1 Then Return n*factorial(n-1);
                Else Return 1; 
                EndIf.
            EndBody.
            Function: main
            Body:
                Return factorial(x);
            EndBody.
        """
        expect = str(TypeMismatchInExpression(CallExpr(Id("factorial"),[Id("x")])))
        self.assertTrue(TestChecker.test(input,expect,419))

    def test20(self):
        input = """
            Var: x = 10.0;
            Function: factorial
            Parameter: n
            Body:
                If n <= 1 Then Return n*factorial(n-1);
                Else Return 1; 
                EndIf.
            EndBody.
            Function: main
            Body:
                Return factorial();
            EndBody.
        """
        expect = str(TypeMismatchInExpression(CallExpr(Id("factorial"),[])))
        self.assertTrue(TestChecker.test(input,expect,420))
    
    def test21(self):
        input = """ Var:a;
                    Function: main  
                    Parameter:a,b
                    Body:
                        Var:x=1,y;
                        y=x;
                        y=2.0;
                    EndBody.

                    """
        expect = str(TypeMismatchInStatement(Assign(Id("y"),FloatLiteral(2.0))))
        self.assertTrue(TestChecker.test(input,expect,421))
    
    def test22(self):
        input = """Function: main  
                   Body:
                        printStrLn();
                    EndBody."""
        expect = str(TypeMismatchInStatement(CallStmt(Id("printStrLn"),[])))
        self.assertTrue(TestChecker.test(input,expect,422))

    def test23(self):
        """More complex program"""
        input = """Function: main 
                    Body:
                        printStrLn(read(4));
                    EndBody."""
        expect = str(TypeMismatchInExpression(CallExpr(Id("read"),[IntLiteral(4)])))
        self.assertTrue(TestChecker.test(input,expect,423))

    def test24(self):
        """Simple program: main """
        input = Program([FuncDecl(Id("main"),[],([],[
            CallExpr(Id("foo"),[])]))])
        expect = str(Undeclared(Function(),"foo"))
        self.assertTrue(TestChecker.test(input,expect,424))

    def test25(self):
        """nested scopes if"""
        input = """
            Function: main
            Body:
            EndBody.
            Function: foo
            Body:
                If True Then
                    If True Then
                        Return 1;
                    EndIf.
                Else Return 1.0;
                EndIf.  
            EndBody.
        """
        expect = str(TypeMismatchInStatement(Return(FloatLiteral(1.0))))
        self.assertTrue(TestChecker.test(input,expect,425))

    def test26(self):
        input = """
            Function: main
            Body:
            EndBody.
            Function: foo
            Body:
                Return foo();
            EndBody.
        """
        expect = str(TypeCannotBeInferred(Return(CallExpr(Id("foo"),[]))))
        self.assertTrue(TestChecker.test(input,expect,426))

    def test27(self):
        input = """
            Function: fibonacci
            Parameter: n
            Body:
                If n == 0 Then Return 0;
                ElseIf n == 1 Then Return 1;
                Else Return fibonacci(n-1) + fibonacci(n-2);
                EndIf.
            EndBody.
            Function: main
            Body:
                int_of_float(fibonacci(8));
            EndBody.
        """
        expect = str(TypeMismatchInStatement(CallStmt(Id("int_of_float"),[CallExpr(Id("fibonacci"),[IntLiteral(8)])])))
        self.assertTrue(TestChecker.test(input,expect,427))
    
    def test28(self):
        input = """
            Function: main
            Body:
                Var: x;
                x = printStr("abc");
            EndBody.
        """
        expect = str(TypeMismatchInStatement(Assign(Id("x"),CallExpr(Id("printStr"),[StringLiteral("abc")]))))
        self.assertTrue(TestChecker.test(input,expect,428))

    def test29(self):
        input = """
            Function: main
            Body:
                Var: x;
                x = x + foo();
            EndBody.
            Function: foo
            Body:
                Return 1.0 +. foo();
            EndBody.
        """
        expect = str(TypeMismatchInExpression((BinaryOp("+.",FloatLiteral(1.0),CallExpr(Id("foo"),[])))))
        self.assertTrue(TestChecker.test(input,expect,429))
    
    def test30(self):
        input = """
            Function: main
            Body:
                Var: x;
                x = x + foo();
            EndBody.
            Function: foo
            Body:
                Return 1.0;
            EndBody.
        """
        expect = str(TypeMismatchInStatement(Return(FloatLiteral(1.0))))
        self.assertTrue(TestChecker.test(input,expect,430))
    
    def test31(self):
        input = """
            Function: main
            Body:
                Var: x,y;
                x = x + foo(y);
            EndBody.
            Function: foo
            Parameter: n
            Body:
                Return 1;
            EndBody.
        """
        expect = str(TypeCannotBeInferred(Assign(Id("x"),BinaryOp("+",Id("x"),CallExpr(Id("foo"),[Id("y")])))))
        self.assertTrue(TestChecker.test(input,expect,431))

    def test32(self):
        input = """
            Function: main
            Body:
            EndBody.
            Function: fibo
            Parameter: n
            Body:
                If n >= 1 Then Return fibo(n-1) + fibo(n-2);
                Else 
                    If n == 1 Then Return 1;
                    Else Return;
                    EndIf.
                EndIf.
            EndBody.
        """
        expect = str(TypeMismatchInStatement(Return(None)))
        self.assertTrue(TestChecker.test(input,expect,432))

    def test33(self):
        input = """
            Function: main
            Body:

            EndBody.
            Function: fibo
            Parameter: n
            Body:
                If n >= 1 Then Return fibo(n-1) + fibo(n-2);
                Else 
                    If (n == 1) || (n == 0) Then Return 1;
                    Else 
                        If True Then Return;
                        EndIf.
                    EndIf.
                EndIf.
            EndBody.
        """
        expect = str(TypeMismatchInStatement(Return(None)))
        self.assertTrue(TestChecker.test(input,expect,433))
    def test34(self):
        input = """
            Function: main
            Body:
            EndBody.
            Function: fibo
            Parameter: n
            Body:
                If n >= 1 Then Return fibo(n-1) + fibo(n-2);
                Else 
                    If (n == 1) && !(n <= 5) Then Return;
                    EndIf.
                EndIf.
            EndBody.
        """
        expect = str(TypeMismatchInStatement(Return(None)))
        self.assertTrue(TestChecker.test(input,expect,434))

    def test35(self):
        input = """
            Function: main
            Body:
            EndBody.
            Function: foo
            Parameter: x
            Body:
                Var: y,z;
                y = x && (x == z);
            EndBody.
        """
        expect = str(TypeMismatchInExpression(BinaryOp("==",Id("x"),Id("z"))))
        self.assertTrue(TestChecker.test(input,expect,435))
    
    def test36(self):
        input = """
            Function: main
            Body:
                Var: x = 10;
                If x Then printStr("abc");
                EndIf.
            EndBody.
        """
        expect = str(TypeMismatchInStatement(If([(Id("x"),[],[CallStmt(Id("printStr"),[StringLiteral("abc")])])],([],[]))))
        self.assertTrue(TestChecker.test(input,expect,436))

    def test37(self):
        input = """
            Function: foo
            Body:
                Return 10;
            EndBody.
            Function: main
            Body:
                Var: x = 10;
                If foo() Then printStr("abc");
                EndIf.
            EndBody.
        """
        expect = str(TypeMismatchInStatement(If([(CallExpr(Id("foo"),[]),[],[CallStmt(Id("printStr"),[StringLiteral("abc")])])],([],[]))))
        self.assertTrue(TestChecker.test(input,expect,437))

    def test38(self):
        input = """
            Function: main
            Body:
                Var: x = 10;
                If foo() Then printStr("abc");
                EndIf.
            EndBody.
            Function: foo
            Body:
                Return 10;
            EndBody.
        """
        expect = str(TypeMismatchInStatement(Return(IntLiteral(10))))
        self.assertTrue(TestChecker.test(input,expect,438))
    
    def test39(self):
        input = """
            Function: main
            Body:
                Var: x;
                If x Then 
                ElseIf x < 5 Then
                EndIf.
            EndBody.
            Function: foo
            Body:
                Return 10;
            EndBody.
        """
        expect = str(TypeMismatchInExpression(BinaryOp("<",Id("x"),IntLiteral(5))))
        self.assertTrue(TestChecker.test(input,expect,439))
    
    def test40(self):
        input = """
            Function: main
            Body:
                Var: x;
                If foo() Then 
                ElseIf foo() < 5 Then
                EndIf.
            EndBody.
            Function: foo
            Body:
                Return True && False;
            EndBody.
        """
        expect = str(TypeMismatchInExpression(BinaryOp("<",CallExpr(Id("foo"),[]),IntLiteral(5))))
        self.assertTrue(TestChecker.test(input,expect,440))
    
    def test41(self):
        input = """
            Function: main
            Body:
                Var: x,y,z;
                x = y && ((y-1) > z);
            EndBody.
        """
        expect = str(TypeMismatchInExpression(BinaryOp("-",Id("y"),IntLiteral(1))))
        self.assertTrue(TestChecker.test(input,expect,441))
    
    def test42(self):
        input = """
            Function: main
            Body:
                Var: x,y,z,t,k;
                k = ((((z+1)>y)&&(t<t+1)) || ((x-7)<9)) && !x;
            EndBody.
        """
        expect = str(TypeMismatchInExpression(UnaryOp("!",Id("x"))))
        self.assertTrue(TestChecker.test(input,expect,442))
    
    def test43(self):
        input = """
            Function: main
            Body:
                Var: x,y,z,t,k;
                k = ((((z+1)>y)&&(t<t+1)) || ((x-7)<9)) && !x;
            EndBody.
        """
        expect = str(TypeMismatchInExpression(UnaryOp("!",Id("x"))))
        self.assertTrue(TestChecker.test(input,expect,443))
    
    def test44(self):
        input = """
            Function: main
            Body:
                Var: a;
                a = foo;
            EndBody.
            Function: foo
            Parameter: x
            Body:
                Return 1;
            EndBody.
        """
        expect = str(Undeclared(Identifier(),"foo"))
        self.assertTrue(TestChecker.test(input,expect,444))
    
    def test45(self):
        input = """
            Function: main
            Body:
                Var: a;
                a = 1;
            EndBody.
            Function: foo
            Parameter: x
            Body:
                Var: foo;
                Return foo + 1;
            EndBody.
        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,445))
    
    def test46(self):
        input = """
            Function: foo
            Parameter: x
            Body:
                Var: foo;
                Return foo + 1;
            EndBody.
            Function: main
            Body:
                Var: a;
                a = foo(1)=/=1.0;
            EndBody.
        """
        expect = str(TypeMismatchInExpression(BinaryOp("=/=",CallExpr(Id("foo"),[IntLiteral(1)]),FloatLiteral(1.0))))
        self.assertTrue(TestChecker.test(input,expect,446))
    
    def test47(self):
        input = """
            Function: main
            Body:
                Var: a;
                a = foo(1)=/=1.0;
            EndBody.
            Function: foo
            Parameter: x
            Body:
                Var: foo;
                Return foo + 1;
            EndBody.
        """
        expect = str(TypeMismatchInStatement(Return(BinaryOp("+",Id("foo"),IntLiteral(1)))))
        self.assertTrue(TestChecker.test(input,expect,447))
    
    def test48(self):
        input = """
            Function: main
            Body:
                Var: a, foo;
                a = foo(1)=/=foo;
            EndBody.
            Function: foo
            Parameter: x
            Body:
                Var: foo;
                Return foo + 1;
            EndBody.
        """
        expect = str(TypeMismatchInStatement(Return(BinaryOp("+",Id("foo"),IntLiteral(1)))))
        self.assertTrue(TestChecker.test(input,expect,448))
    
    def test49(self):
        input = """
            Function: main
            Body:
                Var: a, foo;
                a = foo=/=foo();
            EndBody.
        """
        expect = str(Undeclared(Function(),"foo"))
        self.assertTrue(TestChecker.test(input,expect,449))
    
    def test50(self):
        input = """
            Function: main
            Body:
                For(i = 0, True, 5) Do
                EndFor.
            EndBody.
        """
        expect = str(Undeclared(Identifier(),"i"))
        self.assertTrue(TestChecker.test(input,expect,450))
    
    def test51(self):
        input = """
            Function: main
            Body:
                Var: i;
                For(i = 1.0, True, 5) Do
                EndFor.
            EndBody.
        """
        expect = str(TypeMismatchInStatement(For(Id("i"),FloatLiteral(1.0),BooleanLiteral(True),IntLiteral(5),([],[]))))
        self.assertTrue(TestChecker.test(input,expect,451))
    
    def test52(self):
        input = """
            Function: main
            Body:
                Var: i;
                For(i = 1, i, 5) Do
                EndFor.
            EndBody.
        """
        expect = str(TypeMismatchInStatement(For(Id("i"),IntLiteral(1),Id("i"),IntLiteral(5),([],[]))))
        self.assertTrue(TestChecker.test(input,expect,452))
    
    def test53(self):
        input = """
            Function: main
            Body:
                Var: i;
                For(i = 1, foo(), 5) Do
                EndFor.
            EndBody.
            Function: foo
            Body:
                Return 1;
            EndBody.
        """
        expect = str(TypeMismatchInStatement(Return(IntLiteral(1))))
        self.assertTrue(TestChecker.test(input,expect,453))
    
    def test54(self):
        input = """
            Function: main
            Body:
                Var: i;
                For(i = foo(), foo(), 5) Do
                EndFor.
            EndBody.
            Function: foo
            Body:
                Return 1;
            EndBody.
        """
        expect = str(TypeMismatchInStatement(For(Id("i"),CallExpr(Id("foo"),[]),CallExpr(Id("foo"),[]),IntLiteral(5),([],[]))))
        self.assertTrue(TestChecker.test(input,expect,454))
    
    def test55(self):
        input = """
            Function: main
            Body:
                Var: i;
                While(i) Do
                    i = i + 1;
                EndWhile.
            EndBody.
        """
        expect = str(TypeMismatchInExpression(BinaryOp("+",Id("i"),IntLiteral(1))))
        self.assertTrue(TestChecker.test(input,expect,455))
    
    def test56(self):
        input = """
            Function: main
            Body:
                Var: i;
                Do 
                    i = i + 1;
                While (i)
                EndDo.
            EndBody.
        """
        expect = str(TypeMismatchInStatement(Dowhile(([],[Assign(Id("i"),BinaryOp("+",Id("i"),IntLiteral(1)))]),Id("i"))))
        self.assertTrue(TestChecker.test(input,expect,456))

    def test57(self):
        input = """
            Function: foo
            Body:
                Var: i;
                While i Do
                    If i || main() Then
                        Do
                            Return "bcd";
                            If True Then
                                Var: index;
                                For (index = 0, index < 10, index * 10) Do
                                    Return "good";
                                EndFor.
                                Return "hello";
                            EndIf.
                        While i && main()
                        EndDo. 
                    EndIf.
                    Return "abc";
                EndWhile.
            EndBody.
            Function: main
            Body:
                Return;
            EndBody.
        """
        expect = str(TypeMismatchInStatement(Return(None)))
        self.assertTrue(TestChecker.test(input,expect,457))
    
    def test58(self):
        input = """
            Function: foo
            Body:
                Var: i;
                While i Do
                    If i || main() Then
                        Do
                            Return "bcd";
                            If True Then
                                Var: index;
                                For (index = 0, index < 10, index * 10) Do
                                    Return "good";
                                EndFor.
                                Return "hello";
                            EndIf.
                        While i && main()
                        EndDo. 
                    EndIf.
                    Return 0;
                EndWhile.
            EndBody.
            Function: main
            Body:
                Return True;
            EndBody.
        """
        expect = str(TypeMismatchInStatement(Return(IntLiteral(0))))
        self.assertTrue(TestChecker.test(input,expect,458))
    
    def test59(self):
        input = """
            Function: main
            Body:
                Return 0;
            EndBody.

            Function: foo
            Body:
                Var: x;
                Return 7 + 8 +. True;
            EndBody.
            """
        expect = str(TypeMismatchInExpression(BinaryOp("+.",BinaryOp("+",IntLiteral(7),IntLiteral(8)),BooleanLiteral(True))))
        self.assertTrue(TestChecker.test(input,expect,459))
    
    def test60(self):
        input = """
            Function: main
            Body:
                foo(1);
            EndBody.
            Function: foo
            Body:
            EndBody.
        """
        expect = str(TypeMismatchInStatement(CallStmt(Id("foo"),[IntLiteral(1)])))
        self.assertTrue(TestChecker.test(input,expect,460))

    def test61(self):
        input = """
            Function: main
            Body:
                Var: t;
                foo(t);
            EndBody.
            Function: foo
            Parameter: n
            Body:
            EndBody.
        """
        expect = str(TypeCannotBeInferred(CallStmt(Id("foo"),[Id("t")])))
        self.assertTrue(TestChecker.test(input,expect,461))

    def test62(self):
        input = """
            Function: main
            Body:
                Var: t;
                t = foo(t) + t;
            EndBody.
            Function: foo
            Parameter: n
            Body:
            EndBody.
        """
        expect = str(TypeCannotBeInferred(Assign(Id("t"),BinaryOp("+",CallExpr(Id("foo"),[Id("t")]),Id("t")))))
        self.assertTrue(TestChecker.test(input,expect,462))
    
    def test63(self):
        input = """
            Function: bool_of_int
            Parameter: n
            Body:
                If n == 0 Then
                    Return False;
                Else Return True;
                EndIf.
            EndBody.
            Function: main
            Body:
                Var: t;
                t = t + foo(t);
            EndBody.
            Function: foo
            Parameter: n
            Body:
                If bool_of_int(n) || ((n-10)>20) Then
                    Return;
                EndIf.
                Return 0;
            EndBody.
        """
        expect = str(TypeMismatchInStatement(Return(None)))
        self.assertTrue(TestChecker.test(input,expect,463))

    def test64(self):
        input = """
            Function: bool_of_int
            Parameter: n
            Body:
                If n == 0 Then
                    Return False;
                Else Return True;
                EndIf.
            EndBody.
            Function: main
            Body:
                Var: t;
                t = t + foo(t);
            EndBody.
            Function: foo
            Parameter: n
            Body:
                If bool_of_int(n) || ((n-10)>20) Then
                    Return;
                EndIf.
                Return 0;
            EndBody.
        """
        expect = str(TypeMismatchInStatement(Return(None)))
        self.assertTrue(TestChecker.test(input,expect,464))
    '''
    '''
    def test65(self):
        input = """
            Function: main
            Body:
                Return 0;
            EndBody.
            Function: foo
            Parameter: a, b
            Body:
                a = foo(1,True);
                Return;
            EndBody.
        """
        expect = str(TypeMismatchInStatement(Return(None)))
        self.assertTrue(TestChecker.test(input,expect,465))
    '''
    '''
    def test66(self):
        input = """
            Function: main
            Body:
                foo(1,2);
                Return 0;
            EndBody.
            Function: foo
            Parameter: a, b
            Body:
                a = foo(1,1);
            EndBody.
        """
        expect = str(TypeMismatchInStatement(Assign(Id("a"),CallExpr(Id("foo"),[IntLiteral(1),IntLiteral(1)]))))
        self.assertTrue(TestChecker.test(input,expect,466))
    
    def test67(self):
        input = """
            Function: main
            Body:
                Return 0;
            EndBody.
            Function: foo
            Parameter: a, b
            Body:
                Var:x;
                foo(2,3);
                a = foo(a,b);
            EndBody.
        """
        expect = str(TypeMismatchInStatement(Assign(Id("a"),CallExpr(Id("foo"),[Id("a"),Id("b")]))))
        self.assertTrue(TestChecker.test(input,expect,467))
    

    def test68(self):
        input = """
            Function: main
            Body:
                Var: a = 0.0;
                a = gcd(20,65);
            EndBody.
            Function: gcd
            Parameter: a, b
            Body:
                If b > 0 Then
                    Return gcd(b,a % b);
                EndIf.
                Return a;
            EndBody.

        """
        expect = str(TypeMismatchInStatement(Return(Id("a"))))
        self.assertTrue(TestChecker.test(input,expect,468))

    def test69(self):
        input="""
        Function:foo
        Body:
        Return 1;
        EndBody.
        Function:main
        Parameter:a,b,c,d
        Body:
        a=1.0+foo(a);
        EndBody.
        """
        expect=str(TypeMismatchInExpression(CallExpr(Id("foo"),[Id("a")])))
        self.assertTrue(TestChecker.test(input,expect,469))
    
    
    def test70(self):
        input = """
            Function: main
            Body:
            EndBody.
            Function: foo
            Parameter: x, y
            Body:
                Var: z;
                While True Do
                    z = foo(1, foo(x, True));
                EndWhile.
                Return y && z;
            EndBody.
        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,470))
    
    def test71(self):
        input = """
            Function: main
            Body:
            EndBody.
            Function: foo
            Parameter: x,y
            Body:
                Var: z;
                z = foo(1,foo(foo(x,True),y));
            EndBody.
        """
        expect = str(TypeMismatchInExpression(CallExpr(Id("foo"),[IntLiteral(1),CallExpr(Id("foo"),[CallExpr(Id("foo"),[Id("x"),BooleanLiteral(True)]),Id("y")])])))
        self.assertTrue(TestChecker.test(input,expect,471))

    def test72(self):
        input = """
            Function: main
            Body:
                Var: x;
                foo(1, foo(x, True));
            EndBody.
            Function: foo
            Parameter: x,y
            Body:
                Return 0;
            EndBody.
        """
        expect = str(TypeMismatchInStatement(Return(IntLiteral(0))))
        self.assertTrue(TestChecker.test(input,expect,472))

    def test73(self):
        input = """
            Function: foo1
            Parameter: x,y
            Body:
                Return foo(1, True);
            EndBody.
            Function: main
            Body:
                Var: x;
                foo(1, foo(x, True));
            EndBody.
            Function: foo
            Parameter: x,y
            Body:
                Return True;
            EndBody.
        """
        expect = str(TypeCannotBeInferred(Return(CallExpr(Id("foo"),[IntLiteral(1),BooleanLiteral(True)]))))
        self.assertTrue(TestChecker.test(input,expect,473))
    
    def test74(self):
        input = """
            Function: main
            Body:
                Var: x = 0;
                x = gcd(85,95);
            EndBody.
            Function: gcd
            Parameter: a, b
            Body:
                If b == 0 Then Return a;
                EndIf.
                Return gcd(b,a%b);
            EndBody.
        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,474))
    
    def test75(self):
        input = """
            Function: main
            Body:
                Var: x = 0.0;
                x = gcd(85,95);
            EndBody.
            Function: gcd
            Parameter: a, b
            Body:
                If b == 0 Then Return float_of_int(a);
                EndIf.
                Return gcd(b,a%b);
            EndBody.
        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,475))

    def test76(self):
        input = """
            Function: main
            Body:
            EndBody.
            Function: foo
            Parameter: a, b
            Body:
                Do
                    a = a && True;
                While a || b && foo()
                EndDo.
            EndBody.
        """
        expect = str(TypeMismatchInExpression(CallExpr(Id("foo"),[])))
        self.assertTrue(TestChecker.test(input,expect,476))

    def test77(self):
        input = """
            Function: main
            Body:
            EndBody.
            Function: foo
            Parameter: a, b
            Body:
                Do
                    a = a && True;
                While foo(foo(b,a),a)
                EndDo.
                Return 1;
            EndBody.
        """
        expect = str(TypeMismatchInStatement(Return(IntLiteral(1))))
        self.assertTrue(TestChecker.test(input,expect,477))
    
    def test78(self):
        input = """
            Function: main
            Body:
            EndBody.
            Function: foo
            Parameter: a, b
            Body:
                Do
                    a = a && True;
                    Return 1;
                While foo(b,a)
                EndDo.
            EndBody.
        """
        expect = str(TypeMismatchInStatement(Dowhile(([],[Assign(Id("a"),BinaryOp("&&",Id("a"),BooleanLiteral(True))),Return(IntLiteral(1))]),CallExpr(Id("foo"),[Id("b"),Id("a")]))))
        self.assertTrue(TestChecker.test(input,expect,478))
    
    def test79(self):
        input = """
            Function: main
            Parameter: a,b,c,d
            Body:
                Do
                    Var: a;
                    a = a +b;
                    a = 1;
                While(c&&d)
                EndDo.
                a = 1.0;
            EndBody.
        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,479))
    
    def test80(self):
        input = """
            Function: main
            Body:
            EndBody.
            Function: foo
            Parameter: a, b
            Body:
                Do
                    Var: a;
                    a = a && True;
                    Return True;
                While foo(b,a)
                EndDo.
            EndBody.
        """
        expect = str(TypeCannotBeInferred(Dowhile(([VarDecl(Id("a"),[],None)],[Assign(Id("a"),BinaryOp("&&",Id("a"),BooleanLiteral(True))),Return(BooleanLiteral(True))]),CallExpr(Id("foo"),[Id("b"),Id("a")]))))
        self.assertTrue(TestChecker.test(input,expect,480))

    def test81(self):
        input="""
            Function: foo
            Parameter: a, b
            Body:
                For(a = b, a < 10, 1) Do
                    b = foo(a+b,b*a);
                EndFor.
                Return -1;
            EndBody.
            Function: main
            Body:
                Var: z;
                z = -foo(5,foo(foo(True,False),5)) + foo(7,5);
                If z < 10 Then
                EndIf.
            EndBody.
        """
        expect=str(TypeMismatchInExpression(CallExpr(Id("foo"),[BooleanLiteral(True),BooleanLiteral(False)])))
        self.assertTrue(TestChecker.test(input,expect,481))

    def test82(self):
        input="""
            Function: foo
            Parameter: a, b
            Body:
                For(a = b, a < 10, 1) Do
                    b = foo(a+b,b*a);
                EndFor.
                Return -1;
            EndBody.
            Function: main
            Body:
                Var: z;
                z = -foo(5,foo(foo(True,False),5)) + foo(7,5);
                If z < 10 Then
                EndIf.
            EndBody.
        """
        expect=str(TypeMismatchInExpression(CallExpr(Id("foo"),[BooleanLiteral(True),BooleanLiteral(False)])))
        self.assertTrue(TestChecker.test(input,expect,482))

    def test83(self): 
        input = """
            Function: foo
            Body:
                Return;
            EndBody.
            Function: foo1
            Parameter: x, y
            Body:
                x = foo();
            EndBody.
            Function: main
            Body:
            EndBody.
        """
        expect = str(TypeMismatchInStatement(Assign(Id("x"),CallExpr(Id("foo"),[]))))
        self.assertTrue(TestChecker.test(input,expect,483))

    def test84(self):
        input = """
            Var: a, b;
            Function: foo
            Parameter: x, y, z
            Body:
                Return;
            EndBody.

            Function: main
            Body:
                If b + 0 Then 
                    Return a; 
                EndIf.
                foo(1,2,3);
            EndBody.
        """
        expect = str(TypeMismatchInStatement(If([(BinaryOp('+',Id('b'), IntLiteral(0)), [], [Return(Id('a'))])], ([],[]))))
        self.assertTrue(TestChecker.test(input, expect, 484))

    def test85(self):
        input = """
                Function: main
                Parameter: y, a, x
                Body:
                    x = 1;
                    y = a + foo(x);
                EndBody.
                Function: foo
                Parameter: a
                Body:
                    a = False;
                    Return a;
                EndBody.
                """
        expect = str(TypeMismatchInStatement(Assign(Id('a'), BooleanLiteral(False))))
        self.assertTrue(TestChecker.test(input, expect, 485))

    def test86(self):
        input = """
                Var: x[3][2] = { { 1,2 }, { 2,3} , {3,4}   };
                Function: main
                Parameter: y, a, i
                Body:
                    a = 1 + foo();
                EndBody.

                Function: foo
                Body:
                    Return 1.1;
                EndBody.
                """
        expect = str(TypeMismatchInStatement(Return(FloatLiteral(1.1))))
        self.assertTrue(TestChecker.test(input, expect, 486))

    def test87(self):
        input = """
                  Function: main
                  Parameter: x,y,z
                  Body:
                       If foo(2,3,4) Then
                       EndIf. 
                  EndBody.

                  Function: foo
                  Parameter: k, a, i
                  Body:
                        k = k + a + i;
                        i = i +. 1.;
                        Return True;
                  EndBody.
                  """
        expect = str(TypeMismatchInExpression(BinaryOp('+.',Id('i'),FloatLiteral(1.))))
        self.assertTrue(TestChecker.test(input, expect, 487))

    def test88(self):
        input = """
                  Function: main
                  Parameter: x,y,z
                  Body:
                       While x Do   
                       EndWhile. 
                       
                       While y Do   
                       EndWhile.
                       
                       While z Do   
                       EndWhile.
                  EndBody.

                  Function: foo
                  Parameter: k, a, i
                  Body:
                        main(True,False,1);
                  EndBody.
                  """
        expect = str(
            TypeMismatchInStatement(CallStmt(Id('main'), [BooleanLiteral(True), BooleanLiteral(False), IntLiteral(1)])))
        self.assertTrue(TestChecker.test(input, expect, 488))

    def test89(self):
        input = """
                  Function: main
                  Parameter: x,y,z
                  Body:
                       While foo(2,3,4) Do   
                       EndWhile. 
                  EndBody.

                  Function: foo
                  Parameter: k, a, i
                  Body:
                        k = k + a + i;
                        Return { {True,False}   };
                  EndBody.
                  """
        expect = str(TypeMismatchInStatement(Return(ArrayLiteral([ArrayLiteral([BooleanLiteral(True),BooleanLiteral(False)])]))))
        self.assertTrue(TestChecker.test(input, expect, 489))

    def test90(self):
        input = """
                  Function: main
                  Parameter: x,y,z
                  Body:
                       For (x = 0, x < 10, foo(2.0,3,4)) Do
                            y = float_of_int(x);
                       EndFor.
                       Return y;
                  EndBody.

                  Function: foo
                  Parameter: k, a, i
                  Body:
                        k = main(1,2.1,3);
                        k = k +. 1.1;
                        Return { {"a","b"}   };
                  EndBody.
                  """
        expect = str(TypeMismatchInStatement(Return(ArrayLiteral([ArrayLiteral([StringLiteral('a'), StringLiteral('b')])]))))
        self.assertTrue(TestChecker.test(input, expect, 490))

    def test91(self):
        """More complex program"""
        input = """
                Function: foo
                Parameter: a,b
                Body:
                    If a > b Then
                        If a > 0 Then
                            If b > 0 Then
                                Return 1;
                            Else
                                b = b + 10;
                            EndIf.
                        Else
                            Return 1;
                        EndIf.
                    EndIf. 
                    Return;
                EndBody.
                Function: main
                Body:
                    foo(5,2);
                EndBody.
               """
        expect = str(TypeMismatchInStatement(Return(None)))
        self.assertTrue(TestChecker.test(input, expect, 491))

    def test92(self):
        input = """
                Function: foo
                Parameter: a,b
                Body:
                    If a > b Then
                        Var: i;
                        For (i = 2, i < 10, i + 1) Do
                            Var: s;
                            s = string_of_int(i);
                            printStr(s);
                        EndFor.
                    ElseIf a < b Then
                        i = 1;
                        Return i;
                    EndIf. 
                    Return;
                EndBody.
                Function: main
                Body:
                    foo(5,2);
                EndBody.
               """
        expect = str(Undeclared(Identifier(), 'i'))
        self.assertTrue(TestChecker.test(input, expect, 492))

    def test93(self):
        """More complex program"""
        input = """
                Function: main
                Body:
                    Var: x;
                    x = 1 + 2;
                    foo(5,x);
                EndBody.
                Function: foo
                Parameter: x,y
                Body:
                    Return True;
                EndBody.
               """
        expect = str(TypeMismatchInStatement(Return(BooleanLiteral(True))))
        self.assertTrue(TestChecker.test(input, expect, 493))
    
    def test94(self):
        input = """
                Function: foo
                Parameter: x,y
                Body:
                    x = 2;
                    y = 1;
                    Return;
                EndBody.
                Function: main
                Body:
                    Var: x;
                    x = 1 + 2;
                    foo(5.1,x);
                EndBody.
               """
        expect = str(TypeMismatchInStatement(CallStmt(Id('foo'),[FloatLiteral(5.1), Id('x')])))
        self.assertTrue(TestChecker.test(input, expect, 494))

    def test95(self):
        """More complex program"""
        input = """
                 Function: main
                Body:
                    Var: x;
                    x = 1 + 2;
                    foo(5.1,x);
                EndBody.
                Function: foo
                Parameter: x,y
                Body:
                    x = 2;
                    y = 1;
                    Return;
                EndBody.
                
               """
        expect = str(TypeMismatchInStatement(Assign(Id('x'),IntLiteral(2))))
        self.assertTrue(TestChecker.test(input, expect, 495))

    def test96(self):
        input = """
            Var: x = 1;
            Function: foo
            Parameter: x, y, z
            Body:
                x = 0;
                y = 0.0;
                Return y;
            EndBody.

            Function: main
            Body:
                Var: x = 1.1, y;
                x = foo(1, 1.1, "string");
                x = 1 + foo(1, 1.1, 0xF);
            EndBody.
        """
        expect = str(TypeMismatchInExpression(CallExpr(Id('foo'),[IntLiteral(1),FloatLiteral(1.1),IntLiteral(15)])))
        self.assertTrue(TestChecker.test(input, expect, 496))

    def test97(self):
        input = """
            Function: bool_of_string
            Body:
            EndBody.
            Function: main
            Body:
            EndBody.
        """
        expect = str(Redeclared(Function(),"bool_of_string"))
    
    def test98(self):
        input = """
        Var: x;
        Function: main
        Parameter: x
        Body:
            If x Then
                While x Do
                    If x Then
                        Break;
                    ElseIf False Then
                        Continue;
                    EndIf.
                EndWhile.
            EndIf.
        EndBody.
        """
        expect =  str()
        self.assertTrue(TestChecker.test(input, expect, 498))

    def test99(self):
        input = """
        Var: x, a[10], b[5];
        Function: main
        Parameter: x
        Body:
            While f(2, x) Do
            EndWhile.
        EndBody.
        Function: test
        Parameter: x, y
        Body:
        EndBody.
        Function: foo
        Body:
            Return x;
        EndBody.
        Function: f
        Parameter: z, t
        Body:
            Return True;
        EndBody.
        """
        expect = str(TypeCannotBeInferred(While(CallExpr(Id('f'),[IntLiteral(2),Id('x')]),([],[]))))
        self.assertTrue(TestChecker.test(input, expect, 499))