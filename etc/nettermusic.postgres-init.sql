-- create a simple user and database
CREATE ROLE securedatabase_user WITH LOGIN PASSWORD 'securepassword';
CREATE DATABASE securely_validated_db WITH OWNER = securedatabase_user;

-- revoke access for all others
REVOKE ALL ON DATABASE securely_validated_db FROM PUBLIC;

GRANT CONNECT ON DATABASE securely_validated_db TO securedatabase_user;

\c securely_validated_db

GRANT USAGE ON SCHEMA public TO securedatabase_user;

-- create table
CREATE TABLE playlists (
    id SERIAL PRIMARY KEY,
    userid TEXT NOT NULL,
    tracks TEXT NOT NULL
);

GRANT SELECT ON TABLE playlists to securedatabase_user;
GRANT INSERT ON TABLE playlists to securedatabase_user;
GRANT DELETE ON TABLE playlists to securedatabase_user;
GRANT USAGE, SELECT ON SEQUENCE playlists_id_seq TO securedatabase_user;

INSERT INTO playlists VALUES (0, 'ricky', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ');
