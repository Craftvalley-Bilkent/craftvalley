CREATE DATABASE IF NOT EXISTS cvdb CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

USE cvdb;

CREATE TABLE IF NOT EXISTS User (
    user_id 		INT NOT NULL AUTO_INCREMENT,
    user_name 	VARCHAR(255) NOT NULL,
    email 		VARCHAR(255) NOT NULL,
    password		VARCHAR(255) NOT NULL,
    user_type 	VARCHAR(255) NOT NULL,
    address 		VARCHAR(255),
    phone_number 	VARCHAR(20) NOT NULL,
    active 		INT NOT NULL CHECK(active IN(0,1)),
    PRIMARY KEY(user_id),
    UNIQUE KEY(email),
    UNIQUE KEY(phone_number)
);

CREATE TABLE IF NOT EXISTS Small_Business (
    user_id 		INT NOT NULL,
    business_name 	VARCHAR(255) NOT NULL,
    title 		VARCHAR(255) NOT NULL,
    description 	VARCHAR(255), 
    picture 		LONGBLOB,
    balance 		DECIMAL(10,2),
    PRIMARY KEY(user_id),
    FOREIGN KEY(user_id) REFERENCES User(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Customer(
    user_id 		INT NOT NULL,
    picture 		LONGBLOB,
    payment_info 	VARCHAR(255) NOT NULL,
    balance 		DECIMAL(10,2) NOT NULL,
    PRIMARY KEY(user_id),
    FOREIGN KEY(user_id) REFERENCES User(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Admin(
    user_id INT NOT NULL,
    PRIMARY KEY(user_id),
    FOREIGN KEY(user_id) REFERENCES User(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Product(
    product_id 	INT NOT NULL AUTO_INCREMENT,
    title 		VARCHAR(255) NOT NULL,
    description 	VARCHAR(255),
    price 		DECIMAL(10,2) NOT NULL,
    amount 		INT NOT NULL,
    images 		LONGBLOB,
    PRIMARY KEY(product_id)
);

CREATE TABLE IF NOT EXISTS Balance_Record(
    record_id		INT NOT NULL AUTO_INCREMENT,
    record_date 	DATE NOT NULL,
    record_type 	VARCHAR(255) NOT NULL,
    record_amount 	DECIMAL(10,2) NOT NULL,
    PRIMARY KEY(record_id)
);

CREATE TABLE IF NOT EXISTS Recipient(
    recipient_id 		INT NOT NULL AUTO_INCREMENT,
    recipient_name 		VARCHAR(255) NOT NULL,
    PRIMARY KEY(recipient_id),
           UNIQUE KEY(recipient_name)
);

CREATE TABLE IF NOT EXISTS Material(
    material_id 	INT NOT NULL AUTO_INCREMENT,
    material_name 	VARCHAR(255) NOT NULL,
    PRIMARY KEY(material_id),
    UNIQUE KEY(material_name)
);

CREATE TABLE IF NOT EXISTS Main_Category(
    main_category_id 	INT NOT NULL AUTO_INCREMENT,
    main_category_name 	VARCHAR(255) NOT NULL,
    PRIMARY KEY(main_category_id)
);

CREATE TABLE IF NOT EXISTS Sub_Category(
    sub_category_id 	INT NOT NULL AUTO_INCREMENT,
    main_category_id 	INT NOT NULL,
    sub_category_name 	VARCHAR(255) NOT NULL,
    PRIMARY KEY(sub_category_id, main_category_id),
    FOREIGN KEY(main_category_id) REFERENCES Main_Category(main_category_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS In_Category(
    sub_category_id 	INT NOT NULL,
    main_category_id 	INT NOT NULL,
    product_id 		INT NOT NULL,
    PRIMARY KEY(sub_category_id, main_category_id, product_id),
    FOREIGN KEY(main_category_id) REFERENCES Main_Category(main_category_id) ON DELETE CASCADE,
	      FOREIGN KEY(sub_category_id) REFERENCES Sub_Category(sub_category_id) ON DELETE CASCADE,
    FOREIGN KEY(product_id) REFERENCES Product(product_id)ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Has_Reported(
    customer_id 		INT NOT NULL,
    small_business_id 	INT NOT NULL,
    report_description 	VARCHAR(255),
    report_date 		DATE,
    PRIMARY KEY(customer_id, small_business_id),
    FOREIGN KEY(customer_id) REFERENCES Customer(user_id) ON DELETE CASCADE,
    FOREIGN KEY(small_business_id) REFERENCES Small_Business(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Ban(
    admin_id 			INT NOT NULL,
    small_business_id 	INT NOT NULL,
    ban_duration 		VARCHAR(255),
    ban_date 			DATE,
    PRIMARY KEY(admin_id, small_business_id),
    FOREIGN KEY(admin_id) REFERENCES Admin(user_id) ON DELETE CASCADE,
    FOREIGN KEY(small_business_id) REFERENCES Small_Business(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS System_Report(
    report_id 		INT NOT NULL AUTO_INCREMENT,
    report_title 		VARCHAR(255) NOT NULL,
    report_date 		DATE NOT NULL,    
    report_results		VARCHAR(255),
    PRIMARY KEY(report_id)
    );

CREATE TABLE IF NOT EXISTS Create_Report(
    admin_id 		INT NOT NULL,
    report_id 	INT NOT NULL,
    PRIMARY KEY(admin_id, report_id),
    FOREIGN KEY(admin_id) REFERENCES Admin(user_id) ON DELETE CASCADE,
    FOREIGN KEY(report_id) REFERENCES System_Report(report_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Rate(
    customer_id 	INT NOT NULL,
    product_id 	INT NOT NULL,
    star 		DECIMAL(2,1) NOT NULL,
    PRIMARY KEY(customer_id, product_id),
    FOREIGN KEY(customer_id) REFERENCES Customer(user_id) ON DELETE CASCADE,
    FOREIGN KEY(product_id) REFERENCES Product(product_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Wish(
    customer_id 	INT NOT NULL,
    product_id 	INT NOT NULL,
    PRIMARY KEY(customer_id, product_id),
    FOREIGN KEY(customer_id) REFERENCES Customer(user_id) ON DELETE CASCADE,
    FOREIGN KEY(product_id) REFERENCES Product(product_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Add_To_Shopping_Cart(
    customer_id 	INT NOT NULL,
    product_id 	INT NOT NULL,
    count 		INT NOT NULL,
    PRIMARY KEY(customer_id, product_id),
    FOREIGN KEY(customer_id) REFERENCES Customer(user_id) ON DELETE CASCADE,
    FOREIGN KEY(product_id) REFERENCES Product(product_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Select_Product(
    customer_id 	INT NOT NULL,
    product_id 	INT NOT NULL,
    PRIMARY KEY(customer_id, product_id),
    FOREIGN KEY(customer_id) REFERENCES Customer(user_id) ON DELETE CASCADE,
    FOREIGN KEY(product_id) REFERENCES Product(product_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Business_Has_Record(
    small_business_id 	INT NOT NULL,
    record_id 		INT NOT NULL,
    PRIMARY KEY(record_id, small_business_id),
    FOREIGN KEY(small_business_id) REFERENCES Small_Business(user_id) ON DELETE CASCADE,
    FOREIGN KEY(record_id) REFERENCES Balance_Record(record_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Customer_Has_Record(
    customer_id 		INT NOT NULL,
    record_id 		INT NOT NULL,
    PRIMARY KEY(record_id, customer_id),
    FOREIGN KEY(customer_id) REFERENCES Customer(user_id) ON DELETE CASCADE,
    FOREIGN KEY(record_id) REFERENCES Balance_Record(record_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Transaction(
    product_id 		INT NOT NULL,
    customer_id 		INT NOT NULL,
    small_business_id 	INT NOT NULL,
    transaction_date 	DATE NOT NULL,
    count 			INT NOT NULL,
    transaction_status 	VARCHAR(255)NOT NULL,
    PRIMARY KEY(product_id, small_business_id),
    FOREIGN KEY(product_id) REFERENCES Product(product_id) ON DELETE CASCADE,
    FOREIGN KEY(small_business_id) REFERENCES Small_Business(user_id) ON DELETE CASCADE,
    FOREIGN KEY(customer_id) REFERENCES Customer(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Add_Amount(
    product_id 		INT NOT NULL,
    small_business_id 	INT NOT NULL,
    amount 			INT NOT NULL,
    PRIMARY KEY(product_id, small_business_id),
    FOREIGN KEY(product_id) REFERENCES Product(product_id) ON DELETE CASCADE,
    FOREIGN KEY(small_business_id) REFERENCES Small_Business(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Add_Product(
    product_id 		INT NOT NULL,
    small_business_id 	INT NOT NULL,
    post_date 		DATE NOT NULL,
    PRIMARY KEY(product_id, small_business_id),
    FOREIGN KEY(product_id) REFERENCES Product(product_id) ON DELETE CASCADE,
    FOREIGN KEY(small_business_id) REFERENCES Small_Business(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Made_By(
    product_id 	INT NOT NULL,
    material_id 	INT NOT NULL,
    PRIMARY KEY(product_id, material_id),
    FOREIGN KEY(product_id) REFERENCES Product(product_id) ON DELETE CASCADE,
    FOREIGN KEY(material_id) REFERENCES Material(material_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Is_For(
    product_id 	INT NOT NULL,
    recipient_id 	INT NOT NULL,
    PRIMARY KEY(product_id, recipient_id),
    FOREIGN KEY(product_id) REFERENCES Product(product_id) ON DELETE CASCADE,
    FOREIGN KEY(recipient_id) REFERENCES Recipient(recipient_id) ON DELETE CASCADE
);


DELIMITER //

CREATE PROCEDURE CartAdder(IN customer_id INT, IN product_id INT, IN product_amount INT)
BEGIN
    DECLARE product_amount INT;

    SELECT COUNT(*) INTO product_amount 
    FROM Add_To_Shopping_Cart AS A 
    WHERE A.product_id = product_id AND A.customer_id = customer_id;

    IF product_amount > 0 THEN
        UPDATE Add_To_Shopping_Cart 
        SET count = count + product_amount 
        WHERE product_id = product_id AND customer_id = customer_id;

        UPDATE Product
        SET amount = amount - product_amount
        WHERE product_id = product_id AND customer_id = customer_id;
    ELSE
        INSERT INTO Add_To_Shopping_Cart (customer_id, product_id, count) 
        VALUES (customer_id, product_id, product_amount);
    END IF;
END;//

CREATE PROCEDURE ProductPrinter(IN per_page INT, IN start_index INT)
BEGIN
    SELECT P.product_id, P.title, P.description, P.price, P.amount, 
           ROUND(COALESCE(R.avg_rating, 0), 1) AS average_rating, 
           COALESCE(R.num_rating, 0) AS number_of_rating, P.images
    FROM Product P
    LEFT JOIN (
        SELECT product_id, AVG(star) AS avg_rating, COUNT(*) AS num_rating
        FROM Rate
        GROUP BY product_id
    ) R ON P.product_id = R.product_id
    ORDER BY P.product_id DESC
    LIMIT per_page OFFSET start_index;
END;//

CREATE PROCEDURE ProductFilter(
    IN per_page INT, 
    IN start_index INT, 
    IN filter_business_name VARCHAR(255), 
    IN filter_min_price DECIMAL(10,2), 
    IN filter_max_price DECIMAL(10,2), 
    IN sort_method INT
)
BEGIN
    SELECT P.product_id, P.title, P.description, P.price, P.amount, 
           ROUND(COALESCE(R.avg_rating, 0), 1) AS average_rating, 
           COALESCE(R.num_rating, 0) AS number_of_rating, P.images
    FROM Product P
    LEFT JOIN (
        SELECT product_id, AVG(star) AS avg_rating, COUNT(*) AS num_rating
        FROM Rate
        GROUP BY product_id
    ) R ON P.product_id = R.product_id
    JOIN Add_Product AP ON P.product_id = AP.product_id
    JOIN Small_Business SB ON AP.small_business_id = SB.user_id
    WHERE SB.business_name LIKE CONCAT('%', filter_business_name, '%')
    AND P.price BETWEEN filter_min_price AND filter_max_price
    ORDER BY 
        CASE 
            WHEN sort_method = 0 THEN P.product_id 
            WHEN sort_method = 1 THEN P.price 
            WHEN sort_method = 2 THEN P.price 
            WHEN sort_method = 3 THEN P.product_id 
            WHEN sort_method = 4 THEN P.product_id 
        END DESC,
        CASE
            WHEN sort_method = 2 THEN P.price 
            WHEN sort_method = 4 THEN P.product_id 
        END ASC
    LIMIT per_page OFFSET start_index;
END;//

DELIMITER ;

CREATE VIEW UserTransactions AS
SELECT 
    T.product_id,
    P.title AS product_title,
    P.images AS product_image,
    P.description AS product_description,
    P.price AS product_price,
    T.small_business_id,
    SB.business_name,
    T.transaction_date,
    T.count,
    T.transaction_status,
    R.star AS user_rating
FROM 
    Transaction T
JOIN 
    Product P ON T.product_id = P.product_id
JOIN 
    Customer C ON T.customer_id = C.user_id
JOIN 
    User U ON C.user_id = U.user_id
JOIN 
    Small_Business SB ON T.small_business_id = SB.user_id
LEFT JOIN 
    Rate R ON T.customer_id = R.customer_id AND T.product_id = R.product_id;

-- Insert Users (Customers, Businesses, and Admin)
INSERT INTO User (user_name, email, password, user_type, address, phone_number, active)
VALUES 
('Admin', 'admin@example.com', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Admin', 'Admin Address', '555-0301', 1),
('Alice', 'alice@example.com', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Customer', '123 Main St', '555-0101', 1),
('Bob', 'bob@example.com', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Customer', '456 Elm St', '555-0102', 1),
('Charlie', 'charlie@example.com', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Customer', '789 Maple St', '555-0103', 1),
('David', 'david@example.com', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Customer', '101 Oak St', '555-0104', 1),
('Eve', 'eve@example.com', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Customer', '202 Pine St', '555-0105', 1),
('Biz1', 'biz1@example.com', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Small_Business', '303 Birch St', '555-0201', 1),
('Biz2', 'biz2@example.com', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Small_Business', '404 Cedar St', '555-0202', 1),
('Biz3', 'biz3@example.com', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Small_Business', '505 Dogwood St', '555-0203', 1),
('Biz4', 'biz4@example.com', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Small_Business', '606 Fir St', '555-0204', 1),
('Biz5', 'biz5@example.com', '8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92', 'Small_Business', '707 Elm St', '555-0205', 1);

-- Insert Customers
INSERT INTO Customer (user_id, picture, payment_info, balance)
VALUES 
((SELECT user_id FROM User WHERE email='alice@example.com'), NULL, 'Credit Card', 100.00),
((SELECT user_id FROM User WHERE email='bob@example.com'), NULL, 'Credit Card', 100.00),
((SELECT user_id FROM User WHERE email='charlie@example.com'), NULL, 'Credit Card', 100.00),
((SELECT user_id FROM User WHERE email='david@example.com'), NULL, 'Credit Card', 100.00),
((SELECT user_id FROM User WHERE email='eve@example.com'), NULL, 'Credit Card', 100.00);

-- Insert Admin
INSERT INTO Admin (user_id)
VALUES 
((SELECT user_id FROM User WHERE email='admin@example.com'));

-- Insert Small Businesses
INSERT INTO Small_Business (user_id, business_name, title, description, picture, balance)
VALUES 
((SELECT user_id FROM User WHERE email='biz1@example.com'), 'Biz1', 'Biz1 Title', 'Biz1 Description', NULL, 100.00),
((SELECT user_id FROM User WHERE email='biz2@example.com'), 'Biz2', 'Biz2 Title', 'Biz2 Description', NULL, 200.00),
((SELECT user_id FROM User WHERE email='biz3@example.com'), 'Biz3', 'Biz3 Title', 'Biz3 Description', NULL, 300.00),
((SELECT user_id FROM User WHERE email='biz4@example.com'), 'Biz4', 'Biz4 Title', 'Biz4 Description', NULL, 400.00),
((SELECT user_id FROM User WHERE email='biz5@example.com'), 'Biz5', 'Biz5 Title', 'Biz5 Description', NULL, 500.00);

-- Insert Products for Businesses
INSERT INTO Product (title, description, price, amount, images)
VALUES 
('Product1 Biz1', 'Description Product1 Biz1', 10.00, 50, NULL),
('Product2 Biz1', 'Description Product2 Biz1', 20.00, 30, NULL),
('Product1 Biz2', 'Description Product1 Biz2', 15.00, 40, NULL),
('Product2 Biz2', 'Description Product2 Biz2', 25.00, 20, NULL),
('Product1 Biz3', 'Description Product1 Biz3', 30.00, 10, NULL),
('Product2 Biz3', 'Description Product2 Biz3', 35.00, 5, NULL),
('Product1 Biz4', 'Description Product1 Biz4', 40.00, 60, NULL),
('Product2 Biz4', 'Description Product2 Biz4', 45.00, 15, NULL),
('Product1 Biz5', 'Description Product1 Biz5', 50.00, 25, NULL),
('Product2 Biz5', 'Description Product2 Biz5', 55.00, 35, NULL);

-- Link Products with Businesses
INSERT INTO Add_Product (product_id, small_business_id, post_date)
VALUES 
((SELECT product_id FROM Product WHERE title='Product1 Biz1'), (SELECT user_id FROM User WHERE email='biz1@example.com'), '2023-01-01'),
((SELECT product_id FROM Product WHERE title='Product2 Biz1'), (SELECT user_id FROM User WHERE email='biz1@example.com'), '2023-01-01'),
((SELECT product_id FROM Product WHERE title='Product1 Biz2'), (SELECT user_id FROM User WHERE email='biz2@example.com'), '2023-01-01'),
((SELECT product_id FROM Product WHERE title='Product2 Biz2'), (SELECT user_id FROM User WHERE email='biz2@example.com'), '2023-01-01'),
((SELECT product_id FROM Product WHERE title='Product1 Biz3'), (SELECT user_id FROM User WHERE email='biz3@example.com'), '2023-01-01'),
((SELECT product_id FROM Product WHERE title='Product2 Biz3'), (SELECT user_id FROM User WHERE email='biz3@example.com'), '2023-01-01'),
((SELECT product_id FROM Product WHERE title='Product1 Biz4'), (SELECT user_id FROM User WHERE email='biz4@example.com'), '2023-01-01'),
((SELECT product_id FROM Product WHERE title='Product2 Biz4'), (SELECT user_id FROM User WHERE email='biz4@example.com'), '2023-01-01'),
((SELECT product_id FROM Product WHERE title='Product1 Biz5'), (SELECT user_id FROM User WHERE email='biz5@example.com'), '2023-01-01'),
((SELECT product_id FROM Product WHERE title='Product2 Biz5'), (SELECT user_id FROM User WHERE email='biz5@example.com'), '2023-01-01');

-- Insert Transactions
INSERT INTO Transaction (product_id, customer_id, small_business_id, transaction_date, count, transaction_status)
VALUES 
((SELECT product_id FROM Product WHERE title='Product1 Biz1'), (SELECT user_id FROM User WHERE email='alice@example.com'), (SELECT user_id FROM User WHERE email='biz1@example.com'), '2023-05-01', 2, 'Completed'),
((SELECT product_id FROM Product WHERE title='Product2 Biz1'), (SELECT user_id FROM User WHERE email='alice@example.com'), (SELECT user_id FROM User WHERE email='biz1@example.com'), '2023-05-01', 3, 'Completed'),
((SELECT product_id FROM Product WHERE title='Product1 Biz2'), (SELECT user_id FROM User WHERE email='bob@example.com'), (SELECT user_id FROM User WHERE email='biz2@example.com'), '2023-05-02', 1, 'Completed'),
((SELECT product_id FROM Product WHERE title='Product2 Biz2'), (SELECT user_id FROM User WHERE email='charlie@example.com'), (SELECT user_id FROM User WHERE email='biz2@example.com'), '2023-05-02', 2, 'Completed'),
((SELECT product_id FROM Product WHERE title='Product1 Biz3'), (SELECT user_id FROM User WHERE email='david@example.com'), (SELECT user_id FROM User WHERE email='biz3@example.com'), '2023-05-03', 3, 'Completed'),
((SELECT product_id FROM Product WHERE title='Product2 Biz3'), (SELECT user_id FROM User WHERE email='eve@example.com'), (SELECT user_id FROM User WHERE email='biz3@example.com'), '2023-05-03', 1, 'Completed');

-- Insert Reports
INSERT INTO Has_Reported (customer_id, small_business_id, report_description, report_date)
VALUES 
((SELECT user_id FROM User WHERE email='alice@example.com'), (SELECT user_id FROM User WHERE email='biz1@example.com'), 'Issue with product quality', '2023-05-01'),
((SELECT user_id FROM User WHERE email='bob@example.com'), (SELECT user_id FROM User WHERE email='biz2@example.com'), 'Late delivery', '2023-05-02'),
((SELECT user_id FROM User WHERE email='charlie@example.com'), (SELECT user_id FROM User WHERE email='biz2@example.com'), 'Wrong item delivered', '2023-05-02');
