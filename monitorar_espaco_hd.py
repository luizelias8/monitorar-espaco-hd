import psutil
from configparser import ConfigParser
import os
import sys
from winotify import Notification
import schedule
import time

# Obtém o diretório do script atual
diretorio_script = os.path.dirname(__file__)

# Função para exibir notificações no Windows
def exibir_notificacao(titulo, mensagem):
    """
    Exibe uma notificação com título e mensagem especificados.
    """
    # Define o caminho para o ícone
    caminho_icone = os.path.join(diretorio_script, 'icone.ico')

    toast = Notification(
        app_id='Alerta de Espaço em Disco',
        title=titulo,
        msg=mensagem,
        duration='long',
        icon=caminho_icone
    )
    toast.show()

def verificar_espaco_disco():
    # Caminho completo para o arquivo de configuração
    caminho_configuracoes = os.path.join(diretorio_script, 'configuracoes.ini')

    # Lê as configurações do arquivo configuracoes.ini
    configuracoes = ConfigParser()
    configuracoes.read(caminho_configuracoes)

    # Verifica se o valor para espaco_livre_esperado_gb está presente no arquivo configuracoes.ini
    if 'configuracoes' not in configuracoes or 'espaco_livre_esperado_gb' not in configuracoes['configuracoes']:
        exibir_notificacao(
            'Erro de Configuração',
            'O arquivo configuracoes.ini não contém a configuração "espaco_livre_esperado_gb".'
        )
        sys.exit(1)

    # Obtém o valor de espaco_livre_esperado_gb do arquivo de configuração
    espaco_livre_esperado_gb_str = configuracoes['configuracoes']['espaco_livre_esperado_gb']

    # Verifica se o valor espaco_livre_esperado_gb não está vazio
    if not espaco_livre_esperado_gb_str.strip():
        exibir_notificacao(
            'Erro de Configuração',
            'O valor de "espaco_livre_esperado_gb" no arquivo configuracoes.ini está vazio.'
        )
        sys.exit(1)

    try:
        espaco_livre_esperado_gb = int(espaco_livre_esperado_gb_str)
    except ValueError:
        exibir_notificacao(
            'Erro de Configuração',
            'O valor de "espaco_livre_esperado_gb" no arquivo configuracoes.ini não é um número inteiro válido.'
        )
        sys.exit(1)

    # Obtém o uso de disco da partição principal
    disco = psutil.disk_usage('/')

    # Converte o espaço livre de bytes para gigabytes
    espaco_livre_gb = disco.free / (1024 ** 3)

    # Formata o espaço livre com duas casas decimais
    espaco_livre_gb_formatado = f'{espaco_livre_gb:.2f}'

    # Verifica se o espaço livre é menor que esperado
    if espaco_livre_gb < espaco_livre_esperado_gb:
        exibir_notificacao(
            'Atenção: Espaço Insuficiente',
            f'Atenção: O espaço livre no HD é de apenas {espaco_livre_gb_formatado} GB, o que é menor que {espaco_livre_esperado_gb} GB (esperado).'
        )
    else:
        exibir_notificacao(
            'Espaço Livre Suficiente',
            f'O espaço livre no HD é de {espaco_livre_gb_formatado} GB, o que é suficiente.'
        )

if __name__ == '__main__':
    # Agendamento da tarefa para ser executada a cada 1 minuto
    schedule.every(1).minutes.do(verificar_espaco_disco)

    # Loop para executar as tarefas agendadas
    while True:
        schedule.run_pending()
        time.sleep(1)