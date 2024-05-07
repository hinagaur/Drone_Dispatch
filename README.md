# Drone_Dispatch

#### Database Description

A Drone Dispatch Express Delivery System is designed and developed to monitor deliveries of grocery products to customers. This system will support a "third party" grocery service. Customers will place orders with the service. The service will coordinate with grocery stores to find the products (at variable – but hopefully the lowest – prices) and arrange for a drone to deliver the products to the customer. On delivery, the store will be paid electronically by the customer.


#### Instructions to setup the app

Open the phase4.py and ensure all the necessary libraries are installed
pip install mysql-connector-python
pip install tkintertable
pip install datetime

#### To connect to the MySQL first make sure the phase4.sql file is open and running in MySQL Workbench
- Make note of the host name, username, and password used to launch the SQL connection in MySQL
- On line 9 input the information in the corresponding sections and save the changes
- should look like this host='ENTER HOST NAME HERE', username='ENTER USERNAME HERE', password='ENTER PASSWORD HERE'

#### Instructions to run the app

To launch the app open the powershell terminal and execute `python phase4.py`

#### Brief explanation of what technologies were used 

A simple GUI was created using Tkinter to create all the necessary sections (Customers, Products, Drones, etc.) and 
drop down menus (Add Customer, Add Drone, Add Product, etc.) to handle the stored procedures and views,
as well has handle all the contraints on the frontend rather than sending them back to MySQL to prevent any unnecessary requests being made
to the server. MySQL Connector was used to establish the connection between the MySQL Workbench server and the application.

