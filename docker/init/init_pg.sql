#init pg
CREATE TABLE IF NOT EXISTS tel_numbers ( personID INT PRIMARY KEY, tel_number VARCHAR(255) );
INSERT INTO tel_numbers (personID, tel_number) VALUES (1, '+79092223344'), (2, '89997788888');
CREATE TABLE IF NOT EXISTS emails ( personID INT PRIMARY KEY, email VARCHAR(255) );
INSERT INTO emails (personID, email) VALUES (1, 'db@mail.ru'), (2, 'gghf@mail.ru');
