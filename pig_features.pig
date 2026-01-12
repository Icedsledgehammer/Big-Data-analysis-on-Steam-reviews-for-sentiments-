-- LOAD
raw = LOAD '/user/sentiment_project/steam_reviews_combined_english.csv' USING PigStorage(',')
    AS (app_id:long, app_name:chararray, review_id:long, language:chararray,
        review:chararray, timestamp:long, recommended:int,
        votes_helpful:int, votes_funny:int, weighted_vote_score:double,
        steam_purchase:int, received_for_free:int, written_during_early_access:int);

-- FILTER
data = FILTER raw BY app_id IS NOT NULL AND app_id > 0;

-- FEATURES + CLEAN
features = FOREACH data GENERATE
    review_id,
    REPLACE(review, '"', '') AS review,
    recommended AS label,
    (votes_helpful + votes_funny) AS total_votes,
    (float)votes_helpful / (votes_helpful + votes_funny + 1) AS helpful_ratio,
    SIZE(TOKENIZE(LOWER(review))) AS word_count;

-- STORE USING CSV WITHOUT TRAILING COMMA
REGISTER '/opt/pig/lib/piggybank.jar';
DEFINE CSVExcelStorage org.apache.pig.piggybank.storage.CSVExcelStorage();

STORE features INTO '/user/sentiment_project/features_mongo' USING CSVExcelStorage(',', 'YES_MULTILINE', 'NO_ESCAPE');
