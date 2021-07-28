import unittest
from TestUtils import TestLexer

class LexerSuite(unittest.TestCase):

    def test_lower_identifier(self):
        """test identifiers"""
        self.assertTrue(TestLexer.checkLexeme("abc","abc,<EOF>",10))
      
    def test_identifier(self):
        """test identifiers"""
        self.assertTrue(TestLexer.checkLexeme("ppl201","ppl201,<EOF>",101))
        self.assertTrue(TestLexer.checkLexeme("a_a_A_b_e_5_201","a_a_A_b_e_5_201,<EOF>",102))
        self.assertTrue(TestLexer.checkLexeme("A","Error Token A",103))
        self.assertTrue(TestLexer.checkLexeme("ppl201 ppL201 pPl201 pPL201 Ppl201", "ppl201,ppL201,pPl201,pPL201,Error Token P",104))
        self.assertTrue(TestLexer.checkLexeme("_identifier","Error Token _",105))
        self.assertTrue(TestLexer.checkLexeme("a__a a8_A","a__a,a8_A,<EOF>",106))
        self.assertTrue(TestLexer.checkLexeme("hcmut hCMUT HCMUT","hcmut,hCMUT,Error Token H",107))
        self.assertTrue(TestLexer.checkLexeme("a____________________________________________5","a____________________________________________5,<EOF>",108))

    def test_integer_number(self):
        """test integer number"""
        self.assertTrue(TestLexer.checkLexeme("0 199 0xFF 0XABC 0o567 0O77","0,199,0xFF,0XABC,0o567,0O77,<EOF>",109))
        self.assertTrue(TestLexer.checkLexeme("0123","0,123,<EOF>",110))
        self.assertTrue(TestLexer.checkLexeme("123a123","123,a123,<EOF>",111))
        self.assertTrue(TestLexer.checkLexeme("0xFFF 0XABCDF 0x0", "0xFFF,0XABCDF,0,x0,<EOF>",112))
        self.assertTrue(TestLexer.checkLexeme("0xfff","0,xfff,<EOF>",113))
        self.assertTrue(TestLexer.checkLexeme("0x1023456789ABCDEF 0X1023456789ABCDEF","0x1023456789ABCDEF,0X1023456789ABCDEF,<EOF>",114))
        self.assertTrue(TestLexer.checkLexeme("0x1023456789ABCDEF0X1023456789ABCDEF","0x1023456789ABCDEF0,Error Token X",115))
        self.assertTrue(TestLexer.checkLexeme("0O70o7","0O70,o7,<EOF>",116))
        self.assertTrue(TestLexer.checkLexeme("0o80o7","0,o80o7,<EOF>",117))
    
    def test_floating_point_number(self):
        """test floating point number"""
        self.assertTrue(TestLexer.checkLexeme("12.0e3","12.0e3,<EOF>",118))
        self.assertTrue(TestLexer.checkLexeme("0e5","0e5,<EOF>",119))
        self.assertTrue(TestLexer.checkLexeme("0000.e5","0000.e5,<EOF>",120))
        self.assertTrue(TestLexer.checkLexeme("12.0e3 12e3 12.e5 12.0e3 12000. 120000e-1","12.0e3,12e3,12.e5,12.0e3,12000.,120000e-1,<EOF>",121))
        self.assertTrue(TestLexer.checkLexeme("5 123 0x123 0XF0 0xfF 0o7 0o8","5,123,0x123,0XF0,0,xfF,0o7,0,o8,<EOF>",122))

    def test_string(self):
        """test string"""
        self.assertTrue(TestLexer.checkLexeme(""" "This is a string" ""","""This is a string,<EOF>""",123))
        self.assertTrue(TestLexer.checkLexeme(""" "IDENTIFIER" ""","""IDENTIFIER,<EOF>""",124))
        self.assertTrue(TestLexer.checkLexeme(""" "Cristiano Ronaldo is the best football player in the world" ""","""Cristiano Ronaldo is the best football player in the world,<EOF>""",125))
        self.assertTrue(TestLexer.checkLexeme(""" "!@#$%^&*()" ""","""!@#$%^&*(),<EOF>""",126))
        self.assertTrue(TestLexer.checkLexeme(""" "ab!3sa/89-66+48()...." ""","""ab!3sa/89-66+48()....,<EOF>""",127))
        self.assertTrue(TestLexer.checkLexeme(""" "0Xx89o75" ""","""0Xx89o75,<EOF>""",128))
        self.assertTrue(TestLexer.checkLexeme(""" "123 456 789 abc def" ""","""123 456 789 abc def,<EOF>""",129))
        self.assertTrue(TestLexer.checkLexeme(""" "string 1" "string 2" ""","""string 1,string 2,<EOF>""",130))
        self.assertTrue(TestLexer.checkLexeme(""" "+-*/" 0x123 ""","""+-*/,0x123,<EOF>""",131))
        self.assertTrue(TestLexer.checkLexeme(""" 0XF8f8"STRING" ""","""0XF8,f8,STRING,<EOF>""",132))
        self.assertTrue(TestLexer.checkLexeme(""" "" """,""",<EOF>""",133))

    def test_escape_sequence(self):
        """test escape sequence"""
        self.assertTrue(TestLexer.checkLexeme(""" "This is a string containing tab \\t" ""","This is a string containing tab \\t,<EOF>",134))
        self.assertTrue(TestLexer.checkLexeme(""" "a new line \\n" ""","a new line \\n,<EOF>",135))
        self.assertTrue(TestLexer.checkLexeme(""" "a form feed \\f" """, """a form feed \\f,<EOF>""",136))
        self.assertTrue(TestLexer.checkLexeme(""" "multi escape sequence: \\n\\r\\t\\b\\'\\\ " ""","""multi escape sequence: \\n\\r\\t\\b\\'\\\ ,<EOF>""",137))
        self.assertTrue(TestLexer.checkLexeme(""" "a \\n b \\t c \\' d \\r e \\f f" ""","""a \\n b \\t c \\' d \\r e \\f f,<EOF>""",138))
    
    def test_boolean_literal(self):
        """test boolean literal"""
        self.assertTrue(TestLexer.checkLexeme(""" True False truE TruE ""","True,False,truE,Error Token T",139))
        self.assertTrue(TestLexer.checkLexeme(""" TrueFalse TruefAlse ""","True,False,True,fAlse,<EOF>",140))

    def test_keyword(self):
        self.assertTrue(TestLexer.checkLexeme("If EndIf For EndFor Do","If,EndIf,For,EndFor,Do,<EOF>",141))
        self.assertTrue(TestLexer.checkLexeme("If Endif For EndFor Do","If,Error Token E",142))
        self.assertTrue(TestLexer.checkLexeme("iF If IF","iF,If,Error Token I",143))

    def test_unclose_string(self):
        self.assertTrue(TestLexer.checkLexeme(""" "'" ""","""Unclosed String: \'" """,144))
        self.assertTrue(TestLexer.checkLexeme(""" "HCMUT ""","""Unclosed String: HCMUT """,145))
        self.assertTrue(TestLexer.checkLexeme(""" "** ""","""Unclosed String: ** """,146))
        self.assertTrue(TestLexer.checkLexeme(""" "hello lexer ""","""Unclosed String: hello lexer """,147))
        self.assertTrue(TestLexer.checkLexeme(""" 14.e5 "14.e5 ""","""14.e5,Unclosed String: 14.e5 """,148))
        self.assertTrue(TestLexer.checkLexeme(""" "This is an unclose string ""","""Unclosed String: This is an unclose string """,149))
        self.assertTrue(TestLexer.checkLexeme(""" "lam hoai khong xong =(((((( ""","""Unclosed String: lam hoai khong xong =(((((( """,150))

    def test_illegal_escape_sequence(self):
        self.assertTrue(TestLexer.checkLexeme(""" "\\y" ""","""Illegal Escape In String: \\y""",151))
        self.assertTrue(TestLexer.checkLexeme(""" "This string has an illegal escape sequence \\a" ""","""Illegal Escape In String: This string has an illegal escape sequence \\a""",152))
        self.assertTrue(TestLexer.checkLexeme(""" "\\b\\n\\t\\w" ""","""Illegal Escape In String: \\b\\n\\t\\w""",153))
        self.assertTrue(TestLexer.checkLexeme(""" " Hi Hi \\c \\d " ""","Illegal Escape In String:  Hi Hi \c",154))
        self.assertTrue(TestLexer.checkLexeme(""" " Hi Hi \\c\\d\\t\\r\\n " ""","Illegal Escape In String:  Hi Hi \c",155))

    def test_array_literal(self):
        """a dimension array """
        self.assertTrue(TestLexer.checkLexeme("""array = {100,200, 300, 500e-10, 12.}""","array,=,{,100,,,200,,,300,,,500e-10,,,12.,},<EOF>",156))
        self.assertTrue(TestLexer.checkLexeme(""" {123,True,             9797, 4545   ,    FALSE} ""","{,123,,,True,,,9797,,,4545,,,Error Token F",157))
        self.assertTrue(TestLexer.checkLexeme(""" {123,True,             "HCMUT", 4545   ,    18e4} ""","""{,123,,,True,,,HCMUT,,,4545,,,18e4,},<EOF>""",158))
        self.assertTrue(TestLexer.checkLexeme(""" 123,456,             9797, 4545   ,    4554} ""","123,,,456,,,9797,,,4545,,,4554,},<EOF>",159))
        self.assertTrue(TestLexer.checkLexeme(""" {} ""","{,},<EOF>",160))

        """a multidimension array"""
        self.assertTrue(TestLexer.checkLexeme("""{{1,    2},    {8}}""","{,{,1,,,2,},,,{,8,},},<EOF>",161))
        self.assertTrue(TestLexer.checkLexeme("""{{1,2},  {"string", "string1"}, {True, True, False, {45}}}""","""{,{,1,,,2,},,,{,string,,,string1,},,,{,True,,,True,,,False,,,{,45,},},},<EOF>""",162))
        self.assertTrue(TestLexer.checkLexeme(""" {{{{}}}} ""","{,{,{,{,},},},},<EOF>",163))
        self.assertTrue(TestLexer.checkLexeme(""" {{{{{"HCMUT"}, {1,2}}}}} ""","""{,{,{,{,{,HCMUT,},,,{,1,,,2,},},},},},<EOF>""",164))
        self.assertTrue(TestLexer.checkLexeme(""" {{},{{      }},{{{{},        {}}}}} ""","""{,{,},,,{,{,},},,,{,{,{,{,},,,{,},},},},},<EOF>""",165))
        self.assertTrue(TestLexer.checkLexeme(""" {{},{"PPL", {  1   , 8,    6}}} ""","""{,{,},,,{,PPL,,,{,1,,,8,,,6,},},},<EOF>""",166))
        self.assertTrue(TestLexer.checkLexeme(""" {{{{"300"}}}} ""","""{,{,{,{,300,},},},},<EOF>""",167))
        self.assertTrue(TestLexer.checkLexeme(""" {{}      ,     {12e5},    {}, {{True, 857, 697, "string"}}} ""","""{,{,},,,{,12e5,},,,{,},,,{,{,True,,,857,,,697,,,string,},},},<EOF>""",168))
        self.assertTrue(TestLexer.checkLexeme(""" {False, True, {78}} ""","""{,False,,,True,,,{,78,},},<EOF>""",169))
        self.assertTrue(TestLexer.checkLexeme(""" {{}{}} ""","""{,{,},{,},},<EOF>""",170))

    def test_multi(self):
        """test comment"""
        self.assertTrue(TestLexer.checkLexeme("""**This is a single comment**""","<EOF>",171))
        self.assertTrue(TestLexer.checkLexeme("""**This is a multi-comment ** Something ** ** ""","Error Token S",172))
        self.assertTrue(TestLexer.checkLexeme("""12e5 15e8 49 88 .e0 00000E5 "string" "string1" ""","""12e5,15e8,49,88,.,e0,00000E5,string,string1,<EOF>""",173))
        self.assertTrue(TestLexer.checkLexeme("""printLn()""","printLn,(,),<EOF>",174))
        self.assertTrue(TestLexer.checkLexeme("""Function: fact Parameter: n Body: EndBody""","Function,:,fact,Parameter,:,n,Body,:,EndBody,<EOF>",175))
        self.assertTrue(TestLexer.checkLexeme("""""","<EOF>",176))
        self.assertTrue(TestLexer.checkLexeme("""**Unterminated""","Unterminated Comment",177))
        self.assertTrue(TestLexer.checkLexeme("""**This** **is**a**single**** **comment""","a,comment,<EOF>",178))
        self.assertTrue(TestLexer.checkLexeme("""{5,{7  , 25}}""","{,5,,,{,7,,,25,},},<EOF>",179))
        input = """Function: fact
                    Parameter: n
                    Body:
                        If n == 0 Then
                            Return 1;
                        Else
                            Return n * fact (n - 1);
                        EndIf.
                    EndBody."""
        expect = "Function,:,fact,Parameter,:,n,Body,:,If,n,==,0,Then,Return,1,;,Else,Return,n,*,fact,(,n,-,1,),;,EndIf,.,EndBody,.,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input,expect,180))
        input = """Function: Fact
                    Parameter: n
                    Body:
                        If n == 0 Then
                            Return 1;
                        Else
                            Return n * fact (n - 1);
                        EndIf.
                    EndBody."""
        expect = "Function,:,Error Token F"
        self.assertTrue(TestLexer.checkLexeme(input,expect,181))
        input = """Function: fact
                    Parameter: n
                    Body:
                        If n == 0 Then
                            Return 1 + 25 + 27;
                        Else
                            Return n * fact (n - 1) + {25,5,{    98}};
                        EndIf.
                    EndBody."""
        expect = "Function,:,fact,Parameter,:,n,Body,:,If,n,==,0,Then,Return,1,+,25,+,27,;,Else,Return,n,*,fact,(,n,-,1,),+,{,25,,,5,,,{,98,},},;,EndIf,.,EndBody,.,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input,expect,182))
        input = """Function: fact
                    Parameter: n
                    Body:
                        If n * "HCMUT" Then
                            Return 1 + "HCMUT\\h" ;
                        Else
                            Return n * fact (n - 1) + {25,5,{    98}};
                        EndIf.
                    EndBody."""
        expect = "Function,:,fact,Parameter,:,n,Body,:,If,n,*,HCMUT,Then,Return,1,+,Illegal Escape In String: HCMUT\h"
        self.assertTrue(TestLexer.checkLexeme(input,expect,183))
        input = """Function: fact
                    Parameter: n
                    Body:
                        If n * "HCMUT" Then
                            Return 1 + "HCMUT\\t" + "PPL;
                        Else
                            Return n * fact (n - 1) + {25,5,{    98}};
                        EndIf.
                    EndBody."""
        expect = "Function,:,fact,Parameter,:,n,Body,:,If,n,*,HCMUT,Then,Return,1,+,HCMUT\\t,+,Unclosed String: PPL;"
        self.assertTrue(TestLexer.checkLexeme(input,expect,184))
        input = """Function: fact
                    Parameter: n
                    Body:
                        If n * "HCMUT" Then
                            Return 1 + "HCMUT\\t" + "PPL";
                        Else
                            Return n * fact (n - 1) + {25,5,{    98}};
                        EndIf.
                    EndBody."""
        expect = "Function,:,fact,Parameter,:,n,Body,:,If,n,*,HCMUT,Then,Return,1,+,HCMUT\\t,+,PPL,;,Else,Return,n,*,fact,(,n,-,1,),+,{,25,,,5,,,{,98,},},;,EndIf,.,EndBody,.,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input,expect,185))
        input = """Function: fact
                    Parameter: n
                    Body:
                        If n * "HCMUT" Then
                            Return 1 + "HCMUT\\t" + "PPL";
                        Else
                            Return n * fact (n - 1) + {25,5,{    98}};
                        EndIf.
                    EndBody."""
        expect = "Function,:,fact,Parameter,:,n,Body,:,If,n,*,HCMUT,Then,Return,1,+,HCMUT\\t,+,PPL,;,Else,Return,n,*,fact,(,n,-,1,),+,{,25,,,5,,,{,98,},},;,EndIf,.,EndBody,.,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input,expect,186))
        input = """Function: fact
                    Parameter: n
                    Body:
                        If n * "HCMUT" Then
                            Return 1 + "HCMUT\\t" + "PPL" + 12E5 + 12.e5;
                        ElseIf {{{{{}}}}} {{}}
                            Return n * fact (n - 1) + {25,5,{    98}};
                        EndIf.
                    EndBody."""
        expect = "Function,:,fact,Parameter,:,n,Body,:,If,n,*,HCMUT,Then,Return,1,+,HCMUT\\t,+,PPL,+,12E5,+,12.e5,;,ElseIf,{,{,{,{,{,},},},},},{,{,},},Return,n,*,fact,(,n,-,1,),+,{,25,,,5,,,{,98,},},;,EndIf,.,EndBody,.,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input,expect,187))
        self.assertTrue(TestLexer.checkLexeme(""" "abc \\n \\\\a" ""","""abc \\n \\\\a,<EOF>""",188))
        self.assertTrue(TestLexer.checkLexeme(""" +-8e4--25 ""","+,-,8e4,-,-,25,<EOF>",189))
        self.assertTrue(TestLexer.checkLexeme(""" "{1, 2,     5,{}{}       8,7}" ""","{1, 2,     5,{}{}       8,7},<EOF>",190))
        self.assertTrue(TestLexer.checkLexeme(""" "abcdef'" ""","""Unclosed String: abcdef\'" """,191))
        self.assertTrue(TestLexer.checkLexeme("""+-*\\||\\.+.&&>=.""","+,-,*,\,||,\.,+.,&&,>=.,<EOF>",192))
        self.assertTrue(TestLexer.checkLexeme("""+.>=<==-.!%""","+.,>=,<=,=,-.,!,%,<EOF>",193))
        self.assertTrue(TestLexer.checkLexeme("""++0x85-abcd*-""","+,+,0x85,-,abcd,*,-,<EOF>",194))
        self.assertTrue(TestLexer.checkLexeme(""" "Sai gon dep lam Sai gon oi Sai gon oi" ""","Sai gon dep lam Sai gon oi Sai gon oi,<EOF>",195))
        self.assertTrue(TestLexer.checkLexeme("""{25,{**this is a comment** 78, 39}}""","{,25,,,{,78,,,39,},},<EOF>",196))
        self.assertTrue(TestLexer.checkLexeme("""Var: x[5 **comment**] = {**comment**}""","Var,:,x,[,5,],=,{,},<EOF>",197))
        self.assertTrue(TestLexer.checkLexeme("""HCMUT""","Error Token H",198))
        self.assertTrue(TestLexer.checkLexeme("""Var: x[5 **comment** 25] = {**comment** "This is a string", {{{}}}}""","Var,:,x,[,5,25,],=,{,This is a string,,,{,{,{,},},},},<EOF>",199))
        self.assertTrue(TestLexer.checkLexeme("""x[25**This is a comment]""","x,[,25,Unterminated Comment",200))