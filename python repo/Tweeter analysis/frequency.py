import sys
import json
import string

def main():
    tweet_file = open(sys.argv[1]) 

    termsfreq = {}  ## new term scores dict
    totalfreq=0
    
    for line in tweet_file:
	json_tweet=json.loads(line)
	terms = json_tweet.get("text","").encode('utf-8').translate(None,string.punctuation).lower().split()

	for term in terms:
            termsfreq[term]=termsfreq.get(term,0)+1
            totalfreq=totalfreq+1
            
    for term in termsfreq.keys():
        termsfreq[term] = float(termsfreq.get(term,0))/float(totalfreq)

    for term, value in termsfreq.items():
        print "%s %s" % (term,value)

if __name__ == '__main__':
    main()
