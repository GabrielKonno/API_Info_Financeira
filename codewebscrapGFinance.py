import requests
from bs4 import BeautifulSoup
import csv
import sys

# URL da página da Apple no Google Finance
url = 'https://www.google.com/finance/quote/AAPL:NASDAQ'

# Definir cabeçalho User-Agent para evitar bloqueio
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

try:
    # Fazer a requisição HTTP à página
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Verificar se houve erro na requisição HTTP
except requests.exceptions.RequestException as e:
    print(f"Erro ao fazer a requisição: {e}")
    sys.exit(1)

# Fazer o parsing do HTML
soup = BeautifulSoup(response.text, 'html.parser')

# Localizar o preço atual da ação
price_element = soup.find('div', {'class': 'YMlKec fxKbKc'})
if price_element:
    price = price_element.text.strip()
else:
    price = "N/A"

# Localizar outros dados (como preço de abertura, fechamento, volume, etc.)
try:
    prev_close_element = soup.find('div', string='Previous close').find_next('div', {'class': 'P6K39c'})
    prev_close = prev_close_element.text.strip() if prev_close_element else "N/A"
except:
    prev_close = "N/A"

try:
    open_element = soup.find('div', string='Open').find_next('div', {'class': 'P6K39c'})
    open_price = open_element.text.strip() if open_element else "N/A"
except:
    open_price = "N/A"

try:
    high_low_element = soup.find('div', string='Day range').find_next('div', {'class': 'P6K39c'})
    high_low = high_low_element.text.strip() if high_low_element else "N/A"
    high_price, low_price = high_low.split(' - ') if high_low != "N/A" else ("N/A", "N/A")
except:
    high_price, low_price = "N/A", "N/A"

try:
    volume_element = soup.find('div', string='Volume').find_next('div', {'class': 'P6K39c'})
    volume = volume_element.text.strip() if volume_element else "N/A"
except:
    volume = "N/A"

# Organizar os dados
stock_data = [['AAPL', price, open_price, high_price, low_price, prev_close, volume]]

# Salvar os dados em um arquivo CSV
with open('stock_data_google_finance.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Ação', 'Preço Atual', 'Preço de Abertura', 'Preço Máximo', 'Preço Mínimo', 'Preço de Fechamento', 'Volume'])
    writer.writerows(stock_data)

print("Dados de web scraping salvos com sucesso!")
