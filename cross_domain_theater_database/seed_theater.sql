INSERT INTO Theater_Addresses (address_id, street, city, state, zip) VALUES
(1,'123 Main St','Provo','UT','84601'),
(2,'45 State St','Salt Lake City','UT','84111'),
(3,'700 Center Ave','Orem','UT','84057'),
(4,'9 Theater Way','Provo','UT','84601');

INSERT INTO Theater_Person (person_id,address_id,first_name,last_name,phone_number,email) VALUES
(1,1,'Alice','Actor','(555) 111-1001','alice.actor@example.com'),
(2,2,'Ben','Buyer','(555) 111-1002','ben.buyer@example.com'),
(3,3,'Cathy','Customer','(555) 111-1003','cathy.c@example.com'),
(4,3,'Dylan','Doe','(555) 111-1004','dylan.d@example.com'),
(5,1,'Erin','Electric','(555) 111-1005','erin.electric@example.com'),
(6,2,'Frank','Front','(555) 111-1006','frank.front@example.com');

INSERT INTO Theater_Customer (customer_id, birthdate) VALUES
(2,'1994-04-12'),
(3,'1999-09-09'),
(4,'1988-12-01');

INSERT INTO Theater_Employee (employee_id, salary, position) VALUES
(1, 55000.00, 'Actor'),
(5, 52000.00, 'Lighting Tech'),
(6, 42000.00, 'Box Office');

INSERT INTO Theater_Venue (venue_id,address_id,phone_number,location_name) VALUES
(1,4,'(555) 222-0001','Downtown Playhouse'),
(2,2,'(555) 222-0002','Riverside Stage');

INSERT INTO Theater_Section (section_id,venue_id,name,row_count,seat_count) VALUES
(1,1,'Orchestra',20,400),
(2,1,'Balcony',10,200),
(3,2,'Main',15,300);

INSERT INTO Theater_Seat (seat_id,section_id,row_label,seat_number) VALUES
(1,1,'A',1),(2,1,'A',2),(3,1,'A',3),(4,1,'B',1),(5,1,'B',2),
(6,2,'A',1),(7,2,'A',2),
(8,3,'A',1),(9,3,'A',2),(10,3,'A',3);

-- --------------------------
INSERT INTO Theater_Production (production_id,title,author,open_date,close_date,genre,runtime_minutes) VALUES
(1,'Hamlet','William Shakespeare','2025-09-20','2025-11-20','Tragedy',180),
(2,'The Music Man','Meredith Willson','2025-10-01','2025-12-15','Musical',165);

INSERT INTO Theater_Performance (performance_id,production_id,venue_id,starts_at,status) VALUES
(1,1,1,'2025-10-01 19:30:00','OnSale'),
(2,1,1,'2025-10-02 19:30:00','OnSale'),
(3,2,2,'2025-10-05 19:00:00','OnSale');

INSERT INTO Theater_Ticket (ticket_id,performance_id,seat_id,price_paid,barcode,status) VALUES
(1,1,1,45.00,'HAM-20251001-A1','Paid'),
(2,1,2,45.00,'HAM-20251001-A2','Reserved'),
(3,1,3,45.00,'HAM-20251001-A3','Reserved'),
(4,1,4,40.00,'HAM-20251001-B1','Paid'),
(5,1,5,40.00,'HAM-20251001-B2','Paid'),
(6,2,1,45.00,'HAM-20251002-A1','Reserved'),
(7,3,8,55.00,'MM-20251005-A1','Paid'),
(8,3,9,55.00,'MM-20251005-A2','Paid'),
(9,3,10,55.00,'MM-20251005-A3','Reserved');

INSERT INTO Theater_Purchase (purchase_id,buyer_person_id,purchased_at,total_price,channel) VALUES
(1,2,'2025-09-20 10:15:00',85.00,'Web'),
(2,3,'2025-09-21 14:05:00',55.00,'BoxOffice');

INSERT INTO Theater_PurchaseItem (purchase_item_id,purchase_id,ticket_id,item_price) VALUES
(1,1,1,45.00),
(2,1,4,40.00),
(3,2,7,55.00);

INSERT INTO Theater_CastAssignment (cast_assignment_id,performance_id,employee_id,role_name,assignment_type) VALUES
(1,1,1,'Hamlet','Actor'),
(2,1,5,'Lighting Board','Crew'),
(3,3,1,'Professor Harold Hill','Actor');
