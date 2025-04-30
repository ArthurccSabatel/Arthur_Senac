import pandas as pd
import win32com.client as win32

# #importar base de dados

tabelaVendas = pd.read_excel('Vendas.xlsx')

# pip install openpyxl

# visualizar base de dados

pd.set_option('display.max_columns', None)
print(tabelaVendas)

print('-' * 50)

# faturamento por loja

faturamento = tabelaVendas[['ID Loja', 'Valor Final']].groupby('ID Loja').sum()
print(faturamento)

print('-' * 50)

# quantidade de produtos vendidos por loja

quantidade = tabelaVendas[['ID Loja', 'Quantidade']].groupby('ID Loja').sum()
print(quantidade)

print('-' * 50)

# ticket médio por produto em cada loja enviar um email com o relatório
#ticket médio = faturamento/quantidade

ticketMedio = (faturamento['Valor Final'] / quantidade['Quantidade']).to_frame()
ticketMedio = ticketMedio.rename(columns={0: 'Ticket Médio'})
print(ticketMedio)

# enviar um email com o relatório

outlook = win32.Dispatch('outlook.application')
mail = outlook.CreateItem(0)
mail.To = 'user@example.com'
mail.Subject = 'Relatório de Vendas por Loja'
mail.HTMLBody = f'''
<p>Prezados,</p>

<p>Segue o Relatório de Vendas por cada Loja.<p>

<p>Faturamento:<p>
{faturamento.to_html(formatters={'Valor Final': 'R${:,.2f}}'.format})}

<p>Quantidade Vendida:<p>
{quantidade.to_html()}

<p>Ticket Médio dos Produtos em cada Loja:<p>
{ticketMedio.to_html(formatters={'Ticket Médio': 'R${:,.2f}'.format})}

<p>Qualquer dúvida estou à disposição.</p>

<p>Att.,<p/>
<p>Prof. asd<p>
'''

mail.Send()

print('email Enviado'),

