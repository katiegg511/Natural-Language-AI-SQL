PRAGMA foreign_keys = ON;

CREATE TABLE Theater_Addresses (
  address_id   INTEGER PRIMARY KEY,
  street       TEXT NOT NULL,
  city         TEXT NOT NULL,
  state        TEXT NOT NULL,
  zip          TEXT NOT NULL
);

CREATE INDEX ix_address_composite ON Theater_Addresses(street, city, state, zip);

CREATE TABLE Theater_Person (
  person_id    INTEGER PRIMARY KEY,
  address_id   INTEGER,
  first_name   TEXT NOT NULL,
  last_name    TEXT NOT NULL,
  phone_number TEXT,
  email        TEXT,
  UNIQUE (email),
  FOREIGN KEY (address_id) REFERENCES Theater_Addresses(address_id)
    ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE TABLE Theater_Customer (
  customer_id  INTEGER PRIMARY KEY,
  birthdate    TEXT,
  FOREIGN KEY (customer_id) REFERENCES Theater_Person(person_id)
    ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE Theater_Employee (
  employee_id  INTEGER PRIMARY KEY,
  salary       REAL NOT NULL,
  position     TEXT NOT NULL,
  FOREIGN KEY (employee_id) REFERENCES Theater_Person(person_id)
    ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE Theater_Venue (
  venue_id    INTEGER PRIMARY KEY,
  address_id    INTEGER,
  phone_number  TEXT,
  location_name TEXT NOT NULL,
  FOREIGN KEY (address_id) REFERENCES Theater_Addresses(address_id)
    ON UPDATE CASCADE ON DELETE SET NULL
);

CREATE TABLE Theater_Section (
  section_id INTEGER PRIMARY KEY,
  venue_id INTEGER NOT NULL,
  name       TEXT NOT NULL,
  row_count  INTEGER,
  seat_count INTEGER,
  UNIQUE (venue_id, name),
  FOREIGN KEY (venue_id) REFERENCES Theater_Venue(venue_id)
    ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE INDEX ix_section_theater ON Theater_Section(venue_id);

CREATE TABLE Theater_Seat (
  seat_id     INTEGER PRIMARY KEY,
  section_id  INTEGER NOT NULL,
  row_label   TEXT NOT NULL,
  seat_number INTEGER NOT NULL,
  UNIQUE (section_id, row_label, seat_number),
  FOREIGN KEY (section_id) REFERENCES Theater_Section(section_id)
    ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE INDEX ix_seat_section ON Theater_Seat(section_id);

CREATE TABLE Theater_Production (
  production_id   INTEGER PRIMARY KEY,
  title           TEXT NOT NULL,
  author          TEXT,
  open_date       TEXT,
  close_date      TEXT,
  genre           TEXT,
  runtime_minutes INTEGER
);

CREATE TABLE Theater_Performance (
  performance_id INTEGER PRIMARY KEY,
  production_id  INTEGER NOT NULL,
  venue_id     INTEGER NOT NULL,
  starts_at      TEXT NOT NULL,
  status         TEXT NOT NULL,
  FOREIGN KEY (production_id) REFERENCES Theater_Production(production_id)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  FOREIGN KEY (venue_id)   REFERENCES Theater_Venue(venue_id)
    ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE INDEX ix_performance_prod    ON Theater_Performance(production_id);
CREATE INDEX ix_performance_theater ON Theater_Performance(venue_id);
CREATE INDEX ix_performance_start   ON Theater_Performance(starts_at);

CREATE TABLE Theater_Ticket (
  ticket_id      INTEGER PRIMARY KEY,
  performance_id INTEGER NOT NULL,
  seat_id        INTEGER NOT NULL,
  price_paid     REAL NOT NULL,
  barcode        TEXT NOT NULL,
  status         TEXT NOT NULL,
  UNIQUE (performance_id, seat_id),
  UNIQUE (barcode),
  FOREIGN KEY (performance_id) REFERENCES Theater_Performance(performance_id)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  FOREIGN KEY (seat_id)        REFERENCES Theater_Seat(seat_id)
    ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE INDEX ix_ticket_performance ON Theater_Ticket(performance_id);
CREATE INDEX ix_ticket_seat        ON Theater_Ticket(seat_id);

CREATE TABLE Theater_Purchase (
  purchase_id     INTEGER PRIMARY KEY,
  buyer_person_id INTEGER NOT NULL,
  purchased_at    TEXT NOT NULL,
  total_price     REAL NOT NULL,
  channel         TEXT,
  FOREIGN KEY (buyer_person_id) REFERENCES Theater_Person(person_id)
    ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE INDEX ix_purchase_buyer ON Theater_Purchase(buyer_person_id);
CREATE INDEX ix_purchase_date  ON Theater_Purchase(purchased_at);

CREATE TABLE Theater_PurchaseItem (
  purchase_item_id INTEGER PRIMARY KEY,
  purchase_id      INTEGER NOT NULL,
  ticket_id        INTEGER NOT NULL,
  item_price       REAL NOT NULL,
  UNIQUE (ticket_id),
  FOREIGN KEY (purchase_id) REFERENCES Theater_Purchase(purchase_id)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  FOREIGN KEY (ticket_id)   REFERENCES Theater_Ticket(ticket_id)
    ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE INDEX ix_item_purchase ON Theater_PurchaseItem(purchase_id);

CREATE TABLE Theater_CastAssignment (
  cast_assignment_id INTEGER PRIMARY KEY,
  performance_id     INTEGER NOT NULL,
  employee_id        INTEGER NOT NULL,
  role_name          TEXT NOT NULL,
  assignment_type    TEXT NOT NULL,
  FOREIGN KEY (performance_id) REFERENCES Theater_Performance(performance_id)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  FOREIGN KEY (employee_id)    REFERENCES Theater_Employee(employee_id)
    ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE INDEX ix_cast_perf_emp ON Theater_CastAssignment(performance_id, employee_id, assignment_type);
