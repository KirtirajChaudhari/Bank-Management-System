-- Create Database
CREATE DATABASE IF NOT EXISTS bank_management_system;
USE bank_management_system;

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    account_number VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(15) NOT NULL,
    email VARCHAR(100) NOT NULL,
    aadhar_number VARCHAR(20) NOT NULL,
    password VARCHAR(255) NOT NULL,
    balance DECIMAL(10, 2) DEFAULT 0.00
);

-- Transactions Table
CREATE TABLE IF NOT EXISTS transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    account_number VARCHAR(10),
    transaction_type ENUM('credit', 'debit', 'transfer'),
    amount DECIMAL(10, 2),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_number) REFERENCES users(account_number)
);

-- Credit Card Applications Table
CREATE TABLE IF NOT EXISTS credit_card_applications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    account_number VARCHAR(10),
    name VARCHAR(100),
    phone_number VARCHAR(15),
    address TEXT,
    salary DECIMAL(10, 2),
    status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    FOREIGN KEY (account_number) REFERENCES users(account_number)
);
