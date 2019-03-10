
-- table: `users`

    SELECT `user_id`, `username` FROM `user`;

    -- insert new username into db

    INSERT INTO `user` (`username`, `screenname`, `original_user`) VALUES (%s, %s, %s);

        -- fetch the user_id just created
        SELECT `user_id` FROM `user` WHERE `username`=%s;
                      --- note it will proably be significantly faster to just +1 to dict of users

--table: `scrape`

    -- create new scrape instance and fetch the id for inserting posts
    INSERT INTO `scrape` (`user_id`, `post_count`, `follow_count`, `follower_count`,
    `scrape_date`, ) VALUES (%s,%s,%s,%s,%s);
                        -- note: original_user was ommitted because we are moving that data to a new table

        SELECT `id` FROM `scrape` WHERE `user_id` = %s; -- note:with multiple scrapes we will have to pick the most recent one


-- table: `post`
    -- insert all scraped posts posts into `posts`

    INSERT INTO `post` (`user_id`, `post_id_str`, `caption_text`, `post_date`, `like_count`, `scrape_id`)
                VALUES(%s,%s,%s,%s,%s,%s);

    -- get all previous post captions
    SELECT `caption_text` from `post` WHERE `user_id` = %s;


    -- get post ID for inserting `comments`

    SELECT `id` FROM `post` WHERE `scrape_id` = %s AND `post_id_str`= %s;

-- table: `comment`
    -- insert comment for a given post

    INSERT INTO `comment` (`post_id`, `comment_text`, `user_id`) VALUES (%s,%s,%s);

    SELECT `comment_text` from `comment` WHERE user_id = %s;

-- table: `similarity`

    INSERT INTO `similarity` (`user_id`, `user_id_followed`, `cos_sim_value`)

    SELECT `cos_sim_value` FROM `similarity` WHERE user_id= %s and user_id_followed = %s;

