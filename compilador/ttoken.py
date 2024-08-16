#---------------------------------------------------
# Tradutor para a linguagem Mini-pascal(revisada)
#
# Compiladores - 1 semestre 2024
# Thales Henrique do nascimento
#---------------------------------------------------

from enum import IntEnum

class TOKEN(IntEnum):
    erro = 1
    eof = 2
    id = 3
    numinteger = 4
    end = 5
    integer = 6
    REAL = 7
    function = 8
    procedure = 9
    var = 10
    begin = 11
    program = 12
    IF = 13
    then = 14
    ELSE = 15
    WHILE = 16
    do = 17
    assignop = 18
    relop = 19
    addop = 20
    mulop = 21
    NOT = 22
    array = 23
    of = 24
    abrepar = 25
    fechapar = 26
    abrecol = 27 #colchete
    fechacol = 28 #colchete
    virg = 29
    pontovirg = 30
    doispontos = 31
    ponto = 32
    ptopto = 33  # ..
    numreal = 34
    string = 35
    WRITELN = 36
    WRITE = 37
    READLN = 38
    READ = 39
    RETURN = 40

    @classmethod
    def msg(cls, token):
        nomes = {
            1:'erro',
            2:'<eof>',
            3:'id',
            4:'numinteger',
            5:'end',
            6:'integer',
            7:'REAL',
            8:'function',
            9:'procedure',
            10:'var',
            11:'begin',
            12:'program',
            13:'if',
            14:'then',
            15:'else',
            16:'while',
            17:'do',
            18:':=',
            19:'operador relacional',
            20:'operador adicional',
            21:'operador multiplicacional',
            22:'not',
            23:'array',
            24:'of',
            25:'(',
            26:')',
            27:'[',
            28:']',
            29:',',
            30:';',
            31:':',
            32:'.',
            33:'..',
            34:'numreal',
            35:'string',
            36:'writeln',
            37:'write',
            38:'readln',
            39:'read',
            40: 'return'
            
        }
        return nomes[token]

    @classmethod
    def reservada(cls, lexema):
        reservadas = {
            'function': TOKEN.function,
            'procedure': TOKEN.procedure,
            'var': TOKEN.var,
            'begin': TOKEN.begin,
            'program': TOKEN.program,
            'if': TOKEN.IF,
            'then': TOKEN.then,
            'else': TOKEN.ELSE,
            'while': TOKEN.WHILE,
            'do': TOKEN.do,
            'integer': TOKEN.integer,
            'real': TOKEN.REAL,
            'array': TOKEN.array,
            'of': TOKEN.of,
            'mod': TOKEN.mulop,
            'divi': TOKEN.mulop,
            'end': TOKEN.end,
            'not': TOKEN.NOT,
            'writeln': TOKEN.WRITELN,
            'write': TOKEN.WRITE,
            'readln': TOKEN.READLN,
            'read':TOKEN.READ,
            'RETURN': TOKEN.RETURN,
        }
        if lexema in reservadas:
            return reservadas[lexema]
        else:
            return TOKEN.id
