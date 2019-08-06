
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username char(30) UNIQUE NOT NULL,
    screenname char(45) NOT NULL
);

CREATE TABLE scrape (
    id SERIAL PRIMARY KEY,
    user_id SERIAL references users(id),
    post_count INT NOT NULL,
    follow_count INT NOT NULL,
    follower_count INT NOT NULL,
    scrape_date INT NOT NULL,        --unix time
    original_user boolean NOT NULL
);

CREATE TABLE relationship (
    id SERIAL PRIMARY KEY,

    user_id SERIAL references users(id),
    user_id_following SERIAL references users(id),
    unique(user_id, user_id_following)
);

CREATE TABLE similarity (
    relationship_id SERIAL UNIQUE references relationship(id),
    cos_sim_value NUMERIC(4,4)
);

CREATE TABLE post (
    id SERIAL PRIMARY KEY,
    user_id SERIAL references users(id),
    scrape_id SERIAL references scrape(id),

    post_id_str char(45) NOT NULL,
    caption_text TEXT,
    post_date INT NOT NULL,                 -- unix time,
    like_count INT NOT NULL
);

CREATE TABLE comment (
    id SERIAL PRIMARY KEY,
    post_id SERIAL references post(id),
    user_id SERIAL references users(id),

    comment_text TEXT NOT NULL,
    comment_date INT NOT NULL,
    like_count INT NOT NULL,
    unique(post_id, comment_text, comment_date)
);
