CREATE TABLE site
(id INTEGER PRIMARY KEY,
site_name CHARACTER VARYING(30) NOT NULL,
coordinates POINT NOT NULL,
start_query BOOLEAN NOT NULL DEFAULT(FALSE),
);
CREATE INDEX site_name_index ON site(site_name);
CREATE INDEX start_query ON site(start_query);

CREATE TABLE photo
(id BIGINT PRIMARY KEY,
url TEXT NOT NULL,
owner CHARACTER,
site CHARACTER VARYING(30) NOT NULL,
coordinates POINT,
radius FLOAT NOT NULL,
photo_take_date DATE,
photo_upload BIGINT,
accuracy INTEGER,
f_hasface BOOLEAN NOT NULL DEFAULT(FALSE),
start_detect BOOLEAN NOT NULL DEFAULT(FALSE),
start_info BOOLEAN NOT NULL DEFAULT(FALSE),
start_recog BOOLEAN NOT NULL DEFAULT(FALSE)
);
CREATE INDEX photo_id_index ON photo(id);
CREATE INDEX photo_coordinates_index ON photo USING GIST(coordinates);
CREATE INDEX photo_date_index ON photo(photo_date);
CREATE INDEX photo_f_hasface_index ON photo(f_hasface);
CREATE INDEX photo_start_detect_index ON photo(start_detect);
CREATE INDEX photo_start_info_index ON photo(start_info);
CREATE INDEX photo_start_recog_index ON photo(start_recog);

CREATE TABLE facepp
(id BIGINT PRIMARY KEY,
photo_id INTEGER NOT NULL,
site CHARACTER VARYING(30) NOT NULL,
gender INTEGER NOT NULL,
age INTEGER NOT NULL,
race CHARACTER(5) NOT NULL,
smiling FLOAT NOT NULL,
glass FLOAT NOT NULL
);
CREATE INDEX facepp_photo_id_index ON facepp(photo_id);

CREATE TABLE ms_emotion
(id BIGINT PRIMARY KEY,
photo_id INTEGER NOT NULL,
site CHARACTER(30) NOT NULL,
anger FLOAT NOT NULL,
contempt FLOAT NOT NULL,
disgust FLOAT NOT NULL,
fear FLOAT NOT NULL,
happiness FLOAT NOT NULL,
neutral FLOAT NOT NULL,
sadness FLOAT NOT NULL,
surprise FLOAT NOT NULL
);
CREATE INDEX ms_emotion_photo_id_index ON ms_emotion(photo_id);
