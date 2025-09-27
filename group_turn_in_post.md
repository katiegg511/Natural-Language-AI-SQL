# McDonald Database

<!-- One+ sentence description or purpose of your database -->

Our database is designed to help McDonald's keep track of all the information related to their different Franchises, including information like employees, customers, food stock, and orders. Efficient storage of this information will be vital to the company's ability to assess each franchises' success and make changes where necessary.

<!-- Picture of Schema  -->

### McDonald Schema

<img src="../mcdonald_database/schema.png">

### Cross Domain Theater Schema

<img src="../cross_domain_theater_database/theater_schema.png">

<!-- Sample question, SQL query, response that worked (if you have one)  -->

## Query I thought it did well on

zeroshot meeting
"how many big macs does franchise 2 have in stock?"
"SELECT Amount \nFROM FoodStock \nJOIN MenuItem ON FoodStock.MenuItemId = MenuItem.Id \nWHERE MenuItem.Name = 'Big Mac' AND FoodStock.FranchiseId = 2;\n"
response: "[(110,)]"

**Question**:

**GPT SQL Response**:

**Friendly Response**:

<!-- Sample question, SQL query, response that did not work (if you have one)  -->

## Question that it tripped up on
The SQL response was the correct way to answer the question, but then the friendly response invented a name for the franchise.

**Question**: Which franchise has the highest total revenue?

**GPT SQL Response**: ```
SELECT f.Id, SUM(o.Cost) AS TotalRevenue  
FROM Franchise f  
JOIN Orders o ON f.Id = o.FranchiseId  
GROUP BY f.Id  
ORDER BY TotalRevenue DESC  
LIMIT 1;  ```

**Friendly Response**: The franchise with the highest total revenue is Pokémon.

<!-- A file outlining at least 6 other examples.  -->

## File of Other Examples

1.  one_shot
    "how many employees work at the franchise with id = 1"
    "\nSELECT COUNT(\*) FROM Employee WHERE FranchiseId = 1;\n"
    "[(3,)]"

2.  zero_shot
    "what menuItems were ordered in order 3?"
    "\nSELECT MenuItem.Name \nFROM OrderItem \nJOIN MenuItem ON OrderItem.MenuItemId = MenuItem.Id \nWHERE OrderItem.OrderId = 3;\n"
    "[('McChicken',), ('French Fries (Small)',), ('Soft Drink (Small)',)]"

3. zero_shot
Question:
What is the most ordered menu item?

SQL Syntax Response:
SELECT MenuItem.Name
FROM MenuItem
JOIN OrderItem ON MenuItem.Id = OrderItem.MenuItemId
GROUP BY MenuItem.Id
ORDER BY SUM(OrderItem.Quantity) DESC
LIMIT 1;

Query Raw Response:
[('Big Mac',)]
Friendly Response:
The most ordered menu item is the Big Mac.

4. zero_shot
Question:
What is the average wait time for each franchise, from longest to shortest?
SQL Syntax Response:

SELECT FranchiseId, AVG(WaitTime) AS AverageWaitTime
FROM Orders
GROUP BY FranchiseId
ORDER BY AverageWaitTime DESC;

Query Raw Response:
[(1, 20.333333333333332), (4, 18.666666666666668), (3, 18.333333333333332), (6, 18.0), (5, 16.0), (2, 15.666666666666666)]
Friendly Response:
Certainly! Here is the average wait time for each franchise from longest to shortest:

1. Franchise 1: 20.33 minutes
2. Franchise 4: 18.67 minutes
3. Franchise 3: 18.33 minutes
4. Franchise 6: 18.0 minutes
5. Franchise 5: 16.0 minutes
6. Franchise 2: 15.67 minutes

5.

6.

<!-- Describe somewhere which prompting strategies you tried and if you noticed a difference between them. (Note my post only does two of three - which is fine!).  -->

## Conclusion

We tried a meeting strategy, meaning we told chat there was an urgent meeting, in order to see if the urgency did anything. We then did that with zero_shot and one_shot. Chat was able to get all of them correct, with no discernable differences.
While the answers were correct, there were queries that got to the same answer but different ways. For example, to get the number of employees one used the NumEmployee column and another used the EmployeeId foreign key.

We also made a strategy to try and confuse it by having it be completely unrelated to SQL: "who made this chicken??? Was it you?" as a pre-prompt with zero_shot, and it still got everything right.
