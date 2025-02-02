-- Удалем старые таблицы
DROP TABLE IF EXISTS emails;
DROP TABLE IF EXISTS tel_numbers;

ALTER USER postgres WITH PASSWORD '111';
CREATE USER repl_user WITH REPLICATION PASSWORD '111';

SELECT pg_create_physical_replication_slot('replication_slot');

CREATE TABLE emails (
    personID INT PRIMARY KEY,
    email VARCHAR(255) NOT NULL 
);

CREATE TABLE tel_numbers (
    personID INT PRIMARY KEY,
    tel_number VARCHAR(20) NOT NULL 
);

INSERT INTO emails (personID, email) VALUES (1, 'db@mail.ru'), (2, 'gghf@mail.ru');
INSERT INTO tel_numbers (personID, tel_number) VALUES (1, '+79092223344'), (2, '89997788888');



