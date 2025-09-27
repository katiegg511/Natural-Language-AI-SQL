-- Katie's old code for loading CSVs into the database
.mode csv
PRAGMA foreign_keys = ON;
.import csvs/Address.csv Address
.import csvs/MenuItem.csv MenuItem
.import csvs/Person.csv Person
.import csvs/Franchise.csv Franchise
.import csvs/Customer.csv Customer
.import csvs/Employee.csv Employee
.import csvs/FoodStock.csv FoodStock
.import csvs/Orders.csv Orders
.import csvs/OrderItem.csv OrderItem
.import csvs/CustomerOrder.csv CustomerOrder

-- .read loadCsvs.sql