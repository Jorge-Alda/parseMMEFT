import sys
from typing import List
from copy import deepcopy


def curlying(text: str) -> List[str]:
    curly = 0
    item = ''
    items = []
    for c in text:
        if c == '{':
            curly += 1
            if curly == 2:
                item = ''
        elif c == '}':
            curly -= 1
            if curly == 1:
                items.append(item)
        else:
            item += c
    return items


def parenthesize(text: str, func: str) -> str:
    lfun = len(func)
    text2 = list(deepcopy(text))
    for c in range(len(text)-lfun):
        if text[c:c+lfun] == func:
            brackets = 0
            for c2 in range(c, len(text)):
                if text[c2] == '[':
                    brackets += 1
                    if brackets == 1:
                        text2[c2] = '('
                elif text[c2] == ']':
                    brackets -= 1
                    if brackets == 0:
                        text2[c2] = ')'
                        break
    result = ''
    for c in text2:
        result += c
    return result


def splitcoeff(text: str) -> List[str]:
    ll = []
    brackets = 0
    item = ''
    for c in text:
        if c == '[':
            brackets += 1
        elif c == ']':
            brackets -= 1
        if c == ',' and brackets == 0:
            ll.append(deepcopy(item))
            item = ''
        else:
            item += c
    return ll


if __name__ == '__main__':
    inputfile = sys.argv[1]
    outputfile = sys.argv[2]
    with open(inputfile, 'rt') as f:
        text = f.read()

    rules = curlying(text)[2]
    rules = rules.replace('\n', '')
    rules = rules.replace(' ', '')
    rules = rules.replace('_', '')
    #rules = rules.replace('^', '**')
    rules = rules.replace('Pi', 'pi')
    rules = rules.replace(r'\[Mu]', 'HIGHSCALE')
    rules = rules.replace('Log[', 'log[')
    rules = parenthesize(rules, 'log[')
    #rules = parenthesize(rules, 'KroneckerDelta[')

    items = splitcoeff(rules)
    dicitems = {}
    for it in items:
        sp = it.split('->')
        head = sp[0]
        formula = parenthesize(sp[1], 'KroneckerDelta[')
        formula = formula.replace('+', ' + ')
        formula = formula.replace('*', ' * ')
        formula = formula.replace('/', ' / ')
        formula = formula.replace('^', '**')
        if '[' in head:
            (coeff, indx) = head.split('[')
            indx = indx.replace(']', '')
            dicitems.update({coeff: (indx.split(','), formula)})
        else:
            dicitems.update({head: (None, formula)})

    with open(outputfile, 'wt') as f:
        f.write(
            'from math import pi, log\n\nKroneckerDelta = lambda x, y: int(x==y)\n\n')
        f.write(str(dicitems))
