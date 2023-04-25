CREATE DATABASE IF NOT EXISTS libraryDatabase;
USE libraryDatabase;

CREATE TABLE IF NOT EXISTS Admin (
    adminID VARCHAR(5) PRIMARY KEY,
    fName VARCHAR(50) NOT NULL,
    lName VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    status ENUM('Active', 'Disabled') NOT NULL
);
ALTER TABLE Admin AUTO_INCREMENT = 1;

CREATE TABLE IF NOT EXISTS Staff (
    staffID VARCHAR(5) PRIMARY KEY,
    fName VARCHAR(50) NOT NULL,
    lName VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    status ENUM('Active', 'Disabled') NOT NULL
);
ALTER TABLE Staff AUTO_INCREMENT = 1;

CREATE TABLE IF NOT EXISTS Member (
    memberID VARCHAR(5) PRIMARY KEY,
    fName VARCHAR(50) NOT NULL,
    lName VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    status ENUM('Active', 'Disabled') NOT NULL
);
ALTER TABLE Member AUTO_INCREMENT = 1;

CREATE TABLE IF NOT EXISTS Book (
    isbn VARCHAR(13) PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    author VARCHAR(100),
    publisher VARCHAR(100),
    availability ENUM('Available', 'On Loan', 'Deleted') NOT NULL,
    shelf VARCHAR(1) NOT NULL
);



CREATE TABLE IF NOT EXISTS `Order` (
	orderID VARCHAR(6) PRIMARY KEY,
    staffID VARCHAR(5) NOT NULL,
    memberID VARCHAR(5) NOT NULL,
    isbn VARCHAR(13) NOT NULL,
    rentDate DATETIME NOT NULL,
    dueDate DATE NOT NULL,
    status ENUM('On Loan', 'Overdue', 'Returned'),
	returnDate DATETIME,
    
    FOREIGN KEY (staffID) REFERENCES Staff(staffID),
    FOREIGN KEY (memberID) REFERENCES Member(memberID),
    FOREIGN KEY (isbn) REFERENCES Book(isbn)
);