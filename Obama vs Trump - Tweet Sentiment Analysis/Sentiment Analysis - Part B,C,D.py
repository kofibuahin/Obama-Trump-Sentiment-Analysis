# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 00:35:48 2018

@author: Kofi Buahin
"""

#Part B. Preliminary Analysis

import json
from collections import Counter
import nltk
import string
from textblob import TextBlob 
from wordcloud import WordCloud
import matplotlib.pyplot as plt

stopwords = nltk.corpus.stopwords.words('english')
stopwords.append('RT'), stopwords.append('https'), stopwords.append('``'), stopwords.append("'s"), stopwords.append("n't"), 
stopwords.append("amp"),stopwords.append("''"),stopwords.append("..."), stopwords.append("The"), stopwords.append("know"),
stopwords.append("like"), stopwords.append("We"),stopwords.append("This"),stopwords.append("It"), stopwords.append("He"),
stopwords.append("You"), stopwords.append("In"), stopwords.append("since"),stopwords.append("people"),stopwords.append("would"),
stopwords.append("says"), stopwords.append("r..."), stopwords.append("claim"), stopwords.append("netflix")

p = string.punctuation
chars = ['``',"''",'’']
for i in p:
    chars.append(i)
    
with open('tweet_stream_Obama_10000.json', 'r') as infile:
        storedtweets_Obama = json.load(infile)
obama_text = []
obama_text2 = ''
for item in storedtweets_Obama:
    obama_text.append(item['text'])
for tweet in obama_text:
    obama_text2 = obama_text2 + tweet + ' '
obama_words = nltk.word_tokenize(obama_text2)
for w in obama_words:
    if w in chars:
        obama_words.remove(w)
obamawords_freq = nltk.FreqDist(obama_words).most_common(10)
obama_words2 = []
for w in obama_words:
    if w not in stopwords and len(w) > 1:
        if w not in chars:
            obama_words2.append(w)
obamawords2_freq = nltk.FreqDist(obama_words2).most_common(30)

with open('tweet_stream_Trump_10000.json', 'r') as infile:
        storedtweets_Trump = json.load(infile)
trump_text = []
trump_text2 = ''
for item in storedtweets_Trump:
    trump_text.append(item['text'])
for tweet in trump_text:
    trump_text2 = trump_text2 + tweet + ' '
trump_words = nltk.word_tokenize(trump_text2)
for w in trump_words:
    if w in chars:
        trump_words.remove(w)
trumpwords_freq = nltk.FreqDist(trump_words).most_common(10)
trump_words2 = []
for w in trump_words:
    if w not in stopwords and len(w) > 1:
        if w not in chars: 
            trump_words2.append(w)
trumpwords2_freq = nltk.FreqDist(trump_words2).most_common(30)



def collect_text(filename):
    with open(filename, 'r') as infile:
        stored_tweets = json.load(infile)
    tweet_text = [] 
    for item in stored_tweets:
        tweet_text.append(item['text'])
    real_filename = filename
    with open('{}_tweet_text.json'.format(real_filename[13:-5]),'w') as f:
        json.dump(tweet_text, f, indent=4)
                                 
def frequent_mentions(tweet_list):
    mention_list = []
    for tweet in tweet_list:
        mentions = tweet['entities']['user_mentions']
        for ment in mentions:
            mention_list.append(ment['screen_name'])
    c = Counter(mention_list)
    freq_ments = c.most_common(10)
    return freq_ments

def frequent_hashtags(tweet_list):
    h_tags2 = []
    for tweet in tweet_list:
        h_tags = tweet['entities']['hashtags']
        for tag in h_tags:
                h_tags2.append(tag['text'])
    c = Counter(h_tags2)
    freq_hashtags = c.most_common(10)
    return freq_hashtags

def frequent_tweeters(tweet_list):
    user_list = []
    for tweet in tweet_list:
        tweeters = tweet['user']
        user_list.append(tweeters['screen_name'])
    c = Counter(user_list)
    freq_tweeters = c.most_common(1)
    return(freq_tweeters)
    
def influence_score(tweet_list):
    influence = []
    tweet_txt = []
    for tweet in tweet_list:
        tweet_txt.append(tweet['text'])
        quote = tweet['quote_count']
        reply = tweet['reply_count']  
        retweet = tweet['retweet_count']
        influence.append(quote + reply + retweet)
    print(influence)
    influence.sort(reverse=True)
    return influence[0:9]


trump_ans1 = trumpwords_freq
trump_ans105 = trumpwords2_freq
trump_ans2 = frequent_hashtags(storedtweets_Trump)
trump_ans3 = frequent_mentions(storedtweets_Trump)
trump_ans4 = frequent_tweeters(storedtweets_Trump)
trump_ans5 = influence_score(storedtweets_Trump)

obama_ans1 = obamawords_freq
obama_ans105 = obamawords2_freq
obama_ans2 = frequent_hashtags(storedtweets_Obama)
obama_ans3 = frequent_mentions(storedtweets_Obama)
obama_ans4 = frequent_tweeters(storedtweets_Obama)
obama_ans5 = influence_score(storedtweets_Obama)

#Part C. Wordcloud:

wordcloud_obama = WordCloud(max_font_size=40).generate(obama_words2)
plt.figure()
plt.imshow(wordcloud_obama)
plt.axis("off")
plt.show()

wordcloud_trump = WordCloud(max_font_size=40).generate(trump_words2)
plt.figure()
plt.imshow(wordcloud_trump)
plt.axis("off")
plt.show()

#Part D. Sentiment Analysis:
collect_text('tweet_stream_Obama_10000.json')
with open('Obama_10000_tweet_text.json', 'r') as infile:
        readtweets_obama = json.load(infile)
pol_obama = []
sub_obama = []
for tweet in readtweets_obama:
        tb_o = TextBlob(tweet)
        pol_obama.append(tb_o.polarity)
        sub_obama.append(tb_o.subjectivity)

collect_text('tweet_stream_Trump_10000.json')
with open('Trump_10000_tweet_text.json', 'r') as infile:
        readtweets_trump = json.load(infile)        
pol_trump = []
sub_trump = []
for tweet in readtweets_trump:
        tb_t = TextBlob(tweet)
        pol_trump.append(tb_t.polarity)
        sub_trump.append(tb_t.subjectivity)

def make_pol_graph(lst,keyword):
    plt.hist(lst, bins=10) 
    plt.xlabel('Polarity score')
    plt.ylabel('Tweet Count')
    plt.grid(True)
    plt.savefig('Polarity_{}.pdf'.format(keyword))
    
def make_sub_graph(lst,keyword):
    plt.hist(lst, bins=10) 
    plt.xlabel('Subjectivity score')
    plt.ylabel('Tweet Count')
    plt.grid(True)
    plt.savefig('Subjectivity_{}.pdf'.format(keyword))

make_pol_graph(pol_obama,'Obama')
make_pol_graph(pol_trump,'Trump')
make_sub_graph(sub_obama,'Obama')
make_sub_graph(sub_trump,'Trump')

def compute_avg(lst):
    avg = sum(lst)/len(lst)
    return avg

obama_ans6 = compute_avg(pol_obama)
obama_ans7 = compute_avg(sub_obama)
trump_ans6 = compute_avg(pol_trump)
trump_ans7 = compute_avg(sub_trump)
        
#Compile Analysis   
outfile = open('Prelim_Analysis.txt','w')
outfile.write('Keyword 1 Analysis: "Trump" \n')
outfile.write('Most Popular Words: {} \n'.format(trump_ans1))
outfile.write('Most Popular Words(w/o Stopwords): {} \n'.format(trump_ans105))
outfile.write('Most Popular Hashtags: {} \n'.format(trump_ans2))
outfile.write('Most Frequently Appearing Usernames: {} \n'.format(trump_ans3))
outfile.write('Most Frequently Tweeting People: {} \n'.format(trump_ans4))
outfile.write('Most Influential Tweet: {} \n \n'.format(trump_ans5))
outfile.write('Keyword 2 Analysis: "Obama" \n')
outfile.write('Most Popular Words: {} \n'.format(obama_ans1))
outfile.write('Most Popular Words(w/o Stopwords): {} \n'.format(obama_ans105))
outfile.write('Most Popular Hashtags: {} \n'.format(obama_ans2))
outfile.write('Most Frequently Appearing Usernames: {} \n'.format(obama_ans3))
outfile.write('Most Frequently Tweeting People: {} \n'.format(obama_ans4))
outfile.write('Most Influential Tweet: {} \n \n'.format(obama_ans5))
outfile.write('Sentiment Analysis: \n')
outfile.write("The average polarity score for trump related tweets was {:1.2f} \n".format(trump_ans6))
outfile.write("The average polarity score for obama related tweets was {:1.2f} \n".format(obama_ans6))
outfile.write("The average subjectivity score for trump related tweets was {:1.2f} \n".format(trump_ans7))
outfile.write("The average subjectivity score for obama related tweets was {:1.2f} \n".format(obama_ans7))
outfile.close()   











        