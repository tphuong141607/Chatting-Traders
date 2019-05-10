#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 16:40:37 2019
@author: Thao Phuong, Jan
"""
import pandas as pd
import matplotlib.pyplot as plt
import os

USERS_FILE = 'users.tsv'
DISCUSSION_FILE = 'discussions.tsv'
MESSAGE_FILE = 'messages.tsv'
POST_FILE = 'discussion_posts.tsv' 

DATA_FILE_PATH_DIR = '../traders/'
RESULT_FILE_PATH_DIR = '../results/'

# Create directory to store results/images if don't have one
if not os.path.exists(RESULT_FILE_PATH_DIR):
    os.makedirs(RESULT_FILE_PATH_DIR)
    
# DF = dataframes
userDF = pd.read_table(DATA_FILE_PATH_DIR + USERS_FILE)
discussionDF = pd.read_table(DATA_FILE_PATH_DIR + DISCUSSION_FILE) 
messageDF = pd.read_table(DATA_FILE_PATH_DIR + MESSAGE_FILE) 
postDF = pd.read_table(DATA_FILE_PATH_DIR + POST_FILE) 

""" PART I: SIMPLE DESCRIPTIVE STATISTICS """
# 1. How many users are in the database?
total_users = userDF.shape[0]

# 2. What is the time span of the database? 
timeDF = pd.concat([userDF['memberSince'], discussionDF['createDate'], 
                    messageDF['sendDate'], postDF['createDate']], ignore_index=True)
timeSpan = (timeDF.max() - timeDF.min()) / (60*60*24*1000)

# 3. How many messages of each type have been sent? 
messageType_count = messageDF.type.value_counts()
plt.figure(1, figsize=(10, 10))
plt.pie(messageType_count.values, shadow=True, autopct='%1.1f%%')
plt.legend(messageType_count.index)
plt.title('Type of Message Sent')
plt.savefig(RESULT_FILE_PATH_DIR + 'pieChartMessage.png', dpi = 200)
plt.close()

# 4. How many discussions of each type have been sent?
discussionType_count = discussionDF.discussionCategory.value_counts()
plt.figure(2, figsize=(13, 13))
plt.pie(discussionType_count.values,shadow=True, autopct='%1.1f%%')
plt.legend(discussionType_count.index)
plt.title('Type of Discussion Started')
plt.savefig(RESULT_FILE_PATH_DIR + 'pieChartDiscussion.png', dpi = 200)
plt.close()

# 5. How many discussion posts have been posted?
total_posts = postDF['discussion_id'].unique().shape[0]

""" 
PART II: ACTIVITY RANGE 
Activity range is the time between the first and the last message (in ANY category)
sent by the same user. What is the distribution of activity ranges? 
"""
messageGrouped = messageDF.groupby(['sender_id'])
activityRange = (messageGrouped.sendDate.max() - messageGrouped.sendDate.min()) / (60*60*24*1000)

# Drawing 
plt.figure(3, figsize=(10,10))
activityRange.plot.hist(logy='true', color ='c')
plt.title('Activity Range Distribution')
plt.xlabel('Activity Range')
plt.ylabel('Frequency')
plt.savefig(RESULT_FILE_PATH_DIR + 'activityRangeDist.png', dpi = 200)
plt.close()

""" 
PART III: MESSAGE ACTIVITY DELAY 
Message activity delay is the time between user account creation and sending the 
first user message in a specific category. What is the distribution of message 
activity delays in EACH category? Deliverable: a histogram for each category.
"""
messageUserMerge_DF = (pd.merge(userDF, messageDF, left_on='id', right_on='sender_id'))
messageUserMerge_DF.drop(columns=['id_y', 'id_x'], inplace=True)
message_category = messageUserMerge_DF['type'].unique()

# Category: FRIEND_LINK_REQUEST
friendLinkReq_DF = messageUserMerge_DF.loc[messageUserMerge_DF.type == message_category[0]]
messageDelay_friend = friendLinkReq_DF.groupby(['sender_id'])
messageDelay_friend = (messageDelay_friend.sendDate.min() - messageDelay_friend.memberSince.min()) / (60*60*24*1000)

# Category: DIRECT_MESSAGE
directMessage_DF = messageUserMerge_DF.loc[messageUserMerge_DF.type == message_category[1]]
messageDelay_directM = directMessage_DF.groupby(['sender_id'])
messageDelay_directM = (messageDelay_directM.sendDate.min() - messageDelay_directM.memberSince.min()) / (60*60*24*1000)

# Drawing 
plt.figure(4, figsize=(10,10))
plt.title('Message Activity Delay Distribution')
messageDelay_friend.plot.hist(legend=True, stacked=True, label='Friend link request', 
                              alpha=0.5, logy=True, color ='b')
messageDelay_directM.plot.hist(legend=True, stacked=True, label='Direct Message', 
                               alpha = 0.5, logy=True, color ='black').set_ylabel('Frequency')
plt.xlabel('Message Activity Delay')
plt.savefig(RESULT_FILE_PATH_DIR + 'messageDelayDist.png', dpi = 200)
plt.close()


""" 
PART IV: DISCUSSION CATEGORIES BY THE # OF POSTS
What is the distribution of discussion categories by the number of posts? 
What is the most popular category? Deliverable: a pie chart, with the most 
popular category highlighted.
"""
discussionPostMerge_DF = (pd.merge(discussionDF, postDF, left_on='id', right_on='discussion_id'))
discussionPostMerge_DF.drop(columns=['id_x', 'id_y', 'createDate_x', 'creator_id_y', 'discussion_id'], inplace=True)
discussionPostMerge_DF.rename(columns={'createDate_y': 'PostCreateDate', 'creator_id_x': 'creator_id'}, inplace=True)
discussionCategories_Distribution = discussionPostMerge_DF.discussionCategory.value_counts()

# Drawing
plt.figure(5, figsize=(10,10))
plt.title('Discussion Categories Distribution')
plt.pie(discussionCategories_Distribution.values, shadow=True, autopct='%1.1f%%', explode = (0.2, 0, 0,0,0,0.1,-0.2,0.3,0))
plt.legend(discussionCategories_Distribution.index)
plt.savefig(RESULT_FILE_PATH_DIR + 'discussCategoriesDist', dpi = 200)
plt.close()


""" 
PART V: POST ACTIVITY DELAY 
Post activity delay is the time between user account creation and posting the first 
discussion message. What is the distribution of post activity delays in the most popular category? 
Deliverable: a histogram. Note: The most popular category shall be carried over from the previous question.
"""

# discussionCategories_Distribution.index[0]] = the most popular category
postPopularCategory = discussionPostMerge_DF.loc[discussionPostMerge_DF.discussionCategory == discussionCategories_Distribution.index[0]] 
popularPostUserMerge_DF = (pd.merge(postPopularCategory, userDF, left_on='creator_id', right_on='id'))
popularPostUserMerge_DF.drop(columns=['id'], inplace=True)

postActivity = popularPostUserMerge_DF.groupby(['creator_id'])
postActivityDelay = (postActivity.PostCreateDate.min() - postActivity.memberSince.min()) / (60*60*24*1000)

# Drawing
plt.figure(6, figsize=(10,10))
plt.title('The Distribution of Post Activity Delays in The Most Popular Category')
postActivityDelay.plot.hist(legend=True, logy=True, color ='c')
plt.xlabel('Post Activity Delay')
plt.ylabel('Frequency')
plt.savefig(RESULT_FILE_PATH_DIR + 'postsDelayDist', dpi = 200)
plt.close()

# Post activity delay for all category:
allPostUserMerge_DF = pd.merge(postDF, userDF, left_on='creator_id', right_on='id')
postActivityGeneral = allPostUserMerge_DF.groupby(['creator_id'])
postActivityDelayGeneral = (postActivityGeneral.createDate.min() - postActivityGeneral.memberSince.min()) /(60*60*24*1000)


""" 
PART VI: Draw Box Plot
A box plot with whiskers that shows all appropriate statistics for message activity delays 
in EACH category, post activity delays, and activity ranges.
"""

plt.figure(7,figsize = (10,10))

# Message Activity Delays 
plt.subplot(1, 4, 1)
plt.title('Friend Request')
messageDelay_friend.plot.box(label="", showmeans=True).set_ylabel("Box plot")
plt.yscale('log')

plt.subplot(1, 4, 2)
plt.title('Direct message')
messageDelay_directM.plot.box(label="", showmeans=True)
plt.yscale('log')

# Post Activity Delay of all categories
plt.subplot(1, 4, 3)
plt.title('Post Activity Delay')
postActivityDelayGeneral.plot.box(label="", showmeans=True)
plt.yscale('log')

# Activity Range
plt.subplot(1, 4, 4)
plt.title('Activity Range')
activityRange.plot.box(label="", showmeans=True)
plt.yscale('log')

plt.savefig(RESULT_FILE_PATH_DIR + 'boxPlot.png')
plt.close()






