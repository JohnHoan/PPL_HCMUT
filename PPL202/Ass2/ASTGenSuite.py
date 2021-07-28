import unittest
from TestUtils import TestAST
from AST import *


class ASTGenSuite(unittest.TestCase):

    """ Test Variable Decleration """
    def test0(self):
        input = """Let x;"""
        expect = Program([VarDecl(Id('x'), [], NoneType(), None)])
        self.assertTrue(TestAST.checkASTGen(input, expect, 300))

    def test1(self):
        input = """Let x = 5;"""
        expect = Program([VarDecl(Id('x'), [], NoneType(), NumberLiteral(5.0))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 301))

    def test2(self):
        input = """Let x: Number;"""
        expect = Program([VarDecl(Id('x'), [], NumberType(), None)])
        self.assertTrue(TestAST.checkASTGen(input, expect, 302))

    def test3(self):
        input = """Let x: Number = 5;"""
        expect = Program([VarDecl(Id('x'), [], NumberType(), NumberLiteral(5.0))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 303))

    def test4(self):
        input = """Let x[2] : Number = [1,2] ;"""
        expect = Program([VarDecl(Id('x'), [NumberLiteral(2.0)], NumberType(),ArrayLiteral([NumberLiteral(1.0),NumberLiteral(2.0)]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 304))

    def test5(self):
        input = """Let x : Boolean = True;"""
        expect = Program([VarDecl(Id('x'),[],BooleanType(),BooleanLiteral('true'))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 305))

    def test6(self):
        input = """Let x : JSON = {
            name: "Yanxi Place",
            address: "Chinese Forbidden City"
            };"""
        expect = Program([VarDecl(Id('x'), [], JSONType(), 
            JSONLiteral([(Id('name'),StringLiteral('Yanxi Place')),(Id('address'),StringLiteral('Chinese Forbidden City'))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 306))


    def test7(self):
        input = """Let x : String = "I will pass PPL 202";"""
        expect = Program([VarDecl(Id('x'),[],StringType(),StringLiteral('I will pass PPL 202'))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 307))

    def test8(self):
        input = """Let x[3,3];"""
        expect = Program([VarDecl(Id('x'),[NumberLiteral(3.0),NumberLiteral(3.0)],NoneType(),None)])
        self.assertTrue(TestAST.checkASTGen(input, expect, 308))

    def test9(self):
        input = """Let x = False;"""
        expect = Program([VarDecl(Id('x'),[],NoneType(),BooleanLiteral('false'))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 309))

    """ Test Constant Decleration """
    def test10(self):
        input = """Constant $x = 5;"""
        expect = Program([ConstDecl(Id('$x'), [], NoneType(), NumberLiteral(5.0))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 310))

    def test11(self):
        input = """Constant $x = False;"""
        expect = Program([ConstDecl(Id('$x'), [], NoneType(), BooleanLiteral('false'))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 311))

    def test12(self):
        input = """Constant $x: Number = 5;"""
        expect = Program([ConstDecl(Id('$x'), [], NumberType(), NumberLiteral(5.0))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 312))

    def test13(self):
        input = """Constant $x: Number = 5.55;"""
        expect = Program([ConstDecl(Id('$x'), [], NumberType(), NumberLiteral(5.55))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 313))

    def test14(self):
        input = """Constant $x[2] : Number = [1,2] ;"""
        expect = Program([ConstDecl(Id('$x'), [NumberLiteral(2.0)], NumberType(),ArrayLiteral([NumberLiteral(1.0),NumberLiteral(2.0)]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 314))

    def test15(self):
        input = """Constant $x : Boolean = True;"""
        expect = Program([ConstDecl(Id("$x"),[],BooleanType(),BooleanLiteral('true'))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 315))

    def test16(self):
        input = """Constant $x : JSON = {
            name: "Yanxi Place",
            address: "Chinese Forbidden City"
            };"""
        expect = Program([ConstDecl(Id('$x'), [], JSONType(), JSONLiteral([(Id('name'),StringLiteral('Yanxi Place')),(Id('address'),StringLiteral('Chinese Forbidden City'))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 316))

    def test17(self):
        input = """Constant $x : String = "I will pass PPL 202";"""
        expect = Program([ConstDecl(Id('$x'),[],StringType(),StringLiteral('I will pass PPL 202'))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 317))

    def test18(self):
        input = """Constant $x[2, 3] = [[1, 2, 3], [4, 5, 6]];"""
        expect = Program([ConstDecl(Id('$x'),[NumberLiteral(2.0),NumberLiteral(3.0)],NoneType(),ArrayLiteral([ArrayLiteral([NumberLiteral(1.0),NumberLiteral(2.0),NumberLiteral(3.0)]),ArrayLiteral([NumberLiteral(4.0),NumberLiteral(5.0),NumberLiteral(6.0)])]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 318))

    def test19(self):
        input = """Constant $x = 3.14;"""
        expect = Program([ConstDecl(Id('$x'),[],NoneType(),NumberLiteral(3.14))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 319))

    
    """test simple function"""

    def test20(self):
        input = """Function foo(){}"""
        expect = Program([FuncDecl(Id('foo'),[],[])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 320))

    def test21(self):
        input = """Function foo(a[5],b){}"""
        expect = Program([FuncDecl(Id('foo'),[VarDecl(Id('a'),[NumberLiteral(5.0)],NoneType(),None),VarDecl(Id('b'),[],NoneType(),None)],[])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 321))
    
    def test22(self):
        input = """Function foo(a[5],b){
                   Return "I will pass PPL in semester 202";
        }"""
        expect = Program([FuncDecl(Id('foo'),[VarDecl(Id('a'),[NumberLiteral(5.0)],NoneType(),None),VarDecl(Id('b'),[],NoneType(),None)],[Return(StringLiteral('I will pass PPL in semester 202'))])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 322))

    def test23(self):
        input = """Function foo(a[5],b){
                   Let i = "I can do it";
                   Let a = 1;
                   Return i;
        }"""
        expect = Program([FuncDecl(Id('foo'),[VarDecl(Id('a'),[NumberLiteral(5.0)],NoneType(),None),VarDecl(Id('b'),[],NoneType(),None)],[VarDecl(Id('i'),[],NoneType(),StringLiteral('I can do it')),VarDecl(Id('a'),[],NoneType(),NumberLiteral(1.0)),Return(Id('i'))])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 323))

    def test24(self):
        input = """
                   Constant $x = 5;
                   Function foo(a[5],b){
                   Let i = "I can do it";
                   Return i;
        }"""
        expect = Program([ConstDecl(Id('$x'),[],NoneType(),NumberLiteral(5.0)),FuncDecl(Id('foo'),[VarDecl(Id('a'),[NumberLiteral(5.0)],NoneType(),None),VarDecl(Id('b'),[],NoneType(),None)],[VarDecl(Id('i'),[],NoneType(),StringLiteral('I can do it')),Return(Id('i'))])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 324))


    def test25(self):
        input = """
                   Let b = 5;
                   Function foo(a[5],b){
                   Return "I will pass PPL in semester 202";
        }"""
        expect = Program([VarDecl(Id('b'),[],NoneType(),NumberLiteral(5.0)),FuncDecl(Id('foo'),[VarDecl(Id('a'),[NumberLiteral(5.0)],NoneType(),None),VarDecl(Id('b'),[],NoneType(),None)],[Return(StringLiteral('I will pass PPL in semester 202'))])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 325))

    def test26(self):
        input = """
                   Let a = 4;
                   Function foo(a[5],b){
                   b = a + 1;
                   Return "I will pass PPL in semester 202";
        }"""
        expect = Program([VarDecl(Id('a'),[],NoneType(),NumberLiteral(4.0)), 
                 FuncDecl(Id('foo'),[VarDecl(Id('a'),[NumberLiteral(5.0)],NoneType(),None),VarDecl(Id('b'),[],NoneType(),None)],
                [Assign(Id('b'),BinaryOp('+',Id('a'),NumberLiteral(1.0))),Return(StringLiteral('I will pass PPL in semester 202'))])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 326))

    def test27(self):
        input = """
                   Let a = 4;
                   Function foo(a[5],b){
                   b = a + 1;
                   Return b;
        }"""
        expect = Program([VarDecl(Id('a'),[],NoneType(),NumberLiteral(4.0)), 
                 FuncDecl(Id('foo'),[VarDecl(Id('a'),[NumberLiteral(5.0)],NoneType(),None),VarDecl(Id('b'),[],NoneType(),None)],
                [Assign(Id('b'),BinaryOp('+',Id('a'),NumberLiteral(1.0))),Return(Id('b'))])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 327))

    def test28(self):
        input = """
                   Let a = 4;
                   Function foo(a[5],b){
                   Call(foo, [a]);
                   Return ;
        }"""
        expect = Program([
                 VarDecl(Id('a'),[],NoneType(),NumberLiteral(4.0)), 
                 FuncDecl(Id('foo'),
                    [VarDecl(Id('a'),[NumberLiteral(5.0)],NoneType(),None),VarDecl(Id('b'),[],NoneType(),None)],
                    [CallStmt(Id('foo'),[Id('a')]),Return(None)])
                 ])
        self.assertTrue(TestAST.checkASTGen(input, expect, 328))

    def test29(self):
        input = """
                   Let a = 4;
                   Function foo(a[5],b){
                   Call(foo, [a]);
                   Return Call(foo, []) ;
        }"""
        expect = Program([
                 VarDecl(Id('a'),[],NoneType(),NumberLiteral(4.0)), 
                 FuncDecl(Id('foo'),
                    [VarDecl(Id('a'),[NumberLiteral(5.0)],NoneType(),None),VarDecl(Id('b'),[],NoneType(),None)],
                    [CallStmt(Id('foo'),[Id('a')]),Return(CallExpr(Id('foo'),[]))])
                 ])
        self.assertTrue(TestAST.checkASTGen(input, expect, 329)) 

    """test for in for of"""
    def test30(self):
        input = """Function foo(){
                   For i In [1,2,3]{
                       Call(printLn, [i]);
                   }
        }"""
        expect = Program([FuncDecl(Id('foo'),[],[ForIn(Id('i'),ArrayLiteral([NumberLiteral(1.0),NumberLiteral(2.0),NumberLiteral(3.0)]),[CallStmt(Id('printLn'),[Id('i')])])])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 330))

    def test31(self):
        input = """Function foo(){
                   For i In [1,2,3]{
                       i = i + 1;
                   }
        }"""
        expect = Program([FuncDecl(Id('foo'),[],[ForIn(Id('i'),ArrayLiteral([NumberLiteral(1.0),NumberLiteral(2.0),NumberLiteral(3.0)]),[Assign(Id('i'),BinaryOp('+',Id('i'),NumberLiteral(1.0)))])])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 331))

    def test32(self):
        input = """Function foo(){
                   For i In [1,2]{
                        i = i + 1;
                        If(i==2){
                          Break;
                        }
                   }
        }"""
        expect = Program([FuncDecl(Id('foo'),[],
            [ForIn(Id('i'),ArrayLiteral([NumberLiteral(1.0),NumberLiteral(2.0)]),
                [Assign(Id('i'),BinaryOp('+',Id('i'),NumberLiteral(1.0))),
                 If([(BinaryOp('==',Id('i'),NumberLiteral(2.0)),[Break()])],[])
                ])])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 332))

    def test33(self):
        input = """Function foo(){
                   For i In [1,2]{
                        i = i + 1;
                        If(i==2){
                          Continue;
                        }
                   }
        }"""
        expect = Program([FuncDecl(Id('foo'),[],
            [ForIn(Id('i'),ArrayLiteral([NumberLiteral(1.0),NumberLiteral(2.0)]),
                [Assign(Id('i'),BinaryOp('+',Id('i'),NumberLiteral(1.0))),
                 If([(BinaryOp('==',Id('i'),NumberLiteral(2.0)),[Continue()])],[])
                ])])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 333))

    def test34(self):
        input = """Function foo(){
                   For i In [1,2]{
                        i = i + 1;
                        If(i==2){
                          Return i;
                        }
                   }
        }"""
        expect = Program([FuncDecl(Id('foo'),[],
            [ForIn(Id('i'),ArrayLiteral([NumberLiteral(1.0),NumberLiteral(2.0)]),
                [Assign(Id('i'),BinaryOp('+',Id('i'),NumberLiteral(1.0))),
                 If([(BinaryOp('==',Id('i'),NumberLiteral(2.0)),[Return(Id('i'))])],[])
                ])])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 334))

    def test35(self):
        input = """Function foo(){
                   For i In [1,2]{
                        i = i + 1;
                        If(i==2){
                          Call(foo,[]);
                        }
                   }
        }"""
        expect = Program([FuncDecl(Id('foo'),[],
            [ForIn(Id('i'),ArrayLiteral([NumberLiteral(1.0),NumberLiteral(2.0)]),
                [Assign(Id('i'),BinaryOp('+',Id('i'),NumberLiteral(1.0))),
                 If([(BinaryOp('==',Id('i'),NumberLiteral(2.0)),[CallStmt(Id('foo'),[])])],[])
                ])])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 335))

    def test36(self):
        input = """Function foo(){
                   For i Of a{
                        Call(printLn,[i]);
                   }
        }"""
        expect = Program([FuncDecl(Id('foo'),[],
            [ForOf(Id('i'),Id('a'),
                [
                  CallStmt(Id('printLn'),[Id('i')])
                ])])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 336))

    def test37(self):
        input = """Function foo(){
                   For i Of a{
                        i = i +. "I will pass PPL";
                   }
        }"""
        expect = Program([FuncDecl(Id('foo'),[],
            [ForOf(Id('i'),Id('a'),
                [
                  Assign(Id('i'),BinaryOp('+.',Id('i'),StringLiteral('I will pass PPL')))
                ])])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 337))

    def test38(self):
        input = """Function foo(){
                   For i Of a{
                        If(i ==. "Pass PPL"){
                           Call(printLn,["Congrats!"]);
                        }
                   }
        }"""
        expect = Program([FuncDecl(Id('foo'),[],
            [ForOf(Id('i'),Id('a'),
                [
                  If([(BinaryOp('==.',Id('i'),StringLiteral('Pass PPL')),[CallStmt(Id('printLn'),[StringLiteral('Congrats!')])])],[])
                ])])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 338))

    def test39(self):
        input = """
                    Function foo(){
                    For i Of a{
                       Call(printLn, ["Value of " + key + ": " + a{"key"}]);
                   }
        }"""
        expect = Program([FuncDecl(Id('foo'),[],
            [ForOf(Id('i'),Id('a'),
                [
                  CallStmt(Id('printLn'),[BinaryOp('+',BinaryOp('+',BinaryOp('+',StringLiteral('Value of '),Id('key')),StringLiteral(': ')),JSONAccess(Id('a'),[StringLiteral('key')]))])
                ])])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 339))
        StringLiteral('Value of'),Id('key'),StringLiteral(':'),JSONAccess(Id('a'),[StringLiteral('key')])

    def test40(self):
        input = """
                    Let a = {
                        name: "Yanxi Place",
                        address: "Chinese Forbidden City"
                    };
                    Function foo(){
                    For i Of a{
                       Call(printLn, ["Value of " + key + ": " + a{"key"}]);
                   }
        }"""
        expect = Program([
            VarDecl(Id('a'), [], NoneType(), 
            JSONLiteral([
                (Id('name'),StringLiteral('Yanxi Place')),
                (Id('address'),StringLiteral('Chinese Forbidden City'))])),
            FuncDecl(Id('foo'),[],
            [ForOf(Id('i'),Id('a'),
                [
                  CallStmt(Id('printLn'),[BinaryOp('+',BinaryOp('+',BinaryOp('+',StringLiteral('Value of '),Id('key')),StringLiteral(': ')),JSONAccess(Id('a'),[StringLiteral('key')]))])
                ])])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 340))

    def test41(self):
        input = """ Let a : JSON = {
                     name: "John",
                     id: "1711376",
                     address: "Nghe An"
                    };
                    Function foo(){
                    For i Of a{
                       Call(printLn, ["Value of " + key + ": " + a{"key"}]);
                   }
        }"""
        expect = Program([VarDecl(Id('a'), [], JSONType(), 
            JSONLiteral([(Id('name'),StringLiteral('John')),(Id('id'),StringLiteral('1711376')),(Id('address'),StringLiteral('Nghe An'))])),
            FuncDecl(Id('foo'),[],
            [ForOf(Id('i'),Id('a'),
                [
                  CallStmt(Id('printLn'),[BinaryOp('+',BinaryOp('+',BinaryOp('+',StringLiteral('Value of '),Id('key')),StringLiteral(': ')),JSONAccess(Id('a'),[StringLiteral('key')]))])
                ])])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 341))

    def test42(self):
        input = """ Let a : JSON = {
                     name: "John",
                     id: "1711376",
                     address: "Nghe An"
                    };
                    Function foo(){
                    For i Of a{
                       Call(printLn, [a{"key"}]);
                   }
        }"""
        expect = Program([VarDecl(Id('a'), [], JSONType(), 
            JSONLiteral([(Id('name'),StringLiteral('John')),(Id('id'),StringLiteral('1711376')),(Id('address'),StringLiteral('Nghe An'))])),
            FuncDecl(Id('foo'),[],
            [ForOf(Id('i'),Id('a'),
                [
                  CallStmt(Id('printLn'),[JSONAccess(Id('a'),[StringLiteral('key')])])
                ])])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 342))

    """Some more test decl json var"""
    def test43(self):
        input = """Let x : JSON = {
            name: "John",
            id: "1711376",
            address: "Nghe An"

            };"""
        expect = Program([VarDecl(Id('x'), [], JSONType(), 
            JSONLiteral([(Id('name'),StringLiteral('John')),(Id('id'),StringLiteral('1711376')),(Id('address'),StringLiteral('Nghe An'))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 343))

    def test44(self):
        input = """Let x : JSON = {
               name: "PPL",
               members: 92,
               class: [201,"H1"]
            };"""
        expect = Program([VarDecl(Id('x'), [], JSONType(), 
            JSONLiteral([(Id('name'),StringLiteral('PPL')),(Id('members'),NumberLiteral(92.0)),(Id('class'),ArrayLiteral([NumberLiteral(201.0),StringLiteral('H1')]))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 344))

    def test45(self):
        input = """Let x : JSON = {
            name: "John",
            purpose: "Pass PPL",
            flag: True
            };"""
        expect = Program([VarDecl(Id('x'), [], JSONType(), 
            JSONLiteral([(Id('name'),StringLiteral('John')),(Id('purpose'),StringLiteral('Pass PPL')),(Id('flag'),BooleanLiteral('true'))]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 345))

    """some more for of test with if"""
    def test46(self):
        input = """ Let a : JSON = {
                     name: "John",
                     id: "1711376",
                     address: "Nghe An"
                    };
                    Function foo(){
                    For i Of a{
                       If(a[address] ==. "Nghe An"){
                           Call(welcome, ["Hello Bro!"]);
                       }
                   }
        }"""
        expect = Program([VarDecl(Id('a'), [], JSONType(), 
            JSONLiteral([(Id('name'),StringLiteral('John')),(Id('id'),StringLiteral('1711376')),(Id('address'),StringLiteral('Nghe An'))])),
            FuncDecl(Id('foo'),[],
            [ForOf(Id('i'),Id('a'),
                [
                  If([(BinaryOp('==.',ArrayAccess(Id('a'),[Id('address')]),StringLiteral('Nghe An')),[CallStmt(Id('welcome'),[StringLiteral('Hello Bro!')])])],[])
                ])])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 346))

    def test47(self):
        input = """ Let a : JSON = {
                     name: "John",
                     id: "1711376",
                     address: "Nghe An"
                    };
                    Function foo(){
                    For i Of a{
                        Call(writeLn, [a[key]]);
                   }
        }"""
        expect = Program([VarDecl(Id('a'), [], JSONType(), 
            JSONLiteral([(Id('name'),StringLiteral('John')),(Id('id'),StringLiteral('1711376')),(Id('address'),StringLiteral('Nghe An'))])),
            FuncDecl(Id('foo'),[],
            [ForOf(Id('i'),Id('a'),
                [
                  CallStmt(Id('writeLn'),[ArrayAccess(Id('a'),[Id('key')])])
                ])])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 347))

    def test48(self):
        input = """ Let a : JSON = {
                     name: "John",
                     id: "1711376",
                     address: "Nghe An"
                    };
                    Function foo(){
                    For i Of a{
                       If(a[address] ==. "Nghe An"){
                           Call(welcome, ["Hello Bro!"]);
                       }
                       Else {
                           Call(say, ["Hello!"]);
                       }
                   }
        }"""
        expect = Program([VarDecl(Id('a'), [], JSONType(), 
            JSONLiteral([(Id('name'),StringLiteral('John')),(Id('id'),StringLiteral('1711376')),(Id('address'),StringLiteral('Nghe An'))])),
            FuncDecl(Id('foo'),[],
            [ForOf(Id('i'),Id('a'),
                [
                  If([(BinaryOp('==.',ArrayAccess(Id('a'),[Id('address')]),StringLiteral('Nghe An')),[CallStmt(Id('welcome'),[StringLiteral('Hello Bro!')])])],[CallStmt(Id('say'),[StringLiteral('Hello!')])])
                ])])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 348))

    def test49(self):
        input = """ Let a : JSON = {
                     name: "John",
                     id: "1711376",
                     address: "Nghe An"
                    };
                    Function foo(){
                    For i Of a{
                       If(a[address] ==. "Nghe An"){
                           Call(welcome, ["Hello Bro!"]);
                       }
                       Else {
                           Break;
                       }
                   }
        }"""
        expect = Program([VarDecl(Id('a'), [], JSONType(), 
            JSONLiteral([(Id('name'),StringLiteral('John')),(Id('id'),StringLiteral('1711376')),(Id('address'),StringLiteral('Nghe An'))])),
            FuncDecl(Id('foo'),[],
            [ForOf(Id('i'),Id('a'),
                [
                  If([(BinaryOp('==.',ArrayAccess(Id('a'),[Id('address')]),StringLiteral('Nghe An')),[CallStmt(Id('welcome'),[StringLiteral('Hello Bro!')])])],[Break()])
                ])])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 349))

    """test if else statement"""
    def test50(self):
        input = """Function foo(){
            If(a==1){
                Return a;
            }
        }"""
        expect = Program([FuncDecl(Id('foo'),[],[
                 If([(BinaryOp('==',Id('a'),NumberLiteral(1.0)),[Return(Id('a'))])],[])
            ])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 350))

    def test51(self):
        input = """Function foo(){
            If(a==1){
                Return a;
            }Else{
                Return Call(foo,[]) ;
            }
        }"""
        expect = Program([FuncDecl(Id('foo'),[],[
                 If([(BinaryOp('==',Id('a'),NumberLiteral(1.0)),[Return(Id('a'))])],[Return(CallExpr(Id('foo'),[]))])
            ])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 351))

    def test52(self):
        input = """Function foo(){
            If(a==True){
                Return a;
            }Else{
                Return Call(foo,[]) ;
            }
        }"""
        expect = Program([FuncDecl(Id('foo'),[],[
                 If([(BinaryOp('==',Id('a'),BooleanLiteral('true')),[Return(Id('a'))])],[Return(CallExpr(Id('foo'),[]))])
            ])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 352))

    def test53(self):
        input = """Function foo(){
            If(a==1){
                a = a + 100;
                Return a;
            }
        }"""
        expect = Program([FuncDecl(Id('foo'),[],[
                 If([(BinaryOp('==',Id('a'),NumberLiteral(1.0)),
                    [Assign(Id('a'),BinaryOp('+',Id('a'),NumberLiteral(100.0))),Return(Id('a'))])],[])
            ])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 353))

    def test54(self):
        input = """Function foo(){
            If(a==10){
                b = b - a;
            }Else{
                b = a - b;
            }
            Return b;
        }"""
        expect = Program([FuncDecl(Id('foo'),[],[
                 If([(BinaryOp('==',Id('a'),NumberLiteral(10.0)),[
                    Assign(Id('b'),BinaryOp('-',Id('b'),Id('a')))])],[
                    Assign(Id('b'),BinaryOp('-',Id('a'),Id('b')))]), Return(Id('b'))
            ])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 354))


    def test55(self):
        input = """Function foo(){
            If(a!=10){
                b = b - a;
            }Else{
                b = a - b;
            }
            Return b;
        }"""
        expect = Program([FuncDecl(Id('foo'),[],[
                 If([(BinaryOp('!=',Id('a'),NumberLiteral(10.0)),[
                    Assign(Id('b'),BinaryOp('-',Id('b'),Id('a')))])],[
                    Assign(Id('b'),BinaryOp('-',Id('a'),Id('b')))]), Return(Id('b'))
            ])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 355))

    def test56(self):
        input = """Function foo(){
            If(!a){
                b = b - a;
            }Else{
                b = a - b;
            }
            Return b;
        }"""
        expect = Program([FuncDecl(Id('foo'),[],[
                 If([(UnaryOp('!',Id('a')),[
                    Assign(Id('b'),BinaryOp('-',Id('b'),Id('a')))])],[
                    Assign(Id('b'),BinaryOp('-',Id('a'),Id('b')))]), Return(Id('b'))
            ])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 356))

    def test57(self):
        input = """Function foo(){
            If(a>10){
                b = b - a;
            }Elif(a==10){
                b = a - b;
            }Else{
                b = b * 100;
            }
            Return b;
        }"""
        expect = Program([FuncDecl(Id('foo'),[],[
                 If([(BinaryOp('>',Id('a'),NumberLiteral(10.0)),[Assign(Id('b'),BinaryOp('-',Id('b'),Id('a')))]),(
                    BinaryOp('==',Id('a'),NumberLiteral(10.0)),[Assign(Id('b'),BinaryOp('-',Id('a'),Id('b')))])],[
                    Assign(Id('b'),BinaryOp('*',Id('b'),NumberLiteral(100.0)))]), Return(Id('b'))
            ])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 357))

    def test58(self):
        input = """Function foo(){
            If(a>10){
                b = b - a;
            }Elif(a<10){
                b = a - b;
            }Else{
                b = b * 100;
            }
            Return b;
        }"""
        expect = Program([FuncDecl(Id('foo'),[],[
                 If([(BinaryOp('>',Id('a'),NumberLiteral(10.0)),[Assign(Id('b'),BinaryOp('-',Id('b'),Id('a')))]),(
                    BinaryOp('<',Id('a'),NumberLiteral(10.0)),[Assign(Id('b'),BinaryOp('-',Id('a'),Id('b')))])],[
                    Assign(Id('b'),BinaryOp('*',Id('b'),NumberLiteral(100.0)))]), Return(Id('b'))
            ])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 358))


    def test59(self):
        input = """Function foo(){
            If(True){ 

            }Elif(False && !10){

            }Elif(False){

            }Else{

            }
        }"""
        expect = Program([FuncDecl(Id('foo'),[],[
                 If([(BooleanLiteral('true'),[]),
                    (BinaryOp('&&',BooleanLiteral('false'),UnaryOp('!',NumberLiteral(10.0))),[]),
                    (BooleanLiteral('false'),[])],
                    [])
            ])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 359))

    def test60(self):
        input = """Function foo(){
            If((a==1) && (x!=0)){
                a = a + 100;
                Return a;
            }
        }"""
        expect = Program([FuncDecl(Id('foo'),[],[
                 If([(BinaryOp('&&',BinaryOp('==',Id('a'),NumberLiteral(1.0)),BinaryOp('!=',Id('x'),NumberLiteral(0.0))),
                    [Assign(Id('a'),BinaryOp('+',Id('a'),NumberLiteral(100.0))),Return(Id('a'))])],[])
            ])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 360))

    def test61(self):
        input = """Function foo(){
            If((a==1) || (x!=0)){
                a = a + 100;
                Return a;
            }
        }"""
        expect = Program([FuncDecl(Id('foo'),[],[
                 If([(BinaryOp('||',BinaryOp('==',Id('a'),NumberLiteral(1.0)),BinaryOp('!=',Id('x'),NumberLiteral(0.0))),
                    [Assign(Id('a'),BinaryOp('+',Id('a'),NumberLiteral(100.0))),Return(Id('a'))])],[])
            ])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 361))

    """test while statement"""
    def test62(self):
        input = """Function foo(){
                   While(x!=10){
                   }
        }"""
        expect = Program([FuncDecl(Id('foo'),[],[
                 While(BinaryOp('!=',Id('x'),NumberLiteral(10.0)),[])
            ])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 362))

    def test63(self):
        input = """Function foo(){
                   While(x!=10){
                      x = x + 1;
                   }
        }"""
        expect = Program([FuncDecl(Id('foo'),[],[
                 While(BinaryOp('!=',Id('x'),NumberLiteral(10.0)),[Assign(Id('x'),BinaryOp('+',Id('x'),NumberLiteral(1.0)))])
            ])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 363))

    def test64(self):
        input = """Function foo(){
                   While(x!=10){
                      If(x==5){
                         Break;
                      }
                   }
        }"""
        expect = Program([FuncDecl(Id('foo'),[],[
                 While(BinaryOp('!=',Id('x'),NumberLiteral(10.0)),[
                      If([(BinaryOp('==',Id('x'),NumberLiteral(5.0)),[Break()])],[])
                    ])
            ])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 364))

    def test65(self):
        input = """Function foo(){
                   While(x!=10){
                      If(x==5){
                         Continue;
                      }
                   }
        }"""
        expect = Program([FuncDecl(Id('foo'),[],[
                 While(BinaryOp('!=',Id('x'),NumberLiteral(10.0)),[
                      If([(BinaryOp('==',Id('x'),NumberLiteral(5.0)),[Continue()])],[])
                    ])
            ])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 365))

    def test66(self):
        input = """Function foo(){
                   While(x!=10){
                       Call(printLn,[x]);
                   }
        }"""
        expect = Program([FuncDecl(Id('foo'),[],[
                 While(BinaryOp('!=',Id('x'),NumberLiteral(10.0)),[
                      CallStmt(Id('printLn'),[Id('x')])
                    ])
            ])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 366))

    def test67(self):
        input = """Function foo(){
                   While(x!=10){
                      If(x==5){
                         Return x;
                      }
                   }
        }"""
        expect = Program([FuncDecl(Id('foo'),[],[
                 While(BinaryOp('!=',Id('x'),NumberLiteral(10.0)),[
                      If([(BinaryOp('==',Id('x'),NumberLiteral(5.0)),[Return(Id('x'))])],[])
                    ])
            ])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 367))   

    def test68(self):
        input = """Function foo(){
                   While((x!=10) || (x>100)){
                      Return;
                   }
        }"""
        expect = Program([FuncDecl(Id('foo'),[],[
                 While(BinaryOp('||',BinaryOp('!=',Id('x'),NumberLiteral(10.0)),BinaryOp('>',Id('x'),NumberLiteral(100.0))),[Return(None)])
            ])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 368))

    def test69(self):
        input = """Function foo(){
                   While((x!=10) && (x>100)){
                      Return;
                   }
        }"""
        expect = Program([FuncDecl(Id('foo'),[],[
                 While(BinaryOp('&&',BinaryOp('!=',Id('x'),NumberLiteral(10.0)),BinaryOp('>',Id('x'),NumberLiteral(100.0))),[Return(None)])
            ])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 369))


    """test call statement"""
    def test70(self):
        input = """Function foo(){
            Call(foo,[a,b]);
        }"""
        expect = Program([FuncDecl(Id('foo'),[],[CallStmt(Id('foo'),[Id('a'),Id('b')])])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 370))


    def test71(self):
        input = """Function foo(){
            Call(foo,[a,b[5]]);
        }"""
        expect = Program([FuncDecl(Id('foo'),[],[CallStmt(Id('foo'),[Id('a'),ArrayAccess(Id('b'),[NumberLiteral(5.0)])])])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 371))

    def test72(self):
        input = """Function foo(){
            Call(foo, [2 + x, 4 / y]);
        }"""
        expect = Program([FuncDecl(Id('foo'),[],[CallStmt(Id('foo'),[
            BinaryOp('+',NumberLiteral(2.0),Id('x')),BinaryOp('/',NumberLiteral(4.0),Id('y'))])])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 372))

    def test73(self):
        input = """Function foo(){
            Call(foo, [Call(bar,[])]);
        }"""
        expect = Program([FuncDecl(Id('foo'),[],[CallStmt(Id('foo'),[CallExpr(Id('bar'),[])])])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 373))

    def test74(self):
        input = """Function foo(){
            Call(foo, [Call(bar,[a])]);
        }"""
        expect = Program([FuncDecl(Id('foo'),[],[CallStmt(Id('foo'),[CallExpr(Id('bar'),[Id('a')])])])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 374))

    def test75(self):
        input = """Function foo(){
            Call(foo,[]);
        }"""
        expect = Program([FuncDecl(Id('foo'),[],[CallStmt(Id('foo'),[])])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 375))  

    """test assign statement"""
    def test76(self):
        input = """Function foo(){
           x = Call(foo,[]) ;
        }"""
        expect = Program([FuncDecl(Id('foo'),[],[Assign(Id('x'),CallExpr(Id('foo'),[]))])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 376))   
 
    def test77(self):
        input = """Function foo(){
           x = 3 ;
        }"""
        expect = Program([FuncDecl(Id('foo'),[],[Assign(Id('x'),NumberLiteral(3.0))])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 377)) 

    def test78(self):
        input = """Function foo(){
           x[5] = 3 ;
        }"""
        expect = Program([FuncDecl(Id('foo'),[],[Assign(ArrayAccess(Id('x'),[NumberLiteral(5.0)]),NumberLiteral(3.0))])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 378)) 

    def test79(self):
        input = """Function foo(){
           a[i] = (b + 1) * $a;
        }"""
        expect = Program([FuncDecl(Id('foo'),[],[
            Assign(ArrayAccess(Id('a'),[Id('i')]),BinaryOp('*',BinaryOp('+',Id('b'),NumberLiteral(1.0)),Id('$a')))])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 379)) 

    def test80(self):
        input = """Function foo(){
           a[2] = Call(foo, [2]) + Call(foo, [Call(bar, [2, 3])]);   
        }"""
        expect = Program([FuncDecl(Id('foo'),[],[
            Assign(ArrayAccess(Id('a'),[NumberLiteral(2.0)]),BinaryOp('+',CallExpr(Id('foo'),[NumberLiteral(2.0)]),
                CallExpr(Id('foo'),[CallExpr(Id('bar'),[NumberLiteral(2.0),NumberLiteral(3.0)])])))])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 380)) 

    def test81(self):
        input = """Function foo(){
           a[Call(foo, [2])] = a[b{"name"}{"first"}] + 4;  
        }"""
        expect = Program([FuncDecl(Id('foo'),[],[Assign(ArrayAccess(Id('a'),[CallExpr(Id('foo'),[NumberLiteral(2.0)])]),
            BinaryOp('+',ArrayAccess(Id('a'),[JSONAccess(Id('b'),[StringLiteral('name'),StringLiteral('first')])]),NumberLiteral(4.0)))])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 381)) 

    def test82(self):
        input = """Function foo(){
           a[3 + Call(foo, [2])] = a[b[2,3]] + 4;
        }"""
        expect = Program([FuncDecl(Id('foo'),[],[Assign(ArrayAccess(Id('a'),[BinaryOp('+',NumberLiteral(3.0),CallExpr(Id('foo'),[NumberLiteral(2.0)]))]),
            BinaryOp('+',ArrayAccess(Id('a'),[ArrayAccess(Id('b'),[NumberLiteral(2.0),NumberLiteral(3.0)])]),NumberLiteral(4.0)))])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 382)) 

    def test83(self):
        input = """Function foo(){
           x[5] = [3,4] ;
        }"""
        expect = Program([FuncDecl(Id('foo'),[],[Assign(ArrayAccess(Id('x'),[NumberLiteral(5.0)]),ArrayLiteral([NumberLiteral(3.0),NumberLiteral(4.0)]))])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 383)) 

    def test84(self):
        input = """Function foo(){
           x = "John will pass PPL" ;
        }"""
        expect = Program([FuncDecl(Id('foo'),[],[Assign(Id('x'),StringLiteral('John will pass PPL'))])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 384)) 

    def test85(self):
        input = """Function foo(){
           x = 3.33 ;
        }"""
        expect = Program([FuncDecl(Id('foo'),[],[Assign(Id('x'),NumberLiteral(3.33))])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 385)) 

    """for some more decleration test"""
    def test86(self):
        input = """Let r = 10, v;"""
        expect = Program([VarDecl(Id('r'), [], NoneType(), NumberLiteral(10.0)),VarDecl(Id('v'),[],NoneType(),None)])
        self.assertTrue(TestAST.checkASTGen(input, expect, 386))

    def test87(self):
        input = """Constant $r = 10, $v=3;"""
        expect = Program([ConstDecl(Id('$r'), [], NoneType(), NumberLiteral(10.0)),ConstDecl(Id('$v'),[],NoneType(),NumberLiteral(3.0))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 387))

    def test88(self):
        input = """Constant $r = 10;
                   Let v=3;"""
        expect = Program([ConstDecl(Id('$r'), [], NoneType(), NumberLiteral(10.0)),VarDecl(Id('v'),[],NoneType(),NumberLiteral(3.0))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 388))


    def test89(self):
        input = """Let x[2] : String = ["First Name","Last Name"] ;"""
        expect = Program([VarDecl(Id('x'), [NumberLiteral(2.0)], StringType(),ArrayLiteral([StringLiteral('First Name'),StringLiteral('Last Name')]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 389))

    """some more index and key assign test"""
    def test90(self):
        input = """Function foo(){
           x[5,3,1] = 20.21 ;
        }"""
        expect = Program([FuncDecl(Id('foo'),[],[Assign(ArrayAccess(Id('x'),[NumberLiteral(5.0),NumberLiteral(3.0),NumberLiteral(1.0)]),
          NumberLiteral(20.21))])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 390)) 

    def test91(self):
        input = """Function foo(){
           x[5,3] = a{"Id"}{"name"} + 4 ;
        }"""
        expect = Program([FuncDecl(Id('foo'),[],[Assign(ArrayAccess(Id('x'),[NumberLiteral(5.0),NumberLiteral(3.0)]),
          BinaryOp('+',JSONAccess(Id('a'),[StringLiteral('Id'),StringLiteral('name')]),NumberLiteral(4.0)))])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 391)) 

    def test92(self):
        input = """Function foo(){
           x[5,3] = a{"Id"}{"name"};
        }"""
        expect = Program([FuncDecl(Id('foo'),[],[Assign(ArrayAccess(Id('x'),[NumberLiteral(5.0),NumberLiteral(3.0)]),
          JSONAccess(Id('a'),[StringLiteral('Id'),StringLiteral('name')]))])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 392)) 

    def test93(self):
        input = """Function foo(){
           a{"Id"} = "1711376" ;
        }"""
        expect = Program([FuncDecl(Id('foo'),[],[Assign(JSONAccess(Id('a'),[StringLiteral('Id')]),StringLiteral('1711376'))])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 393)) 

    def test94(self):
        input = """Function foo(){
           a{"name"} = "John" ;
        }"""
        expect = Program([FuncDecl(Id('foo'),[],[Assign(JSONAccess(Id('a'),[StringLiteral('name')]),StringLiteral('John'))])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 394)) 

    def test95(self):
        input = """ Let a : JSON = {
                     name: "John",
                     id: "1711376",
                     address: "Nghe An"
                    };
                    Function foo(){
                        a{"name"} = "John Hoan";
        }"""
        expect = Program([VarDecl(Id('a'), [], JSONType(), 
            JSONLiteral([(Id('name'),StringLiteral('John')),(Id('id'),StringLiteral('1711376')),(Id('address'),StringLiteral('Nghe An'))])),
            FuncDecl(Id('foo'),[],
            [Assign(JSONAccess(Id('a'),[StringLiteral('name')]),StringLiteral('John Hoan'))])])
        self.assertTrue(TestAST.checkASTGen(input, expect, 395))

    def test96(self):
        input = """ Let a : JSON = {
                     name: "John",
                     id: "1711376",
                     address: "Nghe An"
                    };
                    Function foo(){
                    
                    Let x = "I will pass PPL 202";
        }"""
        expect = Program([VarDecl(Id('a'), [], JSONType(), 
            JSONLiteral([(Id('name'),StringLiteral('John')),(Id('id'),StringLiteral('1711376')),(Id('address'),StringLiteral('Nghe An'))])),
            FuncDecl(Id('foo'),[],
            [ VarDecl(Id('x'),[],NoneType(),StringLiteral('I will pass PPL 202'))]
            )])
        self.assertTrue(TestAST.checkASTGen(input, expect, 396))   

    def test97(self):
        input = """ Let a : JSON = {
                     name: "John",
                     id: "1711376",
                     address: "Nghe An"
                    };
                    Function foo(){
                    
                    Let x : String = "I will pass PPL 202";
        }"""
        expect = Program([VarDecl(Id('a'), [], JSONType(), 
            JSONLiteral([(Id('name'),StringLiteral('John')),(Id('id'),StringLiteral('1711376')),(Id('address'),StringLiteral('Nghe An'))])),
            FuncDecl(Id('foo'),[],
            [ VarDecl(Id('x'),[],StringType(),StringLiteral('I will pass PPL 202'))]
            )])
        self.assertTrue(TestAST.checkASTGen(input, expect, 397)) 

    def test98(self):
        input = """ Let a : JSON = {
                     name: "John",
                     id: "1711376",
                     address: "Nghe An"
                    };
                    Function foo(){
                    
                    Let b: String = a{"name"} + a{"address"};
        }"""
        expect = Program([VarDecl(Id('a'), [], JSONType(), 
            JSONLiteral([(Id('name'),StringLiteral('John')),(Id('id'),StringLiteral('1711376')),(Id('address'),StringLiteral('Nghe An'))])),
            FuncDecl(Id('foo'),[],
            [ VarDecl(Id('b'),[],StringType(),BinaryOp('+',JSONAccess(Id('a'),[StringLiteral('name')]),JSONAccess(Id('a'),[StringLiteral('address')])))]
            )])
        self.assertTrue(TestAST.checkASTGen(input, expect, 398)) 

    def test99(self):
        input = """Let x[2, 3] = [[1, 2, 3], [4, 5, 6]];"""
        expect = Program([VarDecl(Id('x'),[NumberLiteral(2.0),NumberLiteral(3.0)],NoneType(),ArrayLiteral([ArrayLiteral([NumberLiteral(1.0),NumberLiteral(2.0),NumberLiteral(3.0)]),ArrayLiteral([NumberLiteral(4.0),NumberLiteral(5.0),NumberLiteral(6.0)])]))])
        self.assertTrue(TestAST.checkASTGen(input, expect, 399))



        # something wrong!, you can not declare an array inside function.