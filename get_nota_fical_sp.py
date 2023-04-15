
import os
from dotenv import load_dotenv
load_dotenv()
import requests, re, time


session = requests.session()

headers = {
    "Host": "satsp.fazenda.sp.gov.br",
    "Connection": "keep-alive",
    "sec-ch-ua": "\"Not?A_Brand\";v=\"8\", \"Chromium\";v=\"108\", \"Google Chrome\";v=\"108\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "DNT": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "pt-PT,pt;q=0.9,en-US;q=0.8,en;q=0.7",
}

response_init = session.get(
    url='https://satsp.fazenda.sp.gov.br/COMSAT/Public/ConsultaPublica/ConsultaPublicaCfe.aspx',
    headers=headers, verify=False
)

with open('out_init.html', 'wb') as arq:
    arq.write(response_init.content)


# INICIO captura o g-response
google_key = re.search(r'reCaptchaSiteKey\s*=\s*\'(?P<value>[^\'\"]+)', response_init.text, flags=re.DOTALL|re.IGNORECASE).group('value')

response_init_2captcha = requests.get(
    url=f'http://2captcha.com/in.php?key={os.environ["key_2capcha"]}&method=userrecaptcha&googlekey={google_key}&json=1&pageurl=https://satsp.fazenda.sp.gov.br/COMSAT/Public/ConsultaPublica/ConsultaPublicaCfe.aspx'
)

id_captcha = response_init_2captcha.json().get('request')

time.sleep(21)

response_g_captcha = requests.get(
    url=f'http://2captcha.com/res.php?key={os.environ["key_2capcha"]}&action=get&id={id_captcha}'
)

g_response = response_g_captcha.text.replace('OK|', '')
print('G RESPONSE')
print(g_response)

# FIM CAPTCHA

#regex

VIEWSTATEGENERATOR = re.search(r'id=\"__VIEWSTATEGENERATOR\"\s+value=\"(?P<value>[^\"]+)', response_init.text, flags=re.DOTALL|re.IGNORECASE).group('value')
SCROLLPOSITIONX = re.search(r'id=\"__SCROLLPOSITIONX\"\s+value=\"(?P<value>[^\"]+)', response_init.text, flags=re.DOTALL|re.IGNORECASE).group('value')
SCROLLPOSITIONY = re.search(r'id=\"__SCROLLPOSITIONY\"\s+value=\"(?P<value>[^\"]+)', response_init.text, flags=re.DOTALL|re.IGNORECASE).group('value')
EVENTVALIDATION = re.search(r'id=\"__EVENTVALIDATION\"\s+value=\"(?P<value>[^\"]+)', response_init.text, flags=re.DOTALL|re.IGNORECASE).group('value')
VIEWSTATE = re.search(r'id=\"__VIEWSTATE\"\s+value=\"(?P<value>[^\"]+)', response_init.text, flags=re.DOTALL|re.IGNORECASE).group('value')

data_nota = {
    "ToolkitScriptManager1_HiddenField": "",
    "__EVENTARGUMENT": "",
    "__EVENTTARGET": "",
    "__SCROLLPOSITIONY": SCROLLPOSITIONY,
    "__SCROLLPOSITIONX": SCROLLPOSITIONX,
    "g-recaptcha-response": g_response,
    "ctl00$conteudo$txtChaveAcesso": "3522 1150 0289 7600 2607 5900 1223 5670 0318 8446 8221",
    "ctl00$conteudo$btnConsultar": "Consultar",
    "__VIEWSTATEGENERATOR": VIEWSTATEGENERATOR,
    "__EVENTVALIDATION": EVENTVALIDATION,
    "__VIEWSTATE": VIEWSTATE,
}

headers_nota = {
    "Host": "satsp.fazenda.sp.gov.br",
    "Connection": "keep-alive",
    "Content-Length": "1301",
    "Cache-Control": "max-age=0",
    "sec-ch-ua": "\"Not?A_Brand\";v=\"8\", \"Chromium\";v=\"108\", \"Google Chrome\";v=\"108\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "Origin": "https://satsp.fazenda.sp.gov.br",
    "DNT": "1",
    "Upgrade-Insecure-Requests": "1",
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Referer": "https://satsp.fazenda.sp.gov.br/COMSAT/Public/ConsultaPublica/ConsultaPublicaCfe.aspx",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "pt-PT,pt;q=0.9,en-US;q=0.8,en;q=0.7"
}


url_nota = 'https://satsp.fazenda.sp.gov.br/COMSAT/Public/ConsultaPublica/ConsultaPublicaCfe.aspx'


response_nota = session.post(
    url=url_nota, headers=headers_nota, data=data_nota, verify=False
)


with open('out_nota.html', 'wb') as arq:
    arq.write(response_nota.content)


print('LEASING SPRAY TB MAK' in response_nota.text)