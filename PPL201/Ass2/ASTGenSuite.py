import unittest
from TestUtils import TestAST
from AST import *

class ASTGenSuite(unittest.TestCase):
    def test1(self):
        input = """Var: i;"""
        expect = Program([VarDecl(Id("i"),[],None)])
        self.assertTrue(TestAST.checkASTGen(input,expect,301))

    def test2(self):
        input = """Var: i[5][7][9] = {1,2,"abc"};"""
        expect = Program([VarDecl(Id("i"),[5,7,9],ArrayLiteral([IntLiteral("1"),IntLiteral("2"),StringLiteral("abc")]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,302))

    def test3(self):
        input = """Var: i = 18.5, t;"""
        expect = Program([VarDecl(Id("i"),[],FloatLiteral("18.5")),VarDecl(Id("t"),[],None)])
        self.assertTrue(TestAST.checkASTGen(input,expect,303))

    def test4(self):
        input = """Var: i = 18.5, t, k[5][2] = {True, 18.7, "abc", {22}};"""
        expect = Program([VarDecl(Id("i"),[],FloatLiteral("18.5")),VarDecl(Id("t"),[],None),VarDecl(Id("k"),[5,2],ArrayLiteral([BooleanLiteral("True"),FloatLiteral("18.7"),StringLiteral("abc"),ArrayLiteral([IntLiteral("22")])]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,304))

    def test5(self):
        input = """Var: i[5][7];"""
        expect = Program([VarDecl(Id("i"),[5,7],None)])
        self.assertTrue(TestAST.checkASTGen(input,expect,305))

    def test6(self):
        input = """Var: i[5][7], t[12][8][9] = {{},{}};"""
        expect = Program([VarDecl(Id("i"),[5,7],None),VarDecl(Id("t"),[12,8,9],ArrayLiteral([ArrayLiteral([]),ArrayLiteral([])]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,306))

    def test7(self):
        input = """
                Function: foo 
                Body:
                EndBody.       
        """
        expect = Program([FuncDecl(Id("foo"),[],([],[]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,307))

    def test8(self):
        input = """
                Function: foo
                Parameter: a, b, c[5][7]
                Body:
                EndBody.
        """
        expect = Program([FuncDecl(Id("foo"),[VarDecl(Id("a"),[],None),VarDecl(Id("b"),[],None),VarDecl(Id("c"),[5,7],None)],([],[]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,308))

    def test9(self):
        input = """
                Function: foo
                Parameter: a[7][8][9], t 
                Body:
                EndBody.       
        """
        expect = Program([FuncDecl(Id("foo"),[VarDecl(Id("a"),[7,8,9],None),VarDecl(Id("t"),[],None)],([],[]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,309))

    def test10(self):
        input = """
                Var: t = 7;
                Function: foo
                Body:
                EndBody.       
        """
        expect = Program([VarDecl(Id("t"),[],IntLiteral("7")),FuncDecl(Id("foo"),[],([],[]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,310))

    def test11(self):
        input = """
                Var: t[7][8][9] = "abc";
                Function: foo
                Body:
                EndBody.
                Function:foo1
                Body:
                EndBody.        
        """
        expect = Program([VarDecl(Id("t"),[7,8,9],StringLiteral("abc")),FuncDecl(Id("foo"),[],([],[])),FuncDecl(Id("foo1"),[],([],[]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,311))

    def test12(self):
        input = """
                Function: foo
                Body:
                    Var: c[9][10] = {{},"abc"};
                EndBody.        
        """
        expect = Program([FuncDecl(Id("foo"),[],([VarDecl(Id("c"),[9,10],ArrayLiteral([ArrayLiteral([]),StringLiteral("abc")]))],[]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,312))
    
    def test13(self):
        input = """
                Function: foo
                Body:
                    Var: t = 18;
                EndBody.
        """
        expect = Program([FuncDecl(Id("foo"),[],([VarDecl(Id("t"),[],IntLiteral("18"))],[]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,313))
    
    def test14(self):
        input = """
                Function: foo
                Body:
                    Var: t = 8;
                    Var: c = {{},8,True};
                EndBody.
        """
        expect = Program([FuncDecl(Id("foo"),[],([VarDecl(Id("t"),[],IntLiteral("8")),VarDecl(Id("c"),[],ArrayLiteral([ArrayLiteral([]),IntLiteral("8"),BooleanLiteral("True")]))],[]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,314))

    def test15(self):
        input = """
                Function: foo
                Body:
                    t = "abc";
                EndBody.
        """
        expect = Program([FuncDecl(Id("foo"),[],([],[Assign(Id("t"),StringLiteral("abc"))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,315))
    
    def test16(self):
        input = """
                Function: foo
                Body:
                    t[2] = "abc";
                EndBody.
        """
        expect = Program([FuncDecl(Id("foo"),[],([],[Assign(ArrayCell(Id("t"),[IntLiteral("2")]),StringLiteral("abc"))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,316))
    
    def test17(self):
        input = """
                Function: foo
                Body:
                    t["abc"] = "abc";
                EndBody.
        """
        expect = Program([FuncDecl(Id("foo"),[],([],[Assign(ArrayCell(Id("t"),[StringLiteral("abc")]),StringLiteral("abc"))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,317))

    def test18(self):
        input = """
                Function: foo
                Body:
                    t["abc"[8]] = "abc";
                EndBody.
        """
        expect = Program([FuncDecl(Id("foo"),[],([],[Assign(ArrayCell(Id("t"),[ArrayCell(StringLiteral("abc"),[IntLiteral("8")])]),StringLiteral("abc"))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,318))

    def test19(self):
        input = """
                Function: foo
                Body:
                    t["abc"[8][5]][foo()] = "abc";
                EndBody.
        """
        expect = Program([FuncDecl(Id("foo"),[],([],[Assign(ArrayCell(Id("t"),[ArrayCell(StringLiteral("abc"),[IntLiteral("8"),IntLiteral("5")]),CallExpr(Id("foo"),[])]),StringLiteral("abc"))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,319))

    def test20(self):
        input = """
                Function: foo
                Body:
                    t["abc"[8][5]][foo(a+b)] = "abc";
                EndBody.
        """
        expect = Program([FuncDecl(Id("foo"),[],([],[Assign(ArrayCell(Id("t"),[ArrayCell(StringLiteral("abc"),[IntLiteral("8"),IntLiteral("5")]),CallExpr(Id("foo"),[BinaryOp("+",Id("a"),Id("b"))])]),StringLiteral("abc"))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,320))

    def test21(self):
        input ="""
            Var: x[1][0x12][6][7] = 0XFFF;
        """
        expect = Program(
            [
                VarDecl(Id("x"),[1,18,6,7],IntLiteral(0XFFF))
            ]
        )
        self.assertTrue(TestAST.checkASTGen(input,expect,321))

    def test22(self):
        input ="""
            Var: x[1][0x12][0o12][7] = 0XFFF;
        """
        expect = Program(
            [
                VarDecl(Id("x"),[1,18,10,7],IntLiteral(0XFFF))
            ]
        )
        self.assertTrue(TestAST.checkASTGen(input,expect,322))

    def test23(self):
        input ="""
            Var: x[1][0x12][0o12][7] = 12e7;
        """
        expect = Program(
            [
                VarDecl(Id("x"),[1,18,10,7],FloatLiteral(12e7))
            ]
        )
        self.assertTrue(TestAST.checkASTGen(input,expect,323))

    def test24(self):
        input ="""
            Var: x[1][0x12][0o12][7] = 12.e7;
        """
        expect = Program(
            [
                VarDecl(Id("x"),[1,18,10,7],FloatLiteral(12.e7))
            ]
        )
        self.assertTrue(TestAST.checkASTGen(input,expect,324))

    def test25(self):
        input ="""
            Function: foo
            Body:
                While i < 10
                Do
                EndWhile.
                Continue;
                Break;
            EndBody.
        """
        expect = Program(
            [
                FuncDecl(Id("foo"),[],
                (
                    [],
                    [   While(BinaryOp("<",Id("i"),IntLiteral(10)),([],[])),
                        Continue(),
                        Break()
                    ]
                )
                ) 
            ]
        )
        self.assertTrue(TestAST.checkASTGen(input,expect,325))

    def test26(self):
        input ="""
            Function: foo
            Body:
                For(i = 2, i < 10, a+b)
                Do
                EndFor.
            EndBody.
        """
        expect = Program(
            [
                FuncDecl(Id("foo"),[],
                (
                    [],
                    [For(Id("i"),IntLiteral(2),BinaryOp("<",Id("i"),IntLiteral(10)),BinaryOp("+",Id("a"),Id("b")),([],[]))
                    ]
                )
                ) 
            ]
        )
        self.assertTrue(TestAST.checkASTGen(input,expect,326))

    def test27(self):
        input ="""
            Function: foo
            Body:
                Return;
            EndBody.
        """
        expect = Program(
            [
                FuncDecl(Id("foo"),[],
                (
                    [],
                    [Return(None)]
                )
                ) 
            ]
        )
        self.assertTrue(TestAST.checkASTGen(input,expect,327))

    def test28(self):
        input ="""
            Function: foo
            Body:
                Return a[7]["abc"[9]];
            EndBody.
        """
        expect = Program(
            [
                FuncDecl(Id("foo"),[],
                (
                    [],
                    [Return(ArrayCell(Id("a"),[IntLiteral(7),ArrayCell(StringLiteral("abc"),[IntLiteral(9)])]))]
                )
                ) 
            ]
        )
        self.assertTrue(TestAST.checkASTGen(input,expect,328))

    def test29(self):
        input ="""
            Function: foo
            Body:
                foo();
                Return a[7]["abc"[9]];
            EndBody.
        """
        expect = Program(
            [
                FuncDecl(Id("foo"),[],
                (
                    [],
                    [   CallStmt(Id("foo"),[]),
                        Return(ArrayCell(Id("a"),[IntLiteral(7),ArrayCell(StringLiteral("abc"),[IntLiteral(9)])]))]
                )
                ) 
            ]
        )
        self.assertTrue(TestAST.checkASTGen(input,expect,329))

    def test30(self):
        input ="""
            Function: fibo
            Parameter: n
            Body:
                Var: res = 1;
                While -n Do
                    Var: temp;
                    res = res * n;
                EndWhile.
                Return fibo(res);
            EndBody.
        """
        expect = Program(
            [
                FuncDecl(Id("fibo"),[VarDecl(Id("n"),[],None)],
                (
                    [VarDecl(Id("res"),[],IntLiteral(1))],
                    [   While(UnaryOp("-",Id("n")),([VarDecl(Id("temp"),[],None)],[Assign(Id("res"),BinaryOp("*",Id("res"),Id("n")))])),
                        Return(CallExpr(Id("fibo"),[Id("res")]))]
                )
                ) 
            ]
        )
        self.assertTrue(TestAST.checkASTGen(input,expect,330))

    def test31(self):
        input = """
                Function: foo
                Body:
                    If a < b Then 
                    ElseIf a == b Then
                    Else a = a + b;
                    EndIf.
                EndBody.
        """
        expect = Program([
            FuncDecl(Id("foo"),[],([],[
                If([(BinaryOp("<",Id("a"),Id("b")),[],[]),
                (BinaryOp("==",Id("a"),Id("b")),[],[])],
                ([],[Assign(Id("a"),BinaryOp("+",Id("a"),Id("b")))]))
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input,expect,331))

    def test32(self):
        input = """
                Function: foo
                Body:
                    If a < b Then 
                    ElseIf a == b Then
                    ElseIf a > b Then
                    Else a = a + b;
                    EndIf.
                EndBody.
        """
        expect = Program([
            FuncDecl(Id("foo"),[],([],[
                If([(BinaryOp("<",Id("a"),Id("b")),[],[]),
                (BinaryOp("==",Id("a"),Id("b")),[],[]),
                (BinaryOp(">",Id("a"),Id("b")),[],[])],
                ([],[Assign(Id("a"),BinaryOp("+",Id("a"),Id("b")))]))
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input,expect,332))

    def test33(self):
        input = """
            Function: fibonacci
            Parameter: n
            Body:
                If n == 1 Then Return 1;
                Else Return n*fibonacci(n-1);
                EndIf.
            EndBody.
        """
        expect = Program([
            FuncDecl(Id("fibonacci"),[VarDecl(Id("n"),[],None)],([],[
                If([(BinaryOp("==",Id("n"),IntLiteral(1)),[],[Return(IntLiteral(1))])],
                ([],[Return(BinaryOp("*",Id("n"),CallExpr(Id("fibonacci"),[BinaryOp("-",Id("n"),IntLiteral(1))])))]))
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input,expect,333))
    
    def test34(self):
        input = """
            Function: fibonacci
            Parameter: n
            Body:
                If n == 1 Then 
                Var: t = 7;
                Return 1;
                Else Return n*fibonacci(n-1);
                EndIf.
            EndBody.
        """
        expect = Program([
            FuncDecl(Id("fibonacci"),[VarDecl(Id("n"),[],None)],([],[
                If([(BinaryOp("==",Id("n"),IntLiteral(1)),[VarDecl(Id("t"),[],IntLiteral(7))],[Return(IntLiteral(1))])],
                ([],[Return(BinaryOp("*",Id("n"),CallExpr(Id("fibonacci"),[BinaryOp("-",Id("n"),IntLiteral(1))])))]))
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input,expect,334))

    def test35(self):
        input = """
            Function: foo
            Parameter: n
            Body:
                a = 10*foo[a*10]-10;
            EndBody.
        """
        expect = Program([
            FuncDecl(Id("foo"),[VarDecl(Id("n"),[],None)],([],[
                Assign(Id("a"),BinaryOp("-",BinaryOp("*",IntLiteral(10),ArrayCell(Id("foo"),[BinaryOp("*",Id("a"),IntLiteral(10))])),IntLiteral(10)))
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input,expect,335))

    def test35(self):
        input = """
            Function: foo
            Parameter: n
            Body:
                a = 10*foo[a*10]-10;
            EndBody.
        """
        expect = Program([
            FuncDecl(Id("foo"),[VarDecl(Id("n"),[],None)],([],[
                Assign(Id("a"),BinaryOp("-",BinaryOp("*",IntLiteral(10),ArrayCell(Id("foo"),[BinaryOp("*",Id("a"),IntLiteral(10))])),IntLiteral(10)))
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input,expect,335))

    def test36(self):
        input = """
            Function: foo
            Parameter: n
            Body:
                "abc"[123] = 10*foo[a*10]-10;
            EndBody.
        """
        expect = Program([
            FuncDecl(Id("foo"),[VarDecl(Id("n"),[],None)],([],[
                Assign(ArrayCell(StringLiteral("abc"),[IntLiteral(123)]),BinaryOp("-",BinaryOp("*",IntLiteral(10),ArrayCell(Id("foo"),[BinaryOp("*",Id("a"),IntLiteral(10))])),IntLiteral(10)))
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input,expect,336))

    def test37(self):
        input = """
            Function: foo
            Parameter: n
            Body:
                (a*b - c*foo()[a])[t] = 10*foo[a*10]-10;
            EndBody.
        """
        expect = Program([
            FuncDecl(Id("foo"),[VarDecl(Id("n"),[],None)],([],[
                Assign(ArrayCell(BinaryOp("-",BinaryOp("*",Id("a"),Id("b")),BinaryOp("*",Id("c"),ArrayCell(CallExpr(Id("foo"),[]),[Id("a")]))),[Id("t")]),BinaryOp("-",BinaryOp("*",IntLiteral(10),ArrayCell(Id("foo"),[BinaryOp("*",Id("a"),IntLiteral(10))])),IntLiteral(10)))
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input,expect,337))

    def test38(self):
        input = """
            Function: foo
            Parameter: n
            Body:
                k = !8%9[{{},{}}];
            EndBody.
        """
        expect = Program([
            FuncDecl(Id("foo"),[VarDecl(Id("n"),[],None)],([],[
                Assign(Id("k"),BinaryOp("%",UnaryOp("!",IntLiteral(8)),ArrayCell(IntLiteral(9),[ArrayLiteral([ArrayLiteral([]),ArrayLiteral([])])])))
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input,expect,338))

    def test39(self):
        input = """
            Function: foo
            Parameter: n
            Body:
                While !n < 10 Do
                    Var: k[5][6][7] = {{},{},{}};
                    foo(k[5]);
                    n = n + 1;
                EndWhile.
            EndBody.
        """
        expect = Program([
            FuncDecl(Id("foo"),[VarDecl(Id("n"),[],None)],([],[
                While(BinaryOp("<",UnaryOp("!",Id("n")),IntLiteral(10)),
                    ([VarDecl(Id("k"),[5,6,7],ArrayLiteral([ArrayLiteral([]),ArrayLiteral([]),ArrayLiteral([])]))],
                    [CallStmt(Id("foo"),[ArrayCell(Id("k"),[IntLiteral(5)])]),
                    Assign(Id("n"),BinaryOp("+",Id("n"),IntLiteral(1)))])
                )
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input,expect,339))

    def test40(self):
        input = """
            Function: foo
            Parameter: n
            Body:
                While True Do
                    Do
                    If True Then
                    EndIf.
                    While True EndDo.
                EndWhile.
            EndBody.
        """
        expect = Program([
            FuncDecl(Id("foo"),[VarDecl(Id("n"),[],None)],([],[
                While(BooleanLiteral(True),([],[
                    Dowhile(([],[
                        If([(BooleanLiteral(True),[],[])],([],[]))
                    ]),BooleanLiteral(True))
                ]))
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input,expect,340))

    def test41(self):
        input ="""  Var: a = 3, b;
                    Function: enQueue
                    Body:
                    If(empty(queue)!=null) Then
                        append(append(append()+8)-9); 
                    EndIf.
                    EndBody.
                """
        expect=Program([
            VarDecl(Id("a"),[],IntLiteral(3)),
            VarDecl(Id("b"),[],None),
            FuncDecl(Id("enQueue"),[],([],[
                If([(
                    BinaryOp("!=",CallExpr(Id("empty"),[Id("queue")]),Id("null")),[],
                    [CallStmt(Id("append"),[BinaryOp("-",
                    CallExpr(Id("append"),[BinaryOp("+",
                    CallExpr(Id("append"),[]),IntLiteral(8))]),IntLiteral(9))])])],([],[]))
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input,expect,341))

    def test42(self):
        input ="""
                    Function: foo1
                    Body:
                        If True Then Return foo1(7);
                        ElseIf False Then Return foo2(foo(58)+array[5]+True);
                        EndIf.
                    EndBody.
                """
        expect=Program([
            FuncDecl(Id("foo1"),[],([],[
                If([(BooleanLiteral(True),[],[Return(CallExpr(Id("foo1"),[IntLiteral(7)]))]),
                (BooleanLiteral(False),[],[Return(CallExpr(Id("foo2"),
                [BinaryOp("+",BinaryOp("+",CallExpr(Id("foo"),[IntLiteral(58)]),ArrayCell(Id("array"),[IntLiteral(5)])),BooleanLiteral(True))]))])],([],[]))
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input,expect,342))

    def test43(self):
        input = """
            Var: x[5] = {False, False, False, False, False};
        """
        expect = Program([
            VarDecl(Id("x"),[5],ArrayLiteral([BooleanLiteral(False),BooleanLiteral(False),BooleanLiteral(False),BooleanLiteral(False),BooleanLiteral(False)]))
        ])

        self.assertTrue(TestAST.checkASTGen(input,expect,343))

    def test44(self):
        input = """
            Function: gcd
            Parameter: a, b
            Body:
                Return a[1 - (0x1129FC >=. kfc)*foo(a,b)];
            EndBody.
        """
        expect = Program([
            FuncDecl(Id("gcd"),[
                VarDecl(Id("a"),[],None),
                VarDecl(Id("b"),[],None)
            ],([],[
                Return(ArrayCell(Id("a"),[
                    BinaryOp("-",IntLiteral(1),
                    BinaryOp("*",BinaryOp(">=.",IntLiteral(1124860),Id("kfc")),
                    CallExpr(Id("foo"),[Id("a"),Id("b")])))
                ]))
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input,expect,344))

    def test45(self):
        input = """
            Function: foo
            Body:
                For(i = {False, False}*2+7-8[6],i<25,i+1) Do
                    Var: i[5][2][2];
                    Var: l;
                    Var: ts = False;
                    If a > b Then
                    ElseIf a > b Then
                    ElseIf a > b Then
                    Else a = a + b;
                    EndIf.
                    While a == b Do
                    EndWhile.
                EndFor.
            EndBody.
        """
        expect = Program([
            FuncDecl(Id("foo"),[],([],[
                For(Id("i"),
                BinaryOp("-",
                BinaryOp("+",
                BinaryOp("*",ArrayLiteral([BooleanLiteral(False),BooleanLiteral(False)]),IntLiteral(2)),IntLiteral(7)),ArrayCell(IntLiteral(8),[IntLiteral(6)])),
                BinaryOp("<",Id("i"),IntLiteral(25)),
                BinaryOp("+",Id("i"),IntLiteral(1)),([
                VarDecl(Id("i"),[5,2,2],None),
                VarDecl(Id("l"),[],None),
                VarDecl(Id("ts"),[],BooleanLiteral(False))
                ],[
                If([(
                    BinaryOp(">",Id("a"),Id("b")),[],[]
                ),(
                    BinaryOp(">",Id("a"),Id("b")),[],[]
                ),(
                    BinaryOp(">",Id("a"),Id("b")),[],[]
                )],([],[
                    Assign(Id("a"),BinaryOp("+",Id("a"),Id("b")))
                ])),
                While(BinaryOp("==",Id("a"),Id("b")),([],[]))
            ]))
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input,expect,345))

    def test46(self):
        input = """
            Function: foo
            Body:
                a = a*7+6[8]%3-8+(-9);
            EndBody.
        """
        expect = Program([
            FuncDecl(Id("foo"),[],([],[
                Assign(Id("a"),
                BinaryOp("+",
                BinaryOp("-",
                BinaryOp("+",
                BinaryOp("*",Id("a"),IntLiteral(7)),
                BinaryOp("%",ArrayCell(IntLiteral(6),[IntLiteral(8)]),IntLiteral(3))),
                IntLiteral(8)),
                UnaryOp("-",IntLiteral(9))))
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input,expect,346))

    def test47(self):
        input = """
            Function: foo
            Body:
                a = foo()-89*0XF*!8[8];
            EndBody.
        """
        expect = Program([
            FuncDecl(Id("foo"),[],([],[
                Assign(Id("a"),
                BinaryOp("-",
                CallExpr(Id("foo"),[]),
                BinaryOp("*",
                BinaryOp("*",IntLiteral(89),IntLiteral(15)),
                UnaryOp("!",ArrayCell(IntLiteral(8),[IntLiteral(8)])))))
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input,expect,347))

    def test48(self):
        input = """
            Function: foo
            Body:
            EndBody.
            Function: foo1
            Body:
            EndBody.
        """
        expect = Program([FuncDecl(Id("foo"),[],([],[])),
        FuncDecl(Id("foo1"),[],([],[])),])
        self.assertTrue(TestAST.checkASTGen(input,expect,348))

    def test49(self):
        input = """
            Function: foo
            Body:
                t = a[a[a[a[5]]]];
            EndBody.
        """
        expect = Program([
            FuncDecl(Id("foo"),[],([],[
                Assign(Id("t"),
                    ArrayCell(Id("a"),[
                        ArrayCell(Id("a"),[
                            ArrayCell(Id("a"),[
                                ArrayCell(Id("a"),[
                                    IntLiteral(5)
                                ])
                            ])
                        ])
                    ])
                )
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input,expect,349))

    def test50(self):
        input = """
            Function: foo
            Body:
                t = a[a[a[a[5]]]];
                While (a==5)[8] Do
                EndWhile.
                Do 
                While a==5[8] EndDo.
            EndBody.
        """
        expect = Program([
            FuncDecl(Id("foo"),[],([],[
                Assign(Id("t"),
                    ArrayCell(Id("a"),[
                        ArrayCell(Id("a"),[
                            ArrayCell(Id("a"),[
                                ArrayCell(Id("a"),[
                                    IntLiteral(5)
                                ])
                            ])
                        ])
                    ])
                ),
                While(ArrayCell(BinaryOp("==",Id("a"),IntLiteral(5)),[IntLiteral(8)]),([],[])),
                Dowhile(([],[]),BinaryOp("==",Id("a"),ArrayCell(IntLiteral(5),[IntLiteral(8)])))
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input,expect,350))

    def test51(self):
        input = """
            Function: foo
            Body:
                t = a[a[a[a[5]]]];
                While (a==5)[8] Do
                EndWhile.
                Do Var: t[1][2][3] = "\\n\\t";
                While a==5[8] EndDo.
            EndBody.
        """
        expect = Program([
            FuncDecl(Id("foo"),[],([],[
                Assign(Id("t"),
                    ArrayCell(Id("a"),[
                        ArrayCell(Id("a"),[
                            ArrayCell(Id("a"),[
                                ArrayCell(Id("a"),[
                                    IntLiteral(5)
                                ])
                            ])
                        ])
                    ])
                ),
                While(ArrayCell(BinaryOp("==",Id("a"),IntLiteral(5)),[IntLiteral(8)]),([],[])),
                Dowhile(([
                    VarDecl(Id("t"),[1,2,3],StringLiteral("\\n\\t"))
                ],[]),BinaryOp("==",Id("a"),ArrayCell(IntLiteral(5),[IntLiteral(8)])))
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input,expect,351))

    def test52(self):
        input = """
            Function: foo
            Body:
                a = a*7+6[8]%3-8+(-9);
                For (i = 0, i * 5, i + t + i) Do
                    If True Then print("Beautiful");
                    EndIf.
                EndFor.
            EndBody.
        """
        expect = Program([
            FuncDecl(Id("foo"),[],([],[
                Assign(Id("a"),
                BinaryOp("+",
                BinaryOp("-",
                BinaryOp("+",
                BinaryOp("*",Id("a"),IntLiteral(7)),
                BinaryOp("%",ArrayCell(IntLiteral(6),[IntLiteral(8)]),IntLiteral(3))),
                IntLiteral(8)),
                UnaryOp("-",IntLiteral(9)))),
                For(Id("i"),IntLiteral(0),BinaryOp("*",Id("i"),IntLiteral(5)),
                BinaryOp("+",BinaryOp("+",Id("i"),Id("t")),Id("i")),
                ([],[
                    If([(BooleanLiteral(True),[],[CallStmt(Id("print"),[StringLiteral("Beautiful")])])],([],[]))
                ]))
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input,expect,352))

    def test53(self):
        input = """
            Function: foo
            Body:
                a = a*7+6[8]%3-8+(-9);
                For (i = 0, i * 5, i + t + i) Do
                    If True Then print("Beautiful");
                    EndIf.
                EndFor.
                If True Then 
                    If True Then
                    EndIf.
                EndIf.

            EndBody.
        """
        expect = Program([
            FuncDecl(Id("foo"),[],([],[
                Assign(Id("a"),
                BinaryOp("+",
                BinaryOp("-",
                BinaryOp("+",
                BinaryOp("*",Id("a"),IntLiteral(7)),
                BinaryOp("%",ArrayCell(IntLiteral(6),[IntLiteral(8)]),IntLiteral(3))),
                IntLiteral(8)),
                UnaryOp("-",IntLiteral(9)))),
                For(Id("i"),IntLiteral(0),BinaryOp("*",Id("i"),IntLiteral(5)),
                BinaryOp("+",BinaryOp("+",Id("i"),Id("t")),Id("i")),
                ([],[
                    If([(BooleanLiteral(True),[],[CallStmt(Id("print"),[StringLiteral("Beautiful")])])],([],[]))
                ])),
                If([(BooleanLiteral(True),[],[
                    If([(BooleanLiteral(True),[],[])],([],[]))
                ])],([],[]))
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input,expect,353))

    def test54(self):
        input="""Function: foo
            Parameter:a,b[23]
            Body:
            While a Do
            If a==1 Then
            EndIf.
            EndWhile.
            EndBody.
            """
        expect=Program(
                [FuncDecl(Id("foo"),[VarDecl(Id("a"),[],None),VarDecl(Id("b"),[23],None)],
                ([],[While(Id("a"),([],[If([(BinaryOp("==",Id("a"),IntLiteral(1)),[],[])],([],[])),]))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,354))

    def test55(self):
        input="""Function: foo
            Parameter:a,b[23]
            Body:
            While a Do
            Var: a[5] = {0O12,12.e4};
            If a==1 Then
            EndIf.
            a =  a != "HCMUT\\n";
            EndWhile.
            EndBody.
            """
        expect=Program(
                [FuncDecl(Id("foo"),[VarDecl(Id("a"),[],None),VarDecl(Id("b"),[23],None)],
                ([],[While(Id("a"),([
                    VarDecl(Id("a"),[5],ArrayLiteral([IntLiteral(10),FloatLiteral(12.e4)]))
                ],[
                    If([(BinaryOp("==",Id("a"),IntLiteral(1)),[],[])],([],[])),
                    Assign(Id("a"),BinaryOp("!=",Id("a"),StringLiteral("HCMUT\\n")))
                ]))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,355))

    def test56(self):
        input="""Function: foo
            Parameter:a,b[23]
            Body:
            While a Do
            If a==1 Then
                If False Then
                    If True Then
                        If True Then
                        EndIf.
                    EndIf.
                EndIf.
            EndIf.
            EndWhile.
            EndBody.
            """
        expect=Program(
                [FuncDecl(Id("foo"),[VarDecl(Id("a"),[],None),VarDecl(Id("b"),[23],None)],
                ([],[While(Id("a"),([],[If([(BinaryOp("==",Id("a"),IntLiteral(1)),[],[
                    If([(BooleanLiteral(False),[],[
                        If([(BooleanLiteral(True),[],[
                            If([(BooleanLiteral(True),[],[])],([],[]))
                        ])],([],[]))
                    ])],([],[]))
                ])],([],[])),]))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,356))

    def test57(self):
        input="""Function: foo
            Parameter:a,b[23]
            Body:
            While a Do
            If a==1 Then
            Else If True Then
                Else If False Then
                    EndIf.
                EndIf.
            EndIf.
            EndWhile.
            EndBody.
            """
        expect=Program(
                [FuncDecl(Id("foo"),[VarDecl(Id("a"),[],None),VarDecl(Id("b"),[23],None)],
                ([],[While(Id("a"),([],[If([(BinaryOp("==",Id("a"),IntLiteral(1)),[],[])],([],[
                    If([(BooleanLiteral(True),[],[])],([],[
                        If([(BooleanLiteral(False),[],[])],([],[]))
                    ]))
                ])),]))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,357))
    
    def test58(self):
        input = """
            Function: gcd
            Parameter: a, b
            Body:
                While(a) Do
                    If a == 5 Then
                        Break;
                    EndIf.
                    Continue;
                EndWhile.
                Return a[1 - (0x1129FC >=. kfc)*foo(a,b)];
            EndBody.
        """
        expect = Program([
            FuncDecl(Id("gcd"),[
                VarDecl(Id("a"),[],None),
                VarDecl(Id("b"),[],None)
            ],([],[While(Id("a"),([],[
                If([(BinaryOp("==",Id("a"),IntLiteral(5)),[],[Break()])],([],[])),
                Continue()
            ])),
                Return(ArrayCell(Id("a"),[
                    BinaryOp("-",IntLiteral(1),
                    BinaryOp("*",BinaryOp(">=.",IntLiteral(1124860),Id("kfc")),
                    CallExpr(Id("foo"),[Id("a"),Id("b")])))
                ]))
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input,expect,358))

    def test59(self):
        input = """
                    Var: a;
                    Function: foo
                        Parameter: a,b[4]
                        Body:
                            Var: a[2] = {1,2};
                            motdemsay = a && b || c == f && d + e;
                        EndBody.
                """
        expect = Program([VarDecl(Id("a"), [], None),
                FuncDecl(Id("foo"),
                    [
                        VarDecl(Id("a"), [], None),
                        VarDecl(Id("b"), [4], None)
                    ],
                    ([VarDecl(Id("a"), [2], ArrayLiteral([IntLiteral(1), IntLiteral(2)]))],
                        [Assign(Id("motdemsay"),
                            BinaryOp("==",
                            BinaryOp("||",
                            BinaryOp("&&", Id("a"), Id("b")),Id("c")),
                            BinaryOp("&&",Id("f"),
                            BinaryOp("+", Id("d"), Id("e")))))]))])
        self.assertTrue(TestAST.checkASTGen(input,expect,359))

    def test60(self):
        input = """
                    Function: main Body:
                        a = 1 + 2 - 3 + 4\\foo(4*a[5]+10);
                        Return ((a <= b) || c);
                    EndBody.
                """
        expect = Program(
            [FuncDecl(
                    Id("main"),
                    [

                    ],
                    ([

                    ],
                        [
                        Assign(
                            Id("a"),
                            BinaryOp(
                                "+",
                                BinaryOp(
                                    "-",
                                    BinaryOp("+", IntLiteral(1),
                                             IntLiteral(2)),
                                    IntLiteral(3)
                                ),
                                BinaryOp(
                                    "\\",
                                    IntLiteral(4),
                                    CallExpr(
                                        Id("foo"),
                                        [
                                            BinaryOp(
                                                "+",
                                                BinaryOp(
                                                    "*",
                                                    IntLiteral(4),
                                                    ArrayCell(
                                                        Id("a"), [IntLiteral(5)])
                                                ),
                                                IntLiteral(10)
                                            )
                                        ]
                                    )
                                )
                            )
                        ),
                        Return(
                            BinaryOp(
                                "||",
                                BinaryOp("<=", Id("a"), Id("b")),
                                Id("c")
                            )
                        )
                    ])
                )
            ]
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 360))

    def test361(self):
        input = """
                    Function: test
                        Parameter: x, y, z
                        Body:
                            For (i = 0, i > 0, i + 1) Do
                                x = a + b +. x;
                                y = a + 12000.;
                                z = b || x && c;
                            EndFor.
                        EndBody.
                """
        expect = Program(
            [
                FuncDecl(
                    Id("test"),
                    [
                        VarDecl(Id("x"), [], None),
                        VarDecl(Id("y"), [], None),
                        VarDecl(Id("z"), [], None)
                    ],
                    ([],[For(Id("i"),IntLiteral(0),BinaryOp(">", Id("i"), IntLiteral(0)),BinaryOp("+", Id("i"), IntLiteral(1)),([],
                            [
                                Assign(Id("x"),
                                       BinaryOp("+.",
                                                BinaryOp("+", Id("a"), Id("b")), Id("x")),
                                       ),
                                Assign(Id("y"), BinaryOp(
                                    "+", Id("a"), FloatLiteral(12000.))),
                                Assign(Id("z"),
                                       BinaryOp("&&", BinaryOp("||", Id("b"), Id("x")), Id("c")))
                            ])
                        )
                    ])
                )
            ]
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 361))
    
    def test62(self):
        input = """
                    Function: main
                    Body:
                        Do 
                            a = 10;
                            If (a >= 10.e999 *3 - 76) Then
                                For(i = 100, i =/= 100.93, i - i) Do
                                    read();
                                    print(arr[fo(100, True, False) && "3" + 9]);
                                EndFor.
                            EndIf.
                        While i > 1 % 10
                        EndDo.
                    EndBody.
                """
        expect = Program(
            [
                FuncDecl(
                    Id("main"),
                    [

                    ],
                    ([

                    ],
                        [
                        Dowhile(
                            (
                                [],
                                [
                                    Assign(Id("a"), IntLiteral(10)),
                                    If(
                                        [(
                                            BinaryOp(
                                                ">=",
                                                Id("a"),
                                                BinaryOp(
                                                    "-",
                                                    BinaryOp(
                                                        "*",
                                                        FloatLiteral(10.e999),
                                                        IntLiteral(3)
                                                    ),
                                                    IntLiteral(76)
                                                )
                                            ),
                                            [],
                                            [
                                                For(
                                                    Id("i"),
                                                    IntLiteral(100),
                                                    BinaryOp(
                                                        "=/=", Id("i"), FloatLiteral(100.93)),
                                                    BinaryOp(
                                                        "-", Id("i"), Id("i")),
                                                    ([],
                                                     [
                                                        CallStmt(
                                                            Id("read"), []),
                                                        CallStmt(
                                                            Id("print"),
                                                            [
                                                                ArrayCell(
                                                                    Id("arr"),
                                                                    [
                                                                        BinaryOp(
                                                                            "&&",
                                                                            CallExpr(
                                                                                Id("fo"),
                                                                                [IntLiteral(100), BooleanLiteral(
                                                                                    True), BooleanLiteral(False)]
                                                                            ),
                                                                            BinaryOp(
                                                                                "+", StringLiteral("3"), IntLiteral(9))
                                                                        )
                                                                    ]
                                                                )
                                                            ]
                                                        )
                                                    ])
                                                )
                                            ]
                                        )],
                                        ([], [])
                                    )
                                ]
                            ),
                            BinaryOp(
                                ">",
                                Id("i"),
                                BinaryOp("%", IntLiteral(1), IntLiteral(10))
                            )
                        )
                    ])
                )
            ]
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 362))

    def test63(self):
        input = """
                    Var: date, month, year;
                    Function: print_date_month_year
                        Body:
                            date = read();
                            month = read();
                            year = read();
                            print(string_of_int(date) + "/" + string_of_int(month) + "/" + string_of_int(year));
                        EndBody.
                """
        expect = Program(
            [
                VarDecl(Id("date"), [], None),
                VarDecl(Id("month"), [], None),
                VarDecl(Id("year"), [], None),
                FuncDecl(
                    Id("print_date_month_year"),
                    [

                    ],
                    ([

                    ],
                        [
                        Assign(Id("date"), CallExpr(Id("read"), [])),
                        Assign(Id("month"), CallExpr(Id("read"), [])),
                        Assign(Id("year"), CallExpr(Id("read"), [])),
                        CallStmt(
                            Id("print"),
                            [BinaryOp(
                                "+",
                                BinaryOp(
                                    "+",
                                    BinaryOp(
                                        "+",
                                        BinaryOp(
                                            "+",
                                            CallExpr(Id("string_of_int"), [
                                                     Id("date")]),
                                            StringLiteral("/")
                                        ),
                                        CallExpr(Id("string_of_int"),
                                                 [Id("month")])
                                    ),
                                    StringLiteral("/")
                                ),
                                CallExpr(Id("string_of_int"), [Id("year")])
                            )]
                        )
                    ])
                )
            ]
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 363))

    def test64(self):
        input = """
                    Function: main Body:
                    str1 = "\\b\\t\\n\\r\\f\\'  String";
                    str2 = str1 * 10 \ foo(4,1,a[2][a[2][3]]);
                    EndBody.
                """
        expect = Program(
            [
                FuncDecl(
                    Id("main"),
                    [

                    ],
                    ([

                    ],
                        [
                        Assign(
                            Id("str1"),
                            StringLiteral("\\b\\t\\n\\r\\f\\'  String")
                        ),
                        Assign(
                            Id("str2"),
                            BinaryOp(
                                "\\",
                                BinaryOp("*", Id("str1"), IntLiteral(10)),
                                CallExpr(
                                    Id("foo"),
                                    [IntLiteral(4), IntLiteral(1),
                                     ArrayCell(
                                        Id("a"),
                                        [IntLiteral(2),
                                         ArrayCell(
                                            Id("a"),
                                            [IntLiteral(2), IntLiteral(3)]
                                        )]
                                    )]
                                )
                            )
                        )
                    ])
                )
            ]
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 364))

    def test65(self):
        input = """
                    Var: x= 1.0;
                    Var: y = 10.e03;
                    Function: some_foo
                        Parameter: none
                        Body:
                            string_of_int(x + y - z * k);
                            findIndex_od123(array[10 + foo] \ 1283.9374e-18);
                        EndBody.
                """
        expect = Program(
            [
                VarDecl(Id("x"), [], FloatLiteral(1.0)),
                VarDecl(Id("y"), [], FloatLiteral(10.e03)),
                FuncDecl(
                    Id("some_foo"),
                    [
                        VarDecl(Id("none"), [], None)
                    ],
                    ([

                    ],
                        [
                        CallStmt(Id("string_of_int"), [
                            BinaryOp("-",
                                     BinaryOp("+", Id("x"), Id("y")),
                                     BinaryOp("*", Id("z"), Id("k")))
                        ]),
                        CallStmt(
                            Id("findIndex_od123"),
                            [
                                BinaryOp("\\",
                                         ArrayCell(
                                             Id("array"),
                                             [BinaryOp(
                                                 "+", IntLiteral(10), Id("foo"))]
                                         ),
                                         FloatLiteral(1283.9374e-18))
                            ]
                        )
                    ])
                )
            ]
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 365))

    def test66(self):
        input = """
             Function: foo 
                Parameter: a[5], b[10] 
                Body: 
                    Do 
                        c = b[a[b[8+a[7\\b[8]]]]];
                    While c < 25 || d + -.9e2
                    EndDo.
                EndBody.
            """
        expect = Program([
            FuncDecl(Id("foo"),[
                VarDecl(Id("a"),[5],None),
                VarDecl(Id("b"),[10],None)
            ],([],[
                Dowhile(([],[
                    Assign(Id("c"),ArrayCell(Id("b"),[
                        ArrayCell(Id("a"),[
                            ArrayCell(Id("b"),[
                                BinaryOp("+",IntLiteral(8),
                                ArrayCell(Id("a"),[
                                    BinaryOp("\\",IntLiteral(7),
                                    ArrayCell(Id("b"),[IntLiteral(8)]))
                                ]))
                            ])
                        ])
                    ]))
                ]),
                BinaryOp("<",Id("c"),
                BinaryOp("||",IntLiteral(25),
                BinaryOp("+",Id("d"),UnaryOp("-.",FloatLiteral(9e2))))))
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input, expect, 366))

    def test67(self):
        input = """
             Function: foo 
                Parameter: a[5], b[10] 
                Body: 
                    Do 
                        c = b[a[b[8+a[7\\b[8]]]]];
                        d = "ag"[5>a[8]];
                        While i < 50 Do **do nothing**
                        EndWhile.
                    While c < 25 || d + -.9e2
                    EndDo.
                EndBody.
            """
        expect = Program([
            FuncDecl(Id("foo"),[
                VarDecl(Id("a"),[5],None),
                VarDecl(Id("b"),[10],None)
            ],([],[
                Dowhile(([],[
                    Assign(Id("c"),ArrayCell(Id("b"),[
                        ArrayCell(Id("a"),[
                            ArrayCell(Id("b"),[
                                BinaryOp("+",IntLiteral(8),
                                ArrayCell(Id("a"),[
                                    BinaryOp("\\",IntLiteral(7),
                                    ArrayCell(Id("b"),[IntLiteral(8)]))
                                ]))
                            ])
                        ])
                    ])),
                    Assign(Id("d"),ArrayCell(StringLiteral("ag"),[
                        BinaryOp(">",IntLiteral(5),ArrayCell(Id("a"),[IntLiteral(8)]))
                    ])),
                    While(BinaryOp("<",Id("i"),IntLiteral(50)),([],[]))
                ]),
                BinaryOp("<",Id("c"),
                BinaryOp("||",IntLiteral(25),
                BinaryOp("+",Id("d"),UnaryOp("-.",FloatLiteral(9e2))))))
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input, expect, 367))

    def test68(self):
        input = """
            Function: main
            Body:
                foo(foo());
            EndBody.
        """
        expect = Program([
            FuncDecl(Id("main"),[],([],[
                CallStmt(Id("foo"),[CallExpr(Id("foo"),[])])
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input, expect, 368))

    def test69(self):
        input = """
                    Function: checkSub
                    Body:
                        If (!-ascii) Then
                            do_every_thing_can_do();
                        EndIf.
                    EndBody.
                """
        expect = Program(
            [
                FuncDecl(
                    Id("checkSub"),
                    [

                    ],
                    ([

                    ],
                        [
                        If(
                            [(
                                UnaryOp("!", UnaryOp("-", Id("ascii"))),
                                [],
                                [CallStmt(Id("do_every_thing_can_do"), [])]
                            )],
                            ([], [])
                        )
                    ])
                )
            ]
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 369))

    def test70(self):
        input = r"""
                    Function: calculate
                    Parameter: a, b
                    Body:
                        If char=="+" Then
                            Return a + b;
                        ElseIf char=="-" Then
                            Return a -b;
                        ElseIf char=="*" Then
                            Return a*b;
                        ElseIf char=="\\" Then
                            Return a\b;
                        EndIf.
                    EndBody.
                    Function: main
                    Body:
                        a = read();
                        b = read();
                        op = read();
                        print(call(a,b,op));
                    EndBody.
                """
        expect = Program(
            [
                FuncDecl(
                    Id("calculate"),
                    [
                        VarDecl(Id("a"), [], None),
                        VarDecl(Id("b"), [], None)
                    ],
                    ([

                    ],
                        [
                        If(
                            [
                                (
                                    BinaryOp("==", Id("char"),
                                             StringLiteral("+")),
                                    [],
                                    [Return(BinaryOp("+", Id("a"), Id("b")))]
                                ),
                                (
                                    BinaryOp("==", Id("char"),
                                             StringLiteral("-")),
                                    [],
                                    [Return(BinaryOp("-", Id("a"), Id("b")))]
                                ),
                                (
                                    BinaryOp("==", Id("char"),
                                             StringLiteral("*")),
                                    [],
                                    [Return(BinaryOp("*", Id("a"), Id("b")))]
                                ),
                                (
                                    BinaryOp("==", Id("char"),
                                             StringLiteral("\\\\")),
                                    [],
                                    [Return(BinaryOp("\\", Id("a"), Id("b")))]
                                ),
                            ],
                            ([], [])
                        )
                    ])
                ),
                FuncDecl(
                    Id("main"),
                    [],
                    (
                        [],
                        [
                            Assign(Id("a"), CallExpr(Id("read"), [])),
                            Assign(Id("b"), CallExpr(Id("read"), [])),
                            Assign(Id("op"), CallExpr(Id("read"), [])),
                            CallStmt(Id("print"), [CallExpr(
                                Id("call"), [Id("a"), Id("b"), Id("op")])])
                        ]
                    )
                )
            ]
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 370))

    def test71(self):
        input = """
                    Var: a[5] = {1,4,3,2,0};
                    Var: b[2][3]={{1,2,3},{4,5,6}};
                    Function: check
                        Body:
                            int_of_float();
                            foo(-a[foo(a[foo(a[foo])])]);
                        EndBody.
                """
        expect = Program([
            VarDecl(Id("a"),[5],ArrayLiteral([IntLiteral(1),IntLiteral(4),IntLiteral(3),IntLiteral(2),IntLiteral(0)])),
            VarDecl(Id("b"),[2,3],ArrayLiteral([ArrayLiteral([IntLiteral(1),IntLiteral(2),IntLiteral(3)]),ArrayLiteral([IntLiteral(4),IntLiteral(5),IntLiteral(6)])])),
            FuncDecl(Id("check"),[],([],[
                CallStmt(Id("int_of_float"),[]),
                CallStmt(Id("foo"),[
                    UnaryOp("-",ArrayCell(Id("a"),[
                        CallExpr(Id("foo"),[
                            ArrayCell(Id("a"),[
                                CallExpr(Id("foo"),[
                                    ArrayCell(Id("a"),[Id("foo")])
                                ])
                            ])
                        ])
                    ]))
                ])
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input, expect, 371))   

    def test72(self):
        input = """
        Function: fibonacci
        Parameter: n, o
        Body: 
            If (n == 1) || (n ==2) Then Return 1;
            Else Return fibonacci(n - 1) + fibonacci(n - 2);
            EndIf.
        EndBody. """

        expect = Program([
            FuncDecl(Id("fibonacci"),[
                VarDecl(Id("n"),[],None),
                VarDecl(Id("o"),[],None)
            ],([],[
                If([(BinaryOp("||",
                BinaryOp("==",Id("n"),IntLiteral(1)),
                BinaryOp("==",Id("n"),IntLiteral(2))),[],[
                    Return(IntLiteral(1))
                ])],([],[
                    Return(BinaryOp("+",
                    CallExpr(Id("fibonacci"),[BinaryOp("-",Id("n"),IntLiteral(1))]),
                    CallExpr(Id("fibonacci"),[BinaryOp("-",Id("n"),IntLiteral(2))])))
                ]))
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input, expect, 372))   

    def test73(self):
        input = """
            Function: factorial
            Parameter: col
            Body:
                bray[insert(foo + a[1][2][factorial()*0o714])] = arr[b[1][2][3]];
                printLn(factorial);
            EndBody.
            """
        expect = Program([
            FuncDecl(Id("factorial"),[VarDecl(Id("col"),[],None)],([],[
                Assign(ArrayCell(Id("bray"),[
                    CallExpr(Id("insert"),[
                        BinaryOp("+",Id("foo"),
                        ArrayCell(Id("a"),[
                            IntLiteral(1),
                            IntLiteral(2),
                            BinaryOp("*",
                            CallExpr(Id("factorial"),[]),
                            IntLiteral(460))]))])]),
                            ArrayCell(Id("arr"),[ArrayCell(Id("b"),
                            [IntLiteral(1),IntLiteral(2),IntLiteral(3)])])),
                            CallStmt(Id("printLn"),[Id("factorial")])]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 373)) 

    def test74(self):
        input = """
        Function: fact
            Body:
                Var: k=20;
                If n<=.1 Then Return 1;
                Else Return n=/=fact(n-1)[25][25+foo()||45*63];
                EndIf.
            EndBody.
        """
        expect = Program([
            FuncDecl(Id("fact"),[],([VarDecl(Id("k"),[],IntLiteral(20))],[
                If([(BinaryOp("<=.",Id("n"),IntLiteral(1)),[],[
                    Return(IntLiteral(1))
                ])],([],[
                    Return(BinaryOp("=/=",Id("n"),
                    ArrayCell(CallExpr(Id("fact"),[
                        BinaryOp("-",Id("n"),IntLiteral(1))
                    ]),[
                        IntLiteral(25),
                        BinaryOp("||",
                        BinaryOp("+",IntLiteral(25),CallExpr(Id("foo"),[])),
                        BinaryOp("*",IntLiteral(45),IntLiteral(63)))
                    ])))
                ]))          
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input, expect, 374)) 

    def test75(self):
        input = """
            Function: fact
            Body:
                Var: k=20;
                If n<=.1 Then Return 1;
                ElseIf --.(!n) Then **do something** 
                Else Return n=/=fact(n-1)[25][25+foo()||45*63];
                EndIf.
            EndBody.
        """
        expect = Program([
            FuncDecl(Id("fact"),[],([VarDecl(Id("k"),[],IntLiteral(20))],[
                If([(BinaryOp("<=.",Id("n"),IntLiteral(1)),[],[
                    Return(IntLiteral(1))
                ]),(UnaryOp("-",UnaryOp("-.",UnaryOp("!",Id("n")))),[],[])],([],[
                    Return(BinaryOp("=/=",Id("n"),
                    ArrayCell(CallExpr(Id("fact"),[
                        BinaryOp("-",Id("n"),IntLiteral(1))
                    ]),[
                        IntLiteral(25),
                        BinaryOp("||",
                        BinaryOp("+",IntLiteral(25),CallExpr(Id("foo"),[])),
                        BinaryOp("*",IntLiteral(45),IntLiteral(63)))
                    ])))
                ]))          
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input, expect, 375)) 

    def test76(self):
        input = """
                    Function: factorial
                        Parameter: n
                        Body:
                            If n <=. 1.0000e0 Then
                                Return 1;
                            Else Return n*factorial(n - 1);
                            EndIf.
                        EndBody.
                    Function: main
                        Body:
                            print("Do nothing");
                        EndBody.
                """
        expect = Program(
            [
                FuncDecl(
                    Id("factorial"),
                    [
                        VarDecl(Id("n"), [], None)
                    ],
                    ([

                    ],
                        [
                        If(
                            [(
                                BinaryOp("<=.", Id("n"),
                                         FloatLiteral(1.0000e0)),
                                [],
                                [Return(IntLiteral(1))]
                            )],
                            ([],
                             [Return(
                                 BinaryOp(
                                     "*",
                                     Id("n"),
                                     CallExpr(
                                         Id("factorial"),
                                         [BinaryOp("-", Id("n"),
                                                   IntLiteral(1))]
                                     )
                                 )
                             )])
                        )
                    ])
                ),
                FuncDecl(
                    Id("main"),
                    [],
                    (
                        [],
                        [CallStmt(Id("print"), [StringLiteral("Do nothing")])]
                    )
                )
            ]
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 376))
    def test77(self):
        input = """
                    Function: createTable
                    Body:
                        Var: j=1;
                        Var: output = "<table border=\\'1\\' width=\\'500\\' cellspacing=\\'0\\'cellpadding=\\'5\\'>";
                    EndBody.
                """
        expect = Program(
            [
                FuncDecl(
                    Id("createTable"),
                    [

                    ],
                    ([
                        VarDecl(Id("j"), [], IntLiteral(1)),
                        VarDecl(Id("output"), [],
                                StringLiteral("<table border=\\'1\\' width=\\'500\\' cellspacing=\\'0\\'cellpadding=\\'5\\'>"))
                    ],
                        [

                    ])
                )
            ]
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 377))

    def test78(self):
        input = """
            Function: foo
            Body:
                "abc"["abc"] = "bcd";
            EndBody.
        """
        expect = Program([
            FuncDecl(Id("foo"),[],([],[
                Assign(ArrayCell(StringLiteral("abc"),[StringLiteral("abc")]),StringLiteral("bcd"))
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input, expect, 378))

    def test79(self):
        input = """
            Function: foo
            Body:
                "abc"["abc"][0x123] = "bcd";
            EndBody.
        """
        expect = Program([
            FuncDecl(Id("foo"),[],([],[
                Assign(ArrayCell(StringLiteral("abc"),[StringLiteral("abc"),IntLiteral(291)]),StringLiteral("bcd"))
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input, expect, 379))

    def test80(self):
        input = """
            Function: foo
            Body:
                "abc"["abc"][0x123] = "bcd"["bcd"+"aab"];
            EndBody.
        """
        expect = Program([
            FuncDecl(Id("foo"),[],([],[
                Assign(ArrayCell(StringLiteral("abc"),[StringLiteral("abc"),IntLiteral(291)]),
                ArrayCell(StringLiteral("bcd"),[BinaryOp("+",StringLiteral("bcd"),StringLiteral("aab"))]))
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input, expect, 380))

    def test81(self):
        input = """
            Function: foo
            Body:
                "abc"["abc"][0x123] = "bcd"["bcd"+"aab"];
                foo("abc"[abc]);
            EndBody.
        """
        expect = Program([
            FuncDecl(Id("foo"),[],([],[
                Assign(ArrayCell(StringLiteral("abc"),[StringLiteral("abc"),IntLiteral(291)]),
                ArrayCell(StringLiteral("bcd"),[BinaryOp("+",StringLiteral("bcd"),StringLiteral("aab"))])),
                CallStmt(Id("foo"),[ArrayCell(StringLiteral("abc"),[Id("abc")])])
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input, expect, 381))

    def test82(self):
        input = """
            Function: foo
            Parameter: foo, foo[1][0O11], foo2[2][0o11]
            Body:
                "abc"["abc"][0x123] = "bcd"["bcd"+"aab"];
                foo("abc"[abc]);
            EndBody.
        """
        expect = Program([
            FuncDecl(Id("foo"),[
                VarDecl(Id("foo"),[],None),
                VarDecl(Id("foo"),[1,9],None),
                VarDecl(Id("foo2"),[2,9],None)
            ],([],[
                Assign(ArrayCell(StringLiteral("abc"),[StringLiteral("abc"),IntLiteral(291)]),
                ArrayCell(StringLiteral("bcd"),[BinaryOp("+",StringLiteral("bcd"),StringLiteral("aab"))])),
                CallStmt(Id("foo"),[ArrayCell(StringLiteral("abc"),[Id("abc")])])
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input, expect, 382))

    def test83(self):
        input = """
            Function: foo
            Parameter: foo, foo[1][0O111], foo2[0XAC][0o11]
            Body:
                "abc"["abc"][0x123] = "bcd"["bcd"+"aab"];
                foo("abc"[abc]);
            EndBody.
        """
        expect = Program([
            FuncDecl(Id("foo"),[
                VarDecl(Id("foo"),[],None),
                VarDecl(Id("foo"),[1,73],None),
                VarDecl(Id("foo2"),[172,9],None)
            ],([],[
                Assign(ArrayCell(StringLiteral("abc"),[StringLiteral("abc"),IntLiteral(291)]),
                ArrayCell(StringLiteral("bcd"),[BinaryOp("+",StringLiteral("bcd"),StringLiteral("aab"))])),
                CallStmt(Id("foo"),[ArrayCell(StringLiteral("abc"),[Id("abc")])])
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input, expect, 383))

    def test84(self):
        input = """
            Function: foo
            Parameter: foo, foo[1][0O111], foo2[0XAC][0o11]
            Body:
                "abc"["abc"][0x123] = "bcd"["bcd"+"aab"];
                foo(foo("abc"[abc]));
            EndBody.
        """
        expect = Program([
            FuncDecl(Id("foo"),[
                VarDecl(Id("foo"),[],None),
                VarDecl(Id("foo"),[1,73],None),
                VarDecl(Id("foo2"),[172,9],None)
            ],([],[
                Assign(ArrayCell(StringLiteral("abc"),[StringLiteral("abc"),IntLiteral(291)]),
                ArrayCell(StringLiteral("bcd"),[BinaryOp("+",StringLiteral("bcd"),StringLiteral("aab"))])),
                CallStmt(Id("foo"),[CallExpr(Id("foo"),[ArrayCell(StringLiteral("abc"),[Id("abc")])])])
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input, expect, 384))

    def test85(self):
        input = """
            Function: foo
            Parameter: foo, foo[1][0O111], foo2[0XAC][0o11]
            Body:
                "abc"["abc"][0x123] = "bcd"["bcd"+"aab"];
                foo(foo("abc"[abc]));
            EndBody.
            Function: fact
            Body:
                Var: k=20;
                If n<=.1 Then Return 1;
                ElseIf --.(!n) Then **do something** 
                Else Return n=/=fact(n-1)[25][25+foo()||45*63];
                EndIf.
            EndBody.
        """
        expect = Program([
            FuncDecl(Id("foo"),[
                VarDecl(Id("foo"),[],None),
                VarDecl(Id("foo"),[1,73],None),
                VarDecl(Id("foo2"),[172,9],None)
            ],([],[
                Assign(ArrayCell(StringLiteral("abc"),[StringLiteral("abc"),IntLiteral(291)]),
                ArrayCell(StringLiteral("bcd"),[BinaryOp("+",StringLiteral("bcd"),StringLiteral("aab"))])),
                CallStmt(Id("foo"),[CallExpr(Id("foo"),[ArrayCell(StringLiteral("abc"),[Id("abc")])])])
            ])),
            FuncDecl(Id("fact"),[],([VarDecl(Id("k"),[],IntLiteral(20))],[
                If([(BinaryOp("<=.",Id("n"),IntLiteral(1)),[],[
                    Return(IntLiteral(1))
                ]),(UnaryOp("-",UnaryOp("-.",UnaryOp("!",Id("n")))),[],[])],([],[
                    Return(BinaryOp("=/=",Id("n"),
                    ArrayCell(CallExpr(Id("fact"),[
                        BinaryOp("-",Id("n"),IntLiteral(1))
                    ]),[
                        IntLiteral(25),
                        BinaryOp("||",
                        BinaryOp("+",IntLiteral(25),CallExpr(Id("foo"),[])),
                        BinaryOp("*",IntLiteral(45),IntLiteral(63)))
                    ])))
                ]))          
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input, expect, 385))
    
    def test86(self):
        input = """
            Function: foo
            Body:
                a = a == a;
                a = a != a;
                a = a > a;
                a = a < a;
                a = a >= a;
                a = a <= a;
            EndBody.
        """
        expect = Program([
            FuncDecl(Id("foo"),[],([],[
                Assign(Id("a"),BinaryOp("==",Id("a"),Id("a"))),
                Assign(Id("a"),BinaryOp("!=",Id("a"),Id("a"))),
                Assign(Id("a"),BinaryOp(">",Id("a"),Id("a"))),
                Assign(Id("a"),BinaryOp("<",Id("a"),Id("a"))),
                Assign(Id("a"),BinaryOp(">=",Id("a"),Id("a"))),
                Assign(Id("a"),BinaryOp("<=",Id("a"),Id("a")))
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input, expect, 385))

    def test87(self):
        input = """
            Function: foo
            Body:
                a = a =/= a;
                a = a && a;
                a = a >. a;
                a = a <. a;
                a = a >=. a;
                a = a <=. a;
            EndBody.
        """
        expect = Program([
            FuncDecl(Id("foo"),[],([],[
                Assign(Id("a"),BinaryOp("=/=",Id("a"),Id("a"))),
                Assign(Id("a"),BinaryOp("&&",Id("a"),Id("a"))),
                Assign(Id("a"),BinaryOp(">.",Id("a"),Id("a"))),
                Assign(Id("a"),BinaryOp("<.",Id("a"),Id("a"))),
                Assign(Id("a"),BinaryOp(">=.",Id("a"),Id("a"))),
                Assign(Id("a"),BinaryOp("<=.",Id("a"),Id("a")))
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input, expect, 387))

    def test88(self):
        input = """
            Function: foo
            Body:
                a = a * a;
                a = a || a;
                a = a *. a;
                a = a \\ a;
                a = a \\. a;
                a = a % a;
            EndBody.
        """
        expect = Program([
            FuncDecl(Id("foo"),[],([],[
                Assign(Id("a"),BinaryOp("*",Id("a"),Id("a"))),
                Assign(Id("a"),BinaryOp("||",Id("a"),Id("a"))),
                Assign(Id("a"),BinaryOp("*.",Id("a"),Id("a"))),
                Assign(Id("a"),BinaryOp("\\",Id("a"),Id("a"))),
                Assign(Id("a"),BinaryOp("\\.",Id("a"),Id("a"))),
                Assign(Id("a"),BinaryOp("%",Id("a"),Id("a")))
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input, expect, 388))

    def test89(self):
        input = """
            Function: foo
            Body:
                a = a["abc"[a]];
            EndBody.
        """
        expect = Program([
            FuncDecl(Id("foo"),[],([],[
                Assign(Id("a"),ArrayCell(Id("a"),[
                    ArrayCell(StringLiteral("abc"),[Id("a")])
                ]))
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input, expect, 389))

    def test90(self):
        input = """
            Function: foo
            Body:
                a[True["False"]] = a["abc"[a]];
            EndBody.
        """
        expect = Program([
            FuncDecl(Id("foo"),[],([],[
                Assign(ArrayCell(Id("a"),[
                    ArrayCell(BooleanLiteral(True),[StringLiteral("False")])
                ]),ArrayCell(Id("a"),[
                    ArrayCell(StringLiteral("abc"),[Id("a")])
                ]))
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input, expect, 390))

    def test91(self):
        input = """
                    Function: main
                    Body:
                        Do 
                            a = 10;
                            If (a >= 10.e999 *3 - 76) Then
                                For(i = 100, i =/= 100.93, i - i) Do
                                    read();
                                    print(arr[fo(100, True, False) && "3" + 9]);
                                EndFor.
                            EndIf.
                        While i > 1 % 10
                        EndDo.
                    EndBody.
                """
        expect = Program(
            [
                FuncDecl(
                    Id("main"),
                    [

                    ],
                    ([

                    ],
                        [
                        Dowhile(
                            (
                                [],
                                [
                                    Assign(Id("a"), IntLiteral(10)),
                                    If(
                                        [(
                                            BinaryOp(
                                                ">=",
                                                Id("a"),
                                                BinaryOp(
                                                    "-",
                                                    BinaryOp(
                                                        "*",
                                                        FloatLiteral(10.e999),
                                                        IntLiteral(3)
                                                    ),
                                                    IntLiteral(76)
                                                )
                                            ),
                                            [],
                                            [
                                                For(
                                                    Id("i"),
                                                    IntLiteral(100),
                                                    BinaryOp(
                                                        "=/=", Id("i"), FloatLiteral(100.93)),
                                                    BinaryOp(
                                                        "-", Id("i"), Id("i")),
                                                    ([],
                                                     [
                                                        CallStmt(
                                                            Id("read"), []),
                                                        CallStmt(
                                                            Id("print"),
                                                            [
                                                                ArrayCell(
                                                                    Id("arr"),
                                                                    [
                                                                        BinaryOp(
                                                                            "&&",
                                                                            CallExpr(
                                                                                Id("fo"),
                                                                                [IntLiteral(100), BooleanLiteral(
                                                                                    True), BooleanLiteral(False)]
                                                                            ),
                                                                            BinaryOp(
                                                                                "+", StringLiteral("3"), IntLiteral(9))
                                                                        )
                                                                    ]
                                                                )
                                                            ]
                                                        )
                                                    ])
                                                )
                                            ]
                                        )],
                                        ([], [])
                                    )
                                ]
                            ),
                            BinaryOp(
                                ">",
                                Id("i"),
                                BinaryOp("%", IntLiteral(1), IntLiteral(10))
                            )
                        )
                    ])
                )
            ]
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 391))

    def test92(self):
        input = """
                    Function: main
                        Body:
                            For (i = "12", dasd < 2, 22) Do
                                in = (in(in(in)))[123];
                            EndFor.
                        EndBody.
                """
        expect = Program(
            [
                FuncDecl(
                    Id("main"),
                    [

                    ],
                    ([

                    ],
                        [
                        For(
                            Id("i"),
                            StringLiteral("12"),
                            BinaryOp("<", Id("dasd"), IntLiteral(2)),
                            IntLiteral(22),
                            ([],
                             [Assign(
                                 Id("in"),
                                 ArrayCell(
                                     CallExpr(
                                         Id("in"),
                                         [CallExpr(
                                             Id("in"),
                                             [Id("in")]
                                         )]
                                     ),
                                     [IntLiteral(123)]
                                 )
                             )])
                        )
                    ])
                )
            ]
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 392))

    def test93(self):
        input = """
            Function: foo
            Body:
                For (i = 0, i < 25, i+1) Do
                    If i == 8 Then 
                        Break;
                    EndIf.
                EndFor.
                Return;
            EndBody.
        """
        expect = Program([
            FuncDecl(Id("foo"),[],([],[
                For(Id("i"),IntLiteral(0),BinaryOp("<",Id("i"),IntLiteral(25)),BinaryOp("+",Id("i"),IntLiteral(1)),([],[
                    If([(BinaryOp("==",Id("i"),IntLiteral(8)),[],[
                        Break()
                    ])],([],[]))
                ])),
                Return(None)
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input, expect, 393))

    def test94(self):
        input = """
            Function: foo
            Body:
                For (i = 0, i < 25, i+1) Do
                    If i == 8 Then 
                        Break;
                        i[8][8] = 7;
                    EndIf.
                EndFor.
                Return;
            EndBody.
        """
        expect = Program([
            FuncDecl(Id("foo"),[],([],[
                For(Id("i"),IntLiteral(0),BinaryOp("<",Id("i"),IntLiteral(25)),BinaryOp("+",Id("i"),IntLiteral(1)),([],[
                    If([(BinaryOp("==",Id("i"),IntLiteral(8)),[],[
                        Break(),
                        Assign(ArrayCell(Id("i"),[IntLiteral(8),IntLiteral(8)]),IntLiteral(7))
                    ])],([],[]))
                ])),
                Return(None)
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input, expect, 394))

    def test95(self):
        input = """
            Function: foo
            Body:
                For (i = 0, i < 25, i+1) Do
                    If i == 8 Then 
                        Break;
                        i[8][8] = 7;
                    EndIf.
                    If i == 9 Then
                        Return print("string");
                    EndIf.
                EndFor.
                Return;
            EndBody.
        """
        expect = Program([
            FuncDecl(Id("foo"),[],([],[
                For(Id("i"),IntLiteral(0),BinaryOp("<",Id("i"),IntLiteral(25)),BinaryOp("+",Id("i"),IntLiteral(1)),([],[
                    If([(BinaryOp("==",Id("i"),IntLiteral(8)),[],[
                        Break(),
                        Assign(ArrayCell(Id("i"),[IntLiteral(8),IntLiteral(8)]),IntLiteral(7))
                    ])],([],[])),
                    If([(BinaryOp("==",Id("i"),IntLiteral(9)),[],[
                        Return(CallExpr(Id("print"),[StringLiteral("string")]))
                    ])],([],[]))
                ])),
                Return(None)
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input, expect, 395))

    def test96(self):
        input = """
            Function: foo
            Body:
                For (i = 0, i < 25, i+1) Do
                    If i == 8 Then 
                        Break;
                        i[8][8] = 7;
                    EndIf.
                    If i == 9 Then
                        Return print("string");
                    ElseIf i == 10 Then
                    Else Return;
                    EndIf.
                EndFor.
                Return;
            EndBody.
        """
        expect = Program([
            FuncDecl(Id("foo"),[],([],[
                For(Id("i"),IntLiteral(0),BinaryOp("<",Id("i"),IntLiteral(25)),BinaryOp("+",Id("i"),IntLiteral(1)),([],[
                    If([(BinaryOp("==",Id("i"),IntLiteral(8)),[],[
                        Break(),
                        Assign(ArrayCell(Id("i"),[IntLiteral(8),IntLiteral(8)]),IntLiteral(7))
                    ])],([],[])),
                    If([(BinaryOp("==",Id("i"),IntLiteral(9)),[],[
                        Return(CallExpr(Id("print"),[StringLiteral("string")]))
                    ]),(BinaryOp("==",Id("i"),IntLiteral(10)),[],[])],([],[
                        Return(None)
                    ]))
                ])),
                Return(None)
            ]))
        ])
        self.assertTrue(TestAST.checkASTGen(input, expect, 396))

    def test97(self):
        input = """
            Var: t, t, t;
            Var: t;
        """
        expect = Program([
            VarDecl(Id("t"),[],None),
            VarDecl(Id("t"),[],None),
            VarDecl(Id("t"),[],None),
            VarDecl(Id("t"),[],None)
        ])
        self.assertTrue(TestAST.checkASTGen(input, expect, 397))

    def test98(self):
        input = """
                    Function: fun
                        Parameter: temp, value
                        Body:     
                            If (a && b && c == 0) Then
                                x = fun(temp - 1) *. fun(temp % 2);
                            EndIf.
                        EndBody.
                """
        expect = Program(
            [
                FuncDecl(
                    Id("fun"),
                    [
                        VarDecl(Id("temp"), [], None),
                        VarDecl(Id("value"), [], None)
                    ],
                    ([

                    ],
                        [
                        If(
                            [(
                                BinaryOp(
                                    "==",
                                    BinaryOp(
                                        "&&",
                                        BinaryOp("&&", Id("a"), Id("b")),
                                        Id("c")
                                    ),
                                    IntLiteral(0)
                                ),
                                [],
                                [
                                    Assign(
                                        Id("x"),
                                        BinaryOp(
                                            "*.",
                                            CallExpr(
                                                Id("fun"), [
                                                    BinaryOp("-", Id("temp"), IntLiteral(1))]
                                            ),
                                            CallExpr(
                                                Id("fun"), [
                                                    BinaryOp("%", Id("temp"), IntLiteral(2))]
                                            )
                                        )
                                    )
                                ]
                            )], ([], [])
                        )
                    ]
                    )
                )
            ]
        )
        self.assertTrue(TestAST.checkASTGen(input, expect, 398))

    def test99(self):
        input = """
                    Function: fun
                        Parameter: temp, value
                        Body:     
                            If (a && b && c == 0) Then
                                x = fun(temp - 1) *. fun(temp % 2);
                                If x == 2 Then
                                    While "a" Do
                                    EndWhile.
                                EndIf.
                            EndIf.
                        EndBody.
                """
        
        expect = Program(
            [
                FuncDecl(
                    Id("fun"),
                    [
                        VarDecl(Id("temp"), [], None),
                        VarDecl(Id("value"), [], None)
                    ],
                    ([

                    ],
                        [
                        If(
                            [(
                                BinaryOp(
                                    "==",
                                    BinaryOp(
                                        "&&",
                                        BinaryOp("&&", Id("a"), Id("b")),
                                        Id("c")
                                    ),
                                    IntLiteral(0)
                                ),
                                [],
                                [
                                    Assign(
                                        Id("x"),
                                        BinaryOp(
                                            "*.",
                                            CallExpr(
                                                Id("fun"), [
                                                    BinaryOp("-", Id("temp"), IntLiteral(1))]
                                            ),
                                            CallExpr(
                                                Id("fun"), [
                                                    BinaryOp("%", Id("temp"), IntLiteral(2))]
                                            )
                                        )
                                    ),
                                    If([(BinaryOp("==",Id("x"),IntLiteral(2)),[],[
                        While(StringLiteral("a"),([],[]))
                    ])],([],[]))
                                ]
                            )], ([], [])
                        )
                    ]
                    )
                )
            ]
        )

        self.assertTrue(TestAST.checkASTGen(input, expect, 399))

    def test100(self):
        input = """
                    **Comment**
                    Function: main
                        Parameter: x, y, z
                        Body:
                            Break;
                            Continue;
                            x = foo(1) + foo(2) +. fuho(123);
                        EndBody.
                """
        expect = Program(
            [
                FuncDecl(
                    Id("main"),
                    [
                        VarDecl(Id("x"), [], None),
                        VarDecl(Id("y"), [], None),
                        VarDecl(Id("z"), [], None)
                    ],
                    ([
                        
                    ],
                    [
                        Break(),
                        Continue(),
                        Assign(
                            Id("x"),
                            BinaryOp(
                                "+.",
                                BinaryOp(
                                    "+",
                                    CallExpr(Id("foo"), [IntLiteral(1)]),
                                    CallExpr(Id("foo"), [IntLiteral(2)])
                                ),
                                CallExpr(Id("fuho"), [IntLiteral(123)])
                            )
                        )
                    ])
                )
            ]
        )
        self.assertTrue(TestAST.checkASTGen(input,expect,300))

    def testcase_83(self):
        input = r"""Function: function
            Parameter: i, arr[1000]
            Body:
                function()[i] = -.1.;
                (arr =/= arr)["True"] = i;
                arr[i] = i;
            EndBody."""
        expect = Program([
            FuncDecl(Id('function'),
            [VarDecl(Id('i'),[],None),VarDecl(Id('arr'),[1000],None)],
            ([],
            [Assign(ArrayCell(CallExpr(Id('function'),[]),[Id('i')]),UnaryOp('-.',FloatLiteral(1.0))),Assign(ArrayCell(BinaryOp('=/=',Id('arr'),Id('arr')),[StringLiteral(r"""True""")]),Id('i')),Assign(ArrayCell(Id('arr'),[Id('i')]),Id('i'))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 400))