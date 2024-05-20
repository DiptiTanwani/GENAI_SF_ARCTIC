
CREATE OR REPLACE TABLE ORDERS
    (
     ORDER_ID CHAR(50)NOT NULL,
     CUSTOMER_ID CHAR(50)NOT NULL,
	 PRODUCT_ID CHAR(50)NOT NULL,
	 STORE_ID CHAR(50)NOT NULL,
	 DATE_ID CHAR(50)NOT NULL,
     QUANTITY NUMBER,
     AMOUNT NUMBER,
	 CONSTRAINT ORDER_PK PRIMARY KEY (ORDER_ID)
    );

CREATE OR REPLACE TABLE CUSTOMER
    (
        CUSTOMER_ID CHAR(50)NOT NULL,
        CUSTOMER_FNAME CHAR(50),
        CUSTOMER_LNAME CHAR(50),
        CONSTRAINT CUSTOMER_PK PRIMARY KEY (CUSTOMER_ID)
    );

CREATE OR REPLACE TABLE STORES
    (
        STORE_ID CHAR(50)NOT NULL,
        CITY VARCHAR(50),
        COUNTRY VARCHAR(50),
        CONSTRAINT LOCATION_PK PRIMARY KEY (STORE_ID)
    );


CREATE OR REPLACE TABLE PRODUCT
    (
     PRODUCT_ID CHAR(50)NOT NULL,
     NAME CHAR(50),
     DESCRIPTION VARCHAR(100),
     PRICE NUMBER,
	 CONSTRAINT PRODUCT_PK PRIMARY KEY (PRODUCT_ID)
    );

CREATE OR REPLACE TABLE DATE
    (
     DATE_ID CHAR(50)NOT NULL,
     MONTH CHAR(50),
     YEAR VARCHAR(100),
	 CONSTRAINT DATE_PK PRIMARY KEY (DATE_ID)
    );		
		
ALTER TABLE ORDERS 
    ADD CONSTRAINT ORDERSFK0 FOREIGN KEY (CUSTOMER_ID) REFERENCES CUSTOMER;
ALTER TABLE ORDERS 
    ADD CONSTRAINT STORESFK0 FOREIGN KEY (STORE_ID) REFERENCES STORES;	
ALTER TABLE ORDERS 
    ADD CONSTRAINT PRODUCTFK0 FOREIGN KEY (PRODUCT_ID) REFERENCES PRODUCT;
ALTER TABLE ORDERS 
    ADD CONSTRAINT DATEFK0 FOREIGN KEY (DATE_ID) REFERENCES DATE;


------------------------------------------------------------------------------

insert into CUSTOMER (Customer_ID, Customer_FName, Customer_Lname) values
  ('1', 'Netra','Hegde' ),
  ('2', 'Dipti','Tanwani'),
  ('3', 'Sourav','Ghosh'),
  ('4', 'Sanjib','Manna'),
  ('5', 'Samaresh','Pahar');
  
  
insert into STORES (STORE_ID, CITY, COUNTRY) values
  ('10', 'Bangalore','India' ),
  ('20', 'Kolkatta','India' ),
  ('30', 'Pune','India');

insert into PRODUCT (PRODUCT_ID, NAME, DESCRIPTION, PRICE) values
  ('100', 'AWS','Technical book', 250 ),
  ('200', 'AWS-Bedrock','GEN AI book', 500 ),
  ('300', 'Watsonx','Technical book', 50 ),
  ('400', 'GEN-AI','Technical book', 150 ),
  ('500', 'MS-Copilot','GEN AI book', 400);

insert into DATE (DATE_ID, MONTH, YEAR) values
  ('110', 'Jan','2024' ),
  ('120', 'Feb','2024' ),
  ('130', 'Mar','2024'),
  ('140', 'Apr','2024');

insert into ORDERS (ORDER_ID, CUSTOMER_ID, PRODUCT_ID, STORE_ID, DATE_ID, QUANTITY, AMOUNT) values
  ('210', '1', '200','10','140',1,500 ),
  ('220', '4', '500','20','130',3,1200 ),
  ('230', '2', '100','30','110',1,250 ),
  ('240', '5', '500','20','130',1,400 );


select * from  TECHNOVA.PUBLIC.Customer;
select * from  TECHNOVA.PUBLIC.STORES;
select * from  TECHNOVA.PUBLIC.PRODUCT;
select * from  TECHNOVA.PUBLIC.DATE;
select * from  TECHNOVA.PUBLIC.ORDERS;
	


    