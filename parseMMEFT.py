import sys
from typing import List, Tuple
from copy import deepcopy
import re


privatepars = {'yl', 'ylbar', 'yu', 'yubar', 'yd', 'ydbar', 'g1', 'g2',
               'g3', 'lam', 'muH', 'invepsilonbar', 'KroneckerDelta', 'pi', 'log', 'onelooporder'}
dummyindices = ['mif1', 'mif2', 'mif3', 'mif4', 'mif5', 'MIF1']

noindices = {'alphaO3G': 'G',
             'alphaO3Gt': 'Gtilde',
             'alphaO3W': 'W',
             'alphaO3Wtilde': 'Wtilde',
             'alphaOH': 'phi',
             'alphaOHBox': 'phiBox',
             'alphaOHD': 'phiD',
             'alphaOHG': 'phiG',
             'alphaOHB': 'phiB',
             'alphaOHW': 'phiW',
             'alphaOHWB': 'phiWB',
             'alphaOHGt': 'phiGtilde',
             'alphaOHBt': 'phiBtilde',
             'alphaOHWt': 'phiWtilde',
             'alphaOHWBt': 'phiWtildeB'}
indices33 = {'alphaOuH': 'uphi',
             'alphaOdH': 'dphi',
             'alphaOeH': 'ephi',
             'alphaOeW': 'eW',
             'alphaOeB': 'eB',
             'alphaOuG': 'uG',
             'alphaOuW': 'uW',
             'alphaOuB': 'uB',
             'alphaOdG': 'dG',
             'alphaOdW': 'dW',
             'alphaOdB': 'dB',
             'alphaOHud': 'phiud'}
indices3t = {'alphaOHl1': 'phil1',
             'alphaOHl3': 'phil3',
             'alphaOHe': 'phie',
             'alphaOHq1': 'phiq1',
             'alphaOHq3': 'phiq3',
             'alphaOHu': 'phiu',
             'alphaOHd': 'phid'}
indices4fa = {'alphaOll': 'll',
              'alphaOqq1': 'qq1',
              'alphaOqq3': 'qq3',
              'alphaOuu': 'uu',
              'alphaOdd': 'dd'}
indices4fb = {'alphaOlq1': 'lq1',
              'alphaOlq3': 'lq3',
              'alphaOeu': 'eu',
              'alphaOed': 'ed',
              'alphaOud1': 'ud1',
              'alphaOud8': 'ud8',
              'alphaOle': 'le',
              'alphaOlu': 'lu',
              'alphaOld': 'ld',
              'alphaOqe': 'qe',
              'alphaOqu1': 'qu1',
              'alphaOqu8': 'qu8',
              'alphaOqd1': 'qd1',
              'alphaOqd8': 'qd8',
              'alphaOledq': 'ledq',
              'alphaOquqd1': 'quqd1',
              'alphaOquqd8': 'quqd8',
              'alphaOlequ1': 'lequ1',
              'alphaOlequ3': 'lequ3'}

allwcs = list(noindices.keys()) + list(indices33.keys()) + \
    list(indices3t.keys()) + list(indices4fa.keys()) + list(indices4fb.keys())
allwcs.append('alphaOee')


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


def extractpars(formula: str) -> Tuple[List[str], List[str]]:
    parameters = set(re.findall(r'[a-zA-Z]+[0-9a-zA-Z]*', formula))
    parameters -= privatepars
    parameters -= set(dummyindices)
    barpars = []
    for p in parameters:
        if p[-3:] == 'bar':
            barpars.append(p)
    parameters -= set(barpars)
    parameters = list(parameters)
    parameters.sort()
    barpars.sort()
    return (parameters, barpars)


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
        if formula != '0':
            if '[' in head:
                (coeff, indx) = head.split('[')
                indx = indx.replace(']', '')
                if coeff in allwcs:
                    dicitems.update({coeff: (indx.split(','), formula)})
            else:
                if head in allwcs:
                    dicitems.update({head: (None, formula)})

    with open(outputfile, 'wt') as f:
        f.write('from numpy import pi, log, conj\n')
        f.write('import sminputs\n\n')
        for p in ['g1', 'g2', 'g3', 'lam', 'yu', 'yd', 'yl']:
            f.write(f'{p} = sminputs.parameters["{p}"]\n')
        f.write('yubar = conj(yu)\n')
        f.write('ydbar = conj(yd)\n')
        f.write('ylbar = conj(yl)\n\n')
        f.write('KroneckerDelta = lambda x, y: int(x==y)\n\n')
        f.write('invepsilonbar=0\nonelooporder=1\n\n')

        f.write('def reloadsminputs():\n')
        for p in ['g1', 'g2', 'g3', 'lam', 'yu', 'yd', 'yl']:
            f.write(f'\tglobal {p}\n\t{p} = sminputs.parameters["{p}"]\n')
        f.write('\tglobal yubar \n\tyubar = conj(yu)\n')
        f.write('\tglobal ydbar \n\tydbar = conj(yd)\n')
        f.write('\tglobal ylbar \n\tylbar = conj(yl)\n\n')

        wcdict = ""
        parameters = set()

        for coeff, values in dicitems.items():
            f.write(f'def {coeff}(')
            indx: List[str] = values[0]
            formula: str = values[1]
            pars, bpars = extractpars(formula)
            pars = set(pars)
            if indx is not None:
                pars -= set(indx)
                for i in range(len(indx)):
                    f.write(f'flavour{i}, ')
                    formula = formula.replace(indx[i], f'flavour{i}')
            parameters |= pars

            for p in pars:
                f.write(f'{p}, ')

            f.write('):\n')
            for bp in bpars:
                f.write(f'\t{bp} = conj({bp[:-3]})\n')
            dummies = []
            for d in dummyindices:
                if d in formula:
                    dummies.append(d)
            if len(dummies) == 0:
                f.write('\treturn ' + formula)
            else:
                f.write('\tresult = 0\n')
                for i, d in enumerate(dummies):
                    f.write('\t'*(i+1))
                    f.write(f'for {d} in range(3):\n')
                f.write('\t'*(len(dummies)+2))
                f.write('result += ' + formula + '\n')
                f.write('\treturn result')

            if coeff in noindices.keys():
                coeffname = noindices[coeff]
                wcdict += f'\t        "{coeffname}": {coeff}('
                for p in pars:
                    wcdict += f'{p}, '
                wcdict += '),\n'
            if coeff in indices33.keys():
                for i in range(3):
                    for j in range(3):
                        coeffname = f'{indices33[coeff]}_{i+1}{j+1}'
                        wcdict += f'\t        "{coeffname}": {coeff}({i}, {j}, '
                        for p in pars:
                            wcdict += f'{p}, '
                        wcdict += '),\n'
            if coeff in indices3t.keys():
                for i in range(3):
                    for j in range(i, 3):
                        coeffname = f'{indices3t[coeff]}_{i+1}{j+1}'
                        wcdict += f'\t        "{coeffname}": {coeff}({i}, {j}, '
                        for p in pars:
                            wcdict += f'{p}, '
                        wcdict += '),\n'
            if coeff in indices4fa:
                for label in ['1111', '1112', '1113', '1122', '1123', '1133', '1122', '1123', '1133', '1212', '1213', '1221', '1222', '1223', '1231', '1232', '1233', '1313', '1322', '1323', '1331', '1332', '1333', '2222', '2223', '2233', '2323', '2333', '3333']:
                    i = int(label[0])
                    j = int(label[1])
                    k = int(label[2])
                    l = int(label[3])
                    coeffname = f'{indices4fa[coeff]}_{i}{j}{k}{l}'
                    wcdict += f'\t        "{coeffname}": {coeff}({i-1}, {j-1}, {k-1}, {l-1}, '
                    for p in pars:
                        wcdict += f'{p}, '
                    wcdict += '),\n'
            if coeff in indices4fb:
                for i in range(3):
                    for j in range(i, 3):
                        for k in range(3):
                            for l in range(k, 3):
                                coeffname = f'{indices4fb[coeff]}_{i+1}{j+1}{k+1}{l+1}'
                                wcdict += f'\t        "{coeffname}": {coeff}({i}, {j}, {k}, {l}, '
                                for p in pars:
                                    wcdict += f'{p}, '
                                wcdict += '),\n'
            if coeff == 'alphaOee':
                for label in ['1111', '1112', '1113', '1122', '1123', '1133', '1212', '1213', '1222', '1223', '1232', '1233', '1313', '1323', '1333', '2222', '2223', '2233', '2323', '2333', '3333']:
                    i = int(label[0])
                    j = int(label[1])
                    k = int(label[2])
                    l = int(label[3])
                    coeffname = f'ee_{i}{j}{k}{l}'
                    wcdict += f'\t        "{coeffname}": {coeff}({i-1}, {j-1}, {k-1}, {l-1}, '
                    for p in pars:
                        wcdict += f'{p}, '
                    wcdict += '),\n'
            f.write('\n\n')

        f.write('def wc(')
        for p in parameters:
            f.write(f'{p}, ')
        f.write('):\n')

        f.write('\treturn {\n' + wcdict)
        f.write('\t}')
