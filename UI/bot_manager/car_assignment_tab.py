# from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QHBoxLayout
# from PyQt5.QtGui import QPixmap
# from PyQt5.QtCore import Qt
#
# class CarAssignmentTab(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.initUI()
#
#     def initUI(self):
#         main_layout = QVBoxLayout()
#
#         # Event Image Selection
#         self.event_image_layout = QHBoxLayout()
#         self.event_images = []
#         self.event_labels = []
#
#         events = self.get_events_from_db()
#
#         for event in events:
#             event_label = QLabel(self)
#             event_pixmap = QPixmap(event['img_path'])
#             event_label.setPixmap(event_pixmap.scaled(100, 100, Qt.KeepAspectRatio))
#             event_label.mousePressEvent = lambda _, e=event: self.select_event(e['name'])
#             self.event_image_layout.addWidget(event_label)
#             self.event_images.append(event_pixmap)
#             self.event_labels.append(event_label)
#
#         main_layout.addLayout(self.event_image_layout)
#
#         # Series Selection (hidden initially)
#         self.series_label = QLabel('Select Series:', self)
#         self.series_dropdown = QComboBox(self)
#         main_layout.addWidget(self.series_label)
#         main_layout.addWidget(self.series_dropdown)
#         self.series_label.hide()
#         self.series_dropdown.hide()
#
#         # Car Assignment Dropdowns (hidden initially)
#         self.car_dropdowns = []
#         self.car_labels = []
#         for i in range(5):  # Assuming 5 races per series
#             race_label = QLabel(f'Race {i + 1}:', self)
#             car_dropdown = QComboBox(self)
#             main_layout.addWidget(race_label)
#             main_layout.addWidget(car_dropdown)
#             self.car_labels.append(race_label)
#             self.car_dropdowns.append(car_dropdown)
#             race_label.hide()
#             car_dropdown.hide()
#
#         # Submit Button (hidden initially)
#         self.submit_button = QPushButton('Submit Car Assignments', self)
#         main_layout.addWidget(self.submit_button)
#         self.submit_button.hide()
#
#         self.setLayout(main_layout)
#
#         # Signal-slot connections
#         self.series_dropdown.currentIndexChanged.connect(self.update_car_dropdowns)
#         self.submit_button.clicked.connect(self.submit_car_assignments)
#
#     def get_events_from_db(self):
#         # Placeholder: Fetch event names and image paths from the database
#         return [
#             {"name": "Event 1", "img_path": "C:/Users/joren/PycharmProjects/Top_drives_bot/image_reader/event/test.png"},
#             {"name": "Event 2", "img_path": "C:/Users/joren/PycharmProjects/Top_drives_bot/image_reader/event/test.png"},
#             {"name": "Event 3", "img_path": "C:/Users/joren/PycharmProjects/Top_drives_bot/image_reader/event/test.png"},
#         ]
#
#     def get_series_from_db(self, event_name):
#         # Placeholder: Fetch series names based on the selected event from the database
#         return ["Series 1", "Series 2", "Series 3"]
#
#     def get_cars_from_db(self, series_name):
#         # Placeholder: Fetch car numbers based on the selected series from the database
#         return [str(i) for i in range(1, 6)]  # Assuming car numbers 1-5
#
#     def select_event(self, event_name):
#         print(f"Selected event: {event_name}")
#         series_list = self.get_series_from_db(event_name)
#         self.series_dropdown.clear()
#         self.series_dropdown.addItems(series_list)
#
#         # Show series label and dropdown
#         self.series_label.show()
#         self.series_dropdown.show()
#
#         # Clear and hide the car dropdowns initially
#         for race_label, car_dropdown in zip(self.car_labels, self.car_dropdowns):
#             race_label.hide()
#             car_dropdown.hide()
#
#         # Hide submit button initially
#         self.submit_button.hide()
#
#     def update_car_dropdowns(self):
#         selected_series = self.series_dropdown.currentText()
#
#         if selected_series:
#             car_list = self.get_cars_from_db(selected_series)
#             for race_label, dropdown in zip(self.car_labels, self.car_dropdowns):
#                 dropdown.clear()
#                 dropdown.addItems(car_list)
#
#                 # Show race labels and car dropdowns after series is selected
#                 race_label.show()
#                 dropdown.show()
#
#             # Show the submit button
#             self.submit_button.show()
#
#     def submit_car_assignments(self):
#         # Collect selected car numbers for each race
#         car_assignments = []
#         for i, dropdown in enumerate(self.car_dropdowns):
#             selected_car = dropdown.currentText()
#             car_assignments.append((i + 1, selected_car))  # Race number, car number
#
#         # Log the assignments
#         print(f'Car assignments: {car_assignments}')
#         print("Car assignments submitted.")
#
#         # Save these assignments to the database using a function
#         self.save_car_assignments_to_db(car_assignments)
#
#     def save_car_assignments_to_db(self, car_assignments):
#         # Example function to save assignments to the database
#         for race_number, car_number in car_assignments:
#             # Replace this with actual database insertion logic
#             print(f'Saving Car {car_number} assignment for Race {race_number} to DB')
#             # Call your existing database function here
#

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QHBoxLayout, QSizePolicy
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class CarAssignmentTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()

        # Event Image Selection
        self.event_image_layout = QHBoxLayout()
        self.event_images = []
        self.event_labels = []

        events = self.get_events_from_db()

        for event in events:
            event_label = QLabel(self)
            event_pixmap = QPixmap(event['img_path'])

            # Adjust the image to fit the tab, while maintaining aspect ratio
            event_pixmap = event_pixmap.scaledToHeight(150, Qt.SmoothTransformation)
            event_label.setPixmap(event_pixmap)
            event_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            event_label.setAlignment(Qt.AlignCenter)
            event_label.mousePressEvent = lambda _, e=event: self.select_event(e['name'])

            self.event_image_layout.addWidget(event_label)
            self.event_images.append(event_pixmap)
            self.event_labels.append(event_label)

        main_layout.addLayout(self.event_image_layout)

        # Series Selection (hidden initially)
        self.series_label = QLabel('Select Series:', self)
        self.series_dropdown = QComboBox(self)
        main_layout.addWidget(self.series_label)
        main_layout.addWidget(self.series_dropdown)
        self.series_label.hide()
        self.series_dropdown.hide()

        # Car Assignment Dropdowns (hidden initially)
        self.car_dropdowns = []
        self.car_labels = []
        for i in range(5):  # Assuming 5 races per series
            race_label = QLabel(f'Race {i + 1}:', self)
            car_dropdown = QComboBox(self)
            main_layout.addWidget(race_label)
            main_layout.addWidget(car_dropdown)
            self.car_labels.append(race_label)
            self.car_dropdowns.append(car_dropdown)
            race_label.hide()
            car_dropdown.hide()

        # Submit Button (hidden initially)
        self.submit_button = QPushButton('Submit Car Assignments', self)
        main_layout.addWidget(self.submit_button)
        self.submit_button.hide()

        self.setLayout(main_layout)

        # Signal-slot connections
        self.series_dropdown.currentIndexChanged.connect(self.update_car_dropdowns)
        self.submit_button.clicked.connect(self.submit_car_assignments)

    def get_events_from_db(self):
        # Placeholder: Fetch event names and image paths from the database
        return [
            {"name": "Event 1", "img_path": "C:/Users/joren/PycharmProjects/Top_drives_bot/image_reader/tests/test.png"},
            {"name": "Event 2", "img_path": "C:/Users/joren/PycharmProjects/Top_drives_bot/image_reader/tests/test.png"},
            {"name": "Event 3", "img_path": "C:/Users/joren/PycharmProjects/Top_drives_bot/image_reader/tests/test.png"},
        ]

    def get_series_from_db(self, event_name):
        # Placeholder: Fetch series names based on the selected event from the database
        return ["Series 1", "Series 2", "Series 3"]

    def get_cars_from_db(self, series_name):
        # Placeholder: Fetch car numbers based on the selected series from the database
        return [str(i) for i in range(1, 6)]  # Assuming car numbers 1-5

    def select_event(self, event_name):
        print(f"Selected event: {event_name}")
        series_list = self.get_series_from_db(event_name)
        self.series_dropdown.clear()
        self.series_dropdown.addItems(series_list)

        # Show series label and dropdown
        self.series_label.show()
        self.series_dropdown.show()

        # Clear and hide the car dropdowns initially
        for race_label, car_dropdown in zip(self.car_labels, self.car_dropdowns):
            race_label.hide()
            car_dropdown.hide()

        # Hide submit button initially
        self.submit_button.hide()

    def update_car_dropdowns(self):
        selected_series = self.series_dropdown.currentText()

        if selected_series:
            car_list = self.get_cars_from_db(selected_series)
            for race_label, dropdown in zip(self.car_labels, self.car_dropdowns):
                dropdown.clear()
                dropdown.addItems(car_list)

                # Show race labels and car dropdowns after series is selected
                race_label.show()
                dropdown.show()

            # Show the submit button
            self.submit_button.show()

    def submit_car_assignments(self):
        # Collect selected car numbers for each race
        car_assignments = []
        for i, dropdown in enumerate(self.car_dropdowns):
            selected_car = dropdown.currentText()
            car_assignments.append((i + 1, selected_car))  # Race number, car number

        # Log the assignments
        print(f'Car assignments: {car_assignments}')
        print("Car assignments submitted.")

        # Save these assignments to the database using a function
        self.save_car_assignments_to_db(car_assignments)

    def save_car_assignments_to_db(self, car_assignments):
        # Example function to save assignments to the database
        for race_number, car_number in car_assignments:
            # Replace this with actual database insertion logic
            print(f'Saving Car {car_number} assignment for Race {race_number} to DB')
            # Call your existing database function here
