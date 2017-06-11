
import pandas as pd
import numpy as np
from math import sqrt
import pprint


df = pd.read_csv('./Data/Avanti.csv', index_col='Date')
df['PCT_change'] = ((df['Close Price'] - df['Open Price']) / df['Open Price']) * 100  # Daily Percent Change
avanti = df[['Average Price', 'PCT_change']]

avanti_mean = avanti['PCT_change'].mean()
avanti['MAD'] = ((avanti['PCT_change'] - avanti_mean)**2)
avanti_var = avanti['MAD'].sum() / avanti.shape[0]
avanti_std = sqrt(avanti_var)

firms = ['APLAPOLLO', 'LT', 'TCS', 'FINPIPE', 'SBIN', 'FINCABLES', 'SUNPHARMA', 'LICHSGN']

op = []

for firmL in firms:
    obj = {}
    path = './Data/' + firmL + '.csv'
    df1 = pd.read_csv(path, index_col='Date')
    df1['PCT_change'] = ((df1['Close Price'] - df1['Open Price']) / df1['Open Price']) * 100  # Daily Percent Change
    firm = df1[['Average Price', 'PCT_change']]

    firm_mean = firm['PCT_change'].mean()
    firm['MAD'] = ((firm['PCT_change'] - firm_mean)**2)
    firm_var = firm['MAD'].sum() / firm.shape[0]
    firm_std = sqrt(firm_var)

    corr = avanti.corrwith(firm, 0)['PCT_change']

    avanti_weight = 0.8
    firm_weight = 1 - avanti_weight

    print('avanti_weight: ', avanti_weight)
    print('firm_weight ', firm_weight)

    exp_return = sqrt(((avanti_weight**2) * (avanti_var)) + ((firm_weight**2) * (firm_var)) +
                      (2 * avanti_weight * firm_weight * avanti_std * firm_std * corr))

    print('Expected Rerturn for Avanti and ', firmL, ' is', exp_return)

    risk = avanti_weight * avanti_std + firm_weight * firm_std

    print('Risk for Avanti and ', firmL, ' is', risk)

    obj['Return'] = exp_return
    # obj['Risk'] = risk
    obj['Firm'] = firmL

    op.append(obj.copy())
    obj = None

print('-----------------------------------------------------')
# print(op)
newlist = sorted(op, key=lambda k: k['Return'], reverse=True)
pprint.pprint(newlist)
op = None
newlist = None
