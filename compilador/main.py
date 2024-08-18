#---------------------------------------------------
# Tradutor para a linguagem Mini-pascal(revisada)
#
# Compiladores - 1 semestre 2024
# Thales Henrique do nascimento
#---------------------------------------------------
from lexico import Lexico
from sintatico import Sintatico

class Tradutor:

    def __init__(self, nomeArq):
        self.nomeArq = nomeArq

    def inicializa(self):
        self.arq = open(self.nomeArq, "r")
        self.lexico = Lexico(self.arq)
        self.sintatico = Sintatico(self.lexico)

    def traduz(self):
        self.sintatico.traduz()

    def finaliza(self):
        self.arq.close()

# inicia a traducao
if __name__ == '__main__':
    x = Tradutor('./arquivos/teste.txt')
    x.inicializa()
    x.traduz()
    x.sintatico.testaLexico()
    x.finaliza()

