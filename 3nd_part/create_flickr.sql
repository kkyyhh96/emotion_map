CREATE TABLE flickr
(id BIGINT PRIMARY KEY NOT NULL,
userid TEXT,
user_nickname TEXT,
photo_date_taken DATE,
photo_date_uploaded BIGINT,
device TEXT,
title TEXT,
description TEXT,
user_tags TEXT,
machine_tags TEXT,
longitude FLOAT DEFAULT 0,
latitude FLOAT DEFAULT 0,
/*location POINT,*/
accuracy INTEGER DEFAULT 0,
page_url TEXT NOT NULL,
download_url TEXT NOT NULL,
license_name TEXT,
license_url TEXT,
server_id INTEGER DEFAULT 0,
farm_id INTEGER DEFAULT 0,
secret TEXT,
secret_original TEXT,
extension TEXT,
marker INTEGER DEFAULT 0
);
CREATE INDEX iflickr_id ON flickr(id);
/*CREATE INDEX iflickr_location ON flickr USING GIST(location);*/
CREATE INDEX iflickr_date ON flickr(photo_date_taken);
