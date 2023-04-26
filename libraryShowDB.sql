USE librarydatabase;


SELECT * FROM Book WHERE availability <> 'Deleted' and (title LIKE '%the%');

    
INSERT INTO Book (isbn, title, author, publisher, availability, shelf)
VALUES ('1234567890123', 'The Great Gatsby', 'F. Scott Fitzgerald', 'Scribner', 'Available', 'A')
ON DUPLICATE KEY UPDATE 
    title = VALUES(title), 
    author = VALUES(author), 
    publisher = VALUES(publisher), 
    availability = VALUES(availability), 
    shelf = VALUES(shelf);
