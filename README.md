# Chatting-Traders
Created on 3/30/2019

## What is it about?
Nowadays, communication is a crucial component of everyday life. It is one of those skill sets that might possibly bring people closer to success. While pursuing daily goals to success, traders often utilize their communication skills in winning the daily economical battles. This project analyses four files that describe various communication models used by traders in ForEx trading system. It analyzes scenarios of what possible insights the data can provide us. What are some types of discussions that the most popular post chatters are talking about? Could we find the hidden success formula of Warren Buffett? Let’s dive in and see.

Check out our [report](https://github.com/tphuong141607/YesCode--Chatting-Traders/blob/master/doc/%E2%80%9CThe%20Chatting%20Traders%E2%80%9D%20Project.pdf) in the document folder for more detailed information.

The program was built using Python, matplotlib and Pandas.

## Provided data: 
The data includes four tables that describe users in a ForEx trading system and their communications via direct messages and forum-style discussion boards. All files are TAB-separated. All times in the tables are expressed in milliseconds, starting on midnight, January 1, 1970.

1. The file 'users.tsv' contains unique user ids and account creation dates. 
2. The file messages.tsv contains unique message ids, send dates, sender ids (consistent with those in 'users.tsv'), and message types. 
3. The file 'discussions.tsv' contains unique discussion ids, creation dates, creator ids (consistent with those in 'users.tsv'), and discussion categories. 
4. The file 'discussion_posts.tsv' contain unique post ids, discussion ids (consistent with those in 'discussions.tsv'), and creator ids (consistent with those in 'users.tsv').

## What we did:
1. Answer simple descriptive statistics questions such as:
- How many users are in the database?  
- What is the time span of the database? 
- How many messages of each type have been sent? 
- How many discussions of each type have been started? 
- How many discussion posts have been posted? 

2. Activity range is the time between the first and the last message (in ANY category) sent by the same user. What is the distribution of activity ranges? 

3. Message activity delay is the time between user account creation and sending the first user message in a specific category.  What is the distribution of message activity delays in EACH category? 

4. What is the distribution of discussion categories by the number of posts? What is the most popular category? 

5. Post activity delay is the time between user account creation and posting the first discussion message. What is the distribution of post activity delays in the most popular category? 

6. A box plot with whiskers that shows all appropriate statistics for message activity delays in EACH category, post activity delays, and activity ranges.

## How to run this program on your computer locally?
1. Download Anaconda Navigator [here](https://www.anaconda.com/distribution/#download-section)
2. Install Spider within Anaconda Navigator
3. Launch Spider and import the source code (File --> Open --> select the ChattingTraders.py)
4. Run the program



