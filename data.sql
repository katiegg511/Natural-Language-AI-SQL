-- Katie's script for creating the McDonald's database schema
CREATE TABLE Address(
    Id INTEGER PRIMARY KEY,
    Street VARCHAR(255) NOT NULL,
    City VARCHAR(100) NOT NULL,
    State VARCHAR(100) NOT NULL,
    ZipCode VARCHAR(20) NOT NULL
);

CREATE TABLE Person(
    PersonId INTEGER PRIMARY KEY,
    FirstName VARCHAR(255) NOT NULL,
    LastName VARCHAR(255) NOT NULL,
    AddressId INTEGER,
    FOREIGN KEY(AddressId) REFERENCES Address(Id)
);

CREATE TABLE Customer(
    PersonId INTEGER PRIMARY KEY,
    BirthDate DATE,
    FOREIGN KEY(PersonId) REFERENCES Person(PersonId)
);

CREATE TABLE Franchise(
    Id INTEGER PRIMARY KEY,
    AddressId INTEGER,
    NumEmployees INTEGER,
    OpeningDate DATE,
    FOREIGN KEY(AddressId) REFERENCES Address(Id)
);

CREATE TABLE Employee(
    PersonId INTEGER PRIMARY KEY,
    StartDate DATE,
    Salary DECIMAL(8, 2),
    FranchiseId INTEGER,
    FOREIGN KEY(FranchiseId) REFERENCES Franchise(Id),
    FOREIGN KEY(PersonId) REFERENCES Person(PersonId)
);

CREATE TABLE Orders(
    Id INTEGER PRIMARY KEY,
    Date Date,
    Cost DECIMAL(8, 2),
    WaitTime INTEGER,
    FranchiseId INTEGER,
    FOREIGN KEY(FranchiseId) REFERENCES Franchise(Id)
);

CREATE TABLE CustomerOrder(
    CustomerId INTEGER,
    OrderId INTEGER,
    PRIMARY KEY(CustomerId, OrderId),
    FOREIGN KEY(CustomerId) REFERENCES Customer(PersonId),
    FOREIGN KEY(OrderId) REFERENCES Orders(Id)
);

CREATE TABLE MenuItem(
    Id INTEGER PRIMARY KEY,
    Name VARCHAR(255) UNIQUE NOT NULL,
    Price DECIMAL(8, 2) NOT NULL
);

CREATE TABLE OrderItem(
    Id INTEGER PRIMARY KEY,
    OrderId INTEGER,
    MenuItemId INTEGER,
    Quantity INTEGER NOT NULL,
    FOREIGN KEY(OrderId) REFERENCES Orders(Id),
    FOREIGN KEY(MenuItemId) REFERENCES MenuItem(Id)
);

CREATE TABLE FoodStock(
    Id INTEGER PRIMARY KEY,
    FranchiseId INTEGER,
    MenuItemId INTEGER,
    Amount INTEGER NOT NULL,
    FOREIGN KEY(FranchiseId) REFERENCES Franchise(Id),
    FOREIGN KEY(MenuItemId) REFERENCES MenuItem(Id)
);

-- Insertion order
-- Address, MenuItem
-- Person, Franchise
-- Customer, Employee, FoodStock, Order
-- OrderItem, CustomerOrder


CREATE TABLE CustomerOrder(
    CustomerId INTEGER,
    OrderId INTEGER,
    PRIMARY KEY(CustomerId, OrderId),
    FOREIGN KEY(CustomerId) REFERENCES Customer(PersonId),
    FOREIGN KEY(OrderId) REFERENCES Orders(Id)
);

CREATE TABLE OrderItem(
    Id INTEGER PRIMARY KEY,
    OrderId INTEGER,
    MenuItemId INTEGER,
    Quantity INTEGER NOT NULL,
    FOREIGN KEY(OrderId) REFERENCES Orders(Id),
    FOREIGN KEY(MenuItemId) REFERENCES MenuItem(Id)
);