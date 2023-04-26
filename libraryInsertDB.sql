USE libraryDatabase;

INSERT IGNORE INTO Admin (adminID, fName, lName, email, password, status)
VALUES
	('AD000', 'Test', 'Test', 'ADTest@Test.com', 'TestAD', 'Active'), 
	('AD001', 'Kinh', 'Truong', 'truongkinhlong@gmail.com', 'BLrider301!', 'Active'); 

INSERT IGNORE  INTO Staff (staffID, fName, lName, email, password, status)
VALUES
	('ST000', 'Test', 'Test', '', '', 'Active'),
	('ST001', 'Adrian', 'Nguyen', 'ANguyen@gmail.com', 'AdNg001', 'Active'),
	('ST002', 'Cerian', 'Jaime', 'CJaime@gmail.com', 'CeJa002', 'Active'),
	('ST003', 'Nathan', 'Nguyen', 'NNguyen@gmail.com', 'NaNg003', 'Active'),
	('ST004', 'Cooper', 'Tran', 'CTran@gmail.com', 'CoTr004', 'Active'); 
    
INSERT IGNORE  INTO Member (memberID, fName, lName, email, password, status)
VALUES
	('MB000', 'Test', 'Test', '', '', 'Active'),
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
('9780763647476', 'The Graveyard Book', 'Neil Gaiman', 'HarperCollins Publishers', 'Available', 'F');

INSERT IGNORE INTO `Order` (orderID, staffID, memberID, isbn, rentDate, dueDate, status) 
VALUES
('000001', 'ST000', 'MB000', '9780345337665', '2023-04-23 10:00:00', '2023-04-25', 'On Loan'),
('000006', 'ST000', 'MB000', '9780547928227', '2023-04-23 10:00:00', '2023-04-27', 'On Loan'),
('000004', 'ST000', 'MB000', '9780765356784', '2023-04-23 10:00:00', '2023-04-29', 'On Loan'),
('000003', 'ST000', 'MB000', '9781402894629', '2023-04-23 10:00:00', '2023-04-15', 'Overdue');

INSERT IGNORE INTO `Order` (orderID, staffID, memberID, isbn, rentDate, dueDate, status, returnDate) 
VALUES
('000005', 'ST000', 'MB000', '9780141033570', '2023-04-23 10:00:00', '2023-04-19', 'Returned', '2023-04-18 14:21:59'),
('000002', 'ST000', 'MB000', '9780007117116', '2023-04-23 10:00:00', '2023-04-17', 'Returned', '2023-04-17 19:14:21');
