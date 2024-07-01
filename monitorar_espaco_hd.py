import psutil
from configparser import ConfigParser
import os
import sys
from winotify import Notification
import logging

# Obtém o diretório do script atual
diretorio_script = os.path.dirname(__file__)

# Caminho completo para o arquivo de log
caminho_arquivo_log = os.path.join(diretorio_script, 'espaco_disco.log')

# Configuração do logger
logging.basicConfig(
    filename=caminho_arquivo_log,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%d/%m/%Y %H:%M:%S',
    encoding='utf-8'
)

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
        mensagem_erro = 'O arquivo configuracoes.ini não contém a configuração "espaco_livre_esperado_gb".'
        exibir_notificacao('Erro de Configuração', mensagem_erro)
        logging.error(mensagem_erro)
        sys.exit(1)

    # Obtém o valor de espaco_livre_esperado_gb do arquivo de configuração
    espaco_livre_esperado_gb_str = configuracoes['configuracoes']['espaco_livre_esperado_gb']

    # Verifica se o valor espaco_livre_esperado_gb não está vazio
    if not espaco_livre_esperado_gb_str.strip():
        mensagem_erro = 'O valor de "espaco_livre_esperado_gb" no arquivo configuracoes.ini está vazio.'
        exibir_notificacao('Erro de Configuração', mensagem_erro)
        logging.error(mensagem_erro)
        sys.exit(1)

    try:
        espaco_livre_esperado_gb = int(espaco_livre_esperado_gb_str)
    except ValueError:
        mensagem_erro = 'O valor de "espaco_livre_esperado_gb" no arquivo configuracoes.ini não é um número inteiro válido.'
        exibir_notificacao('Erro de Configuração', mensagem_erro)
        logging.error(mensagem_erro)
        sys.exit(1)

    # Verifica se a chave "particoes" está presente no arquivo configuracoes.ini e não está vazia
    if 'configuracoes' not in configuracoes or 'particoes' not in configuracoes['configuracoes'] or not configuracoes['configuracoes']['particoes'].strip():
        mensagem_erro = 'O arquivo configuracoes.ini não contém a configuração válida para "particoes".'
        exibir_notificacao('Erro de Configuração', mensagem_erro)
        logging.error(mensagem_erro)
        sys.exit(1)

    # Obtém a lista de partições a serem monitoradas
    particoes = configuracoes['configuracoes']['particoes'].split(',')

    # Remove espaços em branco ao redor das letras das unidades
    particoes = [particao.strip() for particao in particoes]

    # Itera sobre as partições e verifica o espaço livre
    for particao in particoes:
        if len(particao) == 1 and particao.isalpha():
            try:
                # Obtém o uso de disco da partição principal
                disco = psutil.disk_usage(f'{particao.upper()}:\\')

                # Converte o espaço livre de bytes para gigabytes
                espaco_livre_gb = disco.free / (1024 ** 3)

                # Formata o espaço livre com duas casas decimais
                espaco_livre_gb_formatado = f'{espaco_livre_gb:.2f}'

                # Verifica se o espaço livre é menor que esperado
                if espaco_livre_gb < espaco_livre_esperado_gb:
                    mensagem_alerta = f'Atenção: O espaço livre no HD é de apenas {espaco_livre_gb_formatado} GB, o que é menor que {espaco_livre_esperado_gb} GB (esperado).'
                    exibir_notificacao('Atenção: Espaço Insuficiente', mensagem_alerta)
                    logging.warning(mensagem_alerta)
                else:
                    mensagem_info = f'O espaço livre no HD é de {espaco_livre_gb_formatado} GB, o que é suficiente.'
                    exibir_notificacao('Espaço Livre Suficiente', mensagem_info)
                    logging.info(mensagem_info)
            except FileNotFoundError:
                mensagem_erro = f'A partição "{particao.upper()}:" especificada no arquivo configuracoes.ini não existe.'
                exibir_notificacao('Erro de Configuração', mensagem_erro)
                logging.error(mensagem_erro)
        else:
            mensagem_erro = f'A partição "{particao}" especificada no arquivo configuracoes.ini não é válida. Use apenas letras para representar unidades de disco.'
            exibir_notificacao('Erro de Configuração', mensagem_erro)
            logging.error(mensagem_erro)

if __name__ == '__main__':
    verificar_espaco_disco()