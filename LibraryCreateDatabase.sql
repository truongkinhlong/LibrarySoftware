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

###Insert DATA###
INSERT IGNORE INTO Admin (adminID, fName, lName, email, password, status)
VALUES
	('AD000', 'ADMIN', 'ADMIN', 'admin', '0000', 'Active'), 
	('AD001', 'Kinh', 'Truong', 'ktruong14@gator.uhd.edu', 'truong', 'Active'); 

INSERT IGNORE  INTO Staff (staffID, fName, lName, email, password, status)
VALUES
	('ST001', 'Adrian', 'Nguyen', 'ANguyen@gmail.com', 'AdNg001', 'Active'),
	('ST002', 'Cerian', 'Jaime', 'CJaime@gmail.com', 'CeJa002', 'Active'),
	('ST003', 'Nathan', 'Nguyen', 'NNguyen@gmail.com', 'NaNg003', 'Active'),
	('ST004', 'Cooper', 'Tran', 'CTran@gmail.com', 'CoTr004', 'Active'); 
    
INSERT IGNORE  INTO Member (memberID, fName, lName, email, password, status)
VALUES
    ('MB001', 'Alice', 'Jones', 'alice.jones@example.com', 'password1', 'Active'),
    ('MB002', 'Bob', 'Smith', 'bob.smith@example.com', 'password2', 'Active'),
    ('MB003', 'Charlie', 'Brown', 'charlie.brown@example.com', 'password3', 'Active'),
    ('MB004', 'David', 'Lee', 'david.lee@example.com', 'password4', 'Active'),
    ('MB005', 'Emily', 'Wang', 'emily.wang@example.com', 'password5', 'Active'),
    ('MB006', 'Frank', 'Garcia', 'frank.garcia@example.com', 'password6', 'Active'),
    ('MB007', 'Grace', 'Nguyen', 'grace.nguyen@example.com', 'password7', 'Active'),
    ('MB008', 'Henry', 'Kim', 'henry.kim@example.com', 'password8', 'Active'),
    ('MB009', 'Isabella', 'Chen', 'isabella.chen@example.com', 'password9', 'Active'),
    ('MB010', 'James', 'Liu', 'james.liu@example.com', 'password10', 'Active');
    
INSERT IGNORE INTO Book (isbn, title, author, publisher, availability, shelf) VALUES 
('9780345337665', 'The Hobbit', 'J.R.R. Tolkien', 'Ballantine Books', 'Available', 'A'),
('9780547928227', 'The Lord of the Rings', 'J.R.R. Tolkien', 'Houghton Mifflin Harcourt', 'Available', 'B'),
('9780765356784', 'A Game of Thrones', 'George R.R. Martin', 'Bantam Books', 'Available', 'C'),
('9780345337665', 'Harry Potter and the Philosopher''s Stone', 'J.K. Rowling', 'Listening Library', 'Available', 'D'),
('9781402894629', 'To Kill a Mockingbird', 'Harper Lee', 'Perfection Learning', 'Available', 'F'),
('9780747532743', 'Harry Potter and the Chamber of Secrets', 'J.K. Rowling', 'Bloomsbury Publishing', 'Available', 'A'),
('9780007117116', 'The Da Vinci Code', 'Dan Brown', 'Doubleday', 'Available', 'B'),
('9780545010221', 'The Hunger Games', 'Suzanne Collins', 'Scholastic Press', 'Available', 'C'),
('9780141033570', '1984', 'George Orwell', 'Penguin Books', 'Available', 'D'),
('9780763647476', 'The Graveyard Book', 'Neil Gaiman', 'HarperCollins Publishers', 'Available', 'F'),
('9780198501775', 'A Brief History of Time', 'Stephen Hawking', 'Bantam Books', 'Available', 'A'),
('9780735211292', 'The Subtle Art of Not Giving a F*ck', 'Mark Manson', 'HarperOne', 'Available', 'B'),
('9780062801975', 'The Alchemist', 'Paulo Coelho', 'HarperOne', 'Available', 'C'),
('9781524763169', 'Becoming', 'Michelle Obama', 'Crown Publishing Group', 'Available', 'D'),
('9780143110165', 'The Power of Now', 'Eckhart Tolle', 'New World Library', 'Available', 'E'),
('9780525536229', 'Educated', 'Tara Westover', 'Random House', 'Available', 'F'),
('9780066620732', 'Good to Great', 'Jim Collins', 'HarperBusiness', 'Available', 'G'),
('9781982141462', 'The Vanishing Half', 'Brit Bennett', 'Riverhead Books', 'Available', 'H'),
('9780066620992', 'The Innovator\'s Dilemma', 'Clayton Christensen', 'HarperBusiness', 'Available', 'I'),
('9781594481710', 'The Kite Runner', 'Khaled Hosseini', 'Riverhead Books', 'Available', 'J'),
('9780446675536', 'The 7 Habits of Highly Effective People', 'Stephen Covey', 'Free Press', 'Available', 'K'),
('9780812984965', 'The Goldfinch', 'Donna Tartt', 'Little, Brown and Company', 'Available', 'L'),
('9780670026198', 'Thinking, Fast and Slow', 'Daniel Kahneman', 'Farrar, Straus and Giroux', 'Available', 'M'),
('9780385537858', 'Zero to One', 'Peter Thiel', 'Crown Business', 'Available', 'N'),
('9780307278628', 'Freakonomics', 'Steven D. Levitt, Stephen J. Dubner', 'William Morrow', 'Available', 'O'),
('9781400069284', 'The Road', 'Cormac McCarthy', 'Alfred A. Knopf', 'Available', 'P'),
('9780307740991', 'The Help', 'Kathryn Stockett', 'Putnam Adult', 'Available', 'Q'),
('9781594204115', 'Grit', 'Angela Duckworth', 'Scribner', 'Available', 'R'),
('9780143129334', 'The Art of Thinking Clearly', 'Rolf Dobelli', 'Harper', 'Available', 'S'),
('9780385682314', 'The Nightingale', 'Kristin Hannah', 'St. Martin\'s Press', 'Available', 'T'),
('9780060555665', 'The Tipping Point', 'Malcolm Gladwell', 'Little, Brown and Company', 'Available', 'U'),
('9780316769480', 'The Catcher in the Rye', 'J.D. Salinger', 'Little, Brown and Company', 'Available', 'V');

INSERT IGNORE INTO `Order` (orderID, staffID, memberID, isbn, rentDate, dueDate, status) 
VALUES
('000001', 'ST004', 'MB002', '9780345337665', '2023-04-23 10:00:00', '2023-04-30', 'On Loan'),
('000002', 'ST001', 'MB001', '9780747532743', '2023-04-25 13:45:00', '2023-04-30', 'On Loan'),
('000003', 'ST002', 'MB002', '9780060555665', '2023-04-26 15:30:00', '2023-04-30', 'On Loan'),
('000004', 'ST003', 'MB003', '9780143129334', '2023-04-27 11:15:00', '2023-04-30', 'On Loan'),
('000005', 'ST004', 'MB004', '9780385682314', '2023-04-28 12:30:00', '2023-05-01', 'On Loan'),
('000006', 'ST003', 'MB005', '9781594204115', '2023-04-29 09:45:00', '2023-05-01', 'On Loan'),
('000007', 'ST003', 'MB006', '9780307740991', '2023-04-30 16:00:00', '2023-05-01', 'On Loan'),
('000008', 'ST002', 'MB007', '9780307278628', '2023-05-01 14:30:00', '2023-05-08', 'On Loan'),
('000009', 'ST001', 'MB008', '9780812984965', '2023-05-01 10:45:00', '2023-05-09', 'On Loan'),
('000010', 'ST002', 'MB009', '9780446675536', '2023-05-01 12:15:00', '2023-05-10', 'On Loan'),
('000011', 'ST001', 'MB010', '9780066620732', '2023-05-01 09:00:00', '2023-05-11', 'On Loan'),
('000012', 'ST004', 'MB002', '9781524763169', '2023-05-01 13:00:00', '2023-05-12', 'On Loan'),
('000013', 'ST002', 'MB008', '9780735211292', '2023-05-01 11:30:00', '2023-05-13', 'On Loan'),
('000014', 'ST004', 'MB008', '9780765356784', '2023-05-01 14:45:00', '2023-05-14', 'On Loan'),
('000015', 'ST004', 'MB002', '9781402894629', '2023-05-01 10:15:00', '2023-05-15', 'On Loan'),
('000016', 'ST002', 'MB005', '9780345337665', '2023-05-01 15:00:00', '2023-05-16', 'On Loan'),
('000017', 'ST002', 'MB003', '9780007117116', '2023-05-01 12:30:00', '2023-05-17', 'On Loan');