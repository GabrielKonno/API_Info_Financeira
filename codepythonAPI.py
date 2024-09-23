import requests
import csv
import sys

# Sua chave de API da Alpha Vantage
api_key = 'AVM953YNH0G3XPZG'  # Chave de API fornecida
symbol = 'AAPL'  # Símbolo da ação que deseja consultar
interval = '5min'  # Intervalo dos dados (ex: '1min', '5min', '15min', '30min', '60min')

# Função para buscar dados de ações com tratamento de erros aprimorado
def fetch_stock_data(symbol, interval='5min', append=False, outputsize='compact'):
    api_url = 'https://www.alphavantage.co/query'
    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval': interval,
        'apikey': api_key,
        'outputsize': outputsize  # 'compact' (últimos 100 dados) ou 'full' (dados completos)
    }

    try:
        # Fazer a requisição à API
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # Verifica se houve erro na requisição HTTP
        data = response.json()

        # Verificar se há mensagens de erro na resposta
        if 'Error Message' in data:
            raise Exception(f"Erro na API: {data['Error Message']}")
        if 'Note' in data:
            raise Exception(f"Nota da API: {data['Note']}")

        # Chave esperada com base no intervalo
        time_series_key = f'Time Series ({interval})'

        # Verificar se a chave de dados está presente
        if time_series_key not in data:
            print("Resposta da API não contém a chave esperada.")
            print("Resposta completa da API para depuração:")
            print(data)  # Imprimir a resposta completa para entender o que está sendo retornado
            raise KeyError(f"Dados de '{time_series_key}' não encontrados na resposta da API")

        # Extrair os dados mais recentes
        latest_time = list(data[time_series_key].keys())[0]
        latest_data = data[time_series_key][latest_time]
        price_open = latest_data['1. open']
        price_high = latest_data['2. high']
        price_low = latest_data['3. low']
        price_close = latest_data['4. close']
        volume = latest_data['5. volume']

        # Organizar os dados
        stock_data = [[symbol, latest_time, price_open, price_high, price_low, price_close, volume]]

        # Salvar os dados em um arquivo CSV
        mode = 'a' if append else 'w'
        with open('stock_data_api.csv', mode, newline='') as file:
            writer = csv.writer(file)
            if not append:
                writer.writerow(['Ação', 'Horário', 'Preço de Abertura', 'Preço Máximo', 'Preço Mínimo', 'Preço de Fechamento', 'Volume'])  # Cabeçalhos
            writer.writerows(stock_data)

        print(f"Dados da ação {symbol} no intervalo '{interval}' salvos com sucesso!")

    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}", file=sys.stderr)
    except KeyError as e:
        print(f"Erro ao processar os dados da API: {e}", file=sys.stderr)
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}", file=sys.stderr)

# Exemplo de uso da função
fetch_stock_data(symbol='AAPL', interval='5min', append=False)
