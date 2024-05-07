
set global transaction isolation level serializable;
set global SQL_MODE = 'ANSI,TRADITIONAL';
set names utf8mb4;
set SQL_SAFE_UPDATES = 0;

set @thisDatabase = 'drone_dispatch';
drop database if exists drone_dispatch;
create database if not exists drone_dispatch;
use drone_dispatch;

-- -----------------------------------------------
-- table structures
-- -----------------------------------------------

create table users (
uname varchar(40) not null,
first_name varchar(100) not null,
last_name varchar(100) not null,
address varchar(500) not null,
birthdate date default null,
primary key (uname)
) engine = innodb;

create table customers (
uname varchar(40) not null,
rating integer not null,
credit integer not null,
primary key (uname)
) engine = innodb;

create table employees (
uname varchar(40) not null,
taxID varchar(40) not null,
service integer not null,
salary integer not null,
primary key (uname),
unique key (taxID)
) engine = innodb;

create table drone_pilots (
uname varchar(40) not null,
licenseID varchar(40) not null,
experience integer not null,
primary key (uname),
unique key (licenseID)
) engine = innodb;

create table store_workers (
uname varchar(40) not null,
primary key (uname)
) engine = innodb;

create table products (
barcode varchar(40) not null,
pname varchar(100) not null,
weight integer not null,
primary key (barcode)
) engine = innodb;

create table orders (
orderID varchar(40) not null,
sold_on date not null,
purchased_by varchar(40) not null,
carrier_store varchar(40) not null,
carrier_tag integer not null,
primary key (orderID)
) engine = innodb;

create table stores (
storeID varchar(40) not null,
sname varchar(100) not null,
revenue integer not null,
manager varchar(40) not null,
primary key (storeID)
) engine = innodb;

create table drones (
storeID varchar(40) not null,
droneTag integer not null,
capacity integer not null,
remaining_trips integer not null,
pilot varchar(40) not null,
primary key (storeID, droneTag)
) engine = innodb;

create table order_lines (
orderID varchar(40) not null,
barcode varchar(40) not null,
price integer not null,
quantity integer not null,
primary key (orderID, barcode)
) engine = innodb;

create table employed_workers (
storeID varchar(40) not null,
uname varchar(40) not null,
primary key (storeID, uname)
) engine = innodb;

-- -----------------------------------------------
-- referential structures
-- -----------------------------------------------

alter table customers add constraint fk1 foreign key (uname) references users (uname)
	on update cascade on delete cascade;
alter table employees add constraint fk2 foreign key (uname) references users (uname)
	on update cascade on delete cascade;
alter table drone_pilots add constraint fk3 foreign key (uname) references employees (uname)
	on update cascade on delete cascade;
alter table store_workers add constraint fk4 foreign key (uname) references employees (uname)
	on update cascade on delete cascade;
alter table orders add constraint fk8 foreign key (purchased_by) references customers (uname)
	on update cascade on delete cascade;
alter table orders add constraint fk9 foreign key (carrier_store, carrier_tag) references drones (storeID, droneTag)
	on update cascade on delete cascade;
alter table stores add constraint fk11 foreign key (manager) references store_workers (uname)
	on update cascade on delete cascade;
alter table drones add constraint fk5 foreign key (storeID) references stores (storeID)
	on update cascade on delete cascade;
alter table drones add constraint fk10 foreign key (pilot) references drone_pilots (uname)
	on update cascade on delete cascade;
alter table order_lines add constraint fk6 foreign key (orderID) references orders (orderID)
	on update cascade on delete cascade;
alter table order_lines add constraint fk7 foreign key (barcode) references products (barcode)
	on update cascade on delete cascade;
alter table employed_workers add constraint fk12 foreign key (storeID) references stores (storeID)
	on update cascade on delete cascade;
alter table employed_workers add constraint fk13 foreign key (uname) references store_workers (uname)
	on update cascade on delete cascade;

-- -----------------------------------------------
-- table data
-- -----------------------------------------------

insert into users values
('jstone5', 'Jared', 'Stone', '101 Five Finger Way', '1961-01-06'),
('sprince6', 'Sarah', 'Prince', '22 Peachtree Street', '1968-06-15'),
('awilson5', 'Aaron', 'Wilson', '220 Peachtree Street', '1963-11-11'),
('lrodriguez5', 'Lina', 'Rodriguez', '360 Corkscrew Circle', '1975-04-02'),
('tmccall5', 'Trey', 'McCall', '360 Corkscrew Circle', '1973-03-19'),
('eross10', 'Erica', 'Ross', '22 Peachtree Street', '1975-04-02'),
('hstark16', 'Harmon', 'Stark', '53 Tanker Top Lane', '1971-10-27'),
('echarles19', 'Ella', 'Charles', '22 Peachtree Street', '1974-05-06'),
('csoares8', 'Claire', 'Soares', '706 Living Stone Way', '1965-09-03'),
('agarcia7', 'Alejandro', 'Garcia', '710 Living Water Drive', '1966-10-29'),
('bsummers4', 'Brie', 'Summers', '5105 Dragon Star Circle', '1976-02-09'),
('cjordan5', 'Clark', 'Jordan', '77 Infinite Stars Road', '1966-06-05'),
('fprefontaine6', 'Ford', 'Prefontaine', '10 Hitch Hikers Lane', '1961-01-28');

insert into customers values
('jstone5', 4, 40),
('sprince6', 5, 30),
('awilson5', 2, 100),
('lrodriguez5', 4, 60),
('bsummers4', 3, 110),
('cjordan5', 3, 50);

insert into employees values
('awilson5', '111-11-1111', 9, 46000),
('lrodriguez5', '222-22-2222', 20, 58000),
('tmccall5', '333-33-3333', 29, 33000),
('eross10', '444-44-4444', 10, 61000),
('hstark16', '555-55-5555', 20, 59000),
('echarles19', '777-77-7777', 3, 27000),
('csoares8', '888-88-8888', 26, 57000),
('agarcia7', '999-99-9999', 24, 41000),
('bsummers4', '000-00-0000', 17, 35000),
('fprefontaine6', '121-21-2121', 5, 20000);

insert into store_workers values
('eross10'),
('hstark16'),
('echarles19');

insert into stores values
('pub', 'Publix', 200, 'hstark16'),
('krg', 'Kroger', 300, 'echarles19');

insert into employed_workers values
('pub', 'eross10'),
('pub', 'hstark16'),
('krg', 'eross10'),
('krg', 'echarles19');

insert into drone_pilots values
('awilson5', '314159', 41),
('lrodriguez5', '287182', 67),
('tmccall5', '181633', 10),
('agarcia7', '610623', 38),
('bsummers4', '411911', 35),
('fprefontaine6', '657483', 2);

insert into drones values
('pub', 1, 10, 3, 'awilson5'),
('pub', 2, 20, 2, 'lrodriguez5'),
('krg', 1, 15, 4, 'tmccall5'),
('pub', 9, 45, 1, 'fprefontaine6');

insert into products values
('pr_3C6A9R', 'pot roast', 6),
('ss_2D4E6L', 'shrimp salad', 3),
('hs_5E7L23M', 'hoagie sandwich', 3),
('clc_4T9U25X', 'chocolate lava cake', 5),
('ap_9T25E36L', 'antipasto platter', 4);

insert into orders values
('pub_303', '2024-05-23', 'sprince6', 'pub', 1),
('pub_305', '2024-05-22', 'sprince6', 'pub', 2),
('krg_217', '2024-05-23', 'jstone5', 'krg', 1),
('pub_306', '2024-05-22', 'awilson5', 'pub', 2);

insert into order_lines values
('pub_303', 'pr_3C6A9R', 20, 1),
('pub_303', 'ap_9T25E36L', 4, 1),
('pub_305', 'clc_4T9U25X', 3, 2),
('pub_306', 'hs_5E7L23M', 3, 2),
('pub_306', 'ap_9T25E36L', 10, 1),
('krg_217', 'pr_3C6A9R', 15, 2);

-- -----------------------------------------------
-- stored procedures and views
-- -----------------------------------------------

 

-- add customer
drop procedure if exists add_customer;
delimiter //
create procedure add_customer
	(in ip_uname varchar(40), in ip_first_name varchar(100),
	in ip_last_name varchar(100), in ip_address varchar(500),
	in ip_birthdate date, in ip_rating integer, in ip_credit integer)
begin
	sp_main: begin  
    	-- Check for null values and empty strings in the input parameters
    	if ip_uname is null or ip_first_name is null or ip_last_name is null or ip_address is null or ip_rating is null or ip_credit is null
    	or ip_uname = '' or ip_first_name = '' or ip_last_name = '' or ip_address = '' then
        	select 'Error: One or more required fields are null or empty.' as message;
        	leave sp_main; 
    	end if;

    	-- Check if the username is unique
    	IF NOT EXISTS (SELECT uname FROM users WHERE uname = ip_uname) THEN
        	-- Insert the new customer
        	INSERT INTO users (uname, first_name, last_name, address, birthdate)
        	VALUES (ip_uname, ip_first_name, ip_last_name, ip_address, ip_birthdate);

        	INSERT INTO customers (uname, rating, credit)
        	VALUES (ip_uname, ip_rating, ip_credit);

        	SELECT 'New customer added successfully.' AS message;
    	ELSE
        	SELECT 'Username already exists. Please choose a different username.' AS message;
    	END IF;
	end;
end //
delimiter ;


-- add drone pilot
drop procedure if exists add_drone_pilot;
DELIMITER //
#The new pilot's username, tax ID and license will be unique in the system.
create procedure add_drone_pilot (in ip_uname varchar(40),
in ip_first_name varchar(100), in ip_last_name varchar(100),
in ip_address varchar(500), in ip_birthdate date,
in ip_taxID varchar(40), in ip_service integer,
in ip_salary integer, in ip_licenseID varchar(40),
in ip_experience integer)
sp_main: begin

 
    DECLARE uname_count INT;
	DECLARE taxID_count INT;
	DECLARE license_count INT;
    
    if ip_uname is null or ip_first_name is null or ip_last_name is null or ip_address is null or ip_birthdate is null or ip_taxID is null or 
    ip_service is null or ip_salary is null or  ip_licenseID is null or ip_experience is null or ip_uname = '' or  ip_first_name = '' or 
    ip_last_name = '' or ip_address = '' or ip_taxID = '' or  ip_licenseID = '' then leave sp_main; 
	end if;
    
    -- Check if the username already exists
	SELECT COUNT(*) INTO uname_count FROM users WHERE uname = ip_uname;
	-- Check if the tax ID already exists
	SELECT COUNT(*) INTO taxID_count FROM employees WHERE taxID = ip_taxID;
	-- Check if the license ID already exists
	SELECT COUNT(*) INTO license_count FROM drone_pilots WHERE licenseID = ip_licenseID;

	-- If any of the counts are greater than 0, it means there's a duplicate
	IF uname_count = 0  AND taxID_count = 0 and license_count = 0 THEN
    	-- Insert the new pilot record
    	INSERT INTO users(uname,first_name,last_name,address,birthdate) VALUES (ip_uname, ip_first_name, ip_last_name, ip_address, ip_birthdate);
    	INSERT INTO employees (uname, taxID, service, salary) VALUES (ip_uname, ip_taxID, ip_service, ip_salary);
    	INSERT INTO drone_pilots(uname,licenseID,experience) VALUES (ip_uname,ip_licenseID,ip_experience);
	END IF;

end //

delimiter ;


-- add product
DROP PROCEDURE IF EXISTS add_product;
DELIMITER //
CREATE PROCEDURE add_product
    (IN ip_barcode VARCHAR(40), IN ip_pname VARCHAR(100), IN ip_weight INTEGER)
sp_main: 
BEGIN
 
    IF ip_barcode IN (SELECT barcode FROM products) or ip_barcode is null or ip_weight is null or ip_barcode = ''
    or ip_pname = ''  or ip_weight <=0 THEN LEAVE sp_main; 
    END IF;
    INSERT INTO products VALUES (ip_barcode, ip_pname, ip_weight);
END //
DELIMITER ;


-- add drone
drop procedure if exists add_drone;
DELIMITER //

CREATE PROCEDURE add_drone (
    IN ip_storeID VARCHAR(40),
    IN ip_droneTag INTEGER,
    IN ip_capacity INTEGER,
    IN ip_remaining_trips INTEGER,
    IN ip_pilot VARCHAR(40)
)
sp_main: BEGIN

    DECLARE store_exists INT;
    DECLARE pilot_has_drone INT;
    DECLARE valid_drone INT;
    DECLARE valid_pilot INT;
    
    if ip_storeID is null or ip_droneTag is null or ip_capacity is null or ip_remaining_trips is null or ip_pilot is null or ip_storeID = '' or ip_pilot =  ''  
    then leave sp_main; end if; 
  
    SELECT COUNT(*) INTO store_exists FROM stores WHERE storeID = ip_storeID;    
    SELECT COUNT(*) INTO pilot_has_drone FROM drones WHERE pilot = ip_pilot;
    select count(*) into valid_pilot from drone_pilots where uname = ip_pilot;
    SELECT COUNT(*) INTO valid_drone FROM drones WHERE concat(storeID, DroneTag) = concat(ip_storeID, ip_droneTag);
    
    IF store_exists = 1 AND pilot_has_drone = 0 and valid_drone = 0 and valid_pilot = 1 THEN
        INSERT INTO drones (storeID, droneTag, capacity, remaining_trips, pilot)
        VALUES (ip_storeID, ip_droneTag, ip_capacity, ip_remaining_trips, ip_pilot);
    END IF;
    
END //

DELIMITER ;

-- increase customer credits
DROP PROCEDURE IF EXISTS increase_customer_credits;
DELIMITER //
CREATE PROCEDURE increase_customer_credits (IN ip_uname VARCHAR(40), IN ip_money INTEGER)
sp_main: BEGIN
    IF ip_money < 0 OR ip_uname IS NULL OR ip_money IS NULL or ip_uname = '' THEN
        LEAVE sp_main;
    END IF;

    IF EXISTS (SELECT uname FROM customers WHERE uname = ip_uname) THEN
        UPDATE customers
        SET credit = credit + ip_money
        WHERE uname = ip_uname;
    END IF;
END //

DELIMITER ;


-- swap drone control
drop procedure if exists swap_drone_control;
delimiter //
create procedure swap_drone_control (in ip_incoming_pilot varchar(40),in ip_outgoing_pilot varchar(40))
sp_main: Begin

    declare incoming_pilot_valid INT;
	declare incoming_pilot_controlling INT;
	declare outgoing_pilot_controlling INT;
    
    if ip_incoming_pilot is null or ip_outgoing_pilot is null or ip_outgoing_pilot= '' or ip_incoming_pilot = '' then leave sp_main; end if; 
    
    SELECT COUNT(*) INTO incoming_pilot_valid FROM drone_pilots WHERE uname = ip_incoming_pilot;
	SELECT COUNT(*) INTO incoming_pilot_controlling FROM drones WHERE pilot = ip_incoming_pilot;
	SELECT COUNT(*) INTO outgoing_pilot_controlling FROM drones WHERE pilot = ip_outgoing_pilot;
    
	IF incoming_pilot_valid = 1 AND incoming_pilot_controlling = 0 AND outgoing_pilot_controlling = 1 THEN
   	 UPDATE drones SET pilot = ip_incoming_pilot WHERE pilot = ip_outgoing_pilot;
    END IF;
    
end //
delimiter ;


-- repair and refuel a drone
drop procedure if exists repair_refuel_drone;
delimiter //
CREATE PROCEDURE repair_refuel_drone (
    IN ip_drone_store VARCHAR(40),
    IN ip_drone_tag INTEGER,
    IN ip_refueled_trips INTEGER
)
sp_main: BEGIN

	if ip_drone_store is null or ip_drone_tag is null or ip_refueled_trips is null or ip_drone_store='' then leave sp_main;
	end if; 

    IF ip_refueled_trips >= 0 THEN
        UPDATE drones 
        SET remaining_trips = ip_refueled_trips + remaining_trips  
        WHERE storeID = ip_drone_store AND droneTag = ip_drone_tag;
    END IF;
END //

DELIMITER ;


-- begin order
drop procedure if exists begin_order;
delimiter // 
create procedure begin_order
	(in ip_orderID varchar(40), in ip_sold_on date,
    in ip_purchased_by varchar(40), in ip_carrier_store varchar(40),
    in ip_carrier_tag integer, in ip_barcode varchar(40),
    in ip_price integer, in ip_quantity integer)
sp_main: begin
	declare valid_purchased_by int;
    declare valid_orderID int;
    declare valid_carrier_tag int;
    declare valid_barcode int;
    declare rem_credit int;
    declare rem_capacity int;
    declare prod_weight int;
    declare rem_trips int;
    declare total_current_weight int;
    declare total_credit int;
    DECLARE existing_orders INT DEFAULT 0;
    
    select COUNT(*) into valid_purchased_by from customers where uname = ip_purchased_by;
    select COUNT(*) into valid_orderID from orders where orderID = ip_orderID;
    select COUNT(*) into valid_carrier_tag from drones where concat(storeID, droneTag) LIKE concat(ip_carrier_store, ip_carrier_tag);
    select COUNT(*) into valid_barcode from products where barcode = ip_barcode;
    select credit into rem_credit from customers where uname LIKE ip_purchased_by;
	select capacity into rem_capacity from drones join orders on concat(storeID, droneTag) = concat(carrier_store, carrier_tag) where orderID = ip_orderID;
    select weight into prod_weight from products where barcode = ip_barcode;
    
    
    /*#select remaining_trips into rem_trips from drones where concat(storeID, droneTag) LIKE concat(ip_carrier_store, ip_carrier_tag);
    -- Calculate total weight currently assigned to the drone
	#select SUM(ol.quantity * p.weight) INTO total_current_weight from order_lines ol
	#join orders o on ol.orderID = o.orderID join products p on ol.barcode = p.barcode join drones on concat(storeID, droneTag) = concat(o.carrier_store, o.carrier_tag) 
    #where concat(storeID, droneTag) = concat(ip_carrier_store, ip_carrier_tag) group by concat(ip_carrier_store, ip_carrier_tag);
    
    -- calculate the total credits of current order
	#select sum(price* quantity) into total_credit from orders natural join order_lines where orderID = ip_orderID group by purchased_by, orderID;
    
    -- validate condition 1 and for nulls and empty strings
    if  valid_purchased_by != 1 or ip_purchased_by is null or ip_purchased_by = '' then leave sp_main;
    elseif valid_orderID > 0 or ip_orderID is null or ip_orderID = '' then leave sp_main;
    elseif valid_carrier_tag != 1 or ip_carrier_store is null or ip_carrier_tag is null or ip_carrier_store = '' or ip_carrier_tag = '' then leave sp_main;
    elseif valid_barcode != 1 or ip_barcode is null or ip_barcode = '' then leave sp_main;
    -- validate condition 2
    elseif ip_price <= 0 OR ip_quantity <= 0 then leave sp_main;
    -- validate condition 3
    elseif ip_price * ip_quantity > rem_credit then leave sp_main;
    #elseif ((ip_price * ip_quantity) + total_credit) > rem_credit then leave sp_main;
    -- validate condition 4
    elseif rem_capacity < (ip_quantity * prod_weight) then leave sp_main;
    #elseif rem_capacity < (total_current_weight + (ip_quantity * prod_weight)) then leave sp_main;
    -- validate if drone has remaining trips
    #elseif rem_trips <= 0 then leave sp_main;
    end if; 
    insert into orders values (ip_orderID, ip_sold_on, ip_purchased_by, ip_carrier_store, ip_carrier_tag);
    insert into order_lines values (ip_orderID, ip_barcode, ip_price, ip_quantity); */
    
    
    #SELECT COUNT(*) INTO existing_orders FROM orders WHERE purchased_by = ip_purchased_by;

    -- Validate conditions
    IF valid_purchased_by != 1 THEN
        #SELECT 'Invalid customer username' AS message;
        LEAVE sp_main;
    ELSEIF valid_orderID > 0 THEN
        #SELECT 'Invalid order ID' AS message;
        LEAVE sp_main;
    ELSEIF valid_carrier_tag != 1 OR ip_carrier_store IS NULL OR ip_carrier_tag IS NULL OR ip_carrier_store = '' OR ip_carrier_tag = '' THEN
        #SELECT 'Invalid drone or store ID' AS message;
        LEAVE sp_main;
    ELSEIF valid_barcode != 1 OR ip_barcode IS NULL OR ip_barcode = '' THEN
        #SELECT 'Invalid product barcode' AS message;
        LEAVE sp_main;
    ELSEIF ip_price <= 0 OR ip_quantity <= 0 THEN
        #SELECT 'Price must be positive and quantity must be greater than zero' AS message;
        LEAVE sp_main;
    ELSEIF ip_price * ip_quantity > rem_credit THEN
        #SELECT 'Insufficient credits to purchase the product' AS message;
        LEAVE sp_main;
    ELSEIF rem_capacity < ip_quantity * prod_weight THEN
        SELECT 'Insufficient drone capacity to carry the product' AS message;
        LEAVE sp_main;
    ELSEIF rem_trips <= 0 THEN
        #SELECT 'Drone has no remaining trips' AS message;
        LEAVE sp_main;
    #ELSEIF existing_orders > 0 THEN
        #SELECT 'Customer has existing orders. Please wait until they are delivered or canceled.' AS message;
        #LEAVE sp_main;
    END IF;

    -- Insert the order and order line
    INSERT INTO orders (orderID, sold_on, purchased_by, carrier_store, carrier_tag)
    VALUES (ip_orderID, ip_sold_on, ip_purchased_by, ip_carrier_store, ip_carrier_tag);

    INSERT INTO order_lines (orderID, barcode, price, quantity)
    VALUES (ip_orderID, ip_barcode, ip_price, ip_quantity);

    #SELECT 'Order placed successfully' AS message;
		
end //
delimiter ;

call begin_order('aw', '1999-09-09', 'akrishna311', 'krg', 1, 'ap_9T25E36L', 1, 1);

-- add order line
drop procedure if exists add_order_line;
delimiter // 
create procedure add_order_line
	(in ip_orderID varchar(40), in ip_barcode varchar(40),  in ip_price integer, in ip_quantity integer)
sp_main: begin
    declare valid_orderID int;
    declare valid_barcode int;
    declare dup_barcode int;
    declare rem_credit int;
    declare rem_capacity int;
    declare prod_weight int;
    declare total_current_weight int;
    declare total_credit int;
    
    select COUNT(*) into valid_orderID from orders where orderID = ip_orderID;
    select COUNT(*) into valid_barcode from products where barcode = ip_barcode;
    select COUNT(*) into dup_barcode from order_lines where orderID = ip_orderID and barcode = ip_barcode;
    select credit into rem_credit from orders join customers on purchased_by = uname where orderID LIKE ip_orderID;
    select capacity into rem_capacity from drones join orders on concat(storeID, droneTag) = concat(carrier_store, carrier_tag) where orderID = ip_orderID;
    select weight into prod_weight from products where barcode = ip_barcode;
    -- Calculate total weight currently assigned to the drone
	select SUM(ol.quantity * p.weight) INTO total_current_weight from order_lines ol
	join orders o on ol.orderID = o.orderID join products p on ol.barcode = p.barcode join drones on concat(storeID, droneTag) = concat(o.carrier_store, o.carrier_tag) 
    where o.orderID = ip_orderID group by o.orderID;
    
    -- calculate the total credits of current order
	select sum(price* quantity) into total_credit from order_lines where orderID = ip_orderID group by orderID;
    
    -- validate condition 1 and nulls and empty strings
    if valid_orderID != 1 or ip_orderID is null or ip_orderID = '' then leave sp_main;
    elseif valid_barcode != 1  or ip_barcode is null or ip_barcode = '' then leave sp_main;
    -- validate condition 2
    elseif dup_barcode > 0 then leave sp_main;
    -- validate condition 3
    elseif ip_price <= 0 OR ip_quantity <= 0 then leave sp_main;
    -- validate condition 4
    elseif ((ip_price * ip_quantity) + total_credit) > rem_credit then leave sp_main;
	-- Validate condition 5: Check drone capacity including current load
	elseif rem_capacity < (total_current_weight + (ip_quantity * prod_weight)) then leave sp_main;
    else insert into order_lines values (ip_orderID, ip_barcode, ip_price, ip_quantity);
    end if;
end //
delimiter ;


-- deliver order
drop procedure if exists deliver_order;
delimiter // 
create procedure deliver_order(in ip_orderID varchar(40))
sp_main: begin
    declare valid_orderID int;
    declare rem_trips int;
    declare total_cost int;
    declare cust_name varchar(100);
    declare str_name varchar(100);
    declare der_drone_tag varchar(100);
    declare pilot_name varchar(100);
    
    select COUNT(*) into valid_orderID from orders where orderID = ip_orderID;
    select remaining_trips into rem_trips from drones join drone_pilots on pilot=uname where concat(storeID, droneTag) in (select concat(carrier_store, carrier_tag) as drone_tag_tmp from orders where orderID=ip_orderID);
    select sum(price*quantity) into total_cost from order_lines group by orderID having orderID = ip_orderID;
    select purchased_by into cust_name from orders where orderID = ip_orderID;
    select carrier_store into str_name from orders where orderID = ip_orderID;
    select concat(carrier_store, carrier_tag) into der_drone_tag from orders where orderID = ip_orderID;
    select uname into pilot_name from drones join drone_pilots on pilot=uname where concat(storeID, droneTag) in (select concat(carrier_store, carrier_tag) as drone_tag_tmp from orders where orderID=ip_orderID);
    
    -- validate conditions and check for null or empty strings
    if valid_orderID != 1 or ip_orderID is null or ip_orderID = '' then leave sp_main;
    elseif rem_trips <= 0 then leave sp_main;
    end if;
    
    -- reduce credit
    update customers set credit = credit - total_cost where uname = cust_name;
    -- update store revenue
    update stores set revenue = revenue + total_cost where storeID = str_name;
    -- reduce drone trips
    update drones set remaining_trips = remaining_trips - 1 where concat(storeID, droneTag) = der_drone_tag;
    -- update pilot experience
    update drone_pilots set experience = experience + 1 where uname = pilot_name;
    -- update customer rating
    update customers set rating = case when total_cost > 25 and rating != 5 then rating + 1 else rating end where uname = cust_name;
    -- remove order
    delete from order_lines where orderID = ip_orderID;
    delete from orders where orderID = ip_orderID;
    
end //
delimiter ;


-- cancel an order
drop procedure if exists cancel_order;
delimiter //
create procedure cancel_order
	(in ip_orderID varchar(40))
begin
	-- Check if the order ID exists and related fields are not null or empty
	declare orderExists int default 0;
	declare linesValid int default 0;

	-- Check if the order exists and related fields are not null and not empty
	select count(*) into orderExists
	from orders
	where orderID = ip_orderID
	and sold_on is not null
	and carrier_store is not null and carrier_store != ''
	and carrier_tag is not null;

	-- Check if the related order_lines fields are not null for the given orderID
	select count(*) into linesValid
	from order_lines
	where orderID = ip_orderID
	and quantity is not null;

	if orderExists > 0 and linesValid > 0 then
    	-- Decrease customer rating by one (if permitted)
    	update customers set rating = rating - 1
    	where uname = (
        	select purchased_by
        	from orders
        	where orderID = ip_orderID
        	and sold_on = (
            	select max(sold_on)
            	from orders
            	where orderID = ip_orderID
        	)
    	);

    	-- Remove all records of the order
    	delete from order_lines where orderID = ip_orderID;
    	delete from orders where orderID = ip_orderID;
    	select 'Order canceled successfully.' as message;
	else
    	select 'Invalid order ID or null/empty fields detected.' as message;
	end if;
end //
delimiter ;


-- display persons distribution across roles
CREATE OR REPLACE VIEW role_distribution AS
SELECT 'Customers' AS category, COUNT(*) AS total
FROM customers
UNION
SELECT 'Employees' AS category, COUNT(*) AS total
FROM employees
UNION
SELECT 'Users' AS category, COUNT(*) AS total
FROM (
    SELECT uname FROM customers
    UNION
    SELECT uname FROM employees
) AS Users
UNION
SELECT 'Drone_Pilots' AS category, COUNT(*) AS total
FROM drone_pilots
UNION

SELECT 'Store_Workers' AS category, COUNT(*) AS total
FROM store_workers
UNION
SELECT 'Other_Employee_Roles' AS category, COUNT(*) AS total
FROM (
    SELECT uname FROM employees
    WHERE uname NOT IN (SELECT uname FROM drone_pilots)
    AND uname NOT IN (SELECT uname FROM store_workers)
) AS other_employee_roles
UNION
SELECT 'Customer_Employer_Overlap' AS category, COUNT(*) AS total
FROM (
    SELECT e.uname
    FROM employees e
    JOIN customers c ON e.uname = c.uname
) AS Customer_Employer_Overlap;


-- display customer status and current credit and spending activity
create or replace view customer_credit_check as
SELECT 
    uname AS customer_name,
    rating,
    credit AS current_credit,
    IFNULL(SUM(price * quantity), 0) AS credit_already_allocated
FROM 
    orders o 
RIGHT JOIN 
    order_lines ol ON o.orderID = ol.orderID 
RIGHT JOIN 
    customers c ON c.uname = o.purchased_by
GROUP BY 
    Uname;


-- display drone status and current activity
CREATE OR REPLACE VIEW drone_traffic_control AS
SELECT 
    d.storeID AS drone_serves_store,
    d.droneTag AS drone_tag,
    dp.uname AS pilot,
    d.capacity AS total_weight_allowed,
    COALESCE(SUM(ol.quantity * p.weight), 0) AS current_weight,
    d.remaining_trips AS deliveries_allowed,
    COUNT(DISTINCT o.orderID) AS deliveries_in_progress
FROM 
    drones d
LEFT JOIN 
    drone_pilots dp ON d.pilot = dp.uname
LEFT JOIN 
    orders o ON (d.storeID = o.carrier_store AND d.droneTag = o.carrier_tag)
LEFT JOIN 
    order_lines ol ON o.orderID = ol.orderID
LEFT JOIN 
    products p ON ol.barcode = p.barcode
GROUP BY 
    d.storeID, d.droneTag, dp.uname, d.capacity, d.remaining_trips;


-- display product status and current activity including most popular products
create or replace view most_popular_products (barcode, product_name, weight, lowest_price,
	highest_price, lowest_quantity, highest_quantity, total_quantity) as
SELECT p.barcode AS barcode,
       p.pname AS product_name,
       p.weight AS weight,
       MIN(price) AS lowest_price,
       MAX(price) AS highest_price,
       ifnull(MIN(ol.quantity), 0) AS lowest_quantity,
       ifnull(MAX(ol.quantity),0) AS highest_quantity,
       ifnull(SUM(ol.quantity),0) AS total_quantity
FROM products p
left JOIN order_lines ol ON p.barcode = ol.barcode
GROUP BY p.barcode;


-- display drone pilot status and current activity including experience
/*create or replace view drone_pilot_roster as
select uname as pilot,licenseID,storeID as drone_serves_store,droneTag as drone_tag,experience as successful_deliveries,pending_deliveries from drone_pilots left join
(select pilot,count(*) as pending_deliveries,storeID,droneTag from orders natural join order_lines
right join drones on concat(carrier_store,carrier_tag)=concat(storeID,droneTag) group by pilot,storeID,droneTag) as tmp on uname=pilot;
*/

-- display drone pilot status and current activity including experience
create or replace view drone_pilot_roster (pilot, licenseID, drone_serves_store, drone_tag, successful_deliveries, pending_deliveries) as
select uname, licenseID, storeID, droneTag, experience, 
ifnull((select count(*) from drone_pilots dp left join drones on uname=pilot join orders on concat(carrier_store,carrier_tag)=concat(storeID,droneTag) 
where dp.uname = drone_pilots.uname group by uname), 0)
from drone_pilots left join drones on uname=pilot;


-- display store revenue and activity
CREATE OR REPLACE VIEW store_sales_overview AS
SELECT s.storeID AS store_id,
       s.sname,
       s.manager,
       s.revenue + COALESCE(SUM(ol.price * ol.quantity), 0) -
       COALESCE(SUM(CASE WHEN o.orderID IS NULL THEN 0 ELSE ol.price * ol.quantity END), 0) AS current_revenue,
       COALESCE(SUM(CASE WHEN o.orderID IS NULL THEN 0 ELSE ol.price * ol.quantity END), 0) AS incoming_revenue,
       COUNT(DISTINCT o.orderID) AS incoming_orders
FROM stores s
LEFT JOIN orders o ON s.storeID = o.carrier_store
LEFT JOIN order_lines ol ON o.orderID = ol.orderID
GROUP BY s.storeID, s.sname, s.manager, s.revenue;


-- display the current orders that are being placed/in progress
create or replace view orders_in_progress (orderID, cost, num_products, payload, contents) as
select orderID, sum(price*quantity), count(*), sum(weight*quantity), group_concat(pname SEPARATOR ',') 
from orders natural join order_lines natural join products group by orderID;


-- remove customer
drop procedure if exists remove_customer;
delimiter //
create procedure remove_customer
	(in ip_uname varchar(40))
begin
	sp_main: begin
    	-- Check if uname is not null and not an empty string
    	if ip_uname is null or ip_uname = '' then
        	select 'Error: Username is null or empty.' as message;
        	leave sp_main;
    	end if;

    	-- Check if the customer has any orders
    	IF (SELECT COUNT(*) FROM orders WHERE purchased_by = ip_uname) = 0 THEN
        	-- If no orders, check if the user is also an employee
        	IF (SELECT COUNT(*) FROM employees WHERE uname = ip_uname) > 0 THEN
            	-- If also an employee, only delete from customers table
            	DELETE FROM customers WHERE uname = ip_uname;
        	ELSE
            	-- If not an employee, delete from users table
            	DELETE FROM users WHERE uname = ip_uname;
        	END IF;
        	SELECT 'Customer removed successfully.' AS message;
    	ELSE
        	-- If there are orders, do not delete the customer
        	SELECT 'Customer has pending orders and cannot be removed.' AS message;
    	END IF;
	end;
end //
delimiter ;


-- remove drone pilot
drop procedure if exists remove_drone_pilot;
delimiter //
create procedure remove_drone_pilot (in ip_uname varchar(40))
sp_main:begin
    declare control_pilot int;
    declare customer_pilot int;

    if ip_uname is null or ip_uname = '' then
        leave sp_main;
    end if;

    select count(*) into control_pilot from drones where pilot = ip_uname;
    select count(*) into customer_pilot from customers where uname = ip_uname;

    if control_pilot = 0 then
        if customer_pilot = 0 then
            delete from drone_pilots where uname = ip_uname;
            delete from employees where uname = ip_uname;
            delete from users where uname = ip_uname;
       else
            delete from drone_pilots where uname = ip_uname;
            delete from employees where uname = ip_uname;
        end if;
    end if;
end //

delimiter ;


-- remove product
drop procedure if exists remove_product;
delimiter // 
create procedure remove_product
	(in ip_barcode varchar(40))
sp_main: begin
	if ip_barcode in(select barcode from order_lines)  or ip_barcode is null or ip_barcode = '' then leave sp_main; end if;
    delete from products where barcode = ip_barcode;
end //
delimiter ;


-- remove drone
drop procedure if exists remove_drone; 
DELIMITER //

CREATE PROCEDURE remove_drone (
    IN ip_storeID VARCHAR(40),
    IN ip_droneTag INTEGER
)
sp_main: BEGIN
    DECLARE pending_orders INT;

if ip_storeID is null or ip_droneTag is null or ip_storeID = '' then leave sp_main; end if;  

    
    SELECT COUNT(*)
    INTO pending_orders
    FROM orders
    WHERE carrier_store = ip_storeID AND carrier_tag = ip_droneTag;
    
    IF pending_orders = 0 THEN
        DELETE FROM drones
        WHERE storeID = ip_storeID AND droneTag = ip_droneTag;
    END IF;
END //

DELIMITER ;