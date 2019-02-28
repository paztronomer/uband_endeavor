""" Script for plotting the number of objects versus some other features
"""

import os
import numpy as np
from scipy import stats
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns

if __name__ == '__main__':

    fnm = 'r4083_nobjects.csv'
    # 'r4059_nobjects.csv'
    df = pd.read_csv(fnm)

    # Lowercase
    df.columns = df.columns.map(str.lower)
    
    # Subset after visual inspection
    idx = (df['exptime'] >= 30) & (df['exptime'] < 600)
    # df = df.loc[idx]

    # Get the linear least squares
    a, b, r_val, p_val, std_err = stats.linregress(df['exptime'].values, 
                                                   df['nobjects'].values)
    print('Fit:\na={0:.3f} ; b={1:.3f}'.format(a, b))
    f = lambda x: a * x + b

    # Upper and lower limits
    x_aux = np.linspace(df['exptime'].min(), df['exptime'].max())
    a_dw = 0.6 * (f(500) - f(30)) / (500. - 30.)
    f_dw = lambda x: a_dw * x +  0.6 * b 
    a_up = 2.25 * (f(500) - f(30)) / (500. - 30.)
    f_up = lambda x: a_up * x + 2.25 * b 

    txt = 'Upper/Lower limits:\n'
    txt += 'a={0:.3f}/{1:.3f}'.format(a_up, a_dw)
    txt += ' ; b={0:.3f}/{1:.3f}'.format(1e4, 1.4 *  b)
    print(txt)

    # Selection
    def select(g1, g2, x, y):
        if ((g1(x) >= y) and (g2(x) <= y)):
            return True
        else:
            return False
    # Apply the simple selection function to the dataframe
    df['sel'] = [select(f_up, f_dw, row['exptime'], row['nobjects']) 
                 for idx, row in df.iterrows()]
    # Save the list of selected exposures
    np.savetxt('uband_sel01.csv', df.loc[df['sel'], 'expnum'],
               fmt='%d')

    print('Number of selected exposures: ', len(df.loc[df['sel']].index))


    fig, ax = plt.subplots()

    kw = {
        'ls': '--',
        'lw': 2,
        'color': 'navy',
        'alpha': 0.5,
    }
    ax.plot(x_aux, f_dw(x_aux), **kw)
    ax.plot(x_aux, f(x_aux), 'b-')
    ax.plot(x_aux, f_up(x_aux), **kw) 
    ax.fill_between(x_aux, f_up(x_aux), f_dw(x_aux), color='gold', alpha=0.2)

    ax.scatter(df['exptime'], df['nobjects'], marker='.', c='g')
   
    ax.set_xlabel('exptime [s]')
    ax.set_ylabel('FP number of objects')
    ax.set_title('Relation between exposure time and observed objects, u-band',
                 color='orange')
    ax.set_yscale('log')
    
    plt.tight_layout()
    
    plt.savefig('nobj_exptime_r4083.png', format='png', dpi=300)
    plt.show()


    exit()
    # --------------
    # Seaborn linear 
    g = sns.lmplot(x='exptime', y='nobjects', data=df,
                   markers='.')
    g.set(yscale='log')
    g.set_axis_labels('exposure time [s]', 'N objects')


    plt.show()

    exit()

    # Plotting
    plt.close('all')
    fig, ax = plt.subplots()
    #
    ax.scatter(df['exptime'], df['nobjects'], marker='o', s=10, c=df['nite'])
    #
    ax.set_yscale('log')
    plt.show()


