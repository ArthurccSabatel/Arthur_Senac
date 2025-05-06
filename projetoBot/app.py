# AUTOMATIZADOR DE COBRANÇAS VIA WHATSAPP

# Objetivo:
#     -Enviar mensagens de cobrança automaticamente para clientes com vencimentos diferentes
    
# Rescusos utilizados:
#     - Leitura de planilha com openpyxl
#     - Abertura de links via webbrowser
#     - Digitação automatizada com pyautogui
#     - Criação de links personalizados de Whatsapp com urllib.parse.wuote



import openpyxl # le e manipula arquivos excel
from urllib.parse import quote # codifica mensagens para colocar link no Whatsapp
import webbrowser # abre links no navegador
from time import sleep # pausa o código por alguns segundos
import pyautogui # permite clicar automaticamente na tela, como um robô
import os # usado para funções do sistema, como pular linha ao gravar o arquivo



# Abrir o whatsapp web manualmente e dar tempo para carregar

webbrowser.open('https://web.whatsapp.com')
sleep(20) # tempo para escanear o QR code

# Abrir planilha com clientes

workbook = openpyxl.load_workbook('clientes.xlsx')
paginaClientes = workbook['Sheet1']

# Lê a planilha a partir da segunda linha (a primeira geralmente é o cabeçalho)

for linha in paginaClientes.iter_rows(min_row=2):
    nome = linha[0].value
    telefone = linha[1].value
    vencimento = linha[2].value
    
    # Validar dados obrigatórios
    
    if not nome or not telefone or not vencimento:
        print(f'Dados imcompletos na linha: Nome = {nome}, telefone = {telefone}, Vencimento = {vencimento}')
        continue
    
    try:
        mensagem = (f"Olá {nome}, seu boleto vence no dia {vencimento.strftime('%d/%m/%Y')}. "
                    "Favor pagar no link: http://www.linkpagamento.com")
        linkWhatsapp = f'http://web.whatsapp.com/send?phone={telefone}&text={quote(mensagem)}'
        
        webbrowser.open(linkWhatsapp)
        sleep(10) # tempo para abrir o Whatsapp com o número
        
        # Procurar botão de envio (ex: seta verde)
        
        seta = pyautogui.locateCenterOnScreen('seta.png')
        if seta:
            sleep(2)
            pyautogui.leftClick(seta[0], seta[1])
            sleep(2)
            pyautogui.hotkey('ctrl', 'w') #fecha a aba atual
            sleep(2)
        
        else:
            raise Exception("Botão de envio ('seta.png) não localizado na tela.")
        
    except Exception as e:
        print(f'Erro ao enviar mensagem para {nome}. Erro: {e}')
        with open('erros.csv', 'a', newline='', encoding='utf-8') as arquivo:
            arquivo.write(f'{nome},{telefone}{os.linesep}')
        
        
        