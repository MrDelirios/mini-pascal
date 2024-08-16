#---------------------------------------------------
# Tradutor para a linguagem Mini-pascal(revisada)
#
# Compiladores - 1 semestre 2024
# Thales Henrique do nascimento
#---------------------------------------------------
from ttoken import TOKEN

class Lexico:
    def __init__(self, arqFonte):
        self.arqFonte = arqFonte  # objeto file
        self.fonte = self.arqFonte.read()  # string contendo file
        self.tamFonte = len(self.fonte)
        self.indiceFonte = 0
        self.tokenLido = None  # (token, lexema, linha, coluna)
        self.linha = 1  # linha atual no fonte
        self.coluna = 0  # coluna atual no fonte

    def fimDoArquivo(self):
        return self.indiceFonte >= self.tamFonte

    def getchar(self):
        if self.fimDoArquivo():
            return '\0'
        car = self.fonte[self.indiceFonte]
        self.indiceFonte += 1
        if car == '\n':
            self.linha += 1
            self.coluna = 0
        else:
            self.coluna += 1
        return car

    def ungetchar(self, simbolo):
        if simbolo == '\n':
            self.linha -= 1
        if self.indiceFonte > 0:
            self.indiceFonte -= 1
        self.coluna -= 1

    def imprimeToken(self, tokenCorrente):
        (token, lexema, linha, coluna) = tokenCorrente
        msg = TOKEN.msg(token)
        print(f'(tk={msg} lex="{lexema}" lin={linha} col={coluna})')

    def getToken(self):
        estado = 1
        simbolo = self.getchar()
        lexema = ''
        while simbolo in ['#', ' ', '\t', '\n']:
            if simbolo == '#':
                simbolo = self.getchar()
                while simbolo != '\n' and not self.fimDoArquivo():
                    simbolo = self.getchar()
            while simbolo in [' ', '\t', '\n']:
                simbolo = self.getchar()
        lin = self.linha
        col = self.coluna
        while True:
            if estado == 1:
                if simbolo.isalpha():
                    estado = 2
                elif simbolo.isdigit():
                    estado = 3
                elif simbolo == '"':
                    estado = 4
                elif simbolo == "(":
                    return (TOKEN.abrepar, "(", lin, col)
                elif simbolo == ")":
                    return (TOKEN.fechapar, ")", lin, col)
                elif simbolo == ",":
                    return (TOKEN.virg, ",", lin, col)
                elif simbolo == ";":
                    return (TOKEN.pontovirg, ";", lin, col)
                elif simbolo == ".":
                    estado = 7
                elif simbolo == "+":
                    return (TOKEN.addop, "+", lin, col)
                elif simbolo == "'" or simbolo == "'":
                    estado = 12 
                elif simbolo == "-":
                    return (TOKEN.addop, "-", lin, col)
                elif simbolo == "*":
                    return (TOKEN.mulop, "*", lin, col)
                elif simbolo == "/":
                    estado = 11
                elif simbolo == "<":
                    estado = 5
                elif simbolo == ">":
                    estado = 6
                elif simbolo == "=":
                    return(TOKEN.relop,'=', lin, col)
                elif simbolo == ":":  # novo token para os tipos
                    estado = 9
                elif simbolo == '[':
                    return (TOKEN.abrecol, "[", lin, col)
                elif simbolo == ']':
                    return (TOKEN.fechacol, "]", lin, col)
                elif simbolo == '\0':
                    return (TOKEN.eof, '<eof>', lin, col)
                else:
                    lexema += simbolo
                    return (TOKEN.erro, lexema, lin, col)

            elif estado == 2:
                if simbolo.isalnum():
                    estado = 2
                else:
                    self.ungetchar(simbolo)
                    token = TOKEN.reservada(lexema)
                    return (token, lexema, lin, col)

            elif estado == 3:
                if simbolo.isdigit(): #lê numeros inteiros e permanece no 3 enquanto tiver lendo número
                    estado = 3
                elif simbolo == '.': #se achar um ponto, quer dizer que o número é real, portanto vai para o estado 31
                    estado = 31
                elif simbolo.isalpha():
                    lexema += simbolo
                    return (TOKEN.erro,lexema,lin,col)
                else:
                    self.ungetchar(simbolo)
                    return (TOKEN.numinteger,lexema,lin,col)

            elif estado == 31:
                if simbolo.isdigit(): #se achou número depois do ponto, vai para o estado 32
                    estado = 32
                elif simbolo == '.': #leu o .. do vetor. entao precisamos devolver o número que foi lido, e dar um unget pra desler esse segundo ponto e o primeiro ponto
                    self.ungetchar(simbolo)
                    self.ungetchar(simbolo)
                    #lexeama = 1.
                    lexema = lexema[:-1] # lexema = lexema[:-1] também dá certo
                    return (TOKEN.numinteger, lexema, lin, col)
                else:
                    self.ungetchar(simbolo)
                    return (TOKEN.erro,lexema,lin,col)

            elif estado == 32:
                if simbolo.isdigit(): #continua no estado 32 quando lê numeros
                    estado = 32
                elif simbolo.isalpha(): #se tiver alugma letra no meio do número ele retorna erro
                    lexema += simbolo
                    return (TOKEN.erro,lexema,lin,col)
                else: #o número acabou
                    self.ungetchar(simbolo)
                    return (TOKEN.numreal,lexema,lin,col)

            elif estado == 4:
                while True:
                    if simbolo == '"':
                        lexema += simbolo
                        return (TOKEN.string, lexema, lin, col)
                    if simbolo in ['\n', '\0']:
                        return (TOKEN.erro, lexema, lin, col)
                    if simbolo == '\\':
                        lexema += simbolo
                        simbolo = self.getchar()
                        if simbolo in ['\n', '\0']:
                            return (TOKEN.erro, lexema, lin, col)
                    lexema += simbolo
                    simbolo = self.getchar()

            elif estado == 5:
                if simbolo == '=':
                    lexema += simbolo
                    return (TOKEN.relop, '<=', lin, col)
                else:
                    self.ungetchar(simbolo)
                    return (TOKEN.relop, '<', lin, col)

            elif estado == 6:
                if simbolo == '=':
                    lexema += simbolo
                    return (TOKEN.relop, '>=', lin, col)
                else:
                    self.ungetchar(simbolo)
                    return (TOKEN.relop, ">", lin, col)
            elif estado == 7:
                if simbolo == ".":
                    return (TOKEN.ptopto,'..',lin, col)
                else:
                    self.ungetchar(simbolo)
                    return (TOKEN.ponto,'.', lin, col)
            elif estado == 9:
                if simbolo == '=':
                    return (TOKEN.assignop,':=', lin, col)
                else:
                    self.ungetchar(simbolo)
                    return (TOKEN.doispontos, ':', lin, col)
            elif estado == 11:
                if simbolo == '/':
                    while simbolo != '\n' and not self.fimDoArquivo():
                        simbolo = self.getchar()
                else:
                    self.ungetchar(simbolo)
                    return (TOKEN.mulop, '/', lin, col)
            elif estado == 12:
                while True:
                    if simbolo == "'" or simbolo == '"':
                        lexema += simbolo
                        return (TOKEN.string, lexema, lin, col)
                    
                    if simbolo in ["\n", "\0"]:
                        return (TOKEN.erro, lexema, lin, col)
                    
                    if simbolo == '\\':
                        lexema += simbolo
                        simbolo = self.getchar()

                        if simbolo in ["\n", "\0"]:
                            return (TOKEN.erro, lexema, lin, col)
                    lexema += simbolo
                    simbolo = self.getchar()
            else:
                print('BUG!!!')

            lexema += simbolo
            simbolo = self.getchar()
