import re
from flask import Flask, request, render_template

app = Flask(__name__)


def syntactic_analysis(tokens):
    index = 0
    print(tokens)

    def parse_expression(tokens):
        nonlocal index
        if tokens[index][0] == 'STRING':
            index += 1
            if tokens[index][0] == 'OP':
                index += 1
                if tokens[index][0] == 'NUM':
                    index += 1
                    return True
        return False

    def parse_print(tokens):
        nonlocal index
        if tokens[index][0] == 'SYSTEM':
            index += 1
            if tokens[index][0] == 'PARENIZQ':
                index += 1
                if parse_expression(tokens):
                    if tokens[index][0] == 'PARENDER':
                        index += 1
                        if tokens[index][0] == 'PUNTOCOMA':
                            index += 1
                            return True
        return False

    def parse_for(tokens):
        nonlocal index
        if tokens[index][0] == 'FOR':
            index += 1
            if tokens[index][0] == 'PARENIZQ':
                index += 1
                if tokens[index][0] == 'INT':
                    index += 1
                    if tokens[index][0] == 'ID':
                        index += 1
                        if tokens[index][0] == 'EQ':
                            index += 1
                            if tokens[index][0] == 'NUM':
                                index += 1
                                if tokens[index][0] == 'PUNTOCOMA':
                                    index += 1
                                    if tokens[index][0] == 'ID':
                                        index += 1
                                        if tokens[index][0] == 'OP':
                                            index += 1
                                            if tokens[index][0] == 'NUM':
                                                index += 1
                                                if tokens[index][0] == 'PUNTOCOMA':
                                                    index += 1
                                                    if tokens[index][0] == 'ID':
                                                        index += 1
                                                        if tokens[index][0] == 'OP':
                                                            index += 1
                                                            if tokens[index][0] == 'PARENDER':
                                                                index += 1
                                                                if tokens[index][0] == 'LLAVEIZQ':
                                                                    index += 1
                                                                    if parse_print(tokens):
                                                                        if tokens[index][0] == 'LLAVEDER':
                                                                            return "Estructura FOR correcta"
        return "Error linea: " + str(index) + " con el token: " + str(tokens[index])

    return parse_for(tokens)


def lexical_analysis(code):
    tokens = []
    token_specification = [
        ('FOR', r'\bfor\b'),
        ('INT', r'\bint\b'),
        ('PRINTLN', r'\bprintln\b'),
        ('SYSTEM', r'\bsystem\.out\.println\b'),
        ('PARENIZQ', r'\('),
        ('PARENDER', r'\)'),
        ('LLAVEIZQ', r'\{'),
        ('LLAVEDER', r'\}'),
        ('PUNTOCOMA', r';'),
        ('NUM', r'\d+'),
        ('ID', r'[A-Za-z_]\w*'),
        ('OP', r'\+\+|\-\-|\+|\-|\<=|\>=|\<|\>|\==|\!=|\&\&|\|\|'),
        ('EQ', r'='),
        ('STRING', r'".*"'),
        ('COMA', r','),
        ('SPACE', r'\s+'),
        ('UNKNOWN', r'.')
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    line_num = 1
    line_start = 0
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start
        if kind == 'SPACE':
            continue
        tokens.append((kind, value, line_num, column))
    return tokens


@app.route('/', methods=['GET', 'POST'])
def index():
    tokens = []
    syntax_result = ''
    if request.method == 'POST':
        code = request.form['code']
        tokens = lexical_analysis(code)
        syntax_result = syntactic_analysis(tokens)
    return render_template('index.html', tokens=tokens, syntax_result=syntax_result)


if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')
