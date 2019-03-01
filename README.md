# instagram_scrape
Graphing instagram relationships through cosine / jaccard similarity and account statistics


## Backend

This package is designed to collect all metadata from a user and their posts. Using `selenium`, all of a user's captions from thier pictures are scraped and stored. The comments are also stored to better map relationships between users. Once all of a user's data is scraped, it is processed and stored in MySQL. All the accounts that a user is following are then scraped, and the process repeats until there are only private accounts remaining. 

Similarity metrics (Jaccard, Cosine) are implemented in rust to allow quick comparisson between users. All calculations will also be stored in MySQL to alleviate doing the same computations twice. Additionally, text similarity will not be the only metric used to relate two users. Another option we are strongly considering is relating users that comment on posts. If the same user comments on posts often from two different accounts, we can probably say those two accounts are related. 

Due to the prevalence of private instagram accounts, we currnetly plan on only scraping one layer past the specified user. However, we will give the user the option to include information from publicly available accounts that will be crawled when no other work is being done.

## Usage 

The user can choose to input account credientials or set thier account to public for the duration of the scrape. Providing account details allows the bot to access all account the user is following where it might otherwise be blocked by privacy settings. The end goal of this project is to provide an online interface for user inputs and rendering the graph using react with flask. 


## Upcoming work

Most of the backend calculations and computations are completed at this time. The `selenium` scraper is close to being completed, and the basic layout for the website is underway. In the future it would be convienent to use the Instagram API to gather information because it provides the guarantee that we are not storing account credentials. However, at this time it is not practical due to the application process and restrictions Instagram places on new developers.
