# Script: live.py

## Descrição
Este script Python é utilizado para obter eventos esportivos ao vivo de uma API, combiná-los com dados de placar e formatar essas informações para exibição. Ele também monitora atualizações de placares em intervalos regulares e registra quaisquer mudanças significativas.

## Funcionalidades
- **get_live_events()**: Faz uma requisição para a API de eventos esportivos ao vivo e retorna os dados recebidos.
- **cross_reference_events(events)**: Combina os dados de odds e placares dos eventos.
- **format_live_events(combined_events)**: Formata os dados combinados de eventos em uma string legível.
- **check_for_score_updates(interval=30)**: Monitora atualizações de placar em intervalos regulares (padrão de 30 segundos) e exibe as mudanças.

## Estrutura
- **Imports**:
  - `http.client`: Para fazer requisições HTTP.
  - `json`: Para manipulação de dados em JSON.
  - `time`: Para controlar os intervalos de monitoramento.
  - `logging`: Para registrar informações e erros.

- **Configuração do Logger**:
  - Configuração básica do logger para registrar informações em nível INFO com um formato específico de data e mensagem.

- **Funções Principais**:
  - `get_live_events()`: Envia uma requisição GET para a API e retorna os dados dos eventos esportivos ao vivo.
  - `cross_reference_events(events)`: Combina os dados de odds e placares dos eventos.
  - `format_live_events(combined_events)`: Formata os dados combinados de eventos em uma string legível.
  - `check_for_score_updates(interval=30)`: Monitora atualizações de placar em intervalos regulares e exibe as mudanças.

- **Execução Principal**:
  - A função `check_for_score_updates()` é chamada se o script for executado diretamente, iniciando o processo de monitoramento de eventos ao vivo.

## Utilização
1. **Executar o Script**:
   - Para iniciar o monitoramento de eventos ao vivo e exibição de dados formatados, execute o script diretamente:
     ```sh
     python live.py
     ```

2. **Monitoramento de Atualizações**:
   - O script fará requisições à API em intervalos regulares (padrão de 30 segundos) e exibirá atualizações de placar conforme necessário.

## Observações
- **Requisitos**:
  - Conexão com a internet para acessar a API.
  - Biblioteca padrão do Python (http.client, json, time, logging).

- **Erros e Exceções**:
  - O script está preparado para registrar erros e exceções que ocorram durante as requisições à API.

## Exemplo de Saída
Quando o script é executado, ele exibe informações dos eventos ao vivo formatadas como:
