import sys
import json
import string

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2]) #.readlines()

    scores = {} # initialize an empty dictionary
    newterms = {}  ## new term scores dict
    for line in sent_file:
         term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
         scores[term] = int(score)  # Convert the score to an integer.

    for line in tweet_file:
	json_tweet=json.loads(line)
	sentiment=0
	terms = json_tweet.get("text","").encode('utf-8').translate(None,string.punctuation).lower().split()
	for term in terms:
            sentiment=sentiment+scores.get(term,0)
        for term in terms:
            if scores.get(term,0)==0:
                newterms[term]=newterms.get(term,0)+sentiment

    for term, value in newterms.items():
        print "%s %s" % (term,value)

if __name__ == '__main__':
    main()
