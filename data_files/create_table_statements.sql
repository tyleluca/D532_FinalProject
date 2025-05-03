CREATE TABLE store (
    storeId INT NOT NULL PRIMARY KEY,
    storeLocation VARCHAR(255)
);

CREATE TABLE product (
    productId INT NOT NULL PRIMARY KEY,
    productCategory VARCHAR(255),
    productType VARCHAR(255),
    productDetail VARCHAR(255)
);

CREATE TABLE transaction (
    transactionId INT NOT NULL PRIMARY KEY,
    transactionQty INT,
    transactionDatetime TIMESTAMP,
    storeId INT,
    productId INT,
    unitPrice DOUBLE PRECISION,
    FOREIGN KEY (storeId) REFERENCES store(storeId),
    FOREIGN KEY (productId) REFERENCES product(productId)
);

