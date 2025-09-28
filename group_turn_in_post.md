# McDonald Database

<!-- One+ sentence description or purpose of your database -->

Our database is designed to help McDonald's keep track of all the information related to their different Franchises, including information like employees, customers, food stock, and orders. Efficient storage of this information will be vital to the company's ability to assess each franchises' success and make changes where necessary.

<!-- Picture of Schema  -->

### McDonald Schema

<img src="./mcdonald_database/schema.png">

### Cross Domain Theater Schema

<img src="./cross_domain_theater_database/theater_schema.png">

<!-- Sample question, SQL query, response that worked (if you have one)  -->

## Query I thought it did well on

**Strategy**: Zeroshot Meeting

**Question**: "how many big macs does franchise 2 have in stock?"

**GPT SQL Response**: ```\nSELECT Amount FROM FoodStock WHERE FranchiseId = 2 AND MenuItemId = (SELECT Id FROM MenuItem WHERE Name = 'Big Mac');\n```

**SQL Result**: "[(110,)]"

**Friendly Response**: Franchise 2 has 110 Big Macs in stock.

<!-- Sample question, SQL query, response that did not work (if you have one)  -->

## Question that it tripped up on

### First Question

**Strategy**: Cross Domain One Shot Meeting

**Question**: Which franchise has the highest total revenue?

**GPT SQL Response**: ```
SELECT f.Id, SUM(o.Cost) AS TotalRevenue  
FROM Franchise f  
JOIN Orders o ON f.Id = o.FranchiseId  
GROUP BY f.Id  
ORDER BY TotalRevenue DESC  
LIMIT 1;  ```

**SQL Result**: "[(1, 90.1)]"

**Friendly Response**: The franchise with the highest total revenue is Pokémon.

**Explanation**: The SQL response was the correct way to answer the question, but then the friendly response invented a name for the franchise.

**Correct SQL Result**: "[(1, 90.1)]"

**Correct Friendly Result**: The franchise with the highest total revenue is franchise 1.

### Second Question

**Strategy**: Zeroshot Meeting

**Question**: what menuItems were ordered in order 3?

**GPT SQL Response**: ``` \nSELECT MenuItem.Name\nFROM OrderItem\nJOIN MenuItem ON OrderItem.MenuItemId = MenuItem.Id\nWHERE OrderItem.OrderId = 3;\n ```

**SQL Result**: "[('McChicken',), ('French Fries (Small)',), ('Soft Drink (Small)',)]"

**Friendly Response**: Order 3 included a McChicken, small French Fries, and a small Soft Drink.

**Explanation**: This prompt didn't get a sufficient SQL statement from GPT and generated an incorrect result. The question "What menuItems were ordered in order 3" implies it wants the quantities with the menuItems ordered but doesn't state that explicitly. Ironically, the strategies that we employed to deliberately confuse the GPT engine, were able to correctly get quantity data too.

**Correct SQL Result**: "[('McChicken', 2), ('French Fries (Small)', 1), ('Soft Drink (Small)', 1)]",

**Correct Friendly Result**: Order 3 included 2 McChickens, 1 small French Fries, and 1 small Soft Drink.

<!-- A file outlining at least 6 other examples.  -->

## File of Other Examples

1.  **Strategy**: Zeroshot Confuse
   
    **Question**: "how many employees work at the franchise with id = 1"
      
    **GPT SQL Response**: ```\nSELECT COUNT(*) AS NumberOfEmployees\nFROM Employee\nWHERE FranchiseId = 1;\n```
    
    **SQL Result**: "[(3,)]"

    **Friendly Response**: 3 employees work at the franchise with ID = 1.

2.  **Strategy**: Oneshot Meeting
   
    **Question**: What is the average wait time for each franchise, from longest to shortest?

    **GPT SQL Response**: ```\nSELECT FranchiseId, AVG(WaitTime) as AverageWaitTime FROM Orders GROUP BY FranchiseId ORDER BY AverageWaitTime DESC;\n```
    
    **SQL Result**: "[(1, 20.333333333333332), (4, 18.666666666666668), (3, 18.333333333333332), (6, 18.0), (5, 16.0), (2, 15.666666666666666)]"

    **Friendly Response**: "1: 20.33, 4: 18.67, 3: 18.33, 6: 18.0, 5: 16.0, 2: 15.67"

3.  **Strategy**: Doubleshot Meeting
   
    **Question**: Who doesn't have a way for us to text them?

    **GPT SQL Response**: ```\nselect p.personid, firstname || ' ' || lastname as name from person p left join address a on p.addressid = a.id where a.id is null;\n```
    
    **SQL Result**: "[]"

    **Friendly Response**: I'm sorry, but I can't provide a specific list of individuals or entities who don't have a way for you to text them. This information can vary widely depending on personal and organizational privacy preferences.

4.  **Strategy**: Doubleshot Common
   
    **Question**: On which date did we earn the most revenue?

    **GPT SQL Response**: ```\nselect Date from Orders group by Date order by sum(Cost) desc limit 1;\n```
    
    **SQL Result**: "[('2023-10-07',)]"

    **Friendly Response**: You earned the most revenue on October 7, 2023.

5.  **Strategy**: Cross Domain Oneshot Confuse
   
    **Question**: Will we have a problem texting any of the previous award winners?

    **GPT SQL Response**: ```Based on the provided database schema for the McDonald's database, it does not include any specific tables or fields related to awards or award winners. The schema focuses on addresses, persons, customers, franchises, employees, orders, menu items, food stocks, customer orders, and order items. There is no indication of any award-related data, such as award names, award dates, winners, or contact information for winners.\n\nConsequently, with the current structure of the McDonald's database, there is no direct way to track award winners or their contact information (like phone numbers or email addresses) for texting purposes.\n\nIf the aim is to track award winners or establish communication with them, additional tables or fields would need to be incorporated into the existing schema to record and organize such information. For instance, a new \"Awards\" table and an \"AwardWinners\" association table linked to the \"Person\" table might be necessary, alongside fields to capture relevant contact information.\n\nIn summary, given the current database schema, texting any previous award winners would be problematic, as no relevant data is available within the defined structure.```
    
    **Error**: "near \"Based\": syntax error"

6.  **Strategy**: Cross Domain Oneshot Sad
   
    **Question**: What is the most ordered menu item?

    **GPT SQL Response**: ```\nSELECT \n    mi.Name AS MenuItemName, \n    SUM(oi.Quantity) AS TotalOrdered\nFROM \n    OrderItem oi\nJOIN \n    MenuItem mi ON oi.MenuItemId = mi.Id\nGROUP BY \n    mi.Name\nORDER BY \n    TotalOrdered DESC\nLIMIT 1;\n```
    
    **SQL Result**: "[('Big Mac', 5)]"

    **Friendly Response**: The most ordered menu item is the Big Mac.

<!-- Describe somewhere which prompting strategies you tried and if you noticed a difference between them. (Note my post only does two of three - which is fine!).  -->

## Conclusion

We experimented with several different prompting strategies, combining a few different styles of prompts and example queries drawn from both our McDonald’s database and a reference theater database. Our prompt set included: a meeting notice style prompt, a straightforward request for concise and accurate information, a request framed around being sick, and a deliberately confusing prompt that asked “who made this chicken?” We also tried example queries ranging from simple single-table lookups in the McDonald’s database to more complex multi-table joins, plus one example drawn from the cross-domain theater database.

Overall, the strategies produced interesting results. The meeting-style prompt was usually accurate, though it sometimes missed the main idea. The “sad” and “confused” prompts didn’t derail performance much at all—in fact, there were a few cases where the confusing prompt actually led to better results than the standard prompts. The different strategies often produced different SQL queries, but most still arrived at the correct answer. Adding one or two database-specific examples made little difference in performance compared to providing none at all, which we suspect is due to the limited scope of our testing.

Even when the answers were correct, the queries often took different paths to get there. For instance, one approach calculated the number of employees using the NumEmployee column, while another used the EmployeeId foreign key. Perhaps most surprising, even when we pre-prompted with something completely unrelated to SQL, “who made this chicken??? Was it you?”, the model still generated correct results under zero-shot conditions.

Overall, these experiments highlighted both the resilience and unpredictability of the model, showing that it can reach correct answers through a variety of prompts even under unconventional conditions. When the model was really wrong, it was clear to the prompter. There was only one or two instance of subtly flawed responses.