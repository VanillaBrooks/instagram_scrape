

class Queries():
    def __init__(self):

# USERS
        #QUERY: get all ids and usernames (@) for stored users
        self.all_users = 'SELECT `user_id`, `username` FROM `users`;'

        #QUERY: create a new instance of a user in the users table. requires username (@), screen name, and if
        #       they were the original user of a scrape request
        self.new_user = 'INSERT INTO `user` (`username`, `screenname`, `original_user`) \
                        VALUES (%s, %s, %s);'

        #QUERY: manually get a user's id from the datatable. If all goes well this query should not have to run
        #       because the users id can be found by incrementing the largest user_id from the dict
        self.fetch_user_id_manual = 'SELECT `user_id` FROM `user`\
                                    WHERE `username`=%s'
# SCRAPES
        #QUERY: create a new instance of a scrape for a user. Scrapes should only include new information
        #       as all posts will eventually be concatenated together later
        self.create_scrape = 'INSERT INTO `scrape` (`user_id`, `scrape_id`, `post_count`, `follow_count`, \
                              `follower_count`, `scrape_date`) \
                              VALUES (%s,%s,%s,%s,%s,%s);'

        #QUERY: find the id of a scrape that was made. Generally the id can be found
        #       by incrementing the previous scrape id
        self.fetch_scrape_id_manual = 'SELECT `scrape_id` FROM `scrape` WHERE `user_id` = %s'

# POSTS
        #QUERY: create a new instance of a post with all associated metadata
        self.create_new_post = 'INSERT INTO `post` (`user_id`, `post_id_str`, `caption_text`, \
                                `post_date`, `like_count`, `scrape_scrape_id`) \
                                VALUES(%s,%s,%s,%s,%s,%s);'

        #QUERY: # fetch the newly created post_id given the information just inserted
        #        this may be one of the few cases where it is efficient to execute this
        #        since posts will probably be inserted with cursor.executemany()
        self.fetch_post_id_manual = 'SELECT `post_id` FROM `post` \
                                    WHERE `scrape_scrape_id` = %s AND `post_id_str`= %s;'

        # gather all the captions that a given user has made and return them
        self.fetch_all_user_captions = 'SELECT `caption_text` from `post` WHERE `user_id` = %s;'

# COMMENTS
        #QUERY: create a new comment given the post id that was previously found. should probably be done with
        #       a .executemany() call
        self.create_new_comment = 'INSERT INTO `comment` (`post_id`, `comment_text`, `user_id`) VALUES (%s,%s,%s);'
