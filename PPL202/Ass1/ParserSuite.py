import unittest
from TestUtils import TestParser

class ParserSuite(unittest.TestCase):
    def test_1(self):
        
        input = """ Let a = 0.5, b = 72.e2, c = "HCMUT", d = 52, e; """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,201))
    
    def test_2(self):
        input = """ Let r = 10., v; """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,202))
    
    def test_3(self):
        
        input = """ let r = 10., v; """
        expect = "Error on line 1 col 1: let"
        self.assertTrue(TestParser.checkParser(input,expect,203))

    def test_4(self):
        
        input = """ Let r = 10., v """
        expect = "Error on line 1 col 16: <EOF>"
        self.assertTrue(TestParser.checkParser(input,expect,204))

    def test_5(self):
        input = """ Let r = 10;
                    Function abc()
                    { }
                    """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,205))

    def test_6(self):
        
        input = """ Let r = 10;
                    Function abc()
                """
        expect = "Error on line 3 col 16: <EOF>"
        self.assertTrue(TestParser.checkParser(input,expect,206))

    def test_7(self):
        input = """ Let r = 10;
                    Function abc ():
                """
        expect = "Error on line 2 col 35: :"
        self.assertTrue(TestParser.checkParser(input,expect,207))

    def test_8(self):
        input = """ Let r = 10;
                    Function abc { }
                """
        expect = "Error on line 2 col 33: {"
        self.assertTrue(TestParser.checkParser(input,expect,208))
    
    def test_9(self):
        input = """ Let r = 10;
                    Function abc(n,m,a[4]){ }
                """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,209))

    def test_10(self):
        input = """ Let r = 10;
                    Function abc($a , a[2,3,4]) { }
                """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,210))

    def test_11(self):
        input = """ Let r = 10;
                    Function abc (n, a[5,7], bcd[9]) { }
                """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,211))

    def test_12(self):
        input = """ Constant $a = 10;
                    Function foo(a[5], b) {
                    Constant $b: String = "Story of Yanxi Place";
                    Let i = 0;
                    While (i < 5) {
                    a[i] = (b + 1) * $a;
                    Let u: Number = i + 1;
                    If (a[u] == 10) {
                    Return $b;
                    }
                    i = i + 1;
                    }
                    Return $b + ": Done";
                    }
                """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,212))

    def test_13(self):
        input = """ Function foo(a[5], b) {
                    Let i = 0;
                    While (i < 5) {
                    a[i] = b + 1;
                    Let u: Number = i + 1;
                    If (a[u] == 10) {
                    Return a[i];
                    }
                    }
                    Return -1;
                    }
                """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,213))


    def test_14(self):
        input = """ Function foo (a[5], b,) {
                    Let i = 0;
                    While (i < 5) {
                    a[i] = b + 1;
                    let u: Integer = i + 1;
                    If (a[u] == 10) {
                    Return a[i];
                    }
                    }
                    Return -1;
                    }
                """
        expect = "Error on line 1 col 23: )"
        self.assertTrue(TestParser.checkParser(input,expect,214))

    def test_15(self):
        input = """ Function foo(a[5], b) {
                    Let i = 0;
                    While (i < 5) {
                    a[i] = b + 1;
                    Let u: String = i + 1;
                    If (a[u] == 10) {
                    Continue;
                    }
                    }
                    Return -10;
                    }
                """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,215))

    def test_16(self):
        input = """ Let r = 10;
                    Function abc (n, a[5,7], bcd[9])
                    {
                        If ((a==5) || (a != b-7) && !a){
                        return -1;
                        }
                    }
                """
        expect = "Error on line 5 col 31: -"
        self.assertTrue(TestParser.checkParser(input,expect,216))

    def test_17(self):
        input = """ Let r = 10;
                    Function abc (n, a[5,7], bcd[9])
                    {
                        Let r = 10., v;
                        v = (4. +  3.) *. 3.14 *. r *. r *. r;
                        If ((a==5) || (a != b) && !a){
                           a = 123 * 3232;
                           Let smt: String = "print that Dont give it up" ;
                        } 
                        Else {
                           stm = "Try it harder!" ;
                        }
                    }
                """
        expect = "Error on line 5 col 40: ."
        self.assertTrue(TestParser.checkParser(input,expect,217))

    def test_18(self):
        input = """ Let r = 10;
                    Function abc (n, a[5,7], bcd[9])
                    {
                        Let r = 10., v;
                        v = (4. +  3.) * 3.14 * r * r * r;
                        If ((a==5) || (a != b) && !a){
                           a = 123 * 3232;
                           Let smt: String = "print that Dont give it up" ;
                        } 
                        Else{
                           stm = "Try it harder!" ;
                        }
                    }
                """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,218))

    def test_19(self):
        input ="""  Let a = 3, b;
                    Function main ()
                    {
                    While (a<1) {
                    b=b+1; 
                    } 
                    }
                """
        expect="successful"
        self.assertTrue(TestParser.checkParser(input,expect,219))

    def test_20(self):
        input ="""  Let a = 3, b;
                    Function main()
                    {
                    For a In [1, 3, 4] {
                    b=a+1; 
                    } 
                    }
                """
        expect="successful"
        self.assertTrue(TestParser.checkParser(input,expect,220))

    def test_20(self):
        input ="""  Let a = 3, b;
                    Function main()
                    {
                    While (a>=3) {
                     Break; 
                    } 
                    }
                """
        expect="successful"
        self.assertTrue(TestParser.checkParser(input,expect,220))

    def test_21(self):
        input ="""   Let a = 3, b;
                    Function main()
                    {
                    For a Of x{
                    b=a+1; 
                    } 
                    }
                """
        expect="successful"
        self.assertTrue(TestParser.checkParser(input,expect,221))

    def test_22(self):
        input ="""   Let a = 3, b;
                    Function main()
                    {
                    For a In [1, 3, 4] {
                    b=a+1; 
                    } 
                    return a+132;
                    }
                """
        expect="Error on line 7 col 27: a"
        self.assertTrue(TestParser.checkParser(input,expect,222))

    def test_23(self):
        input ="""   Let a = 3, b;
                    Function main ()
                    {
                    a[foo(2)] = a[b["name"]["first"]] + 4;
                    }
                """
        expect="Error on line 4 col 25: ("
        self.assertTrue(TestParser.checkParser(input,expect,223))

    def test_24(self):
        input ="""  Let a = {
                      name: "Yanxi Place",
                      address: "Chinese Forbidden City",
                      surface: 10.2,
                      people: ["Empress Xiaoxianchun", "Yongzheng Emperor"]
                      };
                    Function main()
                    {
                    a[2] = a[a["name"]["first"]] + 4;
                    }
                """
        expect="successful"
        self.assertTrue(TestParser.checkParser(input,expect,224))

    def test_25(self):
        input ="""  Let a = {
                      name: "Yanxi Place",
                      address: "Chinese Forbidden City",
                      surface: 10.2,
                      people: ["Empress Xiaoxianchun", "Yongzheng Emperor"]
                      };
                    Function main()
                    {
                    Let b: String = a["name"] + a["address"];
                    Return b;
                    }
                """
        expect="successful"
        self.assertTrue(TestParser.checkParser(input,expect,225))

    def test_26(self):
        input ="""  Let a = 3, b;
                    Function enQueue(){
                    If(Call(empty, [queue])!=null){
                    Let c = 7;
                    append(element);
                    append(append(append()+8)-9); 
                    } 

                    }
                """
        expect="Error on line 5 col 26: ("
        self.assertTrue(TestParser.checkParser(input,expect,226))
    
    def test_27(self):
        input ="""  Let a = 3, b;
                    Function enQueue()
                    {
                    If(Call(empty, [queue])!=null) {
                        While (e != 5){
                           ## Do somthing here ##
                        }
                    }
                    }
                """
        expect="successful"
        self.assertTrue(TestParser.checkParser(input,expect,227))

    def test_28(self):
        input ="""   Let a = 3, b;
                    Function enQueue(
                    {
                    If(Call(empty, [queue])!=null) {
                        While (e != 5){
                           ## Do somthing here ##
                        }
                    }
                    }
                """
        expect="Error on line 3 col 20: {"
        self.assertTrue(TestParser.checkParser(input,expect,228))

    def test_29(self):
        input ="""  Let a = 3, b;
                    Function enQueue()
                    {
                    If(Call(empty, [queue])!=null) {
                        While (e != 5){
                            For (i = 5 ,id < 20,8) {##do nothing## }
                        }
                    }
                    }
                """
        expect="Error on line 6 col 32: ("
        self.assertTrue(TestParser.checkParser(input,expect,229))

    def test_30(self):
        input ="""  Let a = 3, b;
                    Function enQueue()
                    {
                    If(Call(empty, [queue])!=null) {
                        While (e != 5){
                            For i In [1,5] {##do something## }
                        }
                    }
                    }
                """
        expect="successful"
        self.assertTrue(TestParser.checkParser(input,expect,230))

    def test_31(self):
        input = """
            Function delta (a, b, c)
            {
                Return b * b - 4 * a * c;
            }
            Function main()
            {
                Let a = 1, b = 4, c = 4, del, x1=[[[]]], x2;
            }
            """
        expect="successful"
        self.assertTrue(TestParser.checkParser(input,expect,231))

    def test_32(self):
        """ test while """
        input = """
        Function main()
        {
            If (n>1) {
                a=a+1;}
            Elif (a==5) {
                While (k<Call(foo, [n,b])) {
                    While (f != 11-k) {
                        i=i- 1;
                    }
                }
        }
        Elif (a==6) { i= i - 1;}
        Else {i=i+2; }
        
        }
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,232))

    def test_33(self):
        input = """
             Function foo (a[5], b) 
                {
                    Let i = 0; 
                    While (i < 5) {
                        a[i] = b + 1.0; 
                        i = i + 1; 
                    }
                }
            """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,233))

    def test_34(self):
        input = """
             Function foo (a[5], b[10] )
                {
                    Let i = 0; 
                    While (i < 5) {
                        a[i] = b[2*i]+b[2*i+1] + 1.0 + c[1]; 
                        i = i + 1; 
                    }
                }
            """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,234))

    def test_35(self):
        input = """
            Function foo (a[5], b[10]) 
                {
                    Let i = 0; 
                    While (i < 5) {
                        a[i] = b[2*i]+b[2*i+1] + 1.0 + c[1]; 
                        i = i + 1; 
                        Break;
                        Continue;
                    }
                }

            Function main()
                {
                    Let x = -5;
                    Call(printLn,[]);
                    Return 0;
                }
            
            """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,235))

    def test_36(self):
        input = """
             Function foo (a[5], b[10]) 
                {
                    c = a[i+Call(foo, [5])] - b[a[b[8]]];
                }
            """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,236))

    def test_37(self):
        """Nhap nham khi co nhieu phep tinh relational trong bieu thuc so sanh"""
        input = """
             Function foo (a[5], b[10]) 
                {
                   While((x>=5) && (x!=10)){
                    c = a[i+Call(foo, [5])] - b[a[b[8+a[7+b[8]]]]];
                    }
                }
            """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,237))

    def test_38(self):
        input = """
              Function foo (a[5], b[10]) 
                {
                   While((x>=5) && (x!=10)){
                    c = a[i+Call(foo, [5])] - b[a[b[8+a[7+b[8]]]]];
                    }
                  Let a = {
                  name: "Yanxi Place",
                  address: "Chinese Forbidden City",
                  surface: 10.2,
                  people: ["Empress Xiaoxianchun", "Yongzheng Emperor"]
                  };
                }
            """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,238))

    def test_39(self):
        input = """
             Function foo (a[5], b[10]) 
                {
                   While((x>=5) && (x!=10)){
                    c = a[i+Call(foo, [5])] - b[a[b[8+a[7+b[8]]]]];
                    }
                  Let a = {
                  name: "Yanxi Place",
                  address: "Chinese Forbidden City",
                  surface: 10.2,
                  people: ["Empress Xiaoxianchun", "Yongzheng Emperor"]
                  }
                }
            """
        expect = "Error on line 13 col 16: }"
        self.assertTrue(TestParser.checkParser(input,expect,239))

    def test_40(self):
        input = """
             Function foo (a[5], b[10]) 
                {
                   While(x>=5 && x!=10)
                    c = a[i+foo(5)] - b[a[b[8+a[7+b[8]]]]];
                    }
                  Let a = {
                  name: "Yanxi Place",
                  address: "Chinese Forbidden City",
                  surface: 10.2,
                  people: ["Empress Xiaoxianchun", "Yongzheng Emperor"]
                  };
                }
            """
        expect = "Error on line 4 col 34: !="
        self.assertTrue(TestParser.checkParser(input,expect,240))

    def test_41(self):
        input = """
                    Let x, y, z[3];
                    Function main()
                    {
                       a[2] = Call(foo, [2]) + Call(foo, [Call(bar, [2, 3])]);
                    }
                """
        expect = """successful"""
        self.assertTrue(TestParser.checkParser(input, expect, 241))
    def test_42(self):
        input = """ Let x, y, z[3];
                    Function main()
                    {
                       a[2] = Call(foo, [2]) + Call(foo [Call(bar, [2, 3])];
                    }
                """
        expect ="""Error on line 4 col 56: ["""
        self.assertTrue(TestParser.checkParser(input, expect, 242))
    def test_43(self):
        input = """
                    Function main()
                    {
                        Call(foo, [2]);
                    }
                """
        expect = """successful"""
        self.assertTrue(TestParser.checkParser(input, expect, 243))
    def test_44(self):
        input = """
                    Function foo (a[5], b)
                        {
                            Let i = 0;
                            While (i < 5){
                                a[i] = b + 1.0;
                                i = i + 1;
                            }
                        }
                """
        expect = """successful"""
        self.assertTrue(TestParser.checkParser(input, expect, 244))
    def test_45(self):
        input = """    
                    Function abcxyz()
                        {
                            For (i = 0, i < 10, 2) {
                                i = i + 1;
                                Call(print, [i+2]);
                            } 
                        }
                """
        expect = """Error on line 4 col 32: ("""
        self.assertTrue(TestParser.checkParser(input, expect, 245))
    def test_46(self):
        input = """
                    Function ()
                    {
                        Let r = 10., v;
                        v = (4. / 3.) * 3.14 * r * r * r;
                        Call(int_of_string, [(v+25+a[25]]);
                    }
                """
        expect = """Error on line 2 col 29: ("""
        self.assertTrue(TestParser.checkParser(input, expect, 246))
    def test_47(self):
        input = """
                        abcxyz()
                        {
                            For i in [1, 10] {
                                i = i + 1;
                                Call(print,[i+2]);
                            } 
                        }
                """
        expect = """Error on line 2 col 24: abcxyz"""
        self.assertTrue(TestParser.checkParser(input, expect, 247))

    def test_48(self):
        input = """
                    Let a[5] = [1,4,3,2,0];
                    Let b[2,3]=[[1,2,3],[4,5,6]];
                    Function check()
                        {
                            c = a[-1];
                            Call(printLn,[]);
                            Call(print,["a"]);
                        }
                """
        expect = """successful"""
        self.assertTrue(TestParser.checkParser(input, expect, 248))

    def test_49(self):
        input = """
                     Let a[5] = [1,4,3,2,0];
                    Let b[2,3]=[[1,2,3],[4,5,6]];
                    Function check()
                        {
                            foo(z, [21]);
                        }
                """
        expect = """Error on line 6 col 31: ("""
        self.assertTrue(TestParser.checkParser(input, expect, 249))

    def test_50(self):
        input = """
                    Let a[5] = [1,4,3,2,0];
                    Let b[2,3]=[[1,2,3],[4,5,6]];
                    Function check()
                        {
                            a[1] = i+5 = 4;
                            return -1;
                        }
                """
        expect = """Error on line 6 col 39: ="""
        self.assertTrue(TestParser.checkParser(input, expect, 250))

    def test_51(self):
        input = """
        Function fibonacci (n, o)
        {
            If ((n == 1) || (n ==2)) { Return 1; }
            Else { Return Call(fibonacci, [n - 1]) + Call(fibonacci, [n - 2]); }
            
        }
        Function main (n)
        {
            Call(printLn, ["nhap n: "]);
            Call(printLn, ["HCMUT"]);
            Call(print, ["So fibonacci thu Fibonacci(n)"]);
            Return 0;
        }
        
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,251))

    def test_52(self):
        input = """
                    Function factorial (col)
                        {
                            bray[Call(insert, [(Call(foo,[]) + a[1,2,Call(factorial, [714])]] = arr[b[1,2,3]];
                            Call(printLn, [factorial]);
                        }
                """
        expect = """Error on line 4 col 66: ,"""
        self.assertTrue(TestParser.checkParser(input, expect, 252))
    
    def test_53(self):
        """ test while """
        input = """
        Function fact (n)
            {
                Let k=20;
                If (n<=1) { Return 1; }
                Else {Return n*Call(fact, [n-1]); }
            }
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,253))

    def test_54(self):
        """ test while """
        input = """
        Function fact(n)
            {
                Let k=20;
                If (n<=1) { Return 1;
                Else {Return n*Call(fact, [n-1]); }
                }
            }
        """
        expect = "Error on line 6 col 16: Else"
        self.assertTrue(TestParser.checkParser(input,expect,254))

    def test_55(self):
        """ index operator """
        input = """
        Functionfact(n)
            {
                Let k=20;
                If (n<=1) { Return 1;}
                Else {Return n*Call(fact, [n - 1]); }
            }
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,255))

    def test_56(self):
        input = """
                Function real_madrid_cf (ronaldo) (sergio ramos)

                {
                    ##do nothing##
                }
            
                """
        expect = "Error on line 2 col 50: ("
        self.assertTrue(TestParser.checkParser(input,expect,256))

    def test_57(self):
        input = """
                Function real_madrid_cf (ronaldo, sergio_ramos)
                {
                    Let luka_modric, toni_kroos;
                    Call(print,["toni_kroos,chuyen luka_modric tat bong sergio_ramos danh dau goalllllll"]);
                    ronaldo = arr[4555];
                }
            
                """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,257))

    def test_58(self):
        input = """
                Function real_madrid_cf (ronaldo, sergio_ramos)
                {
                    Let luka_modric, toni_kroos;
                    Call(print,["toni_kroos,chuyen luka_modric tat bong sergio_ramos danh dau goalllllll"]);
                    ronaldo = arr[4555] + "He is good at heading goalllll";
                }
            
                """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,258))

    
    def test_59(self):
        input = """
            Let i=1;
            Function foo (i) 
                {
                While ((x == 1.08765 * 2.098)) {
                    x = x + 1;
                    y = [1,2,3] * 985475;
                    z = "This is a string" - "abcdxzy";
                }
                }
            """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input, expect, 259))

    def test_60(self):
        input=""" Let a, b, c[5] = 5, 6, 7; """;
        expect="Error on line 1 col 21: 6"
        self.assertTrue(TestParser.checkParser(input,expect,260))

    def test_61(self):
        input = """
             Var a, b, c[5] = 5;
            """
        expect = "V"
        self.assertTrue(TestParser.checkParser(input,expect,261))

    def test_62(self):
        input = """
             Let a, b, c[5] = 5,;
            """
        expect = "Error on line 2 col 32: ;"
        self.assertTrue(TestParser.checkParser(input,expect,262))

    def test_63(self):
        
        input = """
        Let a = {
        name: "Yanxi Place",
        address: "Chinese Forbidden City",
        surface: 10.2,
        people: ["Empress Xiaoxianchun", "Yongzheng Emperor"]
        };
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,263))

    def test_64(self):
        input = """
                Let a = {
              name: "Yanxi Place"
              address: "Chinese Forbidden City"
              surface: 10.2
              people: ["Empress Xiaoxianchun", "Yongzheng Emperor"]
              };
        """
        expect = "Error on line 4 col 14: address"
        self.assertTrue(TestParser.checkParser(input,expect,264))

    def test_65(self):
        input = """
               Let a = {
                name "Yanxi Place",
                address "Chinese Forbidden City",
                surface: 10.2,
                people: ["Empress Xiaoxianchun", "Yongzheng Emperor"]
                };
        """
        expect = "Error on line 3 col 21: Yanxi Place"
        self.assertTrue(TestParser.checkParser(input,expect,265))

    def test_66(self):
        input = """
               Let a = (
                name: "Yanxi Place",
                address: "Chinese Forbidden City",
                surface: 10.2,
                people: ["Empress Xiaoxianchun", "Yongzheng Emperor"]
                );
        """
        expect = "Error on line 3 col 20: :"
        self.assertTrue(TestParser.checkParser(input,expect,266))

    def test_67(self):
        input = """
                    Let a = {
                    name= "Yanxi Place",
                    address= "Chinese Forbidden City",
                    surface= 10.2,
                    people= ["Empress Xiaoxianchun", "Yongzheng Emperor"]
                    };
                """
        expect = """Error on line 3 col 24: ="""
        self.assertTrue(TestParser.checkParser(input, expect, 267))

    def test_68(self):
        input = """
                Let b[2, 3] = [[1, 2, 3], [4, 5, 6]];
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,268))


    def test_69(self):
        input = """
                Let a[5]: Number = [1, 2, 3, 4, 5];
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,269))

    def test_70(self):
        input = """
               
                let b[2][3] = [[1, 2, 3], [4, 5, 6]];
        """
        expect = "Error on line 3 col 16: let"
        self.assertTrue(TestParser.checkParser(input,expect,270))

    def test_71(self):
        input = """
               Let b[2, 3] = [[1, 2, 3], [4, 5, 6]]
        """
        expect = "Error on line 3 col 8: <EOF>"
        self.assertTrue(TestParser.checkParser(input,expect,271))

    def test_72(self):
        
        input = """
                Function: main
                Body:
                    print(print(sum_factorial(20)) + a[25] + foo()[36]); 
                    Return 0;
                EndBody.
        """
        expect = "Error on line 2 col 24: :"
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
        expect = "V"
        self.assertTrue(TestParser.checkParser(input,expect,273))

    def test_74(self):
        input = """
       Let a = {
        name: "Yanxi Place",
        address: "Chinese Forbidden City",
        };
        """
        expect = "Error on line 5 col 8: }"
        self.assertTrue(TestParser.checkParser(input, expect,274))

    def test_75(self):
        input = """
            Let c[5][69];    
            """
        expect = "Error on line 2 col 20: ["
        self.assertTrue(TestParser.checkParser(input,expect,275))

    def test_76(self):
        input = """
                Function foo()
                {
                    a = (25+9)[5];
                }
            """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,276))

    def test_77(self):
        input = """Let b: String = a["name"] + a["address"];"""
        expect = """successful"""
        self.assertTrue(TestParser.checkParser(input, expect, 277))

    def test_78(self):
        input = """
                Let b: string = a["name"] + a["address"];
            """
        expect = "Error on line 2 col 23: string"
        self.assertTrue(TestParser.checkParser(input,expect,278))

    def test_79(self):
        input = """
                Let b: String = a[name] + a[address];
            """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,279))

    def test_80(self):
        input = """
                Function foo()
                {
                    If (True) {
                        If (True) {
                            If (True) {
                            }
                        }
                    }
                }
            """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,280))

    def test_81(self):
        input = """
                Function foo()
                {
                    While (True) {
                        While (True) {
                            While (True) {
                            }
                        }
                    }
                }
            """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,281))

    def test_82(self):
        input = """
                Function foo()
                {
                    Return Call(foo, [25]);
                }
            """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,282))

    def test_83(self):
        input = """
                Function foo()
                {
                    Call(foo, [Call(bar, [2, 3])]);
                }
            """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,283))

    def test_84(self):
        input = """  Function foo()
                {
                    Call(foo, (Call(bar, [2, 3])));
                }"""
        expect = "Error on line 3 col 30: ("
        self.assertTrue(TestParser.checkParser(input,expect,284))

    def test_85(self):
        input = """ Let a = 2; 
            foo(25);
        """
        expect = "Error on line 2 col 12: foo"
        self.assertTrue(TestParser.checkParser(input,expect,285))

    def test_86(self):
        input = """  Function foo()
                {
                    call(foo, [Call(bar, [2, 3])];
                }
        """
        expect = "Error on line 3 col 24: ("
        self.assertTrue(TestParser.checkParser(input,expect,286))

    def test_87(self):
        input = """  Function foo()
                {
                    Call(, [Call(bar, [2, 3])];
                }
        """
        expect = "Error on line 3 col 25: ,"
        self.assertTrue(TestParser.checkParser(input,expect,287))

    def test_88(self):
        input = """  Function foo()
                {
                    Call(foo, []);
                }
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,288))

    def test_89(self):
        input = """  Function foo()
                {
                    Call(foo [Call(bar, [2, 3])];
                }
        """
        expect = "Error on line 3 col 29: ["
        self.assertTrue(TestParser.checkParser(input,expect,289))

    def test_90(self):
        input = """Function foo()
                {
                    For key Of a {
                    Call(printLnvvc, ["Value of " + key + ": " + a[key]]);
                    }
                }
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,290))

    def test_91(self):
        input = """ Function foo()
                {
                    For key Of a {
                    Call(printLncv, ["Value of " + key + ": " + a[key]])
                    }
                }
        """
        expect = "Error on line 5 col 20: }"
        self.assertTrue(TestParser.checkParser(input,expect,291))

    def test_92(self):
        input = """ Function main()
            {
            blu = 123 * 23 - 123 - -.--.- "dasd" +++++++++++ ------------------ 25;
            }
        """
        expect = "Error on line 3 col 36: ."
        self.assertTrue(TestParser.checkParser(input,expect,292))

    def test_93(self):
        input = """
       Function foo()
                {
                Let a = {
                name: "Yanxi Place",
                address: "Chinese Forbidden City",
                };
                 For key In a {
                    Call(printLn, ["Value of " + key + ": " + a[key]]);
                    }
                }
        """
        expect = "Error on line 7 col 16: }"
        self.assertTrue(TestParser.checkParser(input,expect,293))

    def test_94(self):
        input = """
          Function foo()
                {
                Let a = {
                name: "Yanxi Place",
                address: "Chinese Forbidden City",
                };
                 For  In a {
                    Call(printLn, ["Value of " + key + ": " + a[key]]);
                    }
                }
        """
        expect = "Error on line 7 col 16: }"
        self.assertTrue(TestParser.checkParser(input,expect,294))

    def test_95(self):
        input = """
        a[2] = Call(foo, [2]) + Call(foo, [Call(bar, [2, 3])];
        """
        expect = "Error on line 2 col 8: a"
        self.assertTrue(TestParser.checkParser(input,expect,295))

    def test_96(self):
        input = """
        Let u: Number = i + 1;
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,296))

    def test_97(self):
        input = """
         Let u: Integer = i + 1;
        """
        expect = "Error on line 2 col 16: In"
        self.assertTrue(TestParser.checkParser(input,expect,297))

    def test_98(self):
        input = """
          Function foo(a[5], b) {
          Let i = 0;
          While (i < 5) {
          a[i] = b + 1;
          Let u: Integer = i + 1;
          If (a[u] == 10) {
          Return a[i];
          }
          }
          Return -1;
          }
        """
        expect = "Error on line 6 col 17: In"
        self.assertTrue(TestParser.checkParser(input,expect,298))

    def test_99(self):
        input = """
          Function foo(a[5], b) {
          Let i = 0;
          While (i < 5) {
          a[i] = b + 1;
          let u: Number = i + 1;
          If (a[u] == 10) {
          Return a[i];
          }
          }
          Return -1;
          Return 0;
          }
        """
        expect = "Error on line 6 col 14: u"
        self.assertTrue(TestParser.checkParser(input,expect,299))

    def test_100(self):
        input = """
        Function foo() {
          Let i = 0;
          While (i < 5) {
          a[i] = b + 1;
          If (a[u] == 10) {
          Return a[i];
          }
          }
          Return -1;
          }
        """
        expect = "successful"
        self.assertTrue(TestParser.checkParser(input,expect,300))



