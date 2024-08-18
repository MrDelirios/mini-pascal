#---------------------------------------------------
# Tradutor para a linguagem Mini-pascal(revisada)
#
# Compiladores - 1 semestre 2024
# Thales Henrique do nascimento
#---------------------------------------------------
from lexico import TOKEN, Lexico
from semantico import Semantico

class Sintatico:

    def __init__(self, lexico):
        self.lexico = lexico
        self.semantico = Semantico(self) #estou passando o sintatico pro semantico

    def traduz(self):
        self.tokenLido = self.lexico.getToken() # o sintatico pede para o lexico token por token
        try: #ao receber o token ele vai na gramática e verifica se está de acordo com a gramática
            self.program() #esse é o método de ponto de partida que faz ele entrar na gramátic
            print('Traduzido com sucesso.')
        except:
            pass

    #o método que chama o consome, vai passar o lexema pra ser consumido. Entao aqui no metodo consome, é feita a verificação: o token que é pra ser consumido, é igual ao tokenLido do método traduz? Se sim, deu certo, se não, trata o erro aqui mesmo no consome "era esperado (tokenAtual) tal coisa mas veio tal coisa (tokenLido)"
    def consome(self, tokenAtual):
        (token, lexema, linha, coluna) = self.tokenLido
        if tokenAtual == token: #se o token consumido é igual ao token lido, pego um novo token pra analisar
            self.tokenLido = self.lexico.getToken()
        else: #trata o erro quando o token que era pra ser consumido não é igual ao token que foi lido
            msgTokenLido = TOKEN.msg(token)
            msgTokenAtual = TOKEN.msg(tokenAtual)
            print(f'Erro na linha {linha}, coluna {coluna}:')
            if token == TOKEN.erro:
                msg = lexema
            else:
                msg = msgTokenLido
            print(f'Era esperado {msgTokenAtual} mas veio {msg}')
            raise Exception


    def testaLexico(self):
        self.tokenLido = self.lexico.getToken()
        (token, lexema, linha, coluna) = self.tokenLido
        while token != TOKEN.eof:
            self.lexico.imprimeToken(self.tokenLido)
            self.tokenLido = self.lexico.getToken()
            (token, lexema, linha, coluna) = self.tokenLido


#                                  =======Gramatica========
    
    # <program> -> program id ( <identifier_list> ) ; <declarations> <subprogram_declarations> <compound_statement> .
    def program(self):
        self.consome(TOKEN.program)
        self.consome(TOKEN.id)
        self.consome(TOKEN.abrepar)
        #self.identifier_list() nao vamos utilizar
        self.consome(TOKEN.fechapar)
        self.consome(TOKEN.pontovirg)
        self.declarations()
        self.subprogram_declarations()
        self.compound_statement()
        self.consome(TOKEN.ponto)

    # <identifier_list> -> id <resto_identifier_list>
    def identifier_list(self):
        nome = self.tokenLido[1]
        self.consome(TOKEN.id)
        lista = [nome]
        lista2 = self.resto_identifier_list()
        return lista + lista2

    # <resto_identifier_list> -> , id <resto_identifier_list> | LAMBDA
    def resto_identifier_list(self):
        if self.tokenLido[0] == TOKEN.virg:
            self.consome(TOKEN.virg)
            return self.identifier_list()
        else:
            return []

    # <declarations> -> var <identifier_list> : <type> ; <declarations> | LAMBDA
    def declarations(self):
        if self.tokenLido[0] == TOKEN.var:
            self.consome(TOKEN.var)
            nomes = self.identifier_list()
            self.consome(TOKEN.doispontos)
            tipo = self.type()
            self.consome(TOKEN.pontovirg)
            self.semantico.declara(nomes,tipo)
            self.declarations()

    # <type> -> <standard_type> | array [ num .. num ] of <standard_type>
    def type(self):
        if self.tokenLido[0] == TOKEN.array:
            self.consome(TOKEN.array)
            self.consome(TOKEN.abrecol)
            self.consome(TOKEN.numinteger)
            self.consome(TOKEN.ptopto)
            self.consome(TOKEN.numinteger)
            self.consome(TOKEN.fechacol)
            self.consome(TOKEN.of)
            tipo = self.standard_type()
            return (TOKEN.array,tipo)
        else:
            return self.standard_type()

    # <standard_type> -> integer | real
    def standard_type(self):
        if self.tokenLido[0] == TOKEN.integer:
            self.consome(TOKEN.integer)
            return TOKEN.integer
        else:
            self.consome(TOKEN.REAL)
            return TOKEN.REAL

    # <subprogram_declarations> -> <subprogram_declaration> ; <subprogram_declarations> | LAMBDA
    def subprogram_declarations(self):
        if self.tokenLido[0] == TOKEN.begin:
            pass
        else:
            self.subprogram_declaration()
            self.consome(TOKEN.pontovirg)
            self.subprogram_declarations()

    # <subprogram_declaration> -> <subprogram_head> <declarations> <compound_statement>
    def subprogram_declaration(self):
        self.subprogram_head()
        self.declarations()
        self.compound_statement()
        self.semantico.saiu_subrotina()

    # <subprogram_head> -> function id <arguments> : <standard_type> ; | procedure id <arguments> ;
    def subprogram_head(self):
        if self.tokenLido[0] == TOKEN.function:
            self.consome(TOKEN.function)
            nomeFuncao = [self.tokenLido[1]]
            self.semantico.entrou_subrotina(nomeFuncao)
            self.consome(TOKEN.id)
            self.semantico.declara(nomeFuncao,TOKEN.function)
            self.arguments()
            self.consome(TOKEN.doispontos)
            self.standard_type()
            self.consome(TOKEN.pontovirg)
        else:
            self.consome(TOKEN.procedure)
            nomeProcedimento = [self.tokenLido[1]]
            self.semantico.entrou_subrotina(nomeProcedimento)
            self.consome(TOKEN.id)
            self.semantico.declara(nomeProcedimento,TOKEN.procedure)
            self.arguments()
            self.consome(TOKEN.pontovirg)

    # <arguments> -> ( <parameter_list> ) | LAMBDA
    def arguments(self):
        if self.tokenLido[0] == TOKEN.abrepar:
            self.consome(TOKEN.abrepar)
            self.parameter_list()
            self.consome(TOKEN.fechapar)

    # <parameter_list> -> <identifier_list> : <type> <resto_parameter_list>
    def parameter_list(self):
        self.identifier_list()
        self.consome(TOKEN.doispontos)
        self.type()
        self.resto_parameter_list()

    # <resto_parameter_list> -> ; <identifier_list> : <type> <resto_parameter_list> | LAMBDA
    def resto_parameter_list(self):
        if self.tokenLido[0] == TOKEN.pontovirg:
            self.consome(TOKEN.pontovirg)
            self.identifier_list()
            self.consome(TOKEN.doispontos)
            self.type()
            self.resto_parameter_list()

    # <compound_statement> -> begin <optional_statements> end
    def compound_statement(self):
        self.consome(TOKEN.begin)
        self.optional_statements()
        self.consome(TOKEN.end)

    # <optional_statements> -> <statement_list> | LAMBDA
    def optional_statements(self):
        if self.tokenLido[0] == TOKEN.end:
            pass
        else:
            self.statement_list()

    # <statement_list> -> <statement> <resto_statement_list>
    def statement_list(self):
        self.statement()
        self.resto_statement_list()

    # <resto_statement_list> -> ; <statement> <resto_statement_list> | LAMBDA
    def resto_statement_list(self):
        if self.tokenLido[0] == TOKEN.pontovirg:
            self.consome(TOKEN.pontovirg)
            self.statement()
            self.resto_statement_list()

    # <statement> -> <variable> assignop <expression> | <procedure_statement> | <compound_statement> | <if_statement> | while <expression> do <statement> | <inputOutput>
    def statement(self):
        if self.tokenLido[0] == TOKEN.id:
            nome = self.tokenLido[1]
            if self.semantico.existe_id(nome):
                tipo = self.semantico.consulta_tipo_id(nome)
                if tipo in [TOKEN.integer,TOKEN.REAL]:
                    self.variable()
                    self.consome(TOKEN.assignop)
                    self.expression()
                else:
                    self.procedure_statement()
            else:
                msg = 'Idenficador ' + nome + ' não declarado.'
                self.semantico.erroSemantico(msg)

        elif self.tokenLido[0] == TOKEN.begin:
            self.compound_statement()

        elif self.tokenLido[0] == TOKEN.IF:
            self.if_statement()

        elif self.tokenLido[0] == TOKEN.RETURN:
            self.consome(TOKEN.RETURN)
            self.expression()

        elif self.tokenLido[0] == TOKEN.WHILE:
            # while <expression> do <statement>
            self.consome(TOKEN.WHILE)
            self.expression()
            self.consome(TOKEN.do)
            self.statement()

        else:
            self.inputOutput()

    # <if_statement> -> if <expression> then <statement> <opc_else>
    def if_statement(self):
        self.consome(TOKEN.IF)
        self.expression()
        self.consome(TOKEN.then)
        self.statement()
        self.opc_else()

    # <opc_else> -> else <statement> | LAMBDA
    def opc_else(self):
        if self.tokenLido[0] == TOKEN.ELSE:
            self.consome(TOKEN.ELSE)
            self.statement()

    # <variable> -> id <opc_index>
    def variable(self):
        self.consome(TOKEN.id)
        self.opc_index()

    # <opc_index> -> [ <expression> ] | LAMBDA
    def opc_index(self):
        if self.tokenLido[0] == TOKEN.assignop:
            pass
        else:
            self.consome(TOKEN.abrecol)
            self.expression()
            self.consome(TOKEN.fechacol)

    # <procedure_statement> -> id <opc_parameters>
    def procedure_statement(self):
        self.consome(TOKEN.id)
        self.opc_parameters()

    # <opc_parameters> -> ( <expression_list> ) | LAMBDA
    def opc_parameters(self):
        if self.tokenLido[0] == TOKEN.abrepar:
            self.consome(TOKEN.abrepar)
            self.expression_list()
            self.consome(TOKEN.fechapar)

    # <expression_list> -> <expression> <resto_expression_list>
    def expression_list(self):
        self.expression()
        self.resto_expression_list()

    # <resto_expression_list> -> , <expression> <resto_expression_list> | LAMBDA
    def resto_expression_list(self):
        if self.tokenLido[0] == TOKEN.virg:
            self.consome(TOKEN.virg)
            self.expression()
            self.resto_expression_list()

    # <expression> -> <simple_expression> <resto_expression>
    def expression(self):
        self.simple_expression()
        self.resto_expression()

    # <resto_expression> -> relop <simple_expression> <resto_expression> | LAMBDA
    def resto_expression(self):
        if self.tokenLido[0] == TOKEN.relop:
            self.consome(TOKEN.relop)
            self.simple_expression()
            self.resto_expression()

    # <simple_expression> -> <term> <resto_simple_expression>
    def simple_expression(self):
        self.term()
        self.resto_simple_expression()

    # <resto_simple_expression> -> addop <term> <resto_simple_expression> | LAMBDA
    def resto_simple_expression(self):
        if self.tokenLido[0] == TOKEN.addop:
            self.consome(TOKEN.addop)
            self.term()
            self.resto_simple_expression()

    # <term> -> <uno> <resto_term>
    def term(self):
        self.uno()
        self.resto_term()

    # <resto_term> -> mulop <uno> <resto_term> | LAMBDA
    def resto_term(self):
        if self.tokenLido[0] == TOKEN.mulop:
            self.consome(TOKEN.mulop)
            self.uno()
            self.resto_term()

    # <uno> -> <factor> | addop <factor>
    def uno(self):
        if self.tokenLido[0] == TOKEN.addop:
            self.consome(TOKEN.addop)
            self.factor()
        else:
            self.factor()

    # <factor> -> id <resto_id> | num | ( <expression> ) | not <factor>
    def factor(self):
        if self.tokenLido[0] == TOKEN.id:
            token_id = self.tokenLido
            self.consome(TOKEN.id)
            self.resto_id(token_id)
        elif self.tokenLido[0] == TOKEN.numinteger:
            self.consome(TOKEN.numinteger)
        elif self.tokenLido[0] == TOKEN.numreal:
            self.consome(TOKEN.numreal)
        elif self.tokenLido[0] == TOKEN.abrepar:
            self.consome(TOKEN.abrepar)
            self.expression()
            self.consome(TOKEN.fechapar)
        else:
            self.consome(TOKEN.NOT)
            self.factor()

    # <resto_id> -> ( <expression_list> ) | LAMBDA
    def resto_id(self, token_id):
        if self.tokenLido[0] == TOKEN.abrepar:
            tipo_id = self.semantico.consulta_tipo_id(token_id[1])
            if tipo_id != TOKEN.function:
                msg = 'O identificador ' + token_id[1] + ' não é uma função.'
                self.semantico.erroSemantico(msg)
            self.consome(TOKEN.abrepar)
            self.expression_list()
            self.consome(TOKEN.fechapar)

    # <inputOutput> -> writeln(<outputs>) | write(<outputs>) | read(id)  | readln(id) 
    def inputOutput(self):
        if self.tokenLido[0] == TOKEN.WRITELN:
            self.consome(TOKEN.WRITELN)
            self.consome(TOKEN.abrepar)
            self.outputs()
            self.consome(TOKEN.fechapar)
        elif self.tokenLido[0] == TOKEN.WRITE:
            self.consome(TOKEN.WRITE)
            self.consome(TOKEN.abrepar)
            self.outputs()
            self.consome(TOKEN.fechapar)
        elif self.tokenLido[0] == TOKEN.READ:
            self.consome(TOKEN.READ)
            self.consome(TOKEN.abrepar)
            self.consome(TOKEN.id)
            self.consome(TOKEN.fechapar)
        else:
            self.consome(TOKEN.READLN)
            self.consome(TOKEN.abrepar)
            self.consome(TOKEN.id)
            self.consome(TOKEN.fechapar)

    # <outputs> -> <out> <restoOutputs>
    def outputs(self):
        self.out()
        self.restoOutputs()

    # <restoOutputs> -> , <out> <restoOutputs> | LAMBDA
    def restoOutputs(self):
        if self.tokenLido[0] == TOKEN.virg:
            self.consome(TOKEN.virg)
            self.out()
            self.restoOutputs()

    # <out> -> num | id | string
    def out(self):
        if self.tokenLido[0] == TOKEN.numinteger:
            self.consome(TOKEN.numinteger)
        elif self.tokenLido[0] == TOKEN.numreal:
            self.consome(TOKEN.numreal)
        elif self.tokenLido[0] == TOKEN.id:
            self.consome(TOKEN.id)
        else:
            self.consome(TOKEN.string)
