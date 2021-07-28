import unittest
from TestUtils import TestChecker
from StaticError import *
from AST import *


class CheckSuite(unittest.TestCase):


    def test01(self):
        """Simple program: main"""
        input = """

            Function main() {
            Call(foo, ["Hoan","John"]);
        }
        Function foo(x,r) {
            Let a;
            a = x + r;
            Return a;
        }       
        """
        expect = str(TypeMismatchInExpression(BinaryOp('+',Id('x'),Id('r'))))
        self.assertTrue(TestChecker.test(input, expect, 401))
    def test02(self):
        """Simple program: main"""
        input = """
            Function main() {
            x = x + 5;
        }
        
        """
        # input = Program([FuncDecl(Id('foo'),[],[CallStmt(Id('foo'), [])])])
        expect = str(Undeclared(Identifier(),'x'))
        self.assertTrue(TestChecker.test(input, expect, 402))

    def test03(self):
        """More complex program"""
        input = Program([ VarDecl(Id("main"),[],StringType(),None)
            ,FuncDecl(Id("main"), [],  [
                CallStmt(Id("printStrLn"), [])
                ])])
        expect = str(Redeclared(Function(),"main"))
        self.assertTrue(TestChecker.test(input, expect, 403))

    def test04(self):
        """Complex program"""
        input = """Function main() {
            Call(printSLn, []);
        }"""
        expect = str(TypeMismatchInStatement(CallStmt(Id("printSLn"), [])))
        self.assertTrue(TestChecker.test(input, expect, 404))

    def test05(self):
        """More complex program"""
        input = """Function main() {
            Call(printSLn, [Call(read, [4])]);
        }
        """
        expect = str(TypeMismatchInExpression(
            CallExpr(Id("read"), [NumberLiteral(4.0)])))
        self.assertTrue(TestChecker.test(input, expect, 405))

    def test06(self):
        """Simple program: main """
        input = Program([FuncDecl(Id("main"), [], [
            CallExpr(Id("foo"), [])])])
        expect = str(Undeclared(Function(), "foo"))
        self.assertTrue(TestChecker.test(input, expect, 406))

    def test07(self):
        """More complex program"""
        input = Program([
            FuncDecl(Id("main"), [],[
                CallStmt(Id("printSLn"), [
                    CallExpr(Id("read"), [NumberLiteral(4.0)])
                ])])])
        expect = str(TypeMismatchInExpression(
            CallExpr(Id("read"), [NumberLiteral(4.0)])))
        self.assertTrue(TestChecker.test(input, expect, 407))

    def test08(self):
        """Complex program"""
        input = Program([
            FuncDecl(Id("main"), [], [
                CallStmt(Id("printSLn"), [])])])
        expect = str(TypeMismatchInStatement(CallStmt(Id("printSLn"), [])))
        self.assertTrue(TestChecker.test(input, expect, 408))

    """Test no entry point"""
    def test09(self):
        input = """
        Function foo(x,y){
        Return x+y;
        }
        """
        expect = str(NoEntryPoint())
        self.assertTrue(TestChecker.test(input, expect, 409))

    """Test Undeclared"""

    def test10(self):
        input = """
        Function main(){
        Return x+y;
        }
        """
        expect = str(Undeclared(Identifier(), 'x'))
        self.assertTrue(TestChecker.test(input, expect, 410))

    def test11(self):
        input = """
        Function main(){
            Call(foo, []);
        }
        """
        expect = str(Undeclared(Function(), 'foo'))
        self.assertTrue(TestChecker.test(input, expect, 411))

    def test12(self):
        """Simple program: main """
        input = Program([FuncDecl(Id("main"),[],[
            CallExpr(Id("foo"),[])])])
        expect = str(Undeclared(Function(),"foo"))
        self.assertTrue(TestChecker.test(input,expect,412))


    """test Redeclared"""
    def test13(self):
        input = """
        Function main(){
            Let x;
            Let x;
        }
        """
        expect = str(Redeclared(Variable(), 'x'))
        self.assertTrue(TestChecker.test(input, expect, 413))

    def test14(self):
        input = """
        Function main(){
            Let x;
        }
        Function main(){
            Let x;
        }       
        """
        expect = str(Redeclared(Function(), 'main'))
        self.assertTrue(TestChecker.test(input, expect, 414))

    def test15(self):
        input = """
        Function main(x, x){
            Return x;
        }
        """
        expect = str(Redeclared(Parameter(), 'x'))
        self.assertTrue(TestChecker.test(input, expect, 415))

    """test TypeMismatchInExpression"""

    def test16(self):
        input = """
        Function main(){
            Let x: Number;
            x = 3 + "PPL202";
        }
        """
        expect = str(TypeMismatchInExpression(BinaryOp('+',NumberLiteral(3.0),StringLiteral('PPL202'))))
        self.assertTrue(TestChecker.test(input, expect, 416))

    def test17(self):
        input = """
        Function main(){
            Let x:Number = 5;
            If (x<"John") {
                x = x -1;
            }
        }
        """
        expect = str(TypeMismatchInExpression(BinaryOp('<',Id('x'),StringLiteral('John'))))
        self.assertTrue(TestChecker.test(input, expect, 417))

    def test18(self):
        input = """
        Function main(){
            Let x:Number = 5;
            While (x<"John") {
                x = x - 1;
            }
        }
        """
        expect = str(TypeMismatchInExpression(BinaryOp('<',Id('x'),StringLiteral('John'))))
        self.assertTrue(TestChecker.test(input, expect, 418))

    def test19(self):
        input = """
        Function main(){
            Let x:Number = 5;
            If (x<10) {
                x = x - 1;
            }
            Elif (x +. 1){
                Return x;
            }
        }
        """
        expect = str(TypeMismatchInExpression(BinaryOp('+.',Id('x'),NumberLiteral(1.0))))
        self.assertTrue(TestChecker.test(input, expect, 419))

    def test20(self):
        input = """
        Function main(){
            Let x:String;
            While (x ==. 5) {
                x = x - 1;
            }
        }
        """
        expect = str(TypeMismatchInExpression(BinaryOp('==.',Id('x'),NumberLiteral(5.0))))
        self.assertTrue(TestChecker.test(input, expect, 420))

    def test21(self):
        input = """
        Function main(){
            Let x:String;
            While (x != 5) {
                x = x - 1;
            }
        }
        """
        expect = str(TypeMismatchInExpression(BinaryOp('!=',Id('x'),NumberLiteral(5.0))))
        self.assertTrue(TestChecker.test(input, expect, 421))


    def test22(self):
        input = """
            Function main()
            {
                Let x;
                x = x + Call(foo,[]);
            }
            Function foo()
            {
                Return 1.0 +. Call(foo,[]);
            }
        """
        expect = str(TypeMismatchInExpression((BinaryOp("+.",NumberLiteral(1.0),CallExpr(Id("foo"),[])))))
        self.assertTrue(TestChecker.test(input,expect,422))

    def test23(self):
        """More complex program"""
        input = """Function main() 
                    {
                        Call(printSLn,[Call(read,[4])]);
                    }
                    """
        expect = str(TypeMismatchInExpression(CallExpr(Id("read"),[NumberLiteral(4.0)])))
        self.assertTrue(TestChecker.test(input,expect,423))

    def test24(self):
        input = """
            Let x = 10.0;
            Function factorial(n)
            {
                If (n <= 1) {
                 Return n*Call(factorial,[n-1]);
                }
                Else {
                Return 1;
                } 
                
            }
            Function main()
            {
                Return Call(factorial,[]);
            }
        """
        expect = str(TypeMismatchInExpression(CallExpr(Id("factorial"),[])))
        self.assertTrue(TestChecker.test(input,expect,424))

    def test25(self):
        input = """
        Function main(){
            Let x:Number = 5;
            If (!x) {
                x = x -1;
            }
        }
        """
        expect = str(TypeMismatchInExpression(UnaryOp('!',Id('x'))))
        self.assertTrue(TestChecker.test(input, expect, 425))    

    def test26(self):
        input = """
            Let a = 1;
            Function foo(x,y)
            {
                a = x + y;
                Return a;
            }

            Function main()
            {
                Let x, y;
                x = Call(foo, [1, 1.1]);
                y = "John" +. x;
            }
        """
        expect = str(TypeMismatchInExpression(BinaryOp('+.',StringLiteral('John'),Id('x'))))
        self.assertTrue(TestChecker.test(input, expect, 426))

    def test27(self):
        input = """
            Let x = 1;
            Function foo(x,y,z)
            {
                x = 0;
                y = 0.0;
                Return y;
            }

            Function main()
            {
                Let x = 1.1, y;
                x = Call(foo,[1, 1.1, "string"]);
                x = 1 + Call(foo,[1, 1.1, 15]);
            }
        """
        expect = str(TypeMismatchInExpression(CallExpr(Id('foo'),[NumberLiteral(1.0),NumberLiteral(1.1),NumberLiteral(15.0)])))
        self.assertTrue(TestChecker.test(input, expect, 427))

    def test28(self):
      input = """
      Function main(){
          Let x:Boolean = False, y = 3;
          If (!x) {
              y = y - False;
          }
      }
      """
      expect = str(TypeMismatchInExpression( BinaryOp('-',Id('y'),BooleanLiteral('false'))))
      self.assertTrue(TestChecker.test(input, expect, 428))  

    def test29(self):
      input = """
      Function main(){
          Let x: Number;
          x = 3 + 5;
          Return !x;
      }
      """
      expect = str(TypeMismatchInExpression(UnaryOp('!',Id('x'))))
      self.assertTrue(TestChecker.test(input, expect, 429))

    def test30(self):
      input = """
      Function main(){
          Let x: Number, y = "John";
          y = -x +. "Hoan";
          Return x;
      }
      """
      expect = str(TypeMismatchInExpression(BinaryOp('+.',UnaryOp('-',Id('x')),StringLiteral('Hoan'))))
      self.assertTrue(TestChecker.test(input, expect, 430))

    """test TypeMismatchInStatement"""

    def test31(self):
        input = """
        Function main(){
            Let x:Number = 5;
            Let b: Number;
            While (x < 10) {
                b = "John" +. "Hoan";
            }
        }
        """
        expect = str(TypeMismatchInStatement(Assign(Id('b'),BinaryOp('+.',StringLiteral('John'),StringLiteral('Hoan')))))
        self.assertTrue(TestChecker.test(input, expect, 431))
    def test32(self):
        input = """
        Function main(){
            Let x:Number = 5;
            For i In x {
                x = x -1;
            }
        }
        """
        expect = str(TypeMismatchInStatement(ForIn(Id('i'),Id('x'),[Assign(Id('x'),BinaryOp('-',Id('x'),NumberLiteral(1.0)))])))
        self.assertTrue(TestChecker.test(input, expect, 432))

    def test33(self):
      input = """
      Function main(){
          Let x: Number, y = "John";
          y = -x;
          Return x;
      }
      """
      expect = str(TypeMismatchInStatement(Assign(Id('y'),UnaryOp('-',Id('x')))))
      self.assertTrue(TestChecker.test(input, expect, 433))

    def test34(self): 
        input = """
            Functionfoo()
            {
                Return;
            }
            Function foo1(x,y)
            {
                x = Call(foo,[]);
            }
            Function main()
            {}
        """
        expect = str(TypeMismatchInStatement(Assign(Id("x"),CallExpr(Id("foo"),[]))))
        self.assertTrue(TestChecker.test(input,expect,434))

    def test35(self):
        input = """
            Function main()
            {
                Let a = True;
                Call(foo,[a]);
            }
            Function foo(a)
            {
                While (1)
                {
                a = a && True;
                }
            }
        """
        expect = str(TypeMismatchInStatement(While(NumberLiteral(1.0),[Assign(Id('a'),BinaryOp('&&',Id('a'),BooleanLiteral('true')))])))
        self.assertTrue(TestChecker.test(input,expect,435))


    def test36(self):
        input = """
            Let x = 10.0;
            Function factorial(n)
            {
                If (!1) {
                 Return n*Call(factorial,[n-1]);
                }
                Else {
                Return 1;
                } 
                
            }
            Function main()
            {
                Return Call(factorial,[]);
            }
        """
        expect = str(TypeMismatchInExpression(UnaryOp('!',NumberLiteral(1.0))))
        self.assertTrue(TestChecker.test(input,expect,436))

    def test37(self): 
        input = """
            Function foo(){
            Return;
            }
            Function foo1(x,y)
            {
                x = Call(foo,[]);
            }
            Function main()
            {}
        """
        expect = str(TypeMismatchInStatement(Assign(Id("x"),CallExpr(Id("foo"),[]))))
        self.assertTrue(TestChecker.test(input,expect,437))

    def test38(self):
        input = """
            Let a, b;
            Function foo(x,y,z)
            {
                Return;
            }
            Function main()
            {
                If (b + 0) { 
                    Return a; 
                }
                Call(foo,[1,2,3]);
            }
        """
        expect = str(TypeMismatchInStatement(If([(BinaryOp('+',Id('b'),NumberLiteral(0.0)),[Return(Id('a'))])],[])))
        self.assertTrue(TestChecker.test(input, expect, 438))

    def test39(self):
        input = """
            Let a, b;
            Function foo(x,y,z)
            {
                Return;
            }
            Function main()
            {
                Let b = 1;
                If (b ==. "John") { 
                    Return a; 
                }
                Call(foo,[1,2,3]);
            }
        """
        expect = str(TypeMismatchInExpression(BinaryOp('==.',Id('b'),StringLiteral('John'))))
        self.assertTrue(TestChecker.test(input, expect, 439))


    def test40(self):
        input = """
            Let a, b;
            Function foo(x,y,z)
            {
                Return;
            }
            Function main()
            {
                If (b * 0) { 
                    Return a; 
                }
                Call(foo,[1,2,3]);
            }
        """
        expect = str(TypeMismatchInStatement(If([(BinaryOp('*',Id('b'),NumberLiteral(0.0)),[Return(Id('a'))])],[])))
        self.assertTrue(TestChecker.test(input, expect, 440))

    def test41(self):
        input = """
            Function main()
            {
                Let a = 5;
                Call(foo,[a]);
            }
            Function foo(a)
            {
                While (a+1)
                {
                a = a && True;
                }
            }
        """
        expect = str(TypeMismatchInStatement(While(BinaryOp('+',Id('a'),NumberLiteral(1.0)),[Assign(Id('a'),BinaryOp('&&',Id('a'),BooleanLiteral('true')))])))
        self.assertTrue(TestChecker.test(input,expect,441))

    def test42(self):
        input = """
            Function main()
            {
                Let a = 5;
                Call(foo,[a]);
            }
            Function foo(a)
            {
                While (a)
                {
                a = a && True;
                }
            }
        """
        expect = str(TypeMismatchInStatement(While(Id('a'),[Assign(Id('a'),BinaryOp('&&',Id('a'),BooleanLiteral('true')))])))
        self.assertTrue(TestChecker.test(input,expect,442))

    def test43(self):
        input = """
            Function main()
            {
                Call(foo,[1,2]);
                Return 0;
            }
            Function foo(a,b)
            {
                a = Call(foo,[1,1]);
            }          
        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,443))

    def test44(self):
        input = """
            Function main()
            {
                Call(foo,[1]);
            }
          
            Function foo(){}
        """
        expect = str(TypeMismatchInStatement(CallStmt(Id("foo"),[NumberLiteral(1.0)])))
        self.assertTrue(TestChecker.test(input,expect,444))

    def test45(self):
        input = """
            Function main()
            {
                For i In 1 {
                    Return 1;
                }
            }
        """
        expect = str(TypeMismatchInStatement(ForIn(Id('i'),NumberLiteral(1.0),[Return(NumberLiteral(1.0))])))
        self.assertTrue(TestChecker.test(input,expect,445))

    def test46(self):
        input = """
            Function main()
            {
                For i In (1 + 2) {
                    Return 1;
                }
            }
        """
        expect = str(TypeMismatchInStatement(ForIn(Id('i'),BinaryOp('+',NumberLiteral(1.0),NumberLiteral(2.0)),[Return(NumberLiteral(1.0))])))
        self.assertTrue(TestChecker.test(input,expect,446))

    def test47(self):
        input = """
            Function main()
            {
                For i Of (1 + 2) {
                    Return 1;
                }
            }
        """
        expect = str(TypeMismatchInStatement(ForOf(Id('i'),BinaryOp('+',NumberLiteral(1.0),NumberLiteral(2.0)),[Return(NumberLiteral(1.0))])))
        self.assertTrue(TestChecker.test(input,expect,447))

    def test48(self):
        input = """
            Function main()
            {
                For i Of 1 {
                    Return 1;
                }
            }
        """
        expect = str(TypeMismatchInStatement(ForOf(Id('i'),NumberLiteral(1.0),[Return(NumberLiteral(1.0))])))
        self.assertTrue(TestChecker.test(input,expect,448)) 

    def test49(self):
        input = """

            Function main()
            {
                If (1) { 
                    Return 1; 
                }
            }
        """
        expect = str(TypeMismatchInStatement(If([(NumberLiteral(1.0),[Return(NumberLiteral(1.0))])],[])))
        self.assertTrue(TestChecker.test(input, expect, 449))

    def test50(self):
        input = """
            Function main()
            {
                For i Of [1,3] {
                    Return 1;
                }
            }
        """
        expect = str(TypeMismatchInStatement(ForOf(Id('i'),ArrayLiteral([NumberLiteral(1.0),NumberLiteral(3.0)]),[Return(NumberLiteral(1.0))])))
        self.assertTrue(TestChecker.test(input,expect,450)) 
    
    """test TypeCannotBeInferred"""
    def test51(self):
        input = """
            Function main()
            {}
            Function foo(a, b)
            {
                While (Call(foo,[b,a]))
                {
                a = a && True;
                Return 1;
                }
            }

        """
        expect = str(TypeCannotBeInferred(While(CallExpr(Id('foo'),[Id('b'),Id('a')]),[Assign(Id('a'),BinaryOp('&&',Id('a'),BooleanLiteral('true'))),Return(NumberLiteral(1.0))])))
        self.assertTrue(TestChecker.test(input,expect,451))

    def test52(self):
        input = """
            Function main()
            {
             Let y, a, x;
             y = a + Call(foo, [x]);
            }
            Function foo(a)
            {
            }


        """
        expect = str(TypeCannotBeInferred(BinaryOp('+',Id('a'),CallExpr(Id('foo'),[Id('x')]))))
        self.assertTrue(TestChecker.test(input,expect,452))

    def test53(self):
        input="""
            Function foo(a,b)
            {
                Let c;
                For i In [1,10] {
                    c = Call(foo,[c,a]);
                }
                Return -1;
            }
            Function main()
            {
                Let z;
                z = Call(foo, [1,2]) + Call(foo, [True, False]);
            }
        """
        expect=str(TypeCannotBeInferred(Assign(Id('c'),CallExpr(Id('foo'),[Id('c'),Id('a')]))))
        self.assertTrue(TestChecker.test(input,expect,453))

    def test54(self):
        input = """
            Function main()
            {
                Return 0;
            }
            Function foo(a,b)
            {
                a = Call(foo,[1,True]);
                Return;
            }
        """
        expect = str(TypeCannotBeInferred(Assign(Id('a'),CallExpr(Id('foo'),[NumberLiteral(1.0),BooleanLiteral('true')]))))
        self.assertTrue(TestChecker.test(input,expect,454))

    def test55(self):
        input = """
            Function main()
            {
                Let a = {
                 name: "Yanxi Place",
                 address: "Chinese Forbidden City",
                 surface: 10.2,
                 people: ["Empress Xiaoxianchun", "Yongzheng Emperor"]
                };
                For i In a{
                    Return 1;
                }
            }
        """
        expect = str(TypeMismatchInStatement(ForIn(Id('i'),Id('a'),[Return(NumberLiteral(1.0))])))
        self.assertTrue(TestChecker.test(input,expect,455)) 

    def test56(self):
        input = """
            Function main()
            {
                Let t;
                Call(foo,[t]);
            }
            Function foo(n){

            }
        """
        expect = str(TypeCannotBeInferred(CallStmt(Id('foo'),[Id('t')])))
        self.assertTrue(TestChecker.test(input,expect,456))

    def test57(self):
        input = """
            Function main(){

            }
            Function foo()
            {
                Return Call(foo,[]);
            }
            
        """
        expect = str(TypeCannotBeInferred(Return(CallExpr(Id('foo'),[]))))
        self.assertTrue(TestChecker.test(input,expect,457))

    def test58(self):
        input = """
            Function main()
            {
                Let x;
                Call(foo,[x, Call(foo,[x, True])]);
            }
            Function foo(x,y)
            {
                Return True;
            }
        """
        expect = str(TypeCannotBeInferred(CallStmt(Id('foo'),[Id('x'),CallExpr(Id('foo'),[Id('x'),BooleanLiteral('true')])])))
        self.assertTrue(TestChecker.test(input,expect,458))

    def test59(self):
        input = """
            Function main()
            {
                Let t;
                t = Call(foo,[t]) + t;
            }
            Function foo(n){}
        """
        expect = str(TypeCannotBeInferred(BinaryOp('+',CallExpr(Id('foo'),[Id('t')]),Id('t'))))
        self.assertTrue(TestChecker.test(input,expect,459))
    

    def test60(self):
        input = """
            Function main()
            {
                Let x,y;
                x = x + Call(foo,[y]);
            }
            Function foo(n)
            {
                Return 1;
            }
        """
        expect = str(TypeCannotBeInferred(BinaryOp('+',Id('x'),CallExpr(Id('foo'),[Id('y')]))))
        self.assertTrue(TestChecker.test(input,expect,460))


    def test61(self):
        input = """
        Function main()
        { 
            Let x;
            Let y;
            x = y;
        }"""
        expect = str(TypeCannotBeInferred(Assign(Id('x'), Id('y'))))
        self.assertTrue(TestChecker.test(input, expect, 461))

    def test62(self):
        input = """
        Function main()
        {
            Let a[5],i;
            For i In [1,5]{
                Let x;
                a[i] = x;
            }
        }"""
        expect = str(TypeCannotBeInferred(Assign(ArrayAccess(Id('a'), [Id('i')]), Id('x'))))
        self.assertTrue(TestChecker.test(input, expect, 462))

    def test63(self):
        input = """ Function foo(a,b){}
                    Function main()
                    {
                        Let a,b;
                        a = a + Call(foo,[a,b]);
                    }"""
        expect = str(TypeCannotBeInferred(BinaryOp('+',Id('a'),CallExpr(Id('foo'),[Id('a'),Id('b')]))))
        self.assertTrue(TestChecker.test(input, expect, 463))


    def test64(self):
        input = """
        Function main()
        { 
            Let a,b;
            a = b;
        }"""
        expect = str(TypeCannotBeInferred(Assign(Id('a'), Id('b'))))
        self.assertTrue(TestChecker.test(input, expect, 464))


    def test65(self):
        input = """
            Function foo(a,b){}
            Function main()
            {
                Let a,b;
                If (Call(foo,[a,b])) { 
                    Return 1; 
                }
            }
        """
        expect = str(TypeCannotBeInferred(If([(CallExpr(Id('foo'),[Id('a'),Id('b')]),[Return(NumberLiteral(1.0))])],[])))
        self.assertTrue(TestChecker.test(input, expect, 465))


    def test66(self):
        input = """
            Function main()
            {
                Let a;
                Return a;
            }
        """
        expect = str(TypeCannotBeInferred(Return(Id('a'))))
        self.assertTrue(TestChecker.test(input, expect, 466))

    def test67(self):
        input = """
            Let x;
            Function main(x)
            {
                Return x;
            }
        """
        expect = str(TypeCannotBeInferred(Return(Id('x'))))
        self.assertTrue(TestChecker.test(input, expect, 467))

    """Mix up all stuff"""
    def test68(self):
        input = """ Function main()
                    {
                        Let a,b;
                        a = a + 1;
                        b = !a;
                    }"""
        expect = str(TypeMismatchInExpression(UnaryOp('!', Id('a'))))
        self.assertTrue(TestChecker.test(input, expect, 468))

    def test69(self):
        input = """ Function main()
                    {
                        Let a,b;
                        Call(a,[]);
                    }
                    """
        expect = str(Undeclared(Function(), "a"))
        self.assertTrue(TestChecker.test(input, expect, 469))


    def test70(self):
        input = """

            Function main() {
            Call(foo, ["Hoan","John"]);
        }
        Function foo(x,r) {
            Let a;
            a = x +. r;
            Return a;
        }       
        """
        expect = str()
        self.assertTrue(TestChecker.test(input, expect, 470))

    def test71(self):
        input = """

            Function main() {
            Let a, b, c;
            c = 2;
            b = 3;
            a = b+c;
            Return a;
        }   
        """
        expect = str()
        self.assertTrue(TestChecker.test(input, expect, 471))

    def test72(self):
        input = """
            Function main()
            {
                Let a[2] = ["Hoan","John"];
                Call(read,[]);
            }
        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,472)) 


    def test73(self):
        input = """
            Function main()
            {
                Call(read,[1]);
            }
        """
        expect = str(TypeMismatchInStatement(CallStmt(Id('read'),[NumberLiteral(1.0)])))
        self.assertTrue(TestChecker.test(input,expect,473))  

    def test74(self):
        input = """
            Function main()
            {
                Call(print,["John Hoan will pass PPL202"]);
            }
        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,474))  

    def test75(self):
        input = """
            Function main()
            {
                Let a = "John";
                Call(read,[a]);
            }
        """
        expect = str(TypeMismatchInStatement(CallStmt(Id('read'),[Id('a')])))
        self.assertTrue(TestChecker.test(input,expect,475))  

    def test76(self):
        input = """
            Function main()
            {
                Let a = 1;
                a = Call(read,[]);
            }
        """
        expect = str(TypeMismatchInStatement(Assign(Id('a'),CallExpr(Id('read'),[]))))
        self.assertTrue(TestChecker.test(input,expect,476)) 

    def test77(self):
        input = """
            Function main()
            {
                Let a: String;
                a = Call(printSLn,[]);
            }
        """
        expect = str(TypeMismatchInExpression(CallExpr(Id('printSLn'),[])))
        self.assertTrue(TestChecker.test(input,expect,477)) 

    def test78(self):
        input = """
            Function main()
            {
                Let a: String = "Hoan";
                Let name;
                name = Call(printSLn,["John"]) + a;
                Return name;
            }
        """
        expect = str(TypeMismatchInExpression(BinaryOp('+',CallExpr(Id('printSLn'),[StringLiteral('John')]),Id('a'))))
        self.assertTrue(TestChecker.test(input,expect,478)) 

    def test79(self):
        input = """
            Function foo(x){
                Return "John";
            }
            Function main()
            {
                Let a: String = "Hoan";
                Let name;
                name = Call(foo,["John"]) +. a;
                Return name;
            }
        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,479)) 

    def test80(self):
        input = """
            Function foo(x){
                Return 1;
            }
            Function main()
            {
                Let a: String = "Hoan";
                Let name;
                name = Call(foo,["John"]) +. a;
                Return name;
            }
        """
        expect = str(TypeMismatchInExpression(BinaryOp('+.',CallExpr(Id('foo'),[StringLiteral('John')]),Id('a'))))
        self.assertTrue(TestChecker.test(input,expect,480)) 

    def test81(self):
        input = """
            Function foo1(x){
                Return 1;
            }
            Function foo()
            {
                Let a: String = "Hoan";
                Let name;
                name = Call(foo1,["John"]) +. a;
                Return name;
            }
        """
        expect = str(NoEntryPoint())
        self.assertTrue(TestChecker.test(input,expect,481))  
    def test82(self):
        input = """
            Function foo1(x){
                Return x;
            }
            Function main()
            {
                Let a: String = "Hoan";
                While(Call(foo1,[a]) ==. a){
                    Return;
                }
            }
        """
        expect = str(TypeCannotBeInferred(Return(Id('x'))))
        self.assertTrue(TestChecker.test(input,expect,482))     

    def test83(self):
        input = """
            Function main()
            {
                Let a: String = "Hoan";
                While(Call(foo1,[a]) ==. a){
                    Return;
                }
            }
            Function foo1(x){
                Return x;
            }
        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,483))     

    def test84(self):
        input = """
            Function main()
            {
                Let a: String = "Hoan";
                While((Call(foo1,[a]) +. a)==."John Hoan"){
                    Return;
                }
            }
            Function foo1(x){
                Return x;
            }
        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,484))  

    def test85(self):
        input = """
            Function main()
            {
                Let a;
                While((Call(foo1,[a]) +. a)==."John Hoan"){
                    Return;
                }
            }
            Function foo1(x){
                Return x;
            }
        """
        expect = str(TypeCannotBeInferred(BinaryOp('+.',CallExpr(Id('foo1'),[Id('a')]),Id('a'))))
        self.assertTrue(TestChecker.test(input,expect,485))  

    def test86(self):
        input = """ Let a,b;
                    Function main(a[3],b[3],a){}"""
        expect = str(Redeclared(Parameter(), 'a'))
        self.assertTrue(TestChecker.test(input, expect, 486))

    def test87(self):
        input = """ Function main(a[3],b[3])
                    {
                        Let a,b;
                    }"""
        expect = str(Redeclared(Variable(), 'a'))
        self.assertTrue(TestChecker.test(input, expect, 487))

    def test88(self):
        input = """ Function main()
                    { 
                        Let a=1;
                        a = "John";
                    }"""
        expect = str(TypeMismatchInStatement(Assign(Id('a'), StringLiteral('John'))))
        self.assertTrue(TestChecker.test(input, expect, 488))


    def test89(self):
        input = """
            Function main()
            {
                Let x,y,z,t,k;
                k = ((((z+1)>y)&&(t<t+1)) || ((x-7)<9)) && !x;
            }
        """
        expect = str(TypeMismatchInExpression(UnaryOp('!',Id('x'))))
        self.assertTrue(TestChecker.test(input,expect,489))

    def test90(self):
        input = """
            Function main()
            {
                Let a,y,z,t,k;
                k = ((((z+1)>y)&&(t<t+1)) || ((a-7)<9)) && !a;
            }
        """
        expect = str(TypeMismatchInExpression(UnaryOp('!',Id('a'))))
        self.assertTrue(TestChecker.test(input,expect,490))

    def test91(self):
        input = """
            Function main()
            {
                Let a;
                a = Call(foo,[]);
            }
            Function foo()
            {
                Return 1;
            }
        """
        expect = str(TypeCannotBeInferred(Assign(Id('a'),CallExpr(Id('foo'),[]))))
        self.assertTrue(TestChecker.test(input,expect,491))

    def test92(self):
        input = """
            Function foo()
            {
                Return 1;
            }
            Function main()
            {
                Let a;
                a = Call(foo,[]);
            }

        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,492))

    def test93(self):
        input = """
            Function main()
            {
                Let a;
                a = 1;
            }
            Function foo(x)
            {
                Let foo;
                Return foo + 1;
            }
        """
        expect = str()
        self.assertTrue(TestChecker.test(input,expect,493))

    def test94(self):
        input = """
            Function main()
            {
                For i Of a {
                }
            }
        """
        expect = str(Undeclared(Identifier(), 'a'))
        self.assertTrue(TestChecker.test(input,expect,494))

    def test95(self):
        input = """
            Function main()
            {
                Let a = {
                 name: "Yanxi Place",
                 address: "Chinese Forbidden City",
                 surface: 10.2,
                 people: ["Empress Xiaoxianchun", "Yongzheng Emperor"]
                };
                a = 1;
            }
        """
        expect = str(TypeMismatchInStatement( Assign(Id('a'),NumberLiteral(1.0))))
        self.assertTrue(TestChecker.test(input,expect,495)) 

    def test96(self):
        input = """
            Function main()
            {
                Let a = {
                 name: "Yanxi Place",
                 address: "Chinese Forbidden City",
                 surface: 10.2,
                 people: ["Empress Xiaoxianchun", "Yongzheng Emperor"]
                };
                a = "Tired";
            }
        """
        expect = str(TypeMismatchInStatement(Assign(Id('a'),StringLiteral('Tired'))))
        self.assertTrue(TestChecker.test(input,expect,496)) 


    def test97(self):
        input = """
            Function main()
            {
                Let a = {
                 name: "Yanxi Place",
                 address: "Chinese Forbidden City",
                 surface: 10.2,
                 people: ["Empress Xiaoxianchun", "Yongzheng Emperor"]
                };
                While(!a){

                }
            }
        """
        expect = str(TypeMismatchInExpression(UnaryOp('!',Id('a'))))
        self.assertTrue(TestChecker.test(input,expect,497)) 
    def test98(self):
        input = """ 
        Function main()
        {
            Let foo;
            Call(foo,[]);
        }"""
        expect = str(Undeclared(Function(), "foo"))
        self.assertTrue(TestChecker.test(input, expect, 498))

    def test99(self):
        input = """
            Function main()
            {
                Let a: String;
                a = Call(printSLn,["Mackeno"]);
            }
        """
        expect = str(TypeMismatchInStatement(Assign(Id('a'),CallExpr(Id('printSLn'),[StringLiteral('Mackeno')]))))
        self.assertTrue(TestChecker.test(input,expect,499)) 

    def test100(self):
        input = """
            Function main()
            {
                Let a: Number = "I will pass PPL202";
                Return a;
            }
        """
        expect = str(TypeMismatchInStatement(VarDecl(Id('a'),[],NumberType(),StringLiteral('I will pass PPL202'))))
        self.assertTrue(TestChecker.test(input,expect,500)) 

