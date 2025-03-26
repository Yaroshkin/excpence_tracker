from bs4 import BeautifulSoup
import requests

def get_usd_exchange_rate():
    url = "https://minfin.com.ua/currency/nbu/usd/"
    response = requests.get(url)
    
    if response.status_code != 200:
        raise ValueError(f"Ошибка при запросе курса: {response.status_code}")
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    rate_tag = soup.find("div", class_="sc-1x32wa2-9 fevpFL")

    if rate_tag:
        rate_text = rate_tag.text.strip()
        
        rate = rate_text.replace(",", ".")
        
        rate_parts = rate.split(".")
        if len(rate_parts) > 1:
            rate = f"{rate_parts[0]}.{rate_parts[1][:2]}"
        else:
            rate = f"{rate_parts[0]}.00"
        
        try:
            return float(rate)
        except ValueError:
            raise ValueError(f"Невозможно преобразовать курс в число: {rate}")
    else:
        raise ValueError("Не удалось найти курс USD на странице.")

try:
    usd_rate = get_usd_exchange_rate()
except Exception as e:
    print(f"Ошибка: {e}")
