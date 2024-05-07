i. Instructions to setup your app

Open the phase4.py and ensure all the necessary libraries are installed
pip install mysql-connector-python
pip install tkintertable
pip install datetime

To connect to the MySQL first make sure the phase4.sql file is open and running in MySQL Workbench
- Make note of the host name, username, and password used to launch the SQL connection in MySQL
- On line 9 input the information in the corresponding sections and save the changes
- should look like this host='ENTER HOST NAME HERE', username='ENTER USERNAME HERE', password='ENTER PASSWORD HERE'

ii. Instructions to run your app

To launch the app open the powershell terminal and execute `python phase4.py`

iii. Brief explanation of what technologies you used and how you accomplished your application

We created a simple GUI using Tkinter to create all the necessary sections (Customers, Products, Drones, etc.) and 
drop down menus (Add Customer, Add Drone, Add Product, etc.) to handle the stored procedures and views,
as well has handle all the contraints on the frontend rather than sending them back to MySQL to prevent any unnecessary requests being made
to the server. We used MySQL Connector to establish the connection between the MySQL Workbench server and the application.

iv. Explanation of how work was distributed among the team members
Prarthana: 
5 Stored Procedures 
Testing/Debugging

Hina: 
5 Stored Procedures 
Testing/Debugging

Anagha:
5 Stored Procedures 
Testing/Debugging

Bengy:
Views 
Testing/Debugging
Readme