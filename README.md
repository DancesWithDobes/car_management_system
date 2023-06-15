# car_management_system




The Car Management System is a PyQt5-based application that allows users to manage maintenance and incidents for different cars. It provides a graphical user interface (GUI) for adding, removing, and viewing maintenance and incident details for each car.

### Functionality


The Car Management System consists of the following main components:

**MainWindow:** The main window of the application displays a combobox that allows the user to select a car from a list. The selected car's details are displayed, including the car's model and year. The user can also click on the "Manage Maintenance" and "Manage Incidents" buttons to open separate dialogs for managing maintenance and incidents related to the selected car.



**MaintenanceDialog:** This dialog allows the user to add and remove maintenance items for a specific car. It displays a list of existing maintenance items and provides buttons for adding new items and removing selected items.



**IncidentsDialog:** This dialog allows the user to add and remove incidents for a specific car. It displays a list of existing incidents and provides buttons for adding new incidents and removing selected incidents.



**Database:** The application uses an SQLite database named "car_management.db" to store car, maintenance, and incident data. The database consists of three tables: "cars," "maintenance," and "incidents." The "cars" table stores information about each car, including the license plate, model, and year. The "maintenance" table stores maintenance items associated with each car. The "incidents" table stores incidents related to each car.

## Screenshot

![image](https://github.com/DancesWithDobes/vehicle_task_manager/assets/69741804/b8302562-1922-4e67-b81c-4945d600f794)





## Usage


**To use the Car Management System, follow these steps:**

Install the required dependencies by running the following command:

``` pip install PyQt5 ```


Be sure the SQLite database file named "car_management.db" is in the same directory as the script.

Execute the script using Python:

``` main.py ```


The main window of the Car Management System will open, displaying a combobox with a list of cars. Select a car from the list to view its details.


Click the "Manage Maintenance" button to open the Maintenance dialog. In this dialog, you can add new maintenance items and remove existing items for the selected car.


Click the "Manage Incidents" button to open the Incidents dialog. In this dialog, you can add new incidents and remove existing incidents for the selected car.


Close the dialogs and main window to exit the application.

## Dependencies

The Car Management System relies on the following dependencies:

``` Python 3.x ```
``` PyQt5 ```
``` SQLite3 ```

Ensure that you have these dependencies installed before running the application.
