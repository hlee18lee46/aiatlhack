drop table trans;
drop table users;
drop table store;
create table users(
email varchar(255),
password varchar(255),
primary key(email)
);
create table trans(
receiptID int, 
email varchar(255),
itemID int, 
itemDesc varchar(255),
price numeric(10, 2),
primary key(receiptID)
);
create table store(
storeID int,
receiptID int,
city varchar(255),
st varchar(255),
primary key(storeID)
);