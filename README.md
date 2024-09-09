# TesteSeleção
Script de Python conforme pedido no teste

# Possíveis dependências a serem instaldas:

- **requests**: Para fazer a requisição HTTP.
  ```bash
  pip install requests
  ```
- **BeautifulSoup** (parte do pacote `bs4`): Para fazer o parsing do HTML.
  ```bash
  pip install beautifulsoup4
  ```

# Sobre a solução:

## Código 1 - API - Alpha Vantage

Este código Python busca dados de ações da API **Alpha Vantage**, que fornece informações financeiras em tempo real, e salva esses dados em um arquivo CSV. Ele lida com erros de forma robusta e realiza uma requisição HTTP para obter informações sobre o preço das ações de uma empresa, organizando-as e exportando para um arquivo CSV.

### Imports e Configuração Inicial
```python
import requests
import csv
import sys
```
Esses módulos são importados:
- **requests**: usado para fazer requisições HTTP à API da Alpha Vantage.
- **csv**: para trabalhar com arquivos CSV.
- **sys**: usado para imprimir mensagens de erro no fluxo de erro padrão (stderr).

```python
api_key = 'AVM953YNH0G3XPZG'  # Chave de API fornecida
symbol = 'AAPL'  # Símbolo da ação que deseja consultar
interval = '5min'  # Intervalo dos dados (ex: '1min', '5min', '15min', '30min', '60min')
```
Aqui, a chave da API, o símbolo da ação (neste caso, da Apple "AAPL") e o intervalo dos dados (de 5 minutos) são configurados. Esses valores são usados para fazer a requisição à API.

### Função `fetch_stock_data`
Esta função faz a requisição à API, processa os dados retornados e os salva em um arquivo CSV. Vamos por partes:

```python
def fetch_stock_data(symbol, interval='5min', append=False, outputsize='compact'):
```
A função tem quatro parâmetros:
- **symbol**: símbolo da ação (ex: AAPL para Apple).
- **interval**: intervalo de tempo entre os dados (ex: 5min, 15min, etc.).
- **append**: se `True`, os dados são adicionados ao final de um arquivo CSV existente; caso contrário, um novo arquivo é criado.
- **outputsize**: pode ser `'compact'` (últimos 100 pontos de dados) ou `'full'` (dados completos).

### Requisição à API e Tratamento de Resposta
```python
params = {
    'function': 'TIME_SERIES_INTRADAY',
    'symbol': symbol,
    'interval': interval,
    'apikey': api_key,
    'outputsize': outputsize
}
```
Aqui, os parâmetros da requisição são configurados, que incluem a função de consulta (`TIME_SERIES_INTRADAY`), o símbolo da ação, o intervalo, a chave da API e o tamanho dos dados de retorno.

```python
response = requests.get(api_url, params=params)
response.raise_for_status()
```
O código faz a requisição HTTP usando o método `get` do `requests`. A função `raise_for_status` verifica se houve algum erro na requisição (como problemas de conexão ou limite da API).

### Tratamento de Erros de Resposta
```python
if 'Error Message' in data:
    raise Exception(f"Erro na API: {data['Error Message']}")
if 'Note' in data:
    raise Exception(f"Nota da API: {data['Note']}")
```
A função verifica se há mensagens de erro na resposta. Se a API retornar uma mensagem de erro ou aviso, ele lança uma exceção.

### Processamento dos Dados da API
```python
time_series_key = f'Time Series ({interval})'

if time_series_key not in data:
    raise KeyError(f"Dados de '{time_series_key}' não encontrados na resposta da API")
```
A função tenta acessar os dados de preços de acordo com o intervalo especificado (ex: `'Time Series (5min)'`). Se essa chave não estiver presente, a função lança um erro.

```python
latest_time = list(data[time_series_key].keys())[0]
latest_data = data[time_series_key][latest_time]
price_open = latest_data['1. open']
price_high = latest_data['2. high']
price_low = latest_data['3. low']
price_close = latest_data['4. close']
volume = latest_data['5. volume']
```
Aqui, o código obtém o horário mais recente (`latest_time`) e os dados de abertura, máximo, mínimo, fechamento e volume das ações para esse momento específico.

### Salvando os Dados em CSV
```python
mode = 'a' if append else 'w'
with open('stock_data_api.csv', mode, newline='') as file:
    writer = csv.writer(file)
    if not append:
        writer.writerow(['Ação', 'Horário', 'Preço de Abertura', 'Preço Máximo', 'Preço Mínimo', 'Preço de Fechamento', 'Volume'])  # Cabeçalhos
    writer.writerows(stock_data)
```
Os dados processados são então gravados em um arquivo CSV. Se o parâmetro `append` for `True`, o arquivo será aberto em modo de adição (`a`); caso contrário, será sobrescrito (`w`). O cabeçalho (nomes das colunas) é adicionado apenas se o arquivo for novo.

### Tratamento de Exceções
```python
except requests.exceptions.RequestException as e:
    print(f"Erro na requisição: {e}", file=sys.stderr)
except KeyError as e:
    print(f"Erro ao processar os dados da API: {e}", file=sys.stderr)
except Exception as e:
    print(f"Ocorreu um erro inesperado: {e}", file=sys.stderr)
```
Esses blocos tratam possíveis exceções, como erros de requisição HTTP, erros ao acessar os dados ou qualquer outro erro inesperado. Todas as mensagens de erro são direcionadas ao fluxo de erro padrão (stderr).

### Exemplo de Uso
```python
fetch_stock_data(symbol='AAPL', interval='5min', append=False)
```
Este exemplo chama a função para buscar dados da ação da Apple no intervalo de 5 minutos e grava no arquivo CSV.

### Resumo Final
O código busca dados de ações em intervalos de tempo curtos (como 5 minutos) da API da Alpha Vantage, processa e salva em um arquivo CSV, lidando com erros comuns de API e rede.

## Código 2 - Web Scraping - Google Finance

Este código faz **web scraping** na página do **Google Finance** para obter informações sobre a ação da Apple (AAPL) e grava essas informações em um arquivo CSV. Ele usa as bibliotecas **requests** para fazer a requisição HTTP e **BeautifulSoup** para analisar e extrair dados do HTML da página.

### Explicação detalhada do código

#### Imports e configuração
```python
import requests
from bs4 import BeautifulSoup
import csv
import sys
```
- **requests**: Faz requisições HTTP para baixar o conteúdo da página web.
- **BeautifulSoup**: Usada para fazer o parsing do HTML e extrair os dados de interesse.
- **csv**: Para salvar os dados extraídos em um arquivo CSV.
- **sys**: Para sair do programa e lidar com erros.

#### URL da página e cabeçalho do User-Agent
```python
url = 'https://www.google.com/finance/quote/AAPL:NASDAQ'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
```
Aqui é especificada a URL da página do Google Finance que contém os dados da ação da Apple. O **User-Agent** é definido no cabeçalho para simular que a requisição está sendo feita por um navegador, evitando bloqueios comuns durante o web scraping.

#### Requisição HTTP à página
```python
try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Verificar se houve erro na requisição HTTP
except requests.exceptions.RequestException as e:
    print(f"Erro ao fazer a requisição: {e}")
    sys.exit(1)
```
Este bloco de código faz a requisição HTTP à página da Apple no Google Finance. Se houver algum erro durante a requisição (como a página não estar acessível), o programa imprime uma mensagem de erro e encerra a execução com `sys.exit(1)`.

#### Parsing do HTML
```python
soup = BeautifulSoup(response.text, 'html.parser')
```
Aqui, o código converte o conteúdo HTML retornado pela requisição em um objeto **BeautifulSoup**, que facilita a navegação e extração de informações específicas dentro do HTML.

#### Extração do preço atual da ação
```python
price_element = soup.find('div', {'class': 'YMlKec fxKbKc'})
if price_element:
    price = price_element.text.strip()
else:
    price = "N/A"
```
O código usa `soup.find` para procurar um elemento HTML `div` que contém a classe `'YMlKec fxKbKc'`, onde o Google Finance exibe o preço atual da ação. Se o elemento for encontrado, o preço é extraído; caso contrário, o valor "N/A" é atribuído.

#### Extração de outros dados: Preço de Fechamento Anterior, Preço de Abertura, Máximos e Mínimos, Volume
O código usa a mesma estratégia para extrair outros dados da página, procurando por elementos específicos no HTML, baseados no texto e classes CSS. Vamos a cada bloco:

##### Preço de Fechamento Anterior
```python
try:
    prev_close_element = soup.find('div', string='Previous close').find_next('div', {'class': 'P6K39c'})
    prev_close = prev_close_element.text.strip() if prev_close_element else "N/A"
except:
    prev_close = "N/A"
```
Aqui, o código procura pela string `'Previous close'` no HTML e depois pega o próximo `div` que contém o valor do preço de fechamento anterior.

##### Preço de Abertura
```python
try:
    open_element = soup.find('div', string='Open').find_next('div', {'class': 'P6K39c'})
    open_price = open_element.text.strip() if open_element else "N/A"
except:
    open_price = "N/A"
```
De forma similar, o código encontra o preço de abertura a partir do texto `'Open'` e pega o próximo `div` correspondente.

##### Máximo e Mínimo do Dia
```python
try:
    high_low_element = soup.find('div', string='Day range').find_next('div', {'class': 'P6K39c'})
    high_low = high_low_element.text.strip() if high_low_element else "N/A"
    high_price, low_price = high_low.split(' - ') if high_low != "N/A" else ("N/A", "N/A")
except:
    high_price, low_price = "N/A", "N/A"
```
Aqui, o código encontra a faixa de preço do dia, que é exibida como "máximo - mínimo". Ele faz o parsing do valor encontrado, dividindo o texto pelo caractere " - ".

##### Volume
```python
try:
    volume_element = soup.find('div', string='Volume').find_next('div', {'class': 'P6K39c'})
    volume = volume_element.text.strip() if volume_element else "N/A"
except:
    volume = "N/A"
```
Da mesma forma, o volume de negociação é extraído a partir da string `'Volume'` e o próximo `div` com a classe `'P6K39c'`.

#### Organização dos Dados
```python
stock_data = [['AAPL', price, open_price, high_price, low_price, prev_close, volume]]
```
Os dados extraídos são organizados em uma lista de listas, com os seguintes valores:
- **'AAPL'**: símbolo da ação.
- **price**: preço atual.
- **open_price**: preço de abertura.
- **high_price**: preço máximo do dia.
- **low_price**: preço mínimo do dia.
- **prev_close**: preço de fechamento do dia anterior.
- **volume**: volume de negociação.

#### Salvando os Dados em um Arquivo CSV
```python
with open('stock_data_google_finance.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Ação', 'Preço Atual', 'Preço de Abertura', 'Preço Máximo', 'Preço Mínimo', 'Preço de Fechamento', 'Volume'])
    writer.writerows(stock_data)
```
Aqui, o código abre/cria um arquivo CSV chamado `stock_data_google_finance.csv` e grava os dados nele. O cabeçalho é escrito primeiro (nome das colunas) e, em seguida, os dados extraídos.

#### Exibindo Sucesso
```python
print("Dados de web scraping salvos com sucesso!")
```
Depois de salvar os dados, o código imprime uma mensagem confirmando que o web scraping foi concluído e os dados foram gravados com sucesso.

### Resumo
O código faz web scraping na página do Google Finance, extraindo informações importantes sobre a ação da Apple, como preço atual, preço de abertura, máximos e mínimos do dia, e volume de negociação, e salva essas informações em um arquivo CSV.


