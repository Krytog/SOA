CREATE DATABASE IF NOT EXISTS statistics;


CREATE TABLE IF NOT EXISTS statistics.kafka_likes (
    post_id UInt64,
    user_id UInt64
) ENGINE = Kafka
SETTINGS
    kafka_broker_list = 'statistics_broker:31341',
    kafka_topic_list = 'likes',
    kafka_group_name = 'likes',
    kafka_format = 'JSONEachRow';


CREATE TABLE IF NOT EXISTS statistics.kafka_views (
    post_id UInt64,
    user_id UInt64
) ENGINE = Kafka
SETTINGS
    kafka_broker_list = 'statistics_broker:31341',
    kafka_topic_list = 'views',
    kafka_group_name = 'views',
    kafka_format = 'JSONEachRow';


CREATE TABLE IF NOT EXISTS statistics.kafka_users_liked (
    user_id UInt64,
    liked_by_id UInt64
) ENGINE = Kafka
SETTINGS
    kafka_broker_list = 'statistics_broker:31341',
    kafka_topic_list = 'users_liked',
    kafka_group_name = 'users_liked',
    kafka_format = 'JSONEachRow';


CREATE TABLE IF NOT EXISTS statistics.likes (
    post_id UInt64,
    user_id UInt64
) ENGINE = MergeTree
ORDER BY (post_id);


CREATE TABLE IF NOT EXISTS statistics.views (
    post_id UInt64,
    user_id UInt64
) ENGINE = MergeTree
ORDER BY (post_id);


CREATE TABLE IF NOT EXISTS statistics.users_liked (
    user_id UInt64,
    liked_by_id UInt64
) ENGINE = MergeTree
ORDER BY (user_id);


CREATE MATERIALIZED VIEW IF NOT EXISTS statistics.kafka_mapper_likes
TO statistics.likes AS
SELECT *
FROM statistics.kafka_likes;


CREATE MATERIALIZED VIEW IF NOT EXISTS statistics.kafka_mapper_views
TO statistics.views AS
SELECT *
FROM statistics.kafka_views;


CREATE MATERIALIZED VIEW IF NOT EXISTS statistics.kafka_mapper_users_liked
TO statistics.users_liked AS
SELECT *
FROM statistics.kafka_users_liked;
