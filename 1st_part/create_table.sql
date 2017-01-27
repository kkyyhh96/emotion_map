CREATE TABLE emotion(
id SERIAL PRIMARY KEY,
site CHARACTER VARYING (50),
url TEXT,
photo_time DATE,
anger FLOAT,
contempt FLOAT,
disgust FLOAT,
fear FLOAT,
happiness FLOAT,
neutral FLOAT,
sadness FLOAT,
surprise FLOAT
);
