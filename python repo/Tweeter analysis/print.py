import oauth2 as oauth
import urllib2 as urllib
import json

# See assignment1.html instructions or README for how to get these credentials

api_key = "0tivEQNNfuDkc565tz2qVhUJJ"
api_secret = "cIXRSaARfONekEZhhhmSVlqzB518zq1DYoswTgKmPcC2ftQJNQ"
access_token_key = "2497475094-aHU5SG74UtbQFQpQFe0ffGKe2doMIaDzQJVmxAb"
access_token_secret = "AyAnEjZUpSDF85X2Yy6XsobJjoBw2vC5JofxVyhRn5a1t"

_debug = 0

oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=api_key, secret=api_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"


http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)

'''
Construct, sign, and open a twitter request
using the hard-coded credentials above.
'''
def twitterreq(url, method, parameters):
  req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                             token=oauth_token,
                                             http_method=http_method,
                                             http_url=url, 
                                             parameters=parameters)

  req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

  headers = req.to_header()

  if http_method == "POST":
    encoded_post_data = req.to_postdata()
  else:
    encoded_post_data = None
    url = req.to_url()

  opener = urllib.OpenerDirector()
  opener.add_handler(http_handler)
  opener.add_handler(https_handler)

  response = opener.open(url, encoded_post_data)

  return response

def fetchsamples():
  url = "https://api.twitter.com/1.1/search/tweets.json?q=microsoft"
  parameters = []
  response = twitterreq(url, "GET", parameters)
  
  # Get Tweets
  pyresponse = json.load(response)
  
  # Get Formatted Tweets (NOTE: For Display Purposes Only)
  #pyresponse = (json.dumps(json.load(response), indent=4, sort_keys=True))

  # Print Twitter stream
  print pyresponse

  # Find type of stream
  #print type(pyresponse)

  # Find stream keys
  #print pyresponse.keys()

  # Look at the "statuses" key
  #print pyresponse['statuses']

  # Find type of "statuses"
  #print type(pyresponse['statuses'])

  # Get Statuses
  #statuses = pyresponse['statuses']

  # Print first element in the "statuses" list
  #print statuses[0]

  # Find type of first element in the "statuses" list
  #print type(statuses[0])

  # Look at the keys of the first element in the "statuses" list
  #print statuses[0].keys()

  # Look at the "text" of the first Tweet
  #print statuses[0]['text']

  # Look at the "text" of the third Tweet
  #print statuses[3]['text']

  # Look at the "text" of ten Tweets
  #for i in range(10):
  #  print statuses[i]['text']

if __name__ == '__main__':
  fetchsamples()
