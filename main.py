import pandas as pd
import matplotlib.pyplot as plt

import argparse

parser = argparse.ArgumentParser()

parser.add_argument('csv_file', type=str, help='Target path')
args = parser.parse_args()

target = args.csv_file
df = pd.read_csv(target,sep=';',encoding='ANSI')
umsatz = df[['Buchungstag', 'Verwendungszweck', 'Buchungstext', 'Beguenstigter/Zahlungspflichtiger', 'Betrag', 'Info']]
umsatz['Betrag'] = pd.to_numeric(umsatz.Betrag.str.replace(',','.'))
plt.show()
umsatz['Buchungstag'] = pd.to_datetime(df.Buchungstag, format = '%d.%m.%y')
umsatz = umsatz.set_index('Buchungstag')
umsatz = umsatz.sort_index()
umsatz['kontostand'] = umsatz.Betrag.cumsum()+4254.4

def by_month(df, column):
    '''Get monthly sum of column'''
    grouped = df.groupby(pd.Grouper(freq='M'))
    acc = grouped[column].sum()
    return acc

monthly = by_month(umsatz, 'Betrag')
income = umsatz.query('Betrag > 0')
monthly_income = by_month(income, 'Betrag')
spending = umsatz.query('Betrag < 0')
monthly_spending = by_month(spending, 'Betrag')

monthly_savings = monthly_income+monthly_spending

monthly_income.plot(color = 'green', linestyle = None,marker='x' )    
monthly_spending.plot(color = 'red',linestyle = None,marker='x') 
monthly_savings.plot(color = 'blue',linestyle = None,marker='x') 
   
plt.show()
