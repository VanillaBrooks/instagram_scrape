-- update usernames BEFORE any data is inserted
with post_user_ids as (select user_id from post where post_id_str IN ('python concat list of ids'))
UPDATE users
    SET username = "new username",
    SET screenname = "new screen name"

-- create a new user *only do this after checking that a previous user did not create change their name*
INSERT INTO users (username, screenname) VALUES ("", "")

-- create new scrape
with with_user_id as (select * from users where username= "original_user")
INSERT INTO scrape (user_id, post_count, follow_count, follower_count, scrape_date)
VALUES ((select * from with_user_id), "post count int", "follow count int", "follower count int", "Scrape date int")

-- create a new follower - following relationship
WITH original_user as (select id from users where username='original_user' ),
following_user as (select id from users where username = 'following_user')
INSERT INTO relationship (user_id, user_id_following) VALUES ((select * from original_user), (select * from following_user))
ON CONFLICT DO NOTHING;

-- create a new post
with with_user_id as (select * from users where username= "original_user")
INSERT INTO post (user_id, scrape_id, post_id_str, caption_text, post_date, like_count, original_user) 
VALUES ((select * from with_user_id), "scrape_id", "post_id_str", "caption_text", "post_date_int", "like_count_int", "original user t/F")
ON CONFLICT
    SET like_count = "new like count here"

-- create new comment
select id from post where post_id_str = "post id str url here" -- cache me!
with with_user_id as (select * from users where username = "commenting username")
INSERT INTO comment (post_id, user_id, comment_text, comment_date, like_count)
VALUES ("cached post id ", (SELECT * from with_user_id), "comment text", "comment_date int", "like count int")
ON CONFLICT
    SET like_count = "new like count int"

-- create a new similarity between users, or update an older similarity
with rel_id as (select id from relationship where user_id = 'original_user' and user_id_following='following_user' )
INSERT INTO similarity (relationship_id, cos_sim_value) VALUES ((SELECT * FROM rel_id), 0.0123)
ON CONFLICT 
    SET cos_sim_value = 0.0123


