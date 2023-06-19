# car_management_system




The Car Management System is a PyQt5-based application that allows users to manage maintenance and incidents for different cars. It provides a graphical user interface (GUI) for adding, removing, and viewing maintenance and incident details for each car.

### Functionality


The Car Management System consists of the following main components:

**MainWindow:** The main window of the application displays a combobox that allows the user to select a car from a list. The selected car's details are displayed, including the car's model and year. The user can also click on the "Manage Maintenance" and "Manage Incidents" buttons to open separate dialogs for managing maintenance and incidents related to the selected car.



**MaintenanceDialog:** This dialog displays a list of existing maintenance items and provides a button for removing selected items.



**IncidentsDialog:** This dialog displays a list of existing incidents and provides a buttons for removing selected incidents.



**Database:** The application uses an SQLite database named "car_management.db" to store car, maintenance, and incident data. The database consists of three tables: "cars," "maintenance," and "incidents." The "cars" table stores information about each car, including the license plate, model, and year. The "maintenance" table stores maintenance items associated with each car. The "incidents" table stores incidents related to each car.

## Screenshot

![image](https://github.com/DancesWithDobes/car_management_system/assets/69741804/1060949e-b856-4b68-a891-50b8cfffca49)


![image](https://github.com/DancesWithDobes/car_management_system/assets/69741804/6844cc40-cc5e-4050-8397-9c80e49764f3)


![image](https://github.com/DancesWithDobes/car_management_system/assets/69741804/e8946560-56e7-4458-9740-28c5c87e5848)

## Usage


**To use the Car Management System, follow these steps:**

Install the required dependencies by running the following command:

``` pip install PyQt5 ```


Be sure the SQLite database file named "car_management.db" is in the same directory as the script.

Execute the script using Python:

``` python3 main.py ```


The main window of the Car Management System will open, displaying a combobox with a list of cars. Select a car from the list to view its details.


Double clicking on a car will open both the Maintenance dialog and Incidents diaglog in sequence. In these dialogs, you can remove existing items for the selected car.


Click the "Add Maintenamce" or "Add Incident" buttons on the main screen to add maintenance or incidents, respectively. Be sure to have the whole role highlighted. A good way to do so, is clicking the number on the far left. This will ensure you won't trigger the maintenance or incidence pop-ups to trigger.

Click "Add vehicle" to add a vehicle to the list. 

To remove a vehicle, click the "Remove Vehicle" button when the row is highlighted. Again, clicking the numbers on the far left is the best way to highlight the row.




Close the dialogs and main window to exit the application.

## Dependencies

The Car Management System relies on the following dependencies:

``` Python 3.x ```
``` PyQt5 ```
``` SQLite3 ```

Ensure that you have these dependencies installed before running the application.
