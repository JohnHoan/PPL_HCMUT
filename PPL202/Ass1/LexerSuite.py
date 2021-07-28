import unittest
from TestUtils import TestLexer

class LexerSuite(unittest.TestCase):

    def test_0(self):
        """test identifiers"""
        self.assertTrue(TestLexer.checkLexeme("abc","abc,<EOF>",100))

    def test_1(self):
        """test identifiers"""
        self.assertTrue(TestLexer.checkLexeme("$ppl202","$ppl202,<EOF>",101))
    def test_2(self):
        self.assertTrue(TestLexer.checkLexeme("a_a_A_b_e_5_202","a_a_A_b_e_5_202,<EOF>",102))
    def test_3(self):
        self.assertTrue(TestLexer.checkLexeme("A","Error Token A",103))
    def test_4(self):
        self.assertTrue(TestLexer.checkLexeme("ppl202 ppL202 pPl202 pPL202 Ppl202", "ppl202,ppL202,pPl202,pPL202,Error Token P",104))
    def test_5(self):
        self.assertTrue(TestLexer.checkLexeme("_identifier","Error Token _",105))
    def test_6(self):
        self.assertTrue(TestLexer.checkLexeme("a__a a8_A","a__a,a8_A,<EOF>",106))
    def test_7(self):
        self.assertTrue(TestLexer.checkLexeme("hcmut hCMUT HCMUT","hcmut,hCMUT,Error Token H",107))
    def test_8(self):
        self.assertTrue(TestLexer.checkLexeme("a____________________________________________5","a____________________________________________5,<EOF>",108))
    def test_9(self):
        self.assertTrue(TestLexer.checkLexeme("0 199 12. 12.3 12.3e3 12.3e-30 ","0,199,12.,12.3,12.3e3,12.3e-30,<EOF>",109))
    def test_10(self):
        self.assertTrue(TestLexer.checkLexeme("0123","0123,<EOF>",110))
    def test_11(self):
        self.assertTrue(TestLexer.checkLexeme("123a123","123,a123,<EOF>",111))
    def test_12(self):
        self.assertTrue(TestLexer.checkLexeme("0xFFF", "0,xFFF,<EOF>",112))
    def test_13(self):
        self.assertTrue(TestLexer.checkLexeme("e123","e123,<EOF>",113))
    def test_14(self):
        self.assertTrue(TestLexer.checkLexeme("12e122","12e122,<EOF>",114))
    def test_15(self):
        self.assertTrue(TestLexer.checkLexeme(".e3213",".,e3213,<EOF>",115))
    def test_16(self):
        self.assertTrue(TestLexer.checkLexeme("32e.1233","32,e,.,1233,<EOF>",116))
    def test_17(self):
        self.assertTrue(TestLexer.checkLexeme("0o80o7","0,o80o7,<EOF>",117))
    def test_18(self):
        self.assertTrue(TestLexer.checkLexeme("12.0e+3","12.0e+3,<EOF>",118))
    def test_19(self):
        self.assertTrue(TestLexer.checkLexeme("0.e-5","0.e-5,<EOF>",119))
    def test_20(self):
        self.assertTrue(TestLexer.checkLexeme("0000.e5","0000.e5,<EOF>",120))
    def test_21(self):
        self.assertTrue(TestLexer.checkLexeme("12.0e3 12e3 12.e5 12.0e3 12000. 120000e-1","12.0e3,12e3,12.e5,12.0e3,12000.,120000e-1,<EOF>",121))
    def test_22(self):
        self.assertTrue(TestLexer.checkLexeme("5 123 0x123 0XF0 0xfF 0o7 0o8","5,123,0,x123,0,Error Token X",122))

    def test_23(self):
        """test string"""
        self.assertTrue(TestLexer.checkLexeme(""" "This is a string" ""","""This is a string,<EOF>""",123))
    def test_24(self):
        self.assertTrue(TestLexer.checkLexeme(""" "IDENTIFIER" ""","""IDENTIFIER,<EOF>""",124))
    def test_25(self):
        self.assertTrue(TestLexer.checkLexeme(""" "Cristiano Ronaldo is the best football player in the world" ""","""Cristiano Ronaldo is the best football player in the world,<EOF>""",125))
    def test_26(self):
        self.assertTrue(TestLexer.checkLexeme(""" "!@#$%^&*()" ""","""!@#$%^&*(),<EOF>""",126))
    def test_27(self):
        self.assertTrue(TestLexer.checkLexeme(""" "ab!3sa/89-66+48()...." ""","""ab!3sa/89-66+48()....,<EOF>""",127))
    def test_28(self):
        self.assertTrue(TestLexer.checkLexeme(""" "0Xx89o75" ""","""0Xx89o75,<EOF>""",128))
    def test_29(self):
        self.assertTrue(TestLexer.checkLexeme(""" "123 456 789 abc def" ""","""123 456 789 abc def,<EOF>""",129))
    def test_30(self):
        self.assertTrue(TestLexer.checkLexeme(""" "string 1" "string 2" ""","""string 1,string 2,<EOF>""",130))
    def test_31(self):
        self.assertTrue(TestLexer.checkLexeme(""" "+-*/" 0x123 ""","""+-*/,0,x123,<EOF>""",131))
    def test_32(self):
        self.assertTrue(TestLexer.checkLexeme(""" 0XF8f8"STRING" ""","""0,Error Token X""",132))
    def test_33(self):
        self.assertTrue(TestLexer.checkLexeme(""" "" """,""",<EOF>""",133))

    def test_34(self):
        """test escape sequence"""
        self.assertTrue(TestLexer.checkLexeme(""" "This is a string containing tab \\t" ""","This is a string containing tab \\t,<EOF>",134))
    def test_35(self):
        self.assertTrue(TestLexer.checkLexeme(""" "a new line \\n" ""","a new line \\n,<EOF>",135))
    def test_36(self):
        self.assertTrue(TestLexer.checkLexeme(""" "a form feed \\f" """, """a form feed \\f,<EOF>""",136))
    def test_37(self):
        self.assertTrue(TestLexer.checkLexeme(""" "multi escape sequence: \\n\\r\\t\\b\\'\\\ " ""","""multi escape sequence: \\n\\r\\t\\b\\'\\\ ,<EOF>""",137))
    def test_38(self):
        self.assertTrue(TestLexer.checkLexeme(""" "a \\n b \\t c \\' d \\r e \\f f" ""","""a \\n b \\t c \\' d \\r e \\f f,<EOF>""",138))

    def test_39(self):
        """test boolean literal"""
        self.assertTrue(TestLexer.checkLexeme(""" True False truE TruE ""","True,False,truE,Error Token T",139))
    def test_40(self):
        self.assertTrue(TestLexer.checkLexeme(""" TrueFalse TruefAlse ""","True,False,True,fAlse,<EOF>",140))

    def test_41(self):
        self.assertTrue(TestLexer.checkLexeme("If For While Let Constant","If,For,While,Let,Constant,<EOF>",141))
    def test_42(self):
        self.assertTrue(TestLexer.checkLexeme("Elseif","Else,if,<EOF>",142))
    def test_43(self):
        self.assertTrue(TestLexer.checkLexeme("iF If IF","iF,If,Error Token I",143))

    def test_44(self):
        self.assertTrue(TestLexer.checkLexeme(""" "'" ""","""Unclosed String: \'" """,144))
    def test_45(self):
        self.assertTrue(TestLexer.checkLexeme(""" "HCMUT ""","""Unclosed String: HCMUT """,145))
    def test_46(self):
        self.assertTrue(TestLexer.checkLexeme(""" "** ""","""Unclosed String: ** """,146))
    def test_47(self):
        self.assertTrue(TestLexer.checkLexeme(""" "hello lexer ""","""Unclosed String: hello lexer """,147))
    def test_48(self):
        self.assertTrue(TestLexer.checkLexeme(""" 14.e5 "14.e5 ""","""14.e5,Unclosed String: 14.e5 """,148))
    def test_49(self):
        self.assertTrue(TestLexer.checkLexeme(""" "This is an unclose string ""","""Unclosed String: This is an unclose string """,149))
    def test_50(self):
        self.assertTrue(TestLexer.checkLexeme(""" "lam hoai khong xong =(((((( ""","""Unclosed String: lam hoai khong xong =(((((( """,150))

    def test_51(self):
        self.assertTrue(TestLexer.checkLexeme(""" "\\y" ""","""Illegal Escape In String: \\y""",151))
    def test_52(self):
        self.assertTrue(TestLexer.checkLexeme(""" "This string has an illegal escape sequence \\a" ""","""Illegal Escape In String: This string has an illegal escape sequence \\a""",152))
    def test_53(self):
        self.assertTrue(TestLexer.checkLexeme(""" "\\b\\n\\t\\w" ""","""Illegal Escape In String: \\b\\n\\t\\w""",153))
    def test_54(self):
        self.assertTrue(TestLexer.checkLexeme(""" " Hi Hi \\c \\d " ""","Illegal Escape In String:  Hi Hi \c",154))
    def test_55(self):
        self.assertTrue(TestLexer.checkLexeme(""" " Hi Hi \\c\\d\\t\\r\\n " ""","Illegal Escape In String:  Hi Hi \c",155))

    def test_56(self):
        """a dimension array """
        self.assertTrue(TestLexer.checkLexeme("""array = [100,200, 300, 500e-10, 12.]""","array,=,[,100,,,200,,,300,,,500e-10,,,12.,],<EOF>",156))
    def test_57(self):
        self.assertTrue(TestLexer.checkLexeme(""" [123,True,             9797, 4545   ,    FALSE] ""","[,123,,,True,,,9797,,,4545,,,Error Token F",157))
    def test_58(self):
        self.assertTrue(TestLexer.checkLexeme(""" [123,True,             "HCMUT", 4545   ,    18e4] ""","""[,123,,,True,,,HCMUT,,,4545,,,18e4,],<EOF>""",158))
    def test_59(self):
        self.assertTrue(TestLexer.checkLexeme(""" 123,456,             9797, 4545   ,    4554} ""","123,,,456,,,9797,,,4545,,,4554,},<EOF>",159))
    def test_60(self):
        self.assertTrue(TestLexer.checkLexeme(""" [] ""","[,],<EOF>",160))
    def test_61(self):

        """a multidimension array"""
        self.assertTrue(TestLexer.checkLexeme("""[[1,    2],    [8]]""","[,[,1,,,2,],,,[,8,],],<EOF>",161))
    def test_62(self):
        self.assertTrue(TestLexer.checkLexeme("""[[1,2],  ["string", "string1"], [True, True, False, [45]]]""","""[,[,1,,,2,],,,[,string,,,string1,],,,[,True,,,True,,,False,,,[,45,],],],<EOF>""",162))
    def test_63(self):
        self.assertTrue(TestLexer.checkLexeme(""" [[[[][]]]] ""","[,[,[,[,],[,],],],],<EOF>",163))
    def test_64(self):
        self.assertTrue(TestLexer.checkLexeme(""" [[[[["HCMUT"][-1234]]]] ""","""[,[,[,[,[,HCMUT,],[,-,1234,],],],],<EOF>""",164))
    def test_65(self):
        self.assertTrue(TestLexer.checkLexeme(""" [[[[     ][     ][     ]]]] ""","""[,[,[,[,],[,],[,],],],],<EOF>""",165))
    def test_66(self):
        self.assertTrue(TestLexer.checkLexeme(""" [["I will pass"]["Ppl202"]["Chaizo"]] ""","""[,[,I will pass,],[,Ppl202,],[,Chaizo,],],<EOF>""",166))
    def test_67(self):
        self.assertTrue(TestLexer.checkLexeme(""" [[[]""","""[,[,[,],<EOF>""",167))
    def test_68(self):
        self.assertTrue(TestLexer.checkLexeme(""" [[]      ,     [12e5],    [], [[True, 857, 697, "string"]]] ""","""[,[,],,,[,12e5,],,,[,],,,[,[,True,,,857,,,697,,,string,],],],<EOF>""",168))
    def test_69(self):
        self.assertTrue(TestLexer.checkLexeme(""" [False, True, 78] ""","""[,False,,,True,,,78,],<EOF>""",169))
    def test_70(self):
        self.assertTrue(TestLexer.checkLexeme(""" [[[]]] ""","""[,[,[,],],],<EOF>""",170))

    def test_71(self):
        self.assertTrue(TestLexer.checkLexeme("""Let a = {
            name: "Yanxi Place",
            address: "Chinese Forbidden City",
            surface: 10.2,
            people: ["Empress Xiaoxianchun", "Yongzheng Emperor"]
            };""","Let,a,=,{,name,:,Yanxi Place,,,address,:,Chinese Forbidden City,,,surface,:,10.2,,,people,:,[,Empress Xiaoxianchun,,,Yongzheng Emperor,],},;,<EOF>",171))
    def test_72(self):
        self.assertTrue(TestLexer.checkLexeme("""let b[2, 3] = [[1, 2, 3], [4, 5, 6]];""","let,b,[,2,,,3,],=,[,[,1,,,2,,,3,],,,[,4,,,5,,,6,],],;,<EOF>",172))
    def test_73(self):
        self.assertTrue(TestLexer.checkLexeme("""let b: String = a["name"] + a["address"];""","let,b,:,String,=,a,[,name,],+,a,[,address,],;,<EOF>",173))
    def test_74(self):
        self.assertTrue(TestLexer.checkLexeme("""a["name"] = "Qianqing Palace";""","a,[,name,],=,Qianqing Palace,;,<EOF>",174))
    def test_75(self):
        self.assertTrue(TestLexer.checkLexeme("""a[3 + Call(foo, [2])] = a[b[2, 3]] + 4;""","a,[,3,+,Call,(,foo,,,[,2,],),],=,a,[,b,[,2,,,3,],],+,4,;,<EOF>",175))
    def test_76(self):
        self.assertTrue(TestLexer.checkLexeme("""a[2] = Call(foo, [2]) + Call(foo, [Call(bar, [2, 3])];""","a,[,2,],=,Call,(,foo,,,[,2,],),+,Call,(,foo,,,[,Call,(,bar,,,[,2,,,3,],),],;,<EOF>",176))

    def test_77(self):
        """test comment"""
        self.assertTrue(TestLexer.checkLexeme("""##This is a single comment##""","<EOF>",177))
    def test_78(self):
        self.assertTrue(TestLexer.checkLexeme("""##This is a multi-comment ## Something ## ## ""","Error Token S",178))
    def test_79(self):
        self.assertTrue(TestLexer.checkLexeme("""""","<EOF>",179))
    def test_80(self):
        self.assertTrue(TestLexer.checkLexeme("""##Unterminated""","Unterminated Comment",180))
    def test_81(self):
        self.assertTrue(TestLexer.checkLexeme("""##This## ##is##a##single#### ##comment""","a,comment,<EOF>",181))

        
    def test_82(self):

        input = """Function foo(a[5], b) {
                    Let i = 0;
                    While (i < 5) {
                    a[i] = b + 1;
                    let u: Integer = i + 1;
                    If (a[u] == 10) {
                    Return a[i];
                    }
                    }
                    Return -1;
                    }"""
        expect = "Function,foo,(,a,[,5,],,,b,),{,Let,i,=,0,;,While,(,i,<,5,),{,a,[,i,],=,b,+,1,;,let,u,:,In,teger,=,i,+,1,;,If,(,a,[,u,],==,10,),{,Return,a,[,i,],;,},},Return,-,1,;,},<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input,expect,182))
    def test_83(self):
        input = """Constant $a = 10;
                    Function foo(a[5], b) {
                    Constant $b: String = "Story of Yanxi Place";
                    Let i = 0;
                    While (i < 5) {
                    a[i] = (b + 1) * $a;
                    let u: Integer = i + 1;
                    If (a[u] == 10) {
                    Return $b;
                    }
                    i = i + 1;
                    }
                    Return $b + ": Done";
                    }"""
        expect = "Constant,$a,=,10,;,Function,foo,(,a,[,5,],,,b,),{,Constant,$b,:,String,=,Story of Yanxi Place,;,Let,i,=,0,;,While,(,i,<,5,),{,a,[,i,],=,(,b,+,1,),*,$a,;,let,u,:,In,teger,=,i,+,1,;,If,(,a,[,u,],==,10,),{,Return,$b,;,},i,=,i,+,1,;,},Return,$b,+,: Done,;,},<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input,expect,183))
    def test_84(self):
        input = """For key In a {
                    Call(printLn, ["Value of " + key + ": " + a[key]])
                    }"""
        expect = "For,key,In,a,{,Call,(,printLn,,,[,Value of ,+,key,+,: ,+,a,[,key,],],),},<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input,expect,184))
    def test_85(self):
        input = """Function: fact { }"""
        expect = "Function,:,fact,{,},<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input,expect,185))
    def test_86(self):
        input = """Function fact("Name") {
        Call(printLn, ["name"]);
        }"""
        expect = "Function,fact,(,Name,),{,Call,(,printLn,,,[,name,],),;,},<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input,expect,186))
    def test_87(self):
        input = """Function foo{ 
        }"""
        expect = "Function,foo,{,},<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input,expect,187))
    def test_88(self):
        input = """Call(foo, [2 + x, 4 / y]);"""
        expect = "Call,(,foo,,,[,2,+,x,,,4,/,y,],),;,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input,expect,188))
    def test_89(self):
        input = """Call(goo, []);"""
        expect = "Call,(,goo,,,[,],),;,<EOF>"
        self.assertTrue(TestLexer.checkLexeme(input,expect,189))
    def test_90(self):
        self.assertTrue(TestLexer.checkLexeme(""" +-8e4--25 ""","+,-,8e4,-,-,25,<EOF>",190))
    def test_91(self):
        self.assertTrue(TestLexer.checkLexeme(""" "{1, 2,     5,{}{}       8,7}" ""","{1, 2,     5,{}{}       8,7},<EOF>",191))
    def test_92(self):
        self.assertTrue(TestLexer.checkLexeme(""" "abcdef'" ""","""Unclosed String: abcdef\'" """,192))
    def test_93(self):
        self.assertTrue(TestLexer.checkLexeme("""+.>=<==-.!%""","+.,>=,<=,=,-,.,!,%,<EOF>",193))
    def test_94(self):
        self.assertTrue(TestLexer.checkLexeme("""++0x85-abcd*-""","+,+,0,x85,-,abcd,*,-,<EOF>",194))
    def test_95(self):
        self.assertTrue(TestLexer.checkLexeme(""" "Sai gon dep lam Sai gon oi Sai gon oi" ""","Sai gon dep lam Sai gon oi Sai gon oi,<EOF>",195))
    def test_96(self):
        self.assertTrue(TestLexer.checkLexeme("""{25,{##this is a comment## 78, 39}}""","{,25,,,{,78,,,39,},},<EOF>",196))
    def test_97(self):
        self.assertTrue(TestLexer.checkLexeme("""Var: x[5 **comment**] = {**comment**}""","Error Token V",197))
    def test_98(self):
        self.assertTrue(TestLexer.checkLexeme("""HCMUT""","Error Token H",198))
    def test_99(self):
        self.assertTrue(TestLexer.checkLexeme("""var: x[5 ##comment## 25] = {##comment## "This is a string", {{{}}}}""","var,:,x,[,5,25,],=,{,This is a string,,,{,{,{,},},},},<EOF>",199))
    def test_100(self):
        self.assertTrue(TestLexer.checkLexeme("""x[25##This is a comment]""","x,[,25,Unterminated Comment",200))