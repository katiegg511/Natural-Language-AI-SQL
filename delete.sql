-- Katie's delete script in case anything goes wrong
PRAGMA foreign_keys = OFF;  -- temporarily disable foreign key checks

DELETE FROM CustomerOrder;
DELETE FROM OrderItem;
DELETE FROM Orders;
DELETE FROM FoodStock;
DELETE FROM Employee;
DELETE FROM Customer;
DELETE FROM Franchise;
DELETE FROM Person;
DELETE FROM MenuItem;
DELETE FROM Address;

PRAGMA foreign_keys = ON;   -- re-enable foreign key checks
