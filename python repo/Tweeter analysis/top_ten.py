import sys
import json

def main():
    tweet_file = open(sys.argv[1]) 
    tags = {} # initialize an empty tags dictionary

    for line in tweet_file:
	tweet=json.loads(line)
	entities = tweet.get("entities",{})
	if not (entities=={} or entities==None):
            hashtags = entities.get("hashtags",[])
            if not (hashtags==[] or hashtags==None):
                for tag in hashtags:
                    tags[tag["text"]]=tags.get(tag["text"],0.0)+1

    for tag,num in sorted(tags.items(),key=lambda (tag,num):num,reverse=True)[0:10]:
        print "%s %s" % (tag,num)
    
if __name__ == '__main__':
    main()


