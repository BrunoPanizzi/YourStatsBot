from time import sleep
from secret import *  # file with the acc details
import datetime
import praw

# login
reddit = praw.Reddit(
		client_id=client_id,
		client_secret=client_secret,
		user_agent=user_agent,
		username=username,
		password=password)

def getDateDifference(date):
	today = datetime.datetime.today()
	firstDate = datetime.datetime.fromtimestamp(date)
	return today - firstDate

def generateReply(user):
	'''creates the reply to a specific user based on their account activity'''

	# start writing the message
	finalMessage = f"Hello {user.name}!\n\nI looked at your profile for a while and this is what i've found:\n\n"
	# the final bit of the message, with the github link
	messageEnding = f"\n\n***\n\n^i'm ^a ^bot, ^here's ^my ^[github!!!](https://github.com/BrunoPanizzi/YourStatsBot)"

	# adding the n of days
	time = getDateDifference(user.created_utc).days
	finalMessage += f"You've been using reddit for {time} days now, "

	# getting some useful data
	posts = list(user.submissions.top(limit = 99999))
	comments = list(user.comments.top(limit = 99999))
	totalPosts = len(posts)
	totalComments = len(comments)

	# most basic case
	if totalComments == 0 and totalPosts == 0:
		finalMessage += f"and in this time you've never made a post, neither a comment!"
		finalMessage += messageEnding
		return finalMessage

	# posts
	if totalPosts == 0:
		finalMessage += f"and in this time you've never made a post.\n\n"
	elif totalPosts == 1:
		post = posts[0]
		finalMessage += f"and in this time you've made only [one post]({'https://www.reddit.com'+post.permalink}), and it had {post.score} upvotes and {post.num_comments} comments.\n\n"
	elif totalPosts > 1:
		bestPost = posts[0]
		worstPost = posts[-1]
		if worstPost.score >= 0:
			rating = 'upvotes'
		else:
			rating = 'downvotes'
		finalMessage += f"and in this time you've made {totalPosts} posts, the most popular one was [this one]({'https://www.reddit.com'+bestPost.permalink}), with {bestPost.score} upvotes and {bestPost.num_comments} comments, "
		finalMessage += f"and the least successful one was [this one]({'https://www.reddit.com'+worstPost.permalink}), with {worstPost.score} {rating} and {worstPost.num_comments} comments.\n\n"

	# comments
	if totalComments == 0:
		finalMessage += f"Now talking about comments, you dont have any of these!\n\n"
	elif totalComments == 1:
		comment = comments[0]
		finalMessage += f"Now talking about comments, you have only [one of these]({'https://www.reddit.com'+comment.permalink}) of these, and it had {comment.score} upvotes.\n\n"
	elif totalComments > 1:
		bestCom = comments[0]
		worstCom = comments[-1]
		if worstCom.score >= 0:
			rating = 'upvotes'
		else:
			rating = 'downvotes'
		finalMessage += f"Now talking about comments, you have {totalComments} of these, the most popular one was [this one]({'https://www.reddit.com'+bestCom.permalink}), with {bestCom.score} upvotes, "
		finalMessage += f"and the most controversial one was [this one]({'https://www.reddit.com'+worstCom.permalink}), with {worstCom.score} {rating}.\n\n"

	finalMessage += messageEnding
	return finalMessage

def sendReply(comment):
	'''replies to a comment using user data'''
	user = comment.author
	reply = generateReply(user)
	comment.reply(reply)
	comment.mark_read()

# actualy running
while True:
	for mention in reddit.inbox.mentions(limit=50):
		if mention.new:
			sendReply(mention)
	sleep(5)