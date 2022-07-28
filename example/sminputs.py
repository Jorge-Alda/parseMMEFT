'''
As a first approximation, we obtain the SM parameters at the scale HIGHSCALE, neglecting the SMEFT contributions
'''

from wilson.run.smeft.smpar import smeftpar

HIGHSCALE = 1000  # <== You might want to change this value
smcoeffs = {'phi': 0, 'phiBox': 0, 'phiD': 0, 'phiG': 0, 'phiW': 0,
            'phiWB': 0, 'phiB': 0, 'dphi': 0, 'uphi': 0, 'ephi': 0}
parameters = {}


def calculate(wc: dict = smcoeffs):
    for coeff in smcoeffs.keys():
        if not coeff in wc.keys():
            wc.update({coeff: 0})
    smpars = smeftpar(HIGHSCALE, wc, 'Warsaw')
    parameters.update({'g1': smpars['gp']})
    parameters.update({'g2': smpars['g']})
    parameters.update({'g3': smpars['gs']})
    parameters.update({'lam': smpars['Lambda']})
    parameters.update({'yu': smpars['Gu']})
    parameters.update({'yd': smpars['Gd']})
    parameters.update({'yl': smpars['Ge']})


calculate()
