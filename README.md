# Monitoramento de Espaço em Disco

Este é um script em Python para monitorar o espaço livre no disco e exibir notificações no Windows quando o espaço livre estiver abaixo do esperado.

## Funcionalidades

- Verificação contínua do espaço livre no disco.
- Notificações no sistema operacional (Windows) quando o espaço livre é insuficiente.
- Agendamento automático da verificação do espaço em disco a cada minuto utilizando a biblioteca `schedule`.

## Requisitos

- Python 3.x
- Bibliotecas Python necessárias: `psutil`, `configparser`, `winotify`, `schedule`

## Instalação

1. Clone o repositório:
```
git clone https://github.com/luizelias8/monitorar-espaco-hd.git
cd monitorar-espaco-hd
```

2. Instale os requisitos necessários:
```
pip install -r requirements.txt
```

3. Configuração do Arquivo de Preferências:
- Renomeie o arquivo `configuracoes-exemplo.ini` para `configuracoes.ini`.
- Edite `configuracoes.ini` e defina `espaco_livre_esperado_gb` com o valor desejado em gigabytes.

## Uso

Execute o script `monitorar_espaco_hd.py`. O script iniciará a monitoração contínua do espaço em disco e exibirá notificações conforme configurado.

## Contribuição

Contribuições são bem-vindas!

## Autor

[Luiz Elias](https://github.com/luizelias8)