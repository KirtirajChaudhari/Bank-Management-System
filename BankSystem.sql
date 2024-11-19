show databases;
CREATE DATABASE BankSystem;

USE BankSystem;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(50) NOT NULL,
    balance DECIMAL(10, 2) DEFAULT 0.00
);

select * from users;
delete users;
