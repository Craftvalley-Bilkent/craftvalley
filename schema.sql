CREATE DATABASE IF NOT EXISTS cvdb CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

USE cvdb;

CREATE TABLE IF NOT EXISTS User (
    user_id INT NOT NULL AUTO_INCREMENT,
    user_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    user_type VARCHAR(255) NOT NULL,
    address VARCHAR(255),
    phone_number VARCHAR(20) NOT NULL,
    active INT NOT NULL CHECK (active IN (0, 1)),
    PRIMARY KEY (user_id),
    UNIQUE KEY (email),
    UNIQUE KEY (phone_number)
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

CREATE TABLE IF NOT EXISTS Admin (
    user_id INT NOT NULL,
    PRIMARY KEY (user_id),
    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE
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

CREATE TABLE IF NOT EXISTS In_Category (
    sub_category_id INT NOT NULL,
    main_category_id INT NOT NULL,
    product_id INT NOT NULL,
    PRIMARY KEY (sub_category_id, main_category_id, product_id),
    FOREIGN KEY (main_category_id) REFERENCES Main_Category(main_category_id) ON DELETE CASCADE,
    FOREIGN KEY (sub_category_id) REFERENCES Sub_Category(sub_category_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES Product(product_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Has_Reported (
    customer_id INT NOT NULL,
    small_business_id INT NOT NULL,
    report_description VARCHAR(255),
    report_date DATE,
    PRIMARY KEY (customer_id, small_business_id),
    FOREIGN KEY (customer_id) REFERENCES Customer(user_id) ON DELETE CASCADE,
    FOREIGN KEY (small_business_id) REFERENCES Small_Business(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Ban (
    admin_id INT NOT NULL,
    small_business_id INT NOT NULL,
    ban_duration VARCHAR(255),
    ban_date DATE,
    PRIMARY KEY (admin_id, small_business_id),
    FOREIGN KEY (admin_id) REFERENCES Admin(user_id) ON DELETE CASCADE,
    FOREIGN KEY (small_business_id) REFERENCES Small_Business(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS System_Report(
    report_id 		INT NOT NULL AUTO_INCREMENT,
    report_title 		VARCHAR(255) NOT NULL,
    report_date 		DATE NOT NULL,    
    report_results		VARCHAR(255),
    PRIMARY KEY(report_id)
    );

CREATE TABLE IF NOT EXISTS Create_Report (
    admin_id INT NOT NULL,
    report_id INT NOT NULL,
    PRIMARY KEY (admin_id, report_id),
    FOREIGN KEY (admin_id) REFERENCES Admin(user_id) ON DELETE CASCADE,
    FOREIGN KEY (report_id) REFERENCES System_Report(report_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Rate (
    customer_id INT NOT NULL,
    product_id INT NOT NULL,
    star DECIMAL(2, 1) NOT NULL,
    PRIMARY KEY (customer_id, product_id),
    FOREIGN KEY (customer_id) REFERENCES Customer(user_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES Product(product_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Wish (
    customer_id INT NOT NULL,
    product_id INT NOT NULL,
    PRIMARY KEY (customer_id, product_id),
    FOREIGN KEY (customer_id) REFERENCES Customer(user_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES Product(product_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Add_To_Shopping_Cart (
    customer_id INT NOT NULL,
    product_id INT NOT NULL,
    count INT NOT NULL,
    PRIMARY KEY (customer_id, product_id),
    FOREIGN KEY (customer_id) REFERENCES Customer(user_id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES Product(product_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Business_Has_Record (
    small_business_id INT NOT NULL,
    record_id INT NOT NULL,
    PRIMARY KEY (record_id, small_business_id),
    FOREIGN KEY (small_business_id) REFERENCES Small_Business(user_id) ON DELETE CASCADE,
    FOREIGN KEY (record_id) REFERENCES Balance_Record(record_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Customer_Has_Record (
    customer_id INT NOT NULL,
    record_id INT NOT NULL,
    PRIMARY KEY (record_id, customer_id),
    FOREIGN KEY (customer_id) REFERENCES Customer(user_id) ON DELETE CASCADE,
    FOREIGN KEY (record_id) REFERENCES Balance_Record(record_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Transaction (
    product_id INT NOT NULL,
    customer_id INT NOT NULL,
    small_business_id INT NOT NULL,
    transaction_date DATE NOT NULL,
    count INT NOT NULL,
    transaction_status VARCHAR(255) NOT NULL,
    PRIMARY KEY (product_id, small_business_id),
    FOREIGN KEY (product_id) REFERENCES Product(product_id) ON DELETE CASCADE,
    FOREIGN KEY (small_business_id) REFERENCES Small_Business(user_id) ON DELETE CASCADE,
    FOREIGN KEY (customer_id) REFERENCES Customer(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Add_Product (
    product_id INT NOT NULL,
    small_business_id INT NOT NULL,
    post_date DATE NOT NULL,
    PRIMARY KEY (product_id, small_business_id),
    FOREIGN KEY (product_id) REFERENCES Product(product_id) ON DELETE CASCADE,
    FOREIGN KEY (small_business_id) REFERENCES Small_Business(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Made_By (
    product_id INT NOT NULL,
    material_id INT NOT NULL,
    PRIMARY KEY (product_id, material_id),
    FOREIGN KEY (product_id) REFERENCES Product(product_id) ON DELETE CASCADE,
    FOREIGN KEY (material_id) REFERENCES Material(material_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Is_For (
    product_id INT NOT NULL,
    recipient_id INT NOT NULL,
    PRIMARY KEY (product_id, recipient_id),
    FOREIGN KEY (product_id) REFERENCES Product(product_id) ON DELETE CASCADE,
    FOREIGN KEY (recipient_id) REFERENCES Recipient(recipient_id) ON DELETE CASCADE
);


DELIMITER //

CREATE PROCEDURE CartAdder(IN customer_id INT, IN product_id INT, IN product_amount INT)
BEGIN
    DECLARE product_amount_in_cart INT;

    SELECT COUNT(*) INTO product_amount_in_cart 
    FROM Add_To_Shopping_Cart AS A 
    WHERE A.product_id = product_id AND A.customer_id = customer_id;

    IF product_amount_in_cart > 0 THEN
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
            WHEN sort_method = 3 THEN P.product_id 
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
    R.star AS user_rating,
    U.user_id AS customer_id
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

-- Insert Reports
INSERT INTO Has_Reported (customer_id, small_business_id, report_description, report_date)
VALUES 
((SELECT user_id FROM User WHERE email='alice@example.com'), (SELECT user_id FROM User WHERE email='biz1@example.com'), 'Issue with product quality', '2023-05-01'),
((SELECT user_id FROM User WHERE email='bob@example.com'), (SELECT user_id FROM User WHERE email='biz2@example.com'), 'Late delivery', '2023-05-02'),
((SELECT user_id FROM User WHERE email='charlie@example.com'), (SELECT user_id FROM User WHERE email='biz2@example.com'), 'Wrong item delivered', '2023-05-02');

-- Insert Main Categories
INSERT INTO Main_Category (main_category_name)
VALUES 
('Accessories'),
('Art & Collectibles'),
('Clothing'),
('Craft'),
('Electronics'),
('Gifts'),
('Home & Living');

-- Insert Sub Categories
INSERT INTO Sub_Category (main_category_id, sub_category_name)
VALUES 
((SELECT main_category_id FROM Main_Category WHERE main_category_name = 'Accessories'), 'Jewelry'),
((SELECT main_category_id FROM Main_Category WHERE main_category_name = 'Accessories'), 'Bags & Purses'),
((SELECT main_category_id FROM Main_Category WHERE main_category_name = 'Accessories'), 'Watches'),
((SELECT main_category_id FROM Main_Category WHERE main_category_name = 'Accessories'), 'Hats'),
((SELECT main_category_id FROM Main_Category WHERE main_category_name = 'Accessories'), 'Belts'),
((SELECT main_category_id FROM Main_Category WHERE main_category_name = 'Art & Collectibles'), 'Paintings'),
((SELECT main_category_id FROM Main_Category WHERE main_category_name = 'Art & Collectibles'), 'Photography'),
((SELECT main_category_id FROM Main_Category WHERE main_category_name = 'Art & Collectibles'), 'Sculptures'),
((SELECT main_category_id FROM Main_Category WHERE main_category_name = 'Art & Collectibles'), 'Prints'),
((SELECT main_category_id FROM Main_Category WHERE main_category_name = 'Clothing'), 'Women'),
((SELECT main_category_id FROM Main_Category WHERE main_category_name = 'Clothing'), 'Men'),
((SELECT main_category_id FROM Main_Category WHERE main_category_name = 'Clothing'), 'Child'),
((SELECT main_category_id FROM Main_Category WHERE main_category_name = 'Craft'), 'Knitting & Crochet'),
((SELECT main_category_id FROM Main_Category WHERE main_category_name = 'Craft'), 'Sewing'),
((SELECT main_category_id FROM Main_Category WHERE main_category_name = 'Craft'), 'Paper Craft'),
((SELECT main_category_id FROM Main_Category WHERE main_category_name = 'Craft'), 'Woodworking'),
((SELECT main_category_id FROM Main_Category WHERE main_category_name = 'Craft'), 'Jewelry Making'),
((SELECT main_category_id FROM Main_Category WHERE main_category_name = 'Electronics'), 'Gadgets'),
((SELECT main_category_id FROM Main_Category WHERE main_category_name = 'Electronics'), 'Computers'),
((SELECT main_category_id FROM Main_Category WHERE main_category_name = 'Electronics'), 'Mobile Phones'),
((SELECT main_category_id FROM Main_Category WHERE main_category_name = 'Gifts'), 'Birthday Gifts'),
((SELECT main_category_id FROM Main_Category WHERE main_category_name = 'Gifts'), 'Wedding Gifts'),
((SELECT main_category_id FROM Main_Category WHERE main_category_name = 'Gifts'), 'Holiday Gifts'),
((SELECT main_category_id FROM Main_Category WHERE main_category_name = 'Home & Living'), 'Furniture'),
((SELECT main_category_id FROM Main_Category WHERE main_category_name = 'Home & Living'), 'Home Decor'),
((SELECT main_category_id FROM Main_Category WHERE main_category_name = 'Home & Living'), 'Kitchen & Dining'),
((SELECT main_category_id FROM Main_Category WHERE main_category_name = 'Home & Living'), 'Bedding');

-- Insert Products for Biz1
INSERT INTO Product (title, description, price, amount, images)
VALUES 
('Jewelry Set - Biz1', 'Description Jewelry Set Biz1', 10.00, 50, NULL),
('Bags & Purses - Biz1', 'Description Bags & Purses Biz1', 15.00, 30, NULL),
('Watches - Biz1', 'Description Watches Biz1', 20.00, 25, NULL),
('Hats - Biz1', 'Description Hats Biz1', 12.00, 40, NULL),
('Belts - Biz1', 'Description Belts Biz1', 8.00, 50, NULL),
('Paintings - Biz1', 'Description Paintings Biz1', 30.00, 20, NULL),
('Photography - Biz1', 'Description Photography Biz1', 25.00, 10, NULL),
('Sculptures - Biz1', 'Description Sculptures Biz1', 40.00, 15, NULL);

-- Insert Products for Biz2
INSERT INTO Product (title, description, price, amount, images)
VALUES 
('Womens Dress - Biz2', 'Description Womens Dress Biz2', 50.00, 30, NULL),
('Mens Shirt - Biz2', 'Description Mens Shirt Biz2', 40.00, 25, NULL),
('Childs Outfit - Biz2', 'Description Childs Outfit Biz2', 30.00, 20, NULL),
('Knitting & Crochet - Biz2', 'Description Knitting & Crochet Biz2', 15.00, 50, NULL),
('Sewing - Biz2', 'Description Sewing Biz2', 20.00, 35, NULL),
('Paper Craft - Biz2', 'Description Paper Craft Biz2', 25.00, 30, NULL),
('Woodworking - Biz2', 'Description Woodworking Biz2', 35.00, 20, NULL),
('Jewelry Making - Biz2', 'Description Jewelry Making Biz2', 45.00, 15, NULL);

-- Insert Products for Biz3
INSERT INTO Product (title, description, price, amount, images)
VALUES 
('Gadgets - Biz3', 'Description Gadgets Biz3', 60.00, 25, NULL),
('Computers - Biz3', 'Description Computers Biz3', 500.00, 10, NULL),
('Mobile Phones - Biz3', 'Description Mobile Phones Biz3', 300.00, 15, NULL),
('Birthday Gifts - Biz3', 'Description Birthday Gifts Biz3', 20.00, 40, NULL),
('Wedding Gifts - Biz3', 'Description Wedding Gifts Biz3', 30.00, 35, NULL),
('Holiday Gifts - Biz3', 'Description Holiday Gifts Biz3', 25.00, 30, NULL),
('Furniture - Biz3', 'Description Furniture Biz3', 200.00, 20, NULL),
('Home Decor - Biz3', 'Description Home Decor Biz3', 50.00, 25, NULL);

-- Insert Products for Biz4
INSERT INTO Product (title, description, price, amount, images)
VALUES 
('Kitchen & Dining - Biz4', 'Description Kitchen & Dining Biz4', 100.00, 30, NULL),
('Bedding - Biz4', 'Description Bedding Biz4', 150.00, 25, NULL),
('Jewelry - Biz4', 'Description Jewelry Biz4', 60.00, 20, NULL),
('Bags & Purses - Biz4', 'Description Bags & Purses Biz4', 70.00, 15, NULL),
('Watches - Biz4', 'Description Watches Biz4', 80.00, 10, NULL),
('Hats - Biz4', 'Description Hats Biz4', 90.00, 25, NULL),
('Belts - Biz4', 'Description Belts Biz4', 40.00, 30, NULL),
('Paintings - Biz4', 'Description Paintings Biz4', 110.00, 20, NULL);

-- Insert Products for Biz5
INSERT INTO Product (title, description, price, amount, images)
VALUES 
('Photography - Biz5', 'Description Photography Biz5', 90.00, 15, NULL),
('Sculptures - Biz5', 'Description Sculptures Biz5', 120.00, 10, NULL),
('Womens Dress - Biz5', 'Description Womens Dress Biz5', 130.00, 5, NULL),
('Mens Shirt - Biz5', 'Description Mens Shirt Biz5', 140.00, 20, NULL),
('Childs Outfit - Biz5', 'Description Childs Outfit Biz5', 150.00, 25, NULL),
('Knitting & Crochet - Biz5', 'Description Knitting & Crochet Biz5', 160.00, 30, NULL),
('Sewing - Biz5', 'Description Sewing Biz5', 170.00, 35, NULL),
('Paper Craft - Biz5', 'Description Paper Craft Biz5', 180.00, 40, NULL);

-- Link Products with Businesses
INSERT INTO Add_Product (product_id, small_business_id, post_date)
VALUES 
((SELECT product_id FROM Product WHERE title='Jewelry Set - Biz1'), (SELECT user_id FROM User WHERE email='biz1@example.com'), '2023-01-01'),
((SELECT product_id FROM Product WHERE title='Bags & Purses - Biz1'), (SELECT user_id FROM User WHERE email='biz1@example.com'), '2023-01-01'),
((SELECT product_id FROM Product WHERE title='Watches - Biz1'), (SELECT user_id FROM User WHERE email='biz1@example.com'), '2023-01-01'),
((SELECT product_id FROM Product WHERE title='Hats - Biz1'), (SELECT user_id FROM User WHERE email='biz1@example.com'), '2023-01-01'),
((SELECT product_id FROM Product WHERE title='Belts - Biz1'), (SELECT user_id FROM User WHERE email='biz1@example.com'), '2023-01-01'),
((SELECT product_id FROM Product WHERE title='Paintings - Biz1'), (SELECT user_id FROM User WHERE email='biz1@example.com'), '2023-01-01'),
((SELECT product_id FROM Product WHERE title='Photography - Biz1'), (SELECT user_id FROM User WHERE email='biz1@example.com'), '2023-01-01'),
((SELECT product_id FROM Product WHERE title='Sculptures - Biz1'), (SELECT user_id FROM User WHERE email='biz1@example.com'), '2023-01-01'),

((SELECT product_id FROM Product WHERE title='Womens Dress - Biz2'), (SELECT user_id FROM User WHERE email='biz2@example.com'), '2023-01-01'),
((SELECT product_id FROM Product WHERE title='Mens Shirt - Biz2'), (SELECT user_id FROM User WHERE email='biz2@example.com'), '2023-01-01'),
((SELECT product_id FROM Product WHERE title='Childs Outfit - Biz2'), (SELECT user_id FROM User WHERE email='biz2@example.com'), '2023-01-01'),
((SELECT product_id FROM Product WHERE title='Knitting & Crochet - Biz2'), (SELECT user_id FROM User WHERE email='biz2@example.com'), '2023-01-01'),
((SELECT product_id FROM Product WHERE title='Sewing - Biz2'), (SELECT user_id FROM User WHERE email='biz2@example.com'), '2023-01-01'),
((SELECT product_id FROM Product WHERE title='Paper Craft - Biz2'), (SELECT user_id FROM User WHERE email='biz2@example.com'), '2023-01-01'),
((SELECT product_id FROM Product WHERE title='Woodworking - Biz2'), (SELECT user_id FROM User WHERE email='biz2@example.com'), '2023-01-01'),
((SELECT product_id FROM Product WHERE title='Jewelry Making - Biz2'), (SELECT user_id FROM User WHERE email='biz2@example.com'), '2023-01-01'),

((SELECT product_id FROM Product WHERE title='Gadgets - Biz3'), (SELECT user_id FROM User WHERE email='biz3@example.com'), '2023-01-01'),
((SELECT product_id FROM Product WHERE title='Computers - Biz3'), (SELECT user_id FROM User WHERE email='biz3@example.com'), '2023-01-01'),
((SELECT product_id FROM Product WHERE title='Mobile Phones - Biz3'), (SELECT user_id FROM User WHERE email='biz3@example.com'), '2023-01-01'),
((SELECT product_id FROM Product WHERE title='Birthday Gifts - Biz3'), (SELECT user_id FROM User WHERE email='biz3@example.com'), '2023-01-01'),
((SELECT product_id FROM Product WHERE title='Wedding Gifts - Biz3'), (SELECT user_id FROM User WHERE email='biz3@example.com'), '2023-01-01'),
((SELECT product_id FROM Product WHERE title='Holiday Gifts - Biz3'), (SELECT user_id FROM User WHERE email='biz3@example.com'), '2023-01-01'),
((SELECT product_id FROM Product WHERE title='Furniture - Biz3'), (SELECT user_id FROM User WHERE email='biz3@example.com'), '2023-01-01'),
((SELECT product_id FROM Product WHERE title='Home Decor - Biz3'), (SELECT user_id FROM User WHERE email='biz3@example.com'), '2023-01-01'),

((SELECT product_id FROM Product WHERE title='Kitchen & Dining - Biz4'), (SELECT user_id FROM User WHERE email='biz4@example.com'), '2023-01-01'),
((SELECT product_id FROM Product WHERE title='Bedding - Biz4'), (SELECT user_id FROM User WHERE email='biz4@example.com'), '2023-01-01'),
((SELECT product_id FROM Product WHERE title='Jewelry - Biz4'), (SELECT user_id FROM User WHERE email='biz4@example.com'), '2023-01-01'),
((SELECT product_id FROM Product WHERE title='Bags & Purses - Biz4'), (SELECT user_id FROM User WHERE email='biz4@example.com'), '2023-01-01'),
((SELECT product_id FROM Product WHERE title='Watches - Biz4'), (SELECT user_id FROM User WHERE email='biz4@example.com'), '2023-01-01'),
((SELECT product_id FROM Product WHERE title='Hats - Biz4'), (SELECT user_id FROM User WHERE email='biz4@example.com'), '2023-01-01'),
((SELECT product_id FROM Product WHERE title='Belts - Biz4'), (SELECT user_id FROM User WHERE email='biz4@example.com'), '2023-01-01'),
((SELECT product_id FROM Product WHERE title='Paintings - Biz4'), (SELECT user_id FROM User WHERE email='biz4@example.com'), '2023-01-01'),

((SELECT product_id FROM Product WHERE title='Photography - Biz5'), (SELECT user_id FROM User WHERE email='biz5@example.com'), '2023-01-01'),
((SELECT product_id FROM Product WHERE title='Sculptures - Biz5'), (SELECT user_id FROM User WHERE email='biz5@example.com'), '2023-01-01'),
((SELECT product_id FROM Product WHERE title='Womens Dress - Biz5'), (SELECT user_id FROM User WHERE email='biz5@example.com'), '2023-01-01'),
((SELECT product_id FROM Product WHERE title='Mens Shirt - Biz5'), (SELECT user_id FROM User WHERE email='biz5@example.com'), '2023-01-01'),
((SELECT product_id FROM Product WHERE title='Childs Outfit - Biz5'), (SELECT user_id FROM User WHERE email='biz5@example.com'), '2023-01-01'),
((SELECT product_id FROM Product WHERE title='Knitting & Crochet - Biz5'), (SELECT user_id FROM User WHERE email='biz5@example.com'), '2023-01-01'),
((SELECT product_id FROM Product WHERE title='Sewing - Biz5'), (SELECT user_id FROM User WHERE email='biz5@example.com'), '2023-01-01'),
((SELECT product_id FROM Product WHERE title='Paper Craft - Biz5'), (SELECT user_id FROM User WHERE email='biz5@example.com'), '2023-01-01');

-- Insert into In_Category
INSERT INTO In_Category (sub_category_id, main_category_id, product_id)
VALUES 
((SELECT sub_category_id FROM Sub_Category WHERE sub_category_name='Jewelry'), (SELECT main_category_id FROM Main_Category WHERE main_category_name='Accessories'), (SELECT product_id FROM Product WHERE title='Jewelry Set - Biz1')),
((SELECT sub_category_id FROM Sub_Category WHERE sub_category_name='Bags & Purses'), (SELECT main_category_id FROM Main_Category WHERE main_category_name='Accessories'), (SELECT product_id FROM Product WHERE title='Bags & Purses - Biz1')),
((SELECT sub_category_id FROM Sub_Category WHERE sub_category_name='Watches'), (SELECT main_category_id FROM Main_Category WHERE main_category_name='Accessories'), (SELECT product_id FROM Product WHERE title='Watches - Biz1')),
((SELECT sub_category_id FROM Sub_Category WHERE sub_category_name='Hats'), (SELECT main_category_id FROM Main_Category WHERE main_category_name='Accessories'), (SELECT product_id FROM Product WHERE title='Hats - Biz1')),
((SELECT sub_category_id FROM Sub_Category WHERE sub_category_name='Belts'), (SELECT main_category_id FROM Main_Category WHERE main_category_name='Accessories'), (SELECT product_id FROM Product WHERE title='Belts - Biz1')),
((SELECT sub_category_id FROM Sub_Category WHERE sub_category_name='Paintings'), (SELECT main_category_id FROM Main_Category WHERE main_category_name='Art & Collectibles'), (SELECT product_id FROM Product WHERE title='Paintings - Biz1')),
((SELECT sub_category_id FROM Sub_Category WHERE sub_category_name='Photography'), (SELECT main_category_id FROM Main_Category WHERE main_category_name='Art & Collectibles'), (SELECT product_id FROM Product WHERE title='Photography - Biz1')),
((SELECT sub_category_id FROM Sub_Category WHERE sub_category_name='Sculptures'), (SELECT main_category_id FROM Main_Category WHERE main_category_name='Art & Collectibles'), (SELECT product_id FROM Product WHERE title='Sculptures - Biz1')),

((SELECT sub_category_id FROM Sub_Category WHERE sub_category_name='Women'), (SELECT main_category_id FROM Main_Category WHERE main_category_name='Clothing'), (SELECT product_id FROM Product WHERE title='Womens Dress - Biz2')),
((SELECT sub_category_id FROM Sub_Category WHERE sub_category_name='Men'), (SELECT main_category_id FROM Main_Category WHERE main_category_name='Clothing'), (SELECT product_id FROM Product WHERE title='Mens Shirt - Biz2')),
((SELECT sub_category_id FROM Sub_Category WHERE sub_category_name='Child'), (SELECT main_category_id FROM Main_Category WHERE main_category_name='Clothing'), (SELECT product_id FROM Product WHERE title='Childs Outfit - Biz2')),
((SELECT sub_category_id FROM Sub_Category WHERE sub_category_name='Knitting & Crochet'), (SELECT main_category_id FROM Main_Category WHERE main_category_name='Craft'), (SELECT product_id FROM Product WHERE title='Knitting & Crochet - Biz2')),
((SELECT sub_category_id FROM Sub_Category WHERE sub_category_name='Sewing'), (SELECT main_category_id FROM Main_Category WHERE main_category_name='Craft'), (SELECT product_id FROM Product WHERE title='Sewing - Biz2')),
((SELECT sub_category_id FROM Sub_Category WHERE sub_category_name='Paper Craft'), (SELECT main_category_id FROM Main_Category WHERE main_category_name='Craft'), (SELECT product_id FROM Product WHERE title='Paper Craft - Biz2')),
((SELECT sub_category_id FROM Sub_Category WHERE sub_category_name='Woodworking'), (SELECT main_category_id FROM Main_Category WHERE main_category_name='Craft'), (SELECT product_id FROM Product WHERE title='Woodworking - Biz2')),
((SELECT sub_category_id FROM Sub_Category WHERE sub_category_name='Jewelry Making'), (SELECT main_category_id FROM Main_Category WHERE main_category_name='Craft'), (SELECT product_id FROM Product WHERE title='Jewelry Making - Biz2')),

((SELECT sub_category_id FROM Sub_Category WHERE sub_category_name='Gadgets'), (SELECT main_category_id FROM Main_Category WHERE main_category_name='Electronics'), (SELECT product_id FROM Product WHERE title='Gadgets - Biz3')),
((SELECT sub_category_id FROM Sub_Category WHERE sub_category_name='Computers'), (SELECT main_category_id FROM Main_Category WHERE main_category_name='Electronics'), (SELECT product_id FROM Product WHERE title='Computers - Biz3')),
((SELECT sub_category_id FROM Sub_Category WHERE sub_category_name='Mobile Phones'), (SELECT main_category_id FROM Main_Category WHERE main_category_name='Electronics'), (SELECT product_id FROM Product WHERE title='Mobile Phones - Biz3')),
((SELECT sub_category_id FROM Sub_Category WHERE sub_category_name='Birthday Gifts'), (SELECT main_category_id FROM Main_Category WHERE main_category_name='Gifts'), (SELECT product_id FROM Product WHERE title='Birthday Gifts - Biz3')),
((SELECT sub_category_id FROM Sub_Category WHERE sub_category_name='Wedding Gifts'), (SELECT main_category_id FROM Main_Category WHERE main_category_name='Gifts'), (SELECT product_id FROM Product WHERE title='Wedding Gifts - Biz3')),
((SELECT sub_category_id FROM Sub_Category WHERE sub_category_name='Holiday Gifts'), (SELECT main_category_id FROM Main_Category WHERE main_category_name='Gifts'), (SELECT product_id FROM Product WHERE title='Holiday Gifts - Biz3')),
((SELECT sub_category_id FROM Sub_Category WHERE sub_category_name='Furniture'), (SELECT main_category_id FROM Main_Category WHERE main_category_name='Home & Living'), (SELECT product_id FROM Product WHERE title='Furniture - Biz3')),
((SELECT sub_category_id FROM Sub_Category WHERE sub_category_name='Home Decor'), (SELECT main_category_id FROM Main_Category WHERE main_category_name='Home & Living'), (SELECT product_id FROM Product WHERE title='Home Decor - Biz3')),

((SELECT sub_category_id FROM Sub_Category WHERE sub_category_name='Kitchen & Dining'), (SELECT main_category_id FROM Main_Category WHERE main_category_name='Home & Living'), (SELECT product_id FROM Product WHERE title='Kitchen & Dining - Biz4')),
((SELECT sub_category_id FROM Sub_Category WHERE sub_category_name='Bedding'), (SELECT main_category_id FROM Main_Category WHERE main_category_name='Home & Living'), (SELECT product_id FROM Product WHERE title='Bedding - Biz4')),
((SELECT sub_category_id FROM Sub_Category WHERE sub_category_name='Jewelry'), (SELECT main_category_id FROM Main_Category WHERE main_category_name='Accessories'), (SELECT product_id FROM Product WHERE title='Jewelry - Biz4')),
((SELECT sub_category_id FROM Sub_Category WHERE sub_category_name='Bags & Purses'), (SELECT main_category_id FROM Main_Category WHERE main_category_name='Accessories'), (SELECT product_id FROM Product WHERE title='Bags & Purses - Biz4')),
((SELECT sub_category_id FROM Sub_Category WHERE sub_category_name='Watches'), (SELECT main_category_id FROM Main_Category WHERE main_category_name='Accessories'), (SELECT product_id FROM Product WHERE title='Watches - Biz4')),
((SELECT sub_category_id FROM Sub_Category WHERE sub_category_name='Hats'), (SELECT main_category_id FROM Main_Category WHERE main_category_name='Accessories'), (SELECT product_id FROM Product WHERE title='Hats - Biz4')),
((SELECT sub_category_id FROM Sub_Category WHERE sub_category_name='Belts'), (SELECT main_category_id FROM Main_Category WHERE main_category_name='Accessories'), (SELECT product_id FROM Product WHERE title='Belts - Biz4')),
((SELECT sub_category_id FROM Sub_Category WHERE sub_category_name='Paintings'), (SELECT main_category_id FROM Main_Category WHERE main_category_name='Art & Collectibles'), (SELECT product_id FROM Product WHERE title='Paintings - Biz4')),

((SELECT sub_category_id FROM Sub_Category WHERE sub_category_name='Photography'), (SELECT main_category_id FROM Main_Category WHERE main_category_name='Art & Collectibles'), (SELECT product_id FROM Product WHERE title='Photography - Biz5')),
((SELECT sub_category_id FROM Sub_Category WHERE sub_category_name='Sculptures'), (SELECT main_category_id FROM Main_Category WHERE main_category_name='Art & Collectibles'), (SELECT product_id FROM Product WHERE title='Sculptures - Biz5')),
((SELECT sub_category_id FROM Sub_Category WHERE sub_category_name='Women'), (SELECT main_category_id FROM Main_Category WHERE main_category_name='Clothing'), (SELECT product_id FROM Product WHERE title='Womens Dress - Biz5')),
((SELECT sub_category_id FROM Sub_Category WHERE sub_category_name='Men'), (SELECT main_category_id FROM Main_Category WHERE main_category_name='Clothing'), (SELECT product_id FROM Product WHERE title='Mens Shirt - Biz5')),
((SELECT sub_category_id FROM Sub_Category WHERE sub_category_name='Child'), (SELECT main_category_id FROM Main_Category WHERE main_category_name='Clothing'), (SELECT product_id FROM Product WHERE title='Childs Outfit - Biz5')),
((SELECT sub_category_id FROM Sub_Category WHERE sub_category_name='Knitting & Crochet'), (SELECT main_category_id FROM Main_Category WHERE main_category_name='Craft'), (SELECT product_id FROM Product WHERE title='Knitting & Crochet - Biz5')),
((SELECT sub_category_id FROM Sub_Category WHERE sub_category_name='Sewing'), (SELECT main_category_id FROM Main_Category WHERE main_category_name='Craft'), (SELECT product_id FROM Product WHERE title='Sewing - Biz5')),
((SELECT sub_category_id FROM Sub_Category WHERE sub_category_name='Paper Craft'), (SELECT main_category_id FROM Main_Category WHERE main_category_name='Craft'), (SELECT product_id FROM Product WHERE title='Paper Craft - Biz5'));

-- Insert Transactions
INSERT INTO Transaction (product_id, customer_id, small_business_id, transaction_date, count, transaction_status)
VALUES 
((SELECT product_id FROM Product WHERE title='Jewelry Set - Biz1'), (SELECT user_id FROM User WHERE email='alice@example.com'), (SELECT user_id FROM User WHERE email='biz1@example.com'), '2023-05-01', 2, 'Completed'),
((SELECT product_id FROM Product WHERE title='Bags & Purses - Biz1'), (SELECT user_id FROM User WHERE email='alice@example.com'), (SELECT user_id FROM User WHERE email='biz1@example.com'), '2023-05-01', 3, 'Completed'),
((SELECT product_id FROM Product WHERE title='Watches - Biz1'), (SELECT user_id FROM User WHERE email='bob@example.com'), (SELECT user_id FROM User WHERE email='biz1@example.com'), '2023-05-02', 1, 'Completed'),
((SELECT product_id FROM Product WHERE title='Hats - Biz1'), (SELECT user_id FROM User WHERE email='charlie@example.com'), (SELECT user_id FROM User WHERE email='biz1@example.com'), '2023-05-02', 2, 'Completed'),
((SELECT product_id FROM Product WHERE title='Belts - Biz1'), (SELECT user_id FROM User WHERE email='david@example.com'), (SELECT user_id FROM User WHERE email='biz1@example.com'), '2023-05-03', 3, 'Completed'),
((SELECT product_id FROM Product WHERE title='Paintings - Biz1'), (SELECT user_id FROM User WHERE email='eve@example.com'), (SELECT user_id FROM User WHERE email='biz1@example.com'), '2023-05-03', 1, 'Completed'),

((SELECT product_id FROM Product WHERE title='Womens Dress - Biz2'), (SELECT user_id FROM User WHERE email='alice@example.com'), (SELECT user_id FROM User WHERE email='biz2@example.com'), '2023-05-01', 1, 'Completed'),
((SELECT product_id FROM Product WHERE title='Mens Shirt - Biz2'), (SELECT user_id FROM User WHERE email='bob@example.com'), (SELECT user_id FROM User WHERE email='biz2@example.com'), '2023-05-02', 2, 'Completed'),
((SELECT product_id FROM Product WHERE title='Childs Outfit - Biz2'), (SELECT user_id FROM User WHERE email='charlie@example.com'), (SELECT user_id FROM User WHERE email='biz2@example.com'), '2023-05-02', 1, 'Completed'),
((SELECT product_id FROM Product WHERE title='Knitting & Crochet - Biz2'), (SELECT user_id FROM User WHERE email='david@example.com'), (SELECT user_id FROM User WHERE email='biz2@example.com'), '2023-05-03', 2, 'Completed'),
((SELECT product_id FROM Product WHERE title='Sewing - Biz2'), (SELECT user_id FROM User WHERE email='eve@example.com'), (SELECT user_id FROM User WHERE email='biz2@example.com'), '2023-05-03', 1, 'Completed'),

((SELECT product_id FROM Product WHERE title='Gadgets - Biz3'), (SELECT user_id FROM User WHERE email='alice@example.com'), (SELECT user_id FROM User WHERE email='biz3@example.com'), '2023-05-01', 1, 'Completed'),
((SELECT product_id FROM Product WHERE title='Computers - Biz3'), (SELECT user_id FROM User WHERE email='bob@example.com'), (SELECT user_id FROM User WHERE email='biz3@example.com'), '2023-05-02', 1, 'Completed'),
((SELECT product_id FROM Product WHERE title='Mobile Phones - Biz3'), (SELECT user_id FROM User WHERE email='charlie@example.com'), (SELECT user_id FROM User WHERE email='biz3@example.com'), '2023-05-02', 1, 'Completed'),
((SELECT product_id FROM Product WHERE title='Birthday Gifts - Biz3'), (SELECT user_id FROM User WHERE email='david@example.com'), (SELECT user_id FROM User WHERE email='biz3@example.com'), '2023-05-03', 2, 'Completed'),
((SELECT product_id FROM Product WHERE title='Wedding Gifts - Biz3'), (SELECT user_id FROM User WHERE email='eve@example.com'), (SELECT user_id FROM User WHERE email='biz3@example.com'), '2023-05-03', 1, 'Completed'),

((SELECT product_id FROM Product WHERE title='Kitchen & Dining - Biz4'), (SELECT user_id FROM User WHERE email='alice@example.com'), (SELECT user_id FROM User WHERE email='biz4@example.com'), '2023-05-01', 2, 'Completed'),
((SELECT product_id FROM Product WHERE title='Bedding - Biz4'), (SELECT user_id FROM User WHERE email='bob@example.com'), (SELECT user_id FROM User WHERE email='biz4@example.com'), '2023-05-02', 2, 'Completed'),
((SELECT product_id FROM Product WHERE title='Jewelry - Biz4'), (SELECT user_id FROM User WHERE email='charlie@example.com'), (SELECT user_id FROM User WHERE email='biz4@example.com'), '2023-05-02', 1, 'Completed'),
((SELECT product_id FROM Product WHERE title='Bags & Purses - Biz4'), (SELECT user_id FROM User WHERE email='david@example.com'), (SELECT user_id FROM User WHERE email='biz4@example.com'), '2023-05-03', 2, 'Completed'),
((SELECT product_id FROM Product WHERE title='Watches - Biz4'), (SELECT user_id FROM User WHERE email='eve@example.com'), (SELECT user_id FROM User WHERE email='biz4@example.com'), '2023-05-03', 1, 'Completed'),

((SELECT product_id FROM Product WHERE title='Photography - Biz5'), (SELECT user_id FROM User WHERE email='alice@example.com'), (SELECT user_id FROM User WHERE email='biz5@example.com'), '2023-05-01', 1, 'Completed'),
((SELECT product_id FROM Product WHERE title='Sculptures - Biz5'), (SELECT user_id FROM User WHERE email='bob@example.com'), (SELECT user_id FROM User WHERE email='biz5@example.com'), '2023-05-02', 1, 'Completed'),
((SELECT product_id FROM Product WHERE title='Womens Dress - Biz5'), (SELECT user_id FROM User WHERE email='charlie@example.com'), (SELECT user_id FROM User WHERE email='biz5@example.com'), '2023-05-02', 1, 'Completed'),
((SELECT product_id FROM Product WHERE title='Mens Shirt - Biz5'), (SELECT user_id FROM User WHERE email='david@example.com'), (SELECT user_id FROM User WHERE email='biz5@example.com'), '2023-05-03', 2, 'Completed'),
((SELECT product_id FROM Product WHERE title='Childs Outfit - Biz5'), (SELECT user_id FROM User WHERE email='eve@example.com'), (SELECT user_id FROM User WHERE email='biz5@example.com'), '2023-05-03', 1, 'Completed');

