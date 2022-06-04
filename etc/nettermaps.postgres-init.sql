-- create a simple user and database
CREATE ROLE securedatabase_user WITH LOGIN PASSWORD 'securepassword';
CREATE DATABASE securely_validated_db WITH OWNER = securedatabase_user;

-- revoke access for all others
REVOKE ALL ON DATABASE securely_validated_db FROM PUBLIC;

GRANT CONNECT ON DATABASE securely_validated_db TO securedatabase_user;

\c securely_validated_db

GRANT USAGE ON SCHEMA public TO securedatabase_user;

-- create table
CREATE TABLE markers (
    owner varchar(256),
    rname varchar(64),
    rlat float,
    rlng float,
    rtype int,
    rvisible int,
    cdate timestamp,
    cref SERIAL
);

ALTER TABLE markers ALTER COLUMN cdate SET DEFAULT now();

GRANT SELECT ON TABLE markers to securedatabase_user;
GRANT INSERT ON TABLE markers to securedatabase_user;
GRANT DELETE ON TABLE markers to securedatabase_user;
GRANT USAGE, SELECT ON SEQUENCE markers_cref_seq TO securedatabase_user;

INSERT INTO markers VALUES ('a70018e128984bd186600df9801ea50a51a25942c8ddbc1a5dc87d97f005fff3', 'Lovely Lake', 73.1960, 124.1961, 9, 0);
