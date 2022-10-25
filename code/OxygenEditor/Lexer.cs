using System.Windows;
using System.Windows.Documents;
using System.Collections.Generic;
using System;

namespace Editor
{

    

    class Lexer
    {
        public static string[] instuctions = { "ADD", "SUB", "MUL", "DIV", "UDIV", "FADD", "FSUB", "FMUL", "FDIV",
            "EXP", "SQRT", "LN",
            "AND", "OR", "NOT", "XOR", "SHIFT",
            "LD", "LDB", "LDBI", "ST", "STB", "STBI", "MOV",

            "INC","DEC","INV",
            "PUTI", "PUTUI", "PUTF", "PUTC", "GETC",

            "PUSH","POP",

            "HALT","RET","CLS",
            "BR", "BRE", "BRL", "BRG", "BRLE", "BRGE", "BRNE",

            "JSR",

            "CMP", "BCMP", "BINV"
        };


        public static string[] regs = { "R0", "R1", "R2", "R3", "R4", "BP", "SP", "BUFF", "PC", "COND", "RSUB" };
        public static string[] spc = { "VAR", "STRING", ".DATA", ".DEF", ".CODE" };
        public static string[] directives = { "LABEL", "INCLUDE", "DEFINE", "ENTRY", "MACRO", "ENDMACRO" };

        public static List<string> allWords { get; }

        static Lexer()
        {
            allWords = new List<string>();
            allWords.AddRange(instuctions);
            allWords.AddRange(regs);
            allWords.AddRange(spc);
            allWords.AddRange(directives);
        }

        public struct Token
        {
            public TextPointer StartPosition;
            public TextPointer EndPosition;
            public string Word;
            public Ttype type;

            public Token(TextPointer s, TextPointer e, string w, Ttype t)
            {
                StartPosition = s;
                EndPosition = e;
                Word = w;
                type = t;
            }
        }


        public enum Ttype
        {
            Word,
            Instr,

            Reg,
            Def,
            Spc,

            Dir,
      
            Num,
            Str,
            Chr,

            Com
        }

        List<Token> tokens = new List<Token>();
        Run run;
        TextPointer start;

        int pos = 0;
        string code;
        int len;

        int current_line = 0;
        public Lexer(Run run)
        {
            code = run.Text + " " ;
            code = to_upper(code);
            len = code.Length;
            this.run = run;
            start = run.ContentStart;
        }

         public List<Token> lex() {


            while (pos < len) {
                char let = code[pos];

                if (let == ' ')
                {
                    pos += 1;
                    continue;
                }
                else if (let == '\n')
                {
                    current_line += 1;
                }
                else if (Char.IsLetter(let) || let =='.' || let == '_')
                {
                    tokens.Add(compose_a_word());
                }
                else if (Char.IsDigit(let))
                {
                    tokens.Add(compose_a_num()); 
                }

                else if (let == '"')
                {
                    tokens.Add(compose_a_string());
                }
                //else if (let in "><"){
                // tokens.Add(new(let, self.current_line));
                //}

                else if (let == '@')
                {
                    tokens.Add(compose_a_directive());
                }

                else if (let == "'"[0])
                {
                    tokens.Add(compose_char()); 
                }
                else if (let == '#')
                {
                    int coment_start = pos;
                    while (let != '\n' && pos < len-1)
                    {
                        pos += 1;
                        let = code[pos];

                    }
                    tokens.Add(new Token(start.GetPositionAtOffset(coment_start), start.GetPositionAtOffset(pos + 1), "", Ttype.Com));
                }
                //else //globals.LEX_ERRORS.Add(SyntaxError("Illegal character error:", let))
                pos += 1;

            
            }
            return tokens;
        }


        Token compose_a_word() {

            char let = code[pos];
            string word = "";
            while ((Char.IsLetterOrDigit(let) || let == '.' || let == '_') && pos < len) {
                word += let;
                pos += 1;
                let = code[pos];
            }
            pos -= 1;

            if (Contains(word, instuctions)) 
                 return new Token(start.GetPositionAtOffset(pos - word.Length), start.GetPositionAtOffset(pos+1),word, Ttype.Instr); 
            
            if (Contains(word, regs))
                return new Token(start.GetPositionAtOffset(pos - word.Length), start.GetPositionAtOffset(pos + 1), word, Ttype.Reg);

            if (Contains(word, spc))
                return new Token(start.GetPositionAtOffset(pos - word.Length), start.GetPositionAtOffset(pos + 1), word, Ttype.Spc);

            return new Token(start.GetPositionAtOffset(pos - word.Length), start.GetPositionAtOffset(pos + 1), word, Ttype.Word);

        }


        Token compose_a_directive() {

            pos += 1;
            char let = code[pos];
            string word = "";

            while ((Char.IsLetterOrDigit(let) || let == '.' || let == '_') && pos < len){
                word += let;
                pos += 1;
                let = code[pos];
            }

            pos -= 1; ;
    
        if (Contains(word, directives))
                return new Token(start.GetPositionAtOffset(pos - word.Length), start.GetPositionAtOffset(pos + 1), word, Ttype.Dir);

            return new Token(start.GetPositionAtOffset(pos - word.Length), start.GetPositionAtOffset(pos + 1), word, Ttype.Word);
        }



        Token compose_a_num() {
            string word = "";
            int dot_count = 0;

            if (code[pos] == '-') {
                word += code[pos];
                pos += 1;
            }

            if (code[pos] == '0' && code[pos + 1] == 'X') {
                word += code[pos];
                word += code[pos+1];
                pos += 2;
            }

            char let = code[pos];
 

            while ((Char.IsDigit(let) || let == '.' || "ABCDEF".Contains(let)) && pos < len) {

                if (let == '.') { dot_count += 1; }

                word += (let);
                pos += 1;
                let = code[pos];
            }

            pos -= 1;


            return new Token(start.GetPositionAtOffset(pos - word.Length), start.GetPositionAtOffset(pos+1), word, Ttype.Num);
        }


        Token compose_a_string() {

            pos += 1;
            char let = code[pos];
            string word = "";
            while (let != '"')
            {
                word += (let);
                pos += 1;

                if(pos == len)
                    return new Token(start.GetPositionAtOffset(pos - word.Length-1), start.GetPositionAtOffset(pos), word, Ttype.Word);

                let = code[pos];
            }
           
    
        return new Token(start.GetPositionAtOffset(pos - word.Length-1 ), start.GetPositionAtOffset(pos+2), word, Ttype.Str);

        }


        Token compose_char()
        {
            pos += 1;
            char let = code[pos];
            pos += 1;
    
        //if (code[pos] != "'"[0])
         //   { let += code[pos].lower()}

           return new Token(start.GetPositionAtOffset(pos - 2), start.GetPositionAtOffset(pos+1), "", Ttype.Chr);

        }

        private string to_upper(string input) {
            char prev_inv = ' ';
            bool invert = true;

            string res = "";
            foreach (char let in input) {
                if (invert) {

                    char a = Char.ToUpper(let);
                    res += a;
                }
                else
                    res += let;

                if (!invert && let == prev_inv)
                    invert = true;
    
                else if (invert && (let == '"' || let == "'"[0]))
                {
                    prev_inv = let;
                    invert = false;
                }


                continue;

            }
           
        
    return res; }
        private bool Contains(string word, string[] array)
        {
            foreach (var item in array)
            {
                if (item.Equals(word))
                {
                    return true;
                }
            }
            return false;
        }
    }
}
