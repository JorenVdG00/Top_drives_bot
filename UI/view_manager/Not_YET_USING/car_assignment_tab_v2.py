# from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton, QHBoxLayout, QSizePolicy, QDialog, \
#     QApplication, QGridLayout
# from PyQt5.QtGui import QPixmap, QDrag
# from PyQt5.QtCore import Qt, QMimeData, pyqtSignal
# import sys
# from database.methods.db_events import get_all_active_events, get_active_event, get_series, get_event_from_serie_id, \
#     get_serie_number, get_races, get_track_set_from_serie
# from database.db_car_assign import assign_car_to_race
# from config import BASE_DIR


# class DraggableLabel(QLabel):
#     def __init__(self, img_path, parent=None):
#         super().__init__(parent)
#         self.img_path = img_path
#         self.setPixmap(QPixmap(img_path))
#         self.setScaledContents(True)
#         self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
#         self.adjustSize()

#     def mousePressEvent(self, event):
#         if event.button() == Qt.LeftButton:
#             drag = QDrag(self)
#             mime_data = QMimeData()
#             mime_data.setText(self.img_path)
#             drag.setMimeData(mime_data)
#             drag.exec_(Qt.MoveAction)
#         super().mousePressEvent(event)

#     # def dragEnterEvent(self, event):
#     #     if event.mimeData().hasText():
#     #         event.accept()
#     #     else:
#     #         event.ignore()
#     #
#     # def dropEvent(self, event):
#     #     if event.mimeData().hasText():
#     #         car_image_path = event.mimeData().text()
#     #         self.setPixmap(QPixmap(car_image_path).scaledToHeight(100, Qt.SmoothTransformation))
#     #         event.accept()
#     #     else:
#     #         event.ignore()


# class DropTarget(QLabel):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setAlignment(Qt.AlignCenter)
#         self.setStyleSheet("background-color: lightgrey; border: 1px solid black;")
#         self.setFixedSize(120, 80)
#         self.setAcceptDrops(True)
#         self.setObjectName("empty")
#         self.setProperty("car_image_path", None)

#     def dragEnterEvent(self, event):
#         if event.mimeData().hasText():
#             event.accept()
#         else:
#             event.ignore()

#     def dropEvent(self, event):
#         if event.mimeData().hasText():
#             car_image_path = event.mimeData().text()
#             self.setPixmap(QPixmap(car_image_path).scaled(self.width(), self.height(), Qt.KeepAspectRatio,
#                                                           Qt.SmoothTransformation))
#             self.setProperty("car_image_path", car_image_path)  # Store the image path in the property
#             event.accept()
#         else:
#             event.ignore()


# class CarAssignmentTab(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.initUI()

#     def initUI(self):
#         main_layout = QVBoxLayout()

#         # Event Image Selection
#         self.event_image_layout = QHBoxLayout()
#         self.event_images = []
#         self.event_labels = []

#         events = self.get_events_from_db()

#         for event in events:
#             event_label = QLabel(self)
#             event_pixmap = QPixmap(event['img_path'])

#             # Adjust the image to fit the tab, while maintaining aspect ratio
#             event_pixmap = event_pixmap.scaledToHeight(150, Qt.SmoothTransformation)
#             event_label.setPixmap(event_pixmap)
#             event_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
#             event_label.setAlignment(Qt.AlignCenter)
#             # event_label.mousePressEvent = lambda _, e=event: self.select_event(e['event_id'])
#             event_label.mousePressEvent = lambda _, e=event: self.open_car_assignment_dialog(e['event_id'])

#             self.event_image_layout.addWidget(event_label)
#             self.event_images.append(event_pixmap)
#             self.event_labels.append(event_label)

#         main_layout.addLayout(self.event_image_layout)

#         # Series Selection (hidden initially)
#         # self.series_label = QLabel('Select Series:', self)
#         # self.series_dropdown = QComboBox(self)
#         # main_layout.addWidget(self.series_label)
#         # main_layout.addWidget(self.series_dropdown)
#         # self.series_label.hide()
#         # self.series_dropdown.hide()

#         # Set layout for the widget
#         self.setLayout(main_layout)

#         # Signal-slot connections
#         # self.series_dropdown.currentIndexChanged.connect(self.open_car_assignment_dialog)

#     def get_events_from_db(self):
#         events = []
#         event_ids = get_all_active_events()
#         if event_ids:
#             for event_id in event_ids:
#                 event = get_active_event(event_id)
#                 if event:
#                     event_dict = {'event_id': event_id, 'name': event[0], 'img_path': f'{event[1]}/display/display.png'}
#                     events.append(event_dict)
#             print(events)
#         # Placeholder: Fetch event names and image paths from the database
#         return events

#     def get_series_from_db(self, event_id):
#         print("event_id2", event_id)
#         serie_ids = get_series(event_id)
#         series = []
#         for serie_id in serie_ids:
#             series.append((serie_id))
#         # Placeholder: Fetch series names based on the selected event from the database
#         return series

#     # def select_event(self, event_id):
#     #     print(f"Selected event: {event_id}")
#     #     self.open_car_assignment_dialog(event_id)

#     def open_car_assignment_dialog(self, event_id):
#         selected_series = self.get_series_from_db(event_id)
#         assignments = {}
#         if selected_series:
#             dialog = CarAssignmentDialog(selected_series[0], 0, selected_series, assignments)
#             dialog.exec_()


# class CarAssignmentDialog(QDialog):
#     def __init__(self, serie_id, series_index, series_list, assignments, parent=None):
#         super().__init__(parent)
#         self.serie_id = serie_id
#         self.series_index = series_index
#         self.series_list = series_list
#         self.assignments = assignments
#         self.initUI()

#     def initUI(self):
#         self.event_id, self.event_dir, self.serie_number = self.get_event_info_from_serie_id()

#         print("serie_id", self.serie_id)
#         print("serie_number: ", self.serie_number)

#         self.setWindowTitle(f"Car Assignment for {self.serie_id}")
#         main_layout = QVBoxLayout()

#         grid_layout = QGridLayout()
#         # Race Images
#         self.car_labels = []
#         self.drop_targets = []

#         for i in range(5):
#             race_label = QLabel(self)
#             race_pixmap = QPixmap(f'{self.event_dir}/cropped_img/{self.serie_number}-{i + 1}/full_race.png')
#             race_pixmap = race_pixmap.scaledToHeight(150, Qt.SmoothTransformation)
#             race_label.setPixmap(race_pixmap)
#             race_label.setAlignment(Qt.AlignCenter)
#             grid_layout.addWidget(race_label, 0, i)

#             # Create drop targets below each race image
#             drop_target = DropTarget(self)
#             drop_target.setObjectName(f'{i + 1}')
#             grid_layout.addWidget(drop_target, 1, i)
#             self.drop_targets.append(drop_target)

#         main_layout.addLayout(grid_layout)

#         if self.serie_id in self.assignments:
#             self.load_previous_assignments()

#         # Car Images at the bottom (Draggable)
#         self.car_images_layout = QHBoxLayout()
#         self.car_image_paths = self.load_car_images()

#         for img_path in self.car_image_paths:
#             car_label = DraggableLabel(img_path, self)
#             self.car_images_layout.addWidget(car_label)
#             self.car_labels.append(car_label)

#         main_layout.addLayout(self.car_images_layout)

#         # Refresh Button
#         self.refresh_button = QPushButton('Refresh', self)
#         self.refresh_button.clicked.connect(self.refresh)
#         main_layout.addWidget(self.refresh_button)

#         # Submit Button
#         self.submit_button = QPushButton('Submit Car Assignments', self)
#         self.submit_button.clicked.connect(self.submit_car_assignments)
#         main_layout.addWidget(self.submit_button)

#         self.setLayout(main_layout)

#     def load_car_images(self):
#         car_image_paths = []
#         for i in range(1, 6):
#             car_image_path = f'{self.event_dir}/cars/car{i}.png'
#             car_image_paths.append(car_image_path)
#         return car_image_paths

#     def load_previous_assignments(self):
#         for race_number, car_number in self.assignments[self.serie_id].items():
#             drop_target = self.drop_targets[race_number - 1]
#             car_image_path = self.car_image_paths[car_number - 1]
#             car_pixmap = QPixmap(car_image_path)
#             drop_target.setPixmap(car_pixmap)
#             drop_target.setProperty('car_image_path', car_image_path)

#     def get_event_info_from_serie_id(self):
#         event_id = get_event_from_serie_id(self.serie_id)
#         event = get_active_event(event_id)
#         event_dir = event[1]
#         serie_number = get_serie_number(self.serie_id)
#         return event_id, event_dir, serie_number

#     def refresh(self):
#         for target in self.drop_targets:
#             target.clear()

#         for car_label in self.car_labels:
#             car_label.setPixmap(QPixmap(car_label.img_path))
#             car_label.adjustSize()

#     def submit_car_assignments(self):
#         assignments = {}
#         for target in self.drop_targets:
#             car_image_path = target.property("car_image_path")
#             if car_image_path:
#                 car_img_path = car_image_path.split('.')[-2]
#                 car_number = car_img_path[-1]
#                 race_number = int(target.objectName())
#                 assignments[race_number] = car_number  # Storing race number and car number

#         print(f'Car assignments for {self.serie_id}: {assignments}')
#         print("Car assignments submitted.")

#         self.assignments[self.serie_id] = assignments

#         self.save_car_assignments_to_db(assignments)
#         self.load_next_series()

#     # def save_car_assignments_to_db(self, car_assignments):
#     #     races = get_races(self.serie_id)
#     #     race_dict = {}
#     #     print(races)
#     #     for race_id, race in races.items():
#     #         race_number = race['number']
#     #         print(race_number)
#     #         race_dict[race_number] = race_id
#     #     # Example function to save assignments to the database
#     #     for race_number, car_number in car_assignments:
#     #         print('Car Number: ', car_number)
#     #         race_id = race_dict[race_number]
#     #         assign_car_to_race(race_id, car_number)
#     #         # Replace this with actual database insertion logic
#     #         print(f'Saving Car {car_number} assignment for Race {race_number} in Series {self.serie_id} to DB')
#     #         # Call your existing database function here
#     #     self.accept()  # Close the dialog after saving

#     def save_car_assignments_to_db(self, car_assignments):
#         races = get_races(self.serie_id)
#         race_dict = {race['number']: race_id for race_id, race in races.items()}
#         for race_number, car_number in car_assignments.items():
#             race_id = race_dict[race_number]
#             assign_car_to_race(race_id, car_number)
#             print(f'Saving Car {car_number} assignment for Race {race_number} in Series {self.serie_id} to DB')

#         self.accept()  #

#     def load_next_series(self):
#         self.series_index += 1
#         if self.series_index < len(self.series_list):
#             next_serie_id = self.series_list[self.series_index]
#             next_dialog = CarAssignmentDialog(next_serie_id, self.series_index, self.series_list, self.assignments)
#             self.accept()
#             next_dialog.exec_()
#         else:
#             self.accept()  # Close dialog when all series are assigned


# # Application Execution
# # if __name__ == '__main__':
# #     app = QApplication(sys.argv)
# #     window = CarAssignmentTab()
# #     window.show()
# #     sys.exit(app.exec_())
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     dialog = CarAssignmentDialog(1)
#     dialog.exec_()
#     sys.exit(app.exec_())
