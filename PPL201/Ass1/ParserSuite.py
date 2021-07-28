import unittest
from TestUtils import TestParser

class ParserSuite(unittest.TestCase):
    def test_1(self):
        """Simple program: Var declaration """
        input = """ Var: a = 0.5, b = 72.e2, c = "HCMUT", d = 52, e; """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,201))
    
    def test_2(self):
        input = """ Var: r = 10., v; """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,202))
    
    def test_3(self):
        """Missing ':' in declaration"""
        input = """ Var r = 10., v; """
        expect = "Error on line 1 col 5: r"
        self.assertTrue(TestParser.checkParser(input,expect,203))

    def test_4(self):
        """Missing ';' in declaration"""
        input = """ Var: r = 10., v """
        expect = "Error on line 1 col 17: <EOF>"
        self.assertTrue(TestParser.checkParser(input,expect,204))

    def test_5(self):
        """Global variable declaration and Function"""
        input = """ Var: r = 10;
                    Function: abc
                    Body:
                    EndBody.
                    """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,205))

    def test_6(self):
        """Global variable declaration and Function missing Body"""
        input = """ Var: r = 10;
                    Function: abc
                """
        expect = "Error on line 3 col 16: <EOF>"
        self.assertTrue(TestParser.checkParser(input,expect,206))

    def test_7(self):
        input = """ Var: r = 10;
                    Function: abc
                    Parameter:
                    Body:
                    EndBody.
                """
        expect = "Error on line 4 col 20: Body"
        self.assertTrue(TestParser.checkParser(input,expect,207))

    def test_8(self):
        input = """ Var: r = 10;
                    Function: abc
                    Parameter: n = 8
                    Body:
                    EndBody.
                """
        expect = "Error on line 3 col 33: ="
        self.assertTrue(TestParser.checkParser(input,expect,208))
    
    def test_9(self):
        input = """ Var: r = 10;
                    Function: abc
                    Parameter: n, m
                    Body:
                    EndBody.
                """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,209))

    def test_10(self):
        input = """ Var: r = 10;
                    Function: abc
                    Parameter: n, 8
                    Body:
                    EndBody.
                """
        expect = "Error on line 3 col 34: 8"
        self.assertTrue(TestParser.checkParser(input,expect,210))

    def test_11(self):
        input = """ Var: r = 10;
                    Function: abc
                    Parameter: n, a[5][7], bcd[9]
                    Body:
                    EndBody.
                """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,211))

    def test_12(self):
        input = """ Var: r = 10;
                    Function: abc
                    Parameter: n, a[5][7], bcd[9]
                    Body:
                        Var: r = 10., v;
                        v = (4. \. 3.) *. 3.14 *. r *. r *. r;
                    EndBody.
                """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,212))

    def test_13(self):
        input = """ Var: r = 10;
                    Function: abc
                    Parameter: n, a[5][7], bcd[9]
                    Body:
                        Var: r = 10., v;
                        v = (4. \. 3.) *. 3.14 *. r *. r *. r;
                        Var: t = 58;
                    EndBody.
                """
        expect = "Error on line 7 col 24: Var"
        self.assertTrue(TestParser.checkParser(input,expect,213))

    def test_13(self):
        input = """ Var: r = 10;
                    Function: abc
                    Parameter: n, a[5][7], bcd[9]
                    Body:
                        Var: r = 10., v;
                        v = (4. \. 3.) *. 3.14 *. r *. r *. r;
                        Var: t = 58;
                    EndBody.
                """
        expect = "Error on line 7 col 24: Var"
        self.assertTrue(TestParser.checkParser(input,expect,213))

    def test_14(self):
        input = """ Var: r = 10;
                    Function: abc
                    Parameter: n, a[5][7], bcd[9]
                    Body:
                        Var: r = 10., v;
                        v = (4. \. 3.) *. 3.14 *. r *. r *. r;
                        If Then
                        ElseIf Then
                        Else
                        EndIf.
                    EndBody.
                """
        expect = "Error on line 7 col 27: Then"
        self.assertTrue(TestParser.checkParser(input,expect,214))

    def test_15(self):
        input = """ Var: r = 10;
                    Function: abc
                    Parameter: n, a[5][7], bcd[9]
                    Body:
                        Var: r = 10., v;
                        v = (4. \. 3.) *. 3.14 *. r *. r *. r;
                        If (a==5) || (a != b-7) && !a Then
                        EndIf.
                    EndBody.
                """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,215))

    def test_16(self):
        input = """ Var: r = 10;
                    Function: abc
                    Parameter: n, a[5][7], bcd[9]
                    Body:
                        If (a==5) || (a != b-7) && !a 
                            Then a = 7;
                                If e - 7 == 96 Then
                                EndIf
                        EndIf.
                    EndBody.
                """
        expect = "Error on line 9 col 24: EndIf"
        self.assertTrue(TestParser.checkParser(input,expect,216))

    def test_17(self):
        input = """ Var: r = 10;
                    Function: abc
                    Parameter: n, a[5][7], bcd[9]
                    Body:
                        Var: r = 10., v;
                        v = (4. \. 3.) *. 3.14 *. r *. r *. r;
                        If (a==5) || (a != b-7) && !a 
                            Then a = 7;
                                If e - 7 == 96 Then
                                ElseIf identifier >= (e>8) Then
                                EndIf.
                        EndIf.
                    EndBody.
                """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,217))

    def test_18(self):
        input = """ Var: r = 10;
                    Function: abc
                    Parameter: n, a[5][7], bcd[9]
                    Body:
                        Var: r = 10., v;
                        v = (4. \. 3.) *. 3.14 *. r *. r *. r;
                        If (a==5) || (a != b-7) && !a 
                            Then a = 7;
                                If e - 7 == 96 Then
                                ElseIf identifier >= (e>8) Then
                                Else a = 7
                                EndIf.
                        EndIf.
                    EndBody.
                """
        expect = "Error on line 12 col 32: EndIf"
        self.assertTrue(TestParser.checkParser(input,expect,218))

    def test_19(self):
        input ="""  Var: a = 3, b;
                    Function: main
                    Body:
                    While a<1 Do b=b+1; EndWhile.
                    EndBody.
                """
        expect="successful"
        self.assertTrue(TestParser.checkParser(input,expect,219))

    def test_20(self):
        input ="""  Var: a = 3, b;
                    Function: main
                    Body:
                    While a  == a*5\\7 Do b=b+1; EndWhile.
                    EndBody.
                """
        expect="successful"
        self.assertTrue(TestParser.checkParser(input,expect,220))

    def test_20(self):
        input ="""  Var: a = 3, b;
                    Function: main
                    Body:
                    While a  == a*5\\7 Do b=b+1; EndWhile.
                    EndBody.
                """
        expect="successful"
        self.assertTrue(TestParser.checkParser(input,expect,220))

    def test_21(self):
        input ="""  Var: a = 3, b;
                    Function: main
                    Body:
                    While (a == a*5\\7) || (a > foo(foo1(25,78)*25+i())) Do b=b+1; EndWhile.
                    EndBody.
                """
        expect="successful"
        self.assertTrue(TestParser.checkParser(input,expect,221))

    def test_22(self):
        input ="""  Var: a = 3, b;
                    Function: main
                    Body:
                    While (a == a*5\\7) || (a > foo(foo1(25,78)*25+i())) Do b=foo()+foo1() **there is nothing**; EndWhile.
                    EndBody.
                """
        expect="successful"
        self.assertTrue(TestParser.checkParser(input,expect,222))

    def test_23(self):
        input ="""  Var: a = 3, b;
                    Function: enQueue
                    Body:
                    If(empty(queue)!=null) Then append(element);
                    append(append(append()+8)-9); 
                    EndIf.
                    EndBody.
                """
        expect="successful"
        self.assertTrue(TestParser.checkParser(input,expect,223))

    def test_24(self):
        input ="""  Var: a = 3, b;
                    Function: enQueue
                    Body:
                    If(empty(queue)!=null) Then append(element);
                    append(append(append()+8)-9); 

                    EndIf.
                    EndBody.
                """
        expect="successful"
        self.assertTrue(TestParser.checkParser(input,expect,224))

    def test_25(self):
        input ="""  Var: a = 3, b;
                    Function: enQueue
                    Body:
                    If(empty(queue)!=null) Then append(element);
                    append(append(append()+8)-9); 
                    EndIf.
                    EndBody.
                """
        expect="successful"
        self.assertTrue(TestParser.checkParser(input,expect,225))

    def test_26(self):
        input ="""  Var: a = 3, b;
                    Function: enQueue
                    Body:
                    If(empty(queue)!=null) Then 
                    Var: c = 7;
                    append(element);
                    append(append(append()+8)-9); 
                    EndIf.
                    EndBody.
                """
        expect="successful"
        self.assertTrue(TestParser.checkParser(input,expect,226))
    
    def test_27(self):
        input ="""  Var: a = 3, b;
                    Function: enQueue
                    Body:
                    If(empty(queue)!=null) Then 
                        While e != 5 Do
                            For()  EndFor
                        EndWhile.
                    EndIf.
                    EndBody.
                """
        expect="Error on line 6 col 32: )"
        self.assertTrue(TestParser.checkParser(input,expect,227))

    def test_28(self):
        input ="""  Var: a = 3, b;
                    Function: enQueue
                    Body:
                    If(empty(queue)!=null) Then 
                        While e != 5 Do
                            For( id = 5 ,id < 20,8) Do **do nothing** EndFor.
                        EndWhile.
                    EndIf.
                    EndBody.
                """
        expect="successful"
        self.assertTrue(TestParser.checkParser(input,expect,228))

    def test_29(self):
        input ="""  Var: a = 3, b;
                    Function: enQueue
                    Body:
                    If(empty(queue)!=null) Then 
                        While e != 5 Do
                            For( id = 5 ,id < 20,8) Do **do nothing** EndFor.
                        EndWhile.
                    EndIf.
                    EndBody.
                """
        expect="successful"
        self.assertTrue(TestParser.checkParser(input,expect,229))

    def test_30(self):
        input ="""  Function: foo
                    Parameter: a[7][8], b
                    Body:
                        Return foo(7);
                    EndBody.
                    Function: foo1
                    Body:
                        If True Then Return foo1(7);
                        ElseIf False Then Return foo2(foo(58)+array[5]+True);
                        EndIf.
                    EndBody.
                """
        expect="successful"
        self.assertTrue(TestParser.checkParser(input,expect,230))

    def test_31(self):
        input = """
            Function: delta
            Parameter: a, b, c
            Body:
                Return b * b - 4 * a * c;
            EndBody.
            Function: main
            Body:
                Var: a = 1, b = 4, c = 4, del, x1={{{}}}, x2;
            EndBody.
            """
        expect="successful"
        self.assertTrue(TestParser.checkParser(input,expect,231))

    def test_32(self):
        """ test while """
        input = """
        Function: main
        Body:
            If (n>1) Then
                a=a+1;
            ElseIf (a==5) Then
                While (k<foo(a[n][b])) Do
                    While (f!= 11-k) Do
                        i=i-1;
                    EndWhile.
                EndWhile.
        
        ElseIf (a==6) Then i=i-1;
        Else i=i+2;
        EndIf.
        EndBody.
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,232))

    def test_33(self):
        input = """
             Function: foo 
                Parameter: a[5], b 
                Body: 
                    Var: i = 0; 
                    While (i < 5) Do
                        a[i] = b +. 1.0; 
                        i = i + 1; 
                    EndWhile. 
                EndBody.
            """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,233))

    def test_34(self):
        input = """
             Function: foo 
                Parameter: a[5], b[10] 
                Body: 
                    Var: i = 0; 
                    While (i < 5) Do
                        a[i] = b[2*i]+b[2*i+1] +. 1.0 + c[foo()+foo1()]; 
                        i = i + 1; 
                    EndWhile. 
                EndBody.
            """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,234))

    def test_35(self):
        input = """
            Function: foo 
                Parameter: a[5], b[10] 
                Body: 
                    Var: i = 0; 
                    While (i < 5) Do
                        a[i] = b[2*i]+b[2*i+1] +. 1.0 + c[foo()+foo1()]; 
                        i = i + 1; 
                        Break;
                        Continue;
                    EndWhile. 
                EndBody.

            Function: main
                Body:
                    Var x = -5;
                    printLn();
                    Return 0;
                EndBody.
            
            """
        expect = "Error on line 16 col 24: x"
        self.assertTrue(TestParser.checkParser(input,expect,235))

    def test_36(self):
        input = """
             Function: foo 
                Parameter: a[5], b[10] 
                Body: 
                    Do c = a[i+foo(5)] - b[a[b[8]]];
                    While c < 25
                    EndDo.
                EndBody.
            """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,236))

    def test_37(self):
        """Nhap nham khi co nhieu phep tinh relational trong bieu thuc so sanh"""
        input = """
             Function: foo 
                Parameter: a[5], b[10] 
                Body: 
                    Do c = a[i+foo(5)] - b[a[b[8+a[7+b[8]]]]];
                    While c < 25 || d > 9
                    EndDo.
                EndBody.
            """
        expect = "Error on line 6 col 38: >"
        self.assertTrue(TestParser.checkParser(input,expect,237))

    def test_38(self):
        input = """
             Function: foo 
                Parameter: a[5], b[10] 
                Body: 
                    Do 
                        c = a[i+foo(5)] - b[a[b[8+a[7+b[8]]]]];
                        d = a[5>a[8]];
                    While (c < 25) || (d > 9)
                    EndDo.
                EndBody.
            """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,238))

    def test_39(self):
        input = """
             Function: foo 
                Parameter: a[5], b[10] 
                Body: 
                    Do 
                        c = a[i+foo(5)] - b[a[b[8+a[7+b[8]]]]];
                        d = a[5>a[8]];
                        While i < 50 Do **do nothing**
                        EndWhile.
                    While (c < 25) || (d > 9)
                    EndDo.
                EndBody.
            """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,239))

    def test_40(self):
        input = """
             Function: foo 
                Parameter: a[5], b[10] 
                Body: 
                    Do 
                        c = a[i+foo(5)] - b[a[b[8+a[7+b[8]]]]];
                        d = a[5>a[8]>25];
                    While (c < 25) || (d > 9)
                    EndDo.
                EndBody.
            """
        expect = "Error on line 7 col 36: >"
        self.assertTrue(TestParser.checkParser(input,expect,240))

    def test_41(self):
        input = """
                    Var: x, y, z[1][3];
                    Function: main
                    Body:
                        x[1] = x[1 + foo("3",-9)] + 10;
                    EndBody.
                """
        expect = """successful"""
        self.assertTrue(TestParser.checkParser(input, expect, 241))
    def test_42(self):
        input = """
                    Function: main
                    Body:
                        If bool_of_string ("True") Then
                            a = int_of_string (read ());
                            b = float_of_int (a) +. 2.0;
                        EndIf.
                    EndBody.
                """
        expect ="""successful"""
        self.assertTrue(TestParser.checkParser(input, expect, 242))
    def test_43(self):
        input = """
                    Function: int_to_main
                    Body:
                        a[3 + foo(2)] = a[b[2][3]] + 4;
                    EndBody.
                """
        expect = """successful"""
        self.assertTrue(TestParser.checkParser(input, expect, 243))
    def test_44(self):
        input = """
                    Function: foo
                        Parameter: a[5], b
                        Body:
                            Var: i = 0;
                            While (i < 5) Do
                                a[i] = b +. 1.0;
                                i = i + 1;
                            EndWhile.
                        EndBody.
                """
        expect = """successful"""
        self.assertTrue(TestParser.checkParser(input, expect, 244))
    def test_45(self):
        input = """    
                    Function: abcxyz
                        Body:
                            For (i = 0, i < 10, 2) Do
                                i = i + 1;
                                print(i+2);
                            EndFor. 
                        EndBody.
                """
        expect = """successful"""
        self.assertTrue(TestParser.checkParser(input, expect, 245))
    def test_46(self):
        input = """
                    Function: int_main
                    Body:
                        Var: r = 10., v;
                        v = (4. \\. 3.) *. 3.14 *. r *. r *. r;
                        int_of_string(v+25+a[25]);
                    EndBody.
                """
        expect = """successful"""
        self.assertTrue(TestParser.checkParser(input, expect, 246))
    def test_47(self):
        input = """
                    Var: a[5] = {1,4,3,2,0};
                    Var: b[2][3]={{1,2,3},{4,5,6}};
                    Function: check
                        Body:
                         printLn();
                         print(a ,b)
                        EndBody.
                """
        expect = """Error on line 8 col 24: EndBody"""
        self.assertTrue(TestParser.checkParser(input, expect, 247))

    def test_48(self):
        input = """
                    Var: a[5] = {1,4,3,2,0};
                    Var: b[2][3]={{1,2,3},{4,5,6}};
                    Function: check
                        Body:
                            c = a[-1];
                            printLn();
                            print(a ,b);
                        EndBody.
                """
        expect = """successful"""
        self.assertTrue(TestParser.checkParser(input, expect, 248))

    def test_49(self):
        input = """
                    Var: a[5] = {1,4,3,2,0};
                    Var: b[2][3]={{1,2,3},{4,5,6}};
                    Function: check
                        Body:
                            int_of_float();
                            foo(-a[foo(a[foo(a[foo])])]);
                        EndBody.
                """
        expect = """successful"""
        self.assertTrue(TestParser.checkParser(input, expect, 249))

    def test_50(self):
        input = """
                    Function: main
                        Body:
                            Var: string;
                            string = string_of_int(gcd(number1, "context"));
                        EndBody.
                    Function: gcd
                        Parameter: a, b
                        Body:
                            Return a[1 - (0x1129FC >=. kfc)*foo(a,b)];
                        EndBody.
                """
        expect = """successful"""
        self.assertTrue(TestParser.checkParser(input, expect, 250))

    def test_51(self):
        input = """
        Function: fibonacci
        Parameter: n, o
        Body: 
            If (n == 1) || (n ==2) Then Return 1;
            Else Return fibonacci(n - 1) + fibonacci(n - 2);
            EndIf.
        EndBody.
        Function: main
        Parameter: n
        Body:
            printLn (\"nhap n: \");
            printStrLn(\"HCMUT\");
            cout (\"So fibonacci thu Fibonacci(n)\");
            Return 0;
        EndBody.
        
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,251))

    def test_52(self):
        input = """
                    Function: factorial
                        Parameter: col
                        Body:
                            bray[insert(foo + a[1][2][factorial()*0o714])] = arr[b[1][2][3]];
                            printLn(factorial);
                        EndBody.
                """
        expect = """successful"""
        self.assertTrue(TestParser.checkParser(input, expect, 252))
    
    def test_53(self):
        """ test while """
        input = """
        Function: fact
        Parameter: n
            Body:
                Var: k=20;
                If n<=1 Then Return 1;
                Else Return n*fact(n-1);
                EndIf.
            EndBody.
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,253))

    def test_54(self):
        """ test while """
        input = """
        Function: fact
        Parameter: n
            Body:
                Var: k=20;
                If n<=1 Then Return 1;
                Else Return n*fact(n-1)[25][25+foo()];
                EndIf.
            EndBody.
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,254))

    def test_55(self):
        """ index operator """
        input = """
        Function: fact
        Parameter: n
            Body:
                Var: k=20;
                If n<=1 Then Return 1;
                Else Return n*fact(n-1)[25][25+foo()||45*63];
                EndIf.
            EndBody.
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,255))

    def test_56(self):
        input = """
                Function: real_madrid_cf
                Parameter: ronaldo
                Parameter: sergio ramos

                Body:
                    **do nothing**
                EndBody.
            
                """
        expect = "Error on line 4 col 16: Parameter"
        self.assertTrue(TestParser.checkParser(input,expect,256))

    def test_57(self):
        input = """
                Function: real_madrid_cf
                Parameter: ronaldo, sergio_ramos
                Body:
                    Var: luka_modric, toni_kroos;
                    print(toni_kroos,"chuyen",luka_modric,"tat bong",sergio_ramos,"danh dau","goalllllll");
                    ronaldo = arr[4555];
                EndBody.
            
                """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,257))

    def test_58(self):
        input = """
                Function: real_madrid_cf
                Parameter: ronaldo, sergio_ramos
                Body:
                    Var: luka_modric, toni_kroos;
                    print(toni_kroos,"chuyen",luka_modric,"tat bong",sergio_ramos,"danh dau","goalllllll");
                    ronaldo = arr[4555+fooo(b[8]-"string"[25[25]])];
                EndBody.
            
                """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,258))

    
    def test_59(self):
        input = """
            Var: i=1;
            Function: foo
                Parameter: int
                Body:
                While (x == 1.08765 *. 2.098 || True) Do
                    x = x +. 1;
                    y = {1,2,3} *. 985475;
                    z = "This is a string" =/= "abcdxzy";
                EndWhile.
                EndBody.
            """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 259))

    def test_60(self):
        input=""" Var: a, b, c[5] = 5, 6, 7; """;
        expect="Error on line 1 col 22: 6"
        self.assertTrue(TestParser.checkParser(input,expect,260))

    def test_61(self):
        input = """
             Function: foo 
                Parameter: a[5], b 
                Body: 
                    If bool_of_string ("True") Then 
                        a = int_of_string (read ()); 
                        b = float_of_int (a) +. 2.0; 
                    EndIf.
                EndBody.
            """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,261))

    def test_62(self):
        input = """
             Function: hash_file Body:
                        **This is a comment**

                        **hashlib function**
                        h = hashlib * sha1();

                        ** open file for reading in binary mode
                        with open(filename,'rb') as file:**

                        ** loop till the end of the file**
                        chunk = 0;
                        While chunk != b Do
                            ** read only 1024 bytes at a time**
                            chunk = file*read();
                            h = h && update(chunk);
                        EndWhile.
                        Return;
                    EndBody.
            """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,262))

    def test_63(self):
        """Thieu EndIf truoc EndWhile"""
        input = """
        Var: b ; 
        Function: dd
        Parameter: pp
        Body:  
            Do 
                If (a + 0o12) Then **do something** EndIf.
                While dd(9) Do 
                    If (a[5]) Then **do something**  **if staement**
                EndWhile.
                While t*t 
                Do
                EndWhile.
            While foo(8)
            EndDo.   
        EndBody.
        """
        expect = "Error on line 10 col 16: EndWhile"
        self.assertTrue(TestParser.checkParser(input,expect,263))

    def test_64(self):
        input = """
                Var: b ; 
                Function: foo
                Parameter: p
                Body:  
                    a[10] = b()[10+20[25]];
                EndBody.
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,264))

    def test_65(self):
        input = """
                Var: b; 
                Function: foo
                Parameter: p
                Body: 
                    Var: i; 
                    Var: a[20];
                    For(i = index(0),True,temp[10][10]) Do
                        a[i] = a[i]*b[i][2*i+1];
                        If a[i] < 0 Then Break; EndIf.
                    EndFor.
                    a[10] = b()[10+20[25]];
                EndBody.
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,265))

    def test_66(self):
        input = """
                Var: b; 
                Function: foo
                Parameter: p
                Body: 
                    Var: i; 
                    Var: a[20];
                    For(i = index(0),True,temp[10][10]) Do
                        a[i] = a[i]*b[i][2*i+1];
                        If a[i] < 0 Then Continue;
                        ElseIf a[i] == 0 Then 
                            If fFF()[25] Then **Do Nothing** EndIf.
                    EndFor.
                    a[10] = b()[10+20[25]];
                EndBody.
        """
        expect = "Error on line 13 col 20: EndFor"
        self.assertTrue(TestParser.checkParser(input,expect,266))

    def test_67(self):
        input = """
                    Function: createTable
                    Body:
                        Var: j=1;
                        Var: output = "<table border=\'"\'" width=\'"500\'" cellspacing=\'"0\'"cellpadding=\'"5\'">";
                        For(i=1, i<=rows, i+1) Do
    	                    output = output + "<tr>";
                        EndFor.
                        While(j<=cols) Do
  		                    output = output + "<td>" + i*j + "</td>";
   		                    j = j+1;
   		                output = output + "</tr>";
   		                j = 1;
                        EndWhile.
                    EndBody.
                """
        expect = """successful"""
        self.assertTrue(TestParser.checkParser(input, expect, 267))

    def test_68(self):
        input = """
                Var: b; 
                Function: foo
                Parameter: p
                Body: 
                    Var: i; 
                    Var: a[20];
                    While True Do print("Hello World"); EndWhile.
                EndBody.
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,268))


    def test_69(self):
        input = """
                Function: factorial
                Parameter: n
                Body: 
                    If n <= 1 Then Return 1;
                    Else Return n * fact(n-1);
                    EndIf.
                EndBody.

                Function: sum_factorial
                Parameter: n
                Body:
                    Var: sum = 0;
                    Var: i;
                    For(i=0,i<=n,1) Do sum = sum + factorial(i);
                    EndFor.
                    Return sum;
                EndBody.
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,269))

    def test_70(self):
        input = """
                Function: factorial
                Parameter: n
                Body: 
                    If n <= 1 Then Return 1;
                    Else Return n * fact(n-1);
                    EndIf.
                EndBody.

                Function: sum_factorial
                Parameter: n
                Body:
                    Var: sum = 0;
                    Var: i;
                    For(i=0,i<=n,1) Do sum = sum + factorial(i);
                    EndFor.
                    Return sum;
                EndBody.

                Function: main
                Body:
                    print(print(sum_factorial(20)) + a[25] + foo()[36]); 
                    Return 0;
                EndBody.
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,270))

    def test_71(self):
        input = """
                Var: c[5] = {{5  ,2   ,8}, {5,   8}};

                Function: main
                Body:
                    print(print(sum_factorial(20)) + a[25] + foo()[36]); 
                    Return 0;
                EndBody.
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,271))

    def test_72(self):
        """Khong khoi tri cho bien bang so am"""
        input = """
                Var: c[5] = {{5  ,2   ,8}, {5,   8}};
                Var: t = 5;
                Var: e = 7;
                Var: a[4] = -7;

                Function: main
                Body:
                    print(print(sum_factorial(20)) + a[25] + foo()[36]); 
                    Return 0;
                EndBody.
        """
        expect = "Error on line 5 col 28: -"
        self.assertTrue(TestParser.checkParser(input,expect,272))

    def test_73(self):
        """Chi duoc khoi tao mot bien cuc bo sau Body"""
        input = """
                Var: c[5] = {{5  ,2   ,8}, {5,   8}};
                Function: main
                Body:
                    Var: t = 5;
                    Var: e = 7;
                    Var: a[4] = 7;
                    print(print(sum_factorial(20)) + a[25] + foo()[36]); 
                    Var: c = 7;
                    Return 0;
                EndBody.
        """
        expect = "Error on line 9 col 20: Var"
        self.assertTrue(TestParser.checkParser(input,expect,273))

    def test_74(self):
        input = """
        Var: x;
        Function: main
        Body:
           Var: a[10];
           a[3 + foo(2)] = a[b[2][3]] + 3;
           Return 0;
        EndBody.
        """
        self.assertTrue(TestParser.checkParser(input, "successful",274))

    def test_75(self):
        input = """
            Var: c[5][25*69];    
            """
        expect = "Error on line 2 col 24: *"
        self.assertTrue(TestParser.checkParser(input,expect,275))

    def test_76(self):
        input = """
                Function: foo
                Body:
                    a = (25+9)[5];
                EndBody.
            """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,276))

    def test_77(self):
        input = """Function: main Body:
                    str1 = "\\b\\t\\n\\r\\f\\'  String";
                    str2 = str1 * 10 \\ foo(4,1,a[2][a[2][3]]);
                EndBody."""
        expect = """successful"""
        self.assertTrue(TestParser.checkParser(input, expect, 277))

    def test_78(self):
        input = """
                Function: foo
                Body:
                    a = (25+9)[25+9[25+9[a[25+6]]]] + {1,2   ,       3};
                EndBody.
            """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,278))

    def test_79(self):
        input = """
                Function: foo
                Body:
                    a = (25+9)[25+9[25+{}+9[a[25+6]]]] + {1,2   ,       3};
                EndBody.
            """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,279))

    def test_80(self):
        input = """
                Function: foo
                Body:
                    If True Then
                        If True Then
                            If True Then
                            EndIf.
                        EndIf.
                    EndIf.
                EndBody.
            """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,280))

    def test_81(self):
        input = """
                Function: foo
                Body:
                    While True Do
                        While True Do
                            While True Do
                            EndWhile.
                        EndWhile.
                    EndWhile.
                EndBody.
            """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,281))

    def test_82(self):
        input = """
                Function: foo
                Body:
                    Return foo[25] - (3)[25];
                EndBody.
            """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,282))

    def test_83(self):
        input = """
                Function: foo
                Body:
                    Return foo(25+oo()[25]+foo(foo(---foo())));
                EndBody.
            """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,283))

    def test_84(self):
        input = """ Var: a = 2; 
        Function: main
        Parameter: a
        Body:
        y = \"a\"; 
        z[foo(2)*3] = {1.5,9};
        k[(a)] = 5;
        a[10+foo(2)][8] =  a(9);  
        foo(2); 
        EndBody.
        Function: abc
        Parameter: a
        Body:
        y = True; 
        a[10+foo(2)][8] =  a(9);  
        foo(2); 
        EndBody."""
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,284))

    def test_85(self):
        input = """ Var: a = 2; 
            foo(25);
        """
        expect = "Error on line 2 col 12: foo"
        self.assertTrue(TestParser.checkParser(input,expect,285))

    def test_86(self):
        input = """ Var: a = 2; 
            If True Then ** do something ** EndIf.;
        """
        expect = "Error on line 2 col 12: If"
        self.assertTrue(TestParser.checkParser(input,expect,286))

    def test_87(self):
        input = """ Var: a = 2; 
            a = a + 7;
        """
        expect = "Error on line 2 col 12: a"
        self.assertTrue(TestParser.checkParser(input,expect,287))

    def test_88(self):
        input = """ Var: a = 2;
            Function: tem
            Body:
                Var: a[5] = 25 + 7;
            EndBody.
        """
        expect = "Error on line 4 col 31: +"
        self.assertTrue(TestParser.checkParser(input,expect,288))

    def test_89(self):
        input = """ Var: a = 2; 
            Function: tem
            Body:
                Var: a[5] = 25;
                For(i = 7, i < 25, i) Do 
                    For(i = 7, i < 25, j) Do
                        For(i = 7, i < 25, j) Do EndFor. EndFor. EndFor.
            EndBody.
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,289))

    def test_90(self):
        input = """ Var: a = 2; 
            Function: tem
            Body:
                Var: a[5] = 25;
                For(i = 7, i < 25, i + 99) Do **Do something** EndFor.
            EndBody.
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,290))

    def test_91(self):
        input = """ Function: main
            Body:
            blu = 123 * 23 - 123 - -.--.- "dasd";
            While a == 123 Do
                tttttttest();
            EndWhile.
            EndBody.
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,291))

    def test_92(self):
        input = """ Function: main
            Body:
            blu = 123 * 23 - 123 - -.--.- "dasd" +++++++++++ ------------------ 25;
            EndBody.
        """
        expect = "Error on line 3 col 50: +"
        self.assertTrue(TestParser.checkParser(input,expect,292))

    def test_93(self):
        input = """
        Function: hi
        Body:
        For i=1, i<2, n++ Do
            **do something**
        EndFor.
        readln();
        EndBody. 
        """
        expect = "Error on line 4 col 12: i"
        self.assertTrue(TestParser.checkParser(input,expect,293))

    def test_94(self):
        input = """
        Function: hi
        Body:
        For (i=1, i<2, n++) Do
            a = a +1;
        EndFor.
        readln();
        EndBody. 
        """
        expect = "Error on line 4 col 25: +"
        self.assertTrue(TestParser.checkParser(input,expect,294))

    def test_95(self):
        input = """
        Function: fail
        Body:
        For (i=1, 1 , 1) Do 
        a [5+foo(2)][g+8] = a[a+b[0]\\5] ;
        n = m *;
        EndFor.
        EndBody. 
        """
        expect = "Error on line 6 col 15: ;"
        self.assertTrue(TestParser.checkParser(input,expect,295))

    def test_96(self):
        input = """
        Function: hi
        Body:
        For (i=1, i<2, foo()[foo + 25[25]]) Do
            a = a +1;
        EndFor.
        readln();
        EndBody. 
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,296))

    def test_97(self):
        input = """
        Function: hi
        Var x = 5;
        Body:

        EndFor.
        readln();
        EndBody. 
        """
        expect = "Error on line 3 col 8: Var"
        self.assertTrue(TestParser.checkParser(input,expect,297))

    def test_98(self):
        input = """
        Function: hi
        Body:
            Var: a;
            a = {} + {} + {{{{{{}}}}}} + {"string", "string", {"this is string", True, {12e5, 15E2, 0X88}}};
        readln();
        EndBody. 
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,298))

    def test_99(self):
        input = """
        Function: hi
        Body:
            Var: a;
            a[25] = {} + {} + {{{{{{}}}}}} + {"string", "string", {"this is string", True, {12e5, 15E2, 0X88}}};
            b = {}[25];
        readln();
        EndBody. 
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,299))

    def test_100(self):
        input = """
        Function: hi
        Body:
            Var: a;
            a[25] = {} + {} + {{{{{{}}}}}} + {"string", "string", {"this is string", True, {12e5, 15E2, 0X88}}};
            b = {}[25];
            c = {"string",{"this is a string", 19e6, 13.e8}}[25];
        readln();
        EndBody. 
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,300))