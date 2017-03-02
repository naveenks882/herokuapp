from  twitter import *
from requests.exceptions import ReadTimeout


try:
    api = Api(consumer_key='xxxxx', consumer_secret='xxxxxx', access_token_key='xxxxxx', access_token_secret='xxxxxx',timeout=0.300)
    print(api.VerifyCredentials())
    results = api.GetSearch(raw_query="q=twitter%20&result_type=recent&since=2014-07-19&count=2")
    print results
except ReadTimeout as e:
    print "Timeout"
