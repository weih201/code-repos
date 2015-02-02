import sys
import json
import string

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2]) #.readlines()

    scores = {} # initialize an empty dictionary
    for line in sent_file:
         term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
         scores[term] = int(score)  # Convert the score to an integer.

    for line in tweet_file:
	json_tweet=json.loads(line)
	sentiment=0
	for term in json_tweet.get("text","").encode('utf-8').translate(None,string.punctuation).lower().split():
            sentiment=sentiment+scores.get(term,0)
        print sentiment

if __name__ == '__main__':
    main()
