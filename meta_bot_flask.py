from flask import Flask
from flask import render_template
import time
import pandas as pd
import pickle

app = Flask("Snooze")

@app.route('/')
def main_func():

	data = pickle.load(open("topic_dict.pkl", "rb"))
	num_topics = len(data)

	comments = pickle.load(open("comments.pkl", "rb"))

	total_comment_count = sum([x['comment_count'] for x in comments])
	total_comment_count = format(total_comment_count, ',d')
	total_subreddit_count = format(len(comments), ',d')

	comments = comments[:100]
	maxcomments = comments[0]['subreddit']

	upvotes = pickle.load(open("upvotes.pkl", "rb"))
	upvotes = upvotes[:100]
	maxupvotes = upvotes[0]['subreddit']

	ratio = pickle.load(open("ratio.pkl", "rb"))
	ratio = ratio[:100]
	maxratio = ratio[0]['subreddit']

	tri_dim = pickle.load(open("tri_dim.pkl", "rb"))

	final_disp = set()

	for obj in comments:
		final_disp.add(obj['subreddit'])
	for obj in upvotes:
		final_disp.add(obj['subreddit'])
	for obj in ratio:
		final_disp.add(obj['subreddit'])

	unwanted = set(tri_dim) - final_disp
	for unwanted_key in unwanted:
		del tri_dim[unwanted_key]

	del tri_dim['AskReddit']


	top_words_dist = pickle.load(open('top_words_topic.pkl', 'rb'))

	if data is None:
		raise Exception("End my misery :(")

	return render_template('one_page.html',
    	topic_datasets=data,
    	total_subreddit_count=total_subreddit_count,
    	total_comment_count=total_comment_count,
    	tri_dim=tri_dim,
    	maxcomments=maxcomments,
    	maxupvotes=maxupvotes,
    	maxratio=maxratio,
    	num_topics=num_topics,
    	comments=comments,
    	upvotes=upvotes,
    	ratio=ratio,
    	top_words_dist=top_words_dist,
    	timeref = int(time.time()))

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=7777)
