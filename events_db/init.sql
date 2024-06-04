CREATE EXTENSION IF NOT EXISTS postgis;

CREATE SCHEMA IF NOT EXISTS events_schema;
SET search_path TO events_schema;

CREATE TABLE IF NOT EXISTS artists (
    artist_id SERIAL PRIMARY KEY,
    artist_name VARCHAR(255) NOT NULL,
    genre VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS venues (
    venue_id SERIAL PRIMARY KEY,
    venue_name VARCHAR(255) NOT NULL,
    bbox public.geometry(GEOMETRY, 27700),
    capacity INTEGER
);

CREATE TABLE IF NOT EXISTS events (
    event_id SERIAL PRIMARY KEY,
    event_name VARCHAR(255) NOT NULL,
    event_date date NOT NULL,
    venue_id INTEGER NOT NULL,
    FOREIGN KEY (venue_id) REFERENCES venues (venue_id)
);

CREATE TABLE IF NOT EXISTS events_artists (
    artist_id INTEGER NOT NULL,
    event_id INTEGER NOT NULL,
    PRIMARY KEY (artist_id, event_id),
    FOREIGN KEY (artist_id) REFERENCES artists (artist_id),
    FOREIGN KEY (event_id) REFERENCES events (event_id) 
);

DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM venues LIMIT 1) THEN
        COPY venues(venue_name, capacity, bbox) FROM '/docker-entrypoint-initdb.d/data/venues.csv' DELIMITER ',' CSV HEADER;
    END IF;
END $$;

DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM artists LIMIT 1) THEN
        COPY artists(artist_name, genre) FROM '/docker-entrypoint-initdb.d/data/artists.csv' DELIMITER ',' CSV HEADER;
    END IF;
END $$;

DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM events LIMIT 1) THEN
        COPY events(event_name, event_date, venue_id) FROM '/docker-entrypoint-initdb.d/data/events.csv' DELIMITER ',' CSV HEADER;
    END IF;
END $$;

DO $$ 
BEGIN
    IF NOT EXISTS (SELECT 1 FROM events_artists LIMIT 1) THEN
        COPY events_artists(artist_id, event_id) FROM '/docker-entrypoint-initdb.d/data/events_artists.csv' DELIMITER ',' CSV HEADER;
    END IF;
END $$;