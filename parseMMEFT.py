import sys
from typing import List
from copy import deepcopy
import re


privatepars = {'yl', 'ylbar', 'yu', 'yubar', 'yd', 'ydbar', 'g1', 'g2',
               'g3', 'lam', 'muH', 'invepsilonbar', 'KroneckerDelta', 'pi', 'log', 'onelooporder'}
dummyindices = ['mif1', 'mif2', 'mif3', 'mif4', 'mif5', 'MIF1']

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


def to_wcxf(MMEFTcoeffs: dict) -> dict:
    result = {}
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
    for coeff, values in MMEFTcoeffs.items():
        indx: List[str] = values[0]
        formula: str = values[1]
        if coeff in noindices.keys():
            result.update({noindices[coeff]: formula})
        if coeff in indices33.keys():
            for i in range(3):
                for j in range(3):
                    coeffname = f'{indices33[coeff]}_{i+1}{j+1}'
                    formflavour = formula.replace(indx[0], str(i))
                    formflavour = formflavour.replace(indx[1], str(j))
                    result.update({coeffname: formflavour})
        if coeff in indices3t.keys():
            for i in range(3):
                for j in range(i, 3):
                    coeffname = f'{indices3t[coeff]}_{i+1}{j+1}'
                    formflavour = formula.replace(indx[0], str(i))
                    formflavour = formflavour.replace(indx[1], str(j))
                    result.update({coeffname: formflavour})
        if coeff in indices4fa:
            for label in ['1111', '1112', '1113', '1122', '1123', '1133', '1122', '1123', '1133', '1212', '1213', '1221', '1222', '1223', '1231', '1232', '1233', '1313', '1322', '1323', '1331', '1332', '1333', '2222', '2223', '2233', '2323', '2333', '3333']:
                i = int(label[0])
                j = int(label[1])
                k = int(label[2])
                l = int(label[3])
                coeffname = f'{indices4fa[coeff]}_{i}{j}{k}{l}'
                formflavour = formula.replace(indx[0], str(i-1))
                formflavour = formflavour.replace(indx[1], str(j-1))
                formflavour = formflavour.replace(indx[2], str(k-1))
                formflavour = formflavour.replace(indx[3], str(l-1))
                result.update({coeffname: formflavour})
        if coeff in indices4fb:
            for i in range(3):
                for j in range(i, 3):
                    for k in range(3):
                        for l in range(k, 3):
                            coeffname = f'{indices4fb[coeff]}_{i+1}{j+1}{k+1}{l+1}'
                            formflavour = formula.replace(indx[0], str(i))
                            formflavour = formflavour.replace(indx[1], str(j))
                            formflavour = formflavour.replace(indx[2], str(k))
                            formflavour = formflavour.replace(indx[3], str(l))
                            result.update({coeffname: formflavour})
        if coeff == 'alphaOee':
            for i in range(3):
                for j in range(i, 3):
                    for k in range(3):
                        for l in range(k, 3):
                            if int(k+l) >= int(i+j) and i+j+k+l != '1322':
                                coeffname = f'ee_{i+1}{j+1}{k+1}{l+1}'
                                formflavour = formula.replace(indx[0], str(i))
                                formflavour = formflavour.replace(
                                    indx[1], str(j))
                                formflavour = formflavour.replace(
                                    indx[2], str(k))
                                formflavour = formflavour.replace(
                                    indx[3], str(l))
                                result.update({coeffname: formflavour})
    return result

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
    parameters = set()
    for it in items:
        sp = it.split('->')
        head = sp[0]
        formula = parenthesize(sp[1], 'KroneckerDelta[')
        formula = formula.replace('+', ' + ')
        formula = formula.replace('*', ' * ')
        formula = formula.replace('/', ' / ')
        formula = formula.replace('^', '**')
        if formula != '0':
            pars = re.findall(r'[a-zA-Z]+[0-9a-zA-Z]*', formula)
            parameters |= set(pars)
            if '[' in head:
                (coeff, indx) = head.split('[')
                indx = indx.replace(']', '')
                dicitems.update({coeff: (indx.split(','), formula)})
            else:
                dicitems.update({head: (None, formula)})
    wcxfcoeffs = to_wcxf(dicitems)
    parameters -= privatepars
    parameters -= set(dummyindices)
    barpars = []
    for p in parameters:
        if p[-3:] == 'bar':
            barpars.append(p)
    parameters -= set(barpars)
    parameters = list(parameters)
    parameters.sort()

    with open(outputfile, 'wt') as f:
        f.write(
            'from numpy import pi, log, conj\nfrom sminputs import g1, g2, g3, lam, yu, yd, yl\n\nKroneckerDelta = lambda x, y: int(x==y)\n\ninvepsilonbar=0\nonelooporder=1\n\n')
        f.write('def wc(')
        for p in parameters:
            default = 0
            if p == 'HIGHSCALE':
                default = 1000
            f.write(f'{p}={default}, ')
        f.write('):\n')
        for bp in barpars:
            f.write(f'\t{bp} = conj({bp[:-3]})\n')
        f.write('\treturn {\n')
        for k, v in wcxfcoeffs.items():
            f.write('\t        "' + k + '": ' + v + ',\n')
        f.write('\t}')
