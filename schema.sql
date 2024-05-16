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
    picture 		BLOB,
    balance 		DECIMAL(10,2),
    PRIMARY KEY(user_id),
    FOREIGN KEY(user_id) REFERENCES User(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Customer(
    user_id 		INT NOT NULL,
    picture 		BLOB,
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
    product_id 	INT NOT NULL,
    title 		VARCHAR(255) NOT NULL,
    description 	VARCHAR(255),
    price 		DECIMAL(10,2) NOT NULL,
    amount 		INT NOT NULL,
    images 		LONGBLOB,
    PRIMARY KEY(product_id)
);

CREATE TABLE IF NOT EXISTS Balance_Record(
    record_id		INT NOT NULL,
    record_date 	DATE NOT NULL,
    record_type 	VARCHAR(255) NOT NULL,
    record_amount 	DECIMAL(10,2) NOT NULL,
    PRIMARY KEY(record_id)
);

CREATE TABLE IF NOT EXISTS Recipient(
    recipient_id 		INT NOT NULL,
    recipient_name 		VARCHAR(255) NOT NULL,
    PRIMARY KEY(recipient_id),
           UNIQUE KEY(recipient_name)
);

CREATE TABLE IF NOT EXISTS Material(
    material_id 	INT NOT NULL,
    material_name 	VARCHAR(255) NOT NULL,
    PRIMARY KEY(material_id),
    UNIQUE KEY(material_name)
);

CREATE TABLE IF NOT EXISTS Main_Category(
    main_category_id 	INT NOT NULL,
    main_category_name 	VARCHAR(255) NOT NULL,
    PRIMARY KEY(main_category_id)
);

CREATE TABLE IF NOT EXISTS Sub_Category(
    sub_category_id 	INT NOT NULL,
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
    report_id 		INT NOT NULL,
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


DELIMETER //
CREATE PROCEDURE CartAdder(IN user_id INT, IN product_id INT)
BEGIN
    DECLARE product_amount INT;

    SELECT COUNT(*) INTO product_amount 
    FROM Add_To_Shopping_Cart AS A 
    WHERE A.product_id = product_id AND A.user_id = user_id;

    IF product_amount > 0 THEN
        UPDATE Add_To_Shopping_Cart 
        SET count = count + 1 
        WHERE product_id = product_id AND customer_id = user_id;
    ELSE
        INSERT INTO Add_To_Shopping_Cart (customer_id, product_id, count) 
        VALUES (user_id, product_id, 1);
    END IF;
END;//
DELIMETER

DELIMITER //
CREATE PROCEDURE ProductPrinter(IN per_page INT, IN start_index INT)
BEGIN
    DECLARE avg_rating DECIMAL(3,2);
    DECLARE num_rating INT;

    SELECT product_id, AVG(star), COUNT(*)
    INTO avg_rating, num_rating
    FROM Rate
    GROUP BY product_id;

    SELECT P.product_id, P.title, P.description, P.price, P.amount, avg_rating AS average_rating, num_rating AS number_of_rating, P.images
    FROM Product P
    WHERE P.amount > 0
    ORDER BY P.product_id DESC
    LIMIT per_page OFFSET start_index;
END;//
DELIMITER ;
