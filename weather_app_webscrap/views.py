from django.shortcuts import render
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup

# Create your views here.

def get_htmlpage(city):
    
    # We use this code so that google will think us as browser...
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    city = city.replace(' ','+')
    html_page= session.get(f"https://www.google.com/search?q=weather+{city}").text
    
    return html_page



def index(request):
    
    weather = None
    
    if 'city' in request.GET:
        city = request.GET.get('city')
        html_page = get_htmlpage(city)
        soup = BeautifulSoup(html_page, 'html.parser')
        weather = dict()
        weather['region'] = soup.find('div', attrs={'id':'wob_loc'}).text
        weather['daytime'] = soup.find('div', attrs={'id':'wob_dts'}).text
        weather['sky'] = soup.find('span', attrs={'id':'wob_dc'}).text
        weather['temp'] = soup.find('span', attrs={'id':'wob_tm'}).text

    return render(request,'core/index.html',{'weather':weather})
