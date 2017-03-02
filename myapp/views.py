from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting
import json
import requests as rq
from  twitter import *
from requests import Timeout
from requests.exceptions import ReadTimeout

# Create your views here.
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html')


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

def get_google(q,timeout):
    try:
        di = {}
        url = "https://www.googleapis.com/customsearch/v1?key=xxxxxxxxxxxxxxxxxxxxxxxxxxxxx:xxxxxxe&q="+q
        response = rq.get(url,headers=headers,timeout=timeout)
        di['url'] = response.url
        di['text'] = response.text
        return di
    except Timeout as e:
        return {'google' : 'Timed out after {0}seconds'.format(str(timeout))}
    except Exception as e:
        return {'google' : 'No results fetched'}


def get_duckduckgo(q,timeout):
    try:
        di = {}
        url = "http://api.duckduckgo.com/?q={0}&format=json".format(q)
        response = rq.get(url,headers=headers,timeout=timeout)
        di['url'] = response.url
        di['text'] = response.text
        return di
    except Timeout as e:
        return {'duckduckgo' : 'Timed out after {0}seconds'.format(str(timeout))}
    except Exception as e:
        return {'duckduckgo' : 'No results fetched'}


def get_twitter(q,timeout):
    try:
        di = {}
        api = Api(consumer_key='xxxxxx', consumer_secret='xxxxxxx', access_token_key='xxxxxxx', access_token_secret='xxxxx',timeout=timeout)
        results = api.GetSearch(raw_query="q={0}%20&result_type=recent&since=2014-07-19&count=1".format(q))
        if len(results) >= 1:
            di['url'] = results[0].source
            if len(results) >= 1:
                if len(results[0].urls) >= 1:
                    di['url'] = results[0].urls[0].url 
                di['text'] = results[0].text
            return di 
        else:
            return {'twitter' : 'No results fetched from the API'}
    except ReadTimeout as e:
        return {'twitter' : 'Timed out after {0}seconds'.format(str(timeout))}
    except Exception as e:
        return {'twitter' : 'No results fetched'}

def getdata(request):
    try:
        search_q = request.GET['search']
        timeout = 0.3
        if 'timeout' in request.GET:
            timeout = float(request.GET['timeout'])
        response = {'query' : search_q,'results' : {'google': {},'duckduckgo':{},'twitter':{}}}
        response['results'].update({'google' : get_google(search_q,timeout)})
        response['results'].update({'duckduckgo' : get_duckduckgo(search_q,timeout)})
        response['results'].update({'twitter' : get_twitter(search_q,timeout)})
        return render(request, "index.html", {'json_response': json.dumps(response)})
    except Exception as e:
        return render(request,"index.html",{'error': 'Error while processing data'})
