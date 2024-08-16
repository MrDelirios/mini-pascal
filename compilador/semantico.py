#---------------------------------------------------
# Tradutor para a linguagem Mini-pascal(revisada)
#
# Compiladores - 1 semestre 2024
# Thales Henrique do nascimento
#---------------------------------------------------
from ttoken import TOKEN

class Semantico:

    def __init__(self, nomeAlvo):
        self.tabelaSimbolos = dict()
        self.alvo = open(f'./arquivos/{nomeAlvo}', "wt")

    def finaliza(self):
        self.alvo.close()

    def erroSemantico(self, msg):
        (token, lexema, linha, coluna) = self.sintatico.tokenLido
        print(f'Erro na linha {linha}: ')
        print(f' {msg}')
        raise Exception

    def gera(self, nivel, codigo):
        identacao = ' ' * 4 * nivel
        linha = identacao + codigo
        self.alvo.write(linha)

    """ def declara(self, token):
        if token[1] in self.tabelaSimbolos:
            msg = f'Variavel {token[1]} redeclarada'
            self.erroSemantico(token, msg)
        else:
            self.tabelaSimbolos[token[1]] = token[0]"""
        
    def declara(self, nomes, tipo): #tipo será uma string

        for id in nomes:
            if self.existe_id(id):
                msg = f'Identificador {id} ja existente'
                self.erroSemantico(msg)
            else:
               self.tabelaSimbolos[id] = tipo

    def existe_id(self, identificador):
        if identificador in self.tabelaSimbolos:
            True
        else:
            False

    #verifica o que é o identificador que eu passei (se é variavel, funcao, procedimento, etc.)
    def consulta_tipo_id(self,id):
        return self.tabelaSimbolos[id]
