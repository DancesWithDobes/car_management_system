import sys
import sqlite3
from PyQt5 import QtWidgets


class CarManagementSystem(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Car Management System")

        self.car_listwidget = QtWidgets.QListWidget()

        self.add_vehicle_button = QtWidgets.QPushButton("Add Vehicle")
        self.remove_vehicle_button = QtWidgets.QPushButton("Remove Vehicle")
        self.add_maintenance_button = QtWidgets.QPushButton("Add Maintenance")
        self.remove_maintenance_button = QtWidgets.QPushButton("Remove Maintenance")
        self.add_incident_button = QtWidgets.QPushButton("Add Incident")
        self.remove_incident_button = QtWidgets.QPushButton("Remove Incident")

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.add_vehicle_button)
        button_layout.addWidget(self.remove_vehicle_button)
        button_layout.addWidget(self.add_maintenance_button)
        button_layout.addWidget(self.remove_maintenance_button)
        button_layout.addWidget(self.add_incident_button)
        button_layout.addWidget(self.remove_incident_button)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(self.car_listwidget)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        self.load_cars()

        self.car_listwidget.itemClicked.connect(self.view_car_details)
        self.add_vehicle_button.clicked.connect(self.add_vehicle)
        self.remove_vehicle_button.clicked.connect(self.remove_vehicle)
        self.add_maintenance_button.clicked.connect(self.add_maintenance)
        self.remove_maintenance_button.clicked.connect(self.remove_maintenance)
        self.add_incident_button.clicked.connect(self.add_incident)
        self.remove_incident_button.clicked.connect(self.remove_incident)

    def load_cars(self):
        conn = sqlite3.connect("car_management.db")
        cursor = conn.cursor()

        cursor.execute("SELECT license_plate FROM cars")
        cars = cursor.fetchall()

        self.car_listwidget.clear()
        for car in cars:
            car_item = QtWidgets.QListWidgetItem(car[0])
            self.car_listwidget.addItem(car_item)

        conn.close()

    def view_car_details(self, item):
        license_plate = item.text()

        details_dialog = CarDetailsDialog(license_plate)
        details_dialog.exec_()

    def add_vehicle(self):
        dialog = AddVehicleDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            make = dialog.make_input.text()
            model = dialog.model_input.text()
            year = dialog.year_input.text()
            color = dialog.color_input.text()
            license_plate = dialog.license_plate_input.text()

            conn = sqlite3.connect("car_management.db")
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO cars (make, model, year, color, license_plate) VALUES (?, ?, ?, ?, ?)",
                (make, model, year, color, license_plate),
            )

            conn.commit()
            conn.close()

            self.load_cars()

    def remove_vehicle(self):
        selected_item = self.car_listwidget.currentItem()
        if selected_item:
            license_plate = selected_item.text()

            conn = sqlite3.connect("car_management.db")
            cursor = conn.cursor()

            cursor.execute("DELETE FROM cars WHERE license_plate = ?", (license_plate,))

            conn.commit()
            conn.close()

            self.load_cars()

    def add_maintenance(self):
        selected_item = self.car_listwidget.currentItem()
        if selected_item:
            license_plate = selected_item.text()

            dialog = AddMaintenanceDialog(license_plate)
            if dialog.exec_() == QtWidgets.QDialog.Accepted:
                maintenance_type = dialog.maintenance_type_input.text()

                conn = sqlite3.connect("car_management.db")
                cursor = conn.cursor()

                cursor.execute("SELECT id FROM cars WHERE license_plate = ?", (license_plate,))
                car_id = cursor.fetchone()[0]

                cursor.execute(
                    "INSERT INTO maintenance (car_id, maintenance_type) VALUES (?, ?)",
                    (car_id, maintenance_type),
                )

                conn.commit()
                conn.close()

    def remove_maintenance(self):
        selected_item = self.car_listwidget.currentItem()
        if selected_item:
            license_plate = selected_item.text()

            dialog = MaintenanceDialog(license_plate)
            if dialog.exec_() == QtWidgets.QDialog.Accepted:
                maintenance = dialog.selected_maintenance()
                if maintenance:
                    conn = sqlite3.connect("car_management.db")
                    cursor = conn.cursor()

                    cursor.execute("SELECT id FROM cars WHERE license_plate = ?", (license_plate,))
                    car_id = cursor.fetchone()[0]

                    cursor.execute(
                        "DELETE FROM maintenance WHERE car_id = ? AND maintenance_type = ?",
                        (car_id, maintenance),
                    )

                    conn.commit()
                    conn.close()

    def add_incident(self):
        selected_item = self.car_listwidget.currentItem()
        if selected_item:
            license_plate = selected_item.text()

            dialog = AddIncidentDialog(license_plate)
            if dialog.exec_() == QtWidgets.QDialog.Accepted:
                description = dialog.description_input.text()

                conn = sqlite3.connect("car_management.db")
                cursor = conn.cursor()

                cursor.execute("SELECT id FROM cars WHERE license_plate = ?", (license_plate,))
                car_id = cursor.fetchone()[0]

                cursor.execute(
                    "INSERT INTO incidents (car_id, description) VALUES (?, ?)",
                    (car_id, description),
                )

                conn.commit()
                conn.close()

    def remove_incident(self):
        selected_item = self.car_listwidget.currentItem()
        if selected_item:
            license_plate = selected_item.text()

            dialog = IncidentDialog(license_plate)
            if dialog.exec_() == QtWidgets.QDialog.Accepted:
                incident = dialog.selected_incident()
                if incident:
                    conn = sqlite3.connect("car_management.db")
                    cursor = conn.cursor()

                    cursor.execute("SELECT id FROM cars WHERE license_plate = ?", (license_plate,))
                    car_id = cursor.fetchone()[0]

                    cursor.execute(
                        "DELETE FROM incidents WHERE car_id = ? AND description = ?",
                        (car_id, incident),
                    )

                    conn.commit()
                    conn.close()


class CarDetailsDialog(QtWidgets.QDialog):
    def __init__(self, license_plate):
        super().__init__()

        self.setWindowTitle("Car Details")

        self.maintenance_listwidget = QtWidgets.QListWidget()
        self.incident_listwidget = QtWidgets.QListWidget()

        self.cancel_button = QtWidgets.QPushButton("Cancel")

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.cancel_button)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(QtWidgets.QLabel(f"License Plate: {license_plate}"))
        main_layout.addWidget(QtWidgets.QLabel("Maintenance Log:"))
        main_layout.addWidget(self.maintenance_listwidget)
        main_layout.addWidget(QtWidgets.QLabel("Incident Log:"))
        main_layout.addWidget(self.incident_listwidget)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        self.load_maintenance(license_plate)
        self.load_incidents(license_plate)

        self.cancel_button.clicked.connect(self.reject)

    def load_maintenance(self, license_plate):
        conn = sqlite3.connect("car_management.db")
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM cars WHERE license_plate = ?", (license_plate,))
        car_id = cursor.fetchone()[0]

        cursor.execute("SELECT maintenance_type FROM maintenance WHERE car_id = ?", (car_id,))
        maintenance_records = cursor.fetchall()

        self.maintenance_listwidget.clear()
        for record in maintenance_records:
            maintenance_item = QtWidgets.QListWidgetItem(record[0])
            self.maintenance_listwidget.addItem(maintenance_item)

        conn.close()

    def load_incidents(self, license_plate):
        conn = sqlite3.connect("car_management.db")
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM cars WHERE license_plate = ?", (license_plate,))
        car_id = cursor.fetchone()[0]

        cursor.execute("SELECT description FROM incidents WHERE car_id = ?", (car_id,))
        incident_records = cursor.fetchall()

        self.incident_listwidget.clear()
        for record in incident_records:
            incident_item = QtWidgets.QListWidgetItem(record[0])
            self.incident_listwidget.addItem(incident_item)

        conn.close()


class AddVehicleDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add Vehicle")

        self.make_input = QtWidgets.QLineEdit()
        self.model_input = QtWidgets.QLineEdit()
        self.year_input = QtWidgets.QLineEdit()
        self.color_input = QtWidgets.QLineEdit()
        self.license_plate_input = QtWidgets.QLineEdit()

        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.add_button = QtWidgets.QPushButton("Add")

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.add_button)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(QtWidgets.QLabel("Make:"))
        main_layout.addWidget(self.make_input)
        main_layout.addWidget(QtWidgets.QLabel("Model:"))
        main_layout.addWidget(self.model_input)
        main_layout.addWidget(QtWidgets.QLabel("Year:"))
        main_layout.addWidget(self.year_input)
        main_layout.addWidget(QtWidgets.QLabel("Color:"))
        main_layout.addWidget(self.color_input)
        main_layout.addWidget(QtWidgets.QLabel("License Plate:"))
        main_layout.addWidget(self.license_plate_input)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        self.cancel_button.clicked.connect(self.reject)
        self.add_button.clicked.connect(self.accept)


class AddMaintenanceDialog(QtWidgets.QDialog):
    def __init__(self, license_plate):
        super().__init__()

        self.setWindowTitle("Add Maintenance")

        self.maintenance_type_input = QtWidgets.QLineEdit()

        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.add_button = QtWidgets.QPushButton("Add")

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.add_button)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(QtWidgets.QLabel(f"License Plate: {license_plate}"))
        main_layout.addWidget(QtWidgets.QLabel("Maintenance Type:"))
        main_layout.addWidget(self.maintenance_type_input)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        self.cancel_button.clicked.connect(self.reject)
        self.add_button.clicked.connect(self.accept)


class MaintenanceDialog(QtWidgets.QDialog):
    def __init__(self, license_plate):
        super().__init__()

        self.setWindowTitle("Remove Maintenance")

        self.maintenance_listwidget = QtWidgets.QListWidget()

        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.remove_button = QtWidgets.QPushButton("Remove")

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.remove_button)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(QtWidgets.QLabel(f"License Plate: {license_plate}"))
        main_layout.addWidget(QtWidgets.QLabel("Select Maintenance to Remove:"))
        main_layout.addWidget(self.maintenance_listwidget)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        self.load_maintenance(license_plate)

        self.cancel_button.clicked.connect(self.reject)
        self.remove_button.clicked.connect(self.accept)

    def load_maintenance(self, license_plate):
        conn = sqlite3.connect("car_management.db")
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM cars WHERE license_plate = ?", (license_plate,))
        car_id = cursor.fetchone()[0]

        cursor.execute("SELECT maintenance_type FROM maintenance WHERE car_id = ?", (car_id,))
        maintenance_records = cursor.fetchall()

        self.maintenance_listwidget.clear()
        for record in maintenance_records:
            maintenance_item = QtWidgets.QListWidgetItem(record[0])
            self.maintenance_listwidget.addItem(maintenance_item)

        conn.close()

    def selected_maintenance(self):
        selected_item = self.maintenance_listwidget.currentItem()
        if selected_item:
            return selected_item.text()
        return None


class AddIncidentDialog(QtWidgets.QDialog):
    def __init__(self, license_plate):
        super().__init__()

        self.setWindowTitle("Add Incident")

        self.description_input = QtWidgets.QLineEdit()

        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.add_button = QtWidgets.QPushButton("Add")

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.add_button)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(QtWidgets.QLabel(f"License Plate: {license_plate}"))
        main_layout.addWidget(QtWidgets.QLabel("Description:"))
        main_layout.addWidget(self.description_input)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        self.cancel_button.clicked.connect(self.reject)
        self.add_button.clicked.connect(self.accept)


class IncidentDialog(QtWidgets.QDialog):
    def __init__(self, license_plate):
        super().__init__()

        self.setWindowTitle("Remove Incident")

        self.incident_listwidget = QtWidgets.QListWidget()

        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.remove_button = QtWidgets.QPushButton("Remove")

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.remove_button)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addWidget(QtWidgets.QLabel(f"License Plate: {license_plate}"))
        main_layout.addWidget(QtWidgets.QLabel("Select Incident to Remove:"))
        main_layout.addWidget(self.incident_listwidget)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        self.load_incidents(license_plate)

        self.cancel_button.clicked.connect(self.reject)
        self.remove_button.clicked.connect(self.accept)

    def load_incidents(self, license_plate):
        conn = sqlite3.connect("car_management.db")
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM cars WHERE license_plate = ?", (license_plate,))
        car_id = cursor.fetchone()[0]

        cursor.execute("SELECT description FROM incidents WHERE car_id = ?", (car_id,))
        incident_records = cursor.fetchall()

        self.incident_listwidget.clear()
        for record in incident_records:
            incident_item = QtWidgets.QListWidgetItem(record[0])
            self.incident_listwidget.addItem(incident_item)

        conn.close()

    def selected_incident(self):
        selected_item = self.incident_listwidget.currentItem()
        if selected_item:
            return selected_item.text()
        return None


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    conn = sqlite3.connect("car_management.db")
    cursor = conn.cursor()

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS cars (id INTEGER PRIMARY KEY AUTOINCREMENT, make TEXT, model TEXT, year TEXT, color TEXT, license_plate TEXT)"
    )
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS maintenance (id INTEGER PRIMARY KEY AUTOINCREMENT, car_id INTEGER, maintenance_type TEXT)"
    )
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS incidents (id INTEGER PRIMARY KEY AUTOINCREMENT, car_id INTEGER, description TEXT)"
    )

    conn.commit()
    conn.close()

    car_management_system = CarManagementSystem()
    car_management_system.show()

    sys.exit(app.exec_())
