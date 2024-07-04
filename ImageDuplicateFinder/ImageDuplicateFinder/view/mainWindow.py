import matplotlib.pyplot as plt
from PyQt6.QtWidgets import (
    QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QWidget,
    QTextEdit, QScrollArea, QGroupBox, QRadioButton, QSlider, QLabel, QFileDialog,
    QSpinBox
)
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PIL import Image as PILImage
from ImageDuplicateFinder.model.imageLoader import ImageLoader
from ImageDuplicateFinder.model.duplicateFinder import DuplicateFinder
from ImageDuplicateFinder.model.duplicateFinderCNN import find_duplicates_cnn
import matplotlib
matplotlib.use('QtAgg')


class DuplicateImageFinderGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Duplicate Image Finder')
        self.setGeometry(100, 100, 1200, 800)  # Set window size for better visualization

        # Main layout
        main_layout = QVBoxLayout()

        # Folder selection layout
        folder_selection_layout = QHBoxLayout()

        self.btn_select_folder1 = QPushButton('Select Folder 1')
        self.btn_select_folder1.clicked.connect(self.select_folder1)
        folder_selection_layout.addWidget(self.btn_select_folder1)

        self.btn_select_folder2 = QPushButton('Select Folder 2')
        self.btn_select_folder2.clicked.connect(self.select_folder2)
        folder_selection_layout.addWidget(self.btn_select_folder2)

        main_layout.addLayout(folder_selection_layout)

        # Duplicate search buttons layout
        search_buttons_layout = QHBoxLayout()

        self.btn_find_duplicates_folder1 = QPushButton('Find Duplicates in Folder 1')
        self.btn_find_duplicates_folder1.clicked.connect(self.find_duplicates_folder1)
        search_buttons_layout.addWidget(self.btn_find_duplicates_folder1)

        self.btn_compare_folders = QPushButton('Compare Folder 1 and Folder 2')
        self.btn_compare_folders.clicked.connect(self.compare_folders)
        search_buttons_layout.addWidget(self.btn_compare_folders)

        main_layout.addLayout(search_buttons_layout)

        # TextEdit for results
        self.results_text_edit = QTextEdit()
        main_layout.addWidget(self.results_text_edit)

        # Clear results button
        self.btn_clear_results = QPushButton('Clear Results')
        self.btn_clear_results.clicked.connect(self.clear_results)
        main_layout.addWidget(self.btn_clear_results)

        # ScrollArea for image visualization
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_area.setWidget(self.scroll_content)
        main_layout.addWidget(self.scroll_area)

        # Method selection layout
        method_group_box = QGroupBox('Method Selection')
        method_layout = QVBoxLayout()

        self.radio_hash = QRadioButton('Hash')
        self.radio_hash.setChecked(True)
        method_layout.addWidget(self.radio_hash)

        self.radio_cnn = QRadioButton('CNN')
        method_layout.addWidget(self.radio_cnn)

        method_group_box.setLayout(method_layout)
        main_layout.addWidget(method_group_box)

        # CNN parameters layout
        cnn_params_group_box = QGroupBox('CNN Parameters')
        cnn_params_layout = QVBoxLayout()

        self.label_batch_size = QLabel('Batch Size:')
        cnn_params_layout.addWidget(self.label_batch_size)
        self.spin_batch_size = QSpinBox()
        self.spin_batch_size.setRange(1, 32)
        cnn_params_layout.addWidget(self.spin_batch_size)

        self.label_threshold = QLabel('Threshold:')
        cnn_params_layout.addWidget(self.label_threshold)
        self.slider_threshold = QSlider(Qt.Orientation.Horizontal)
        self.slider_threshold.setRange(0, 100)
        self.slider_threshold.setValue(90)
        cnn_params_layout.addWidget(self.slider_threshold)

        self.label_threshold_value = QLabel('0.90')
        cnn_params_layout.addWidget(self.label_threshold_value)

        self.slider_threshold.valueChanged.connect(self.update_threshold_label)

        cnn_params_group_box.setLayout(cnn_params_layout)
        main_layout.addWidget(cnn_params_group_box)

        # Main container
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Folder paths
        self.folder_path1 = ''
        self.folder_path2 = ''

    def select_folder1(self):
        self.folder_path1 = QFileDialog.getExistingDirectory(self, 'Select Folder 1')
        if self.folder_path1:
            self.results_text_edit.append(f'Folder 1 selected: {self.folder_path1}')

    def select_folder2(self):
        self.folder_path2 = QFileDialog.getExistingDirectory(self, 'Select Folder 2')
        if self.folder_path2:
            self.results_text_edit.append(f'Folder 2 selected: {self.folder_path2}')

    def find_duplicates_folder1(self):
        if not self.folder_path1:
            self.results_text_edit.append('Please select Folder 1 first.')
            return

        self.results_text_edit.append('Finding duplicates in Folder 1...')
        folder1 = ImageLoader.load_folder(self.folder_path1)

        if self.radio_hash.isChecked():
            duplicates = DuplicateFinder.find_duplicates(folder1)
        elif self.radio_cnn.isChecked():
            duplicates = find_duplicates_cnn(
                self.folder_path1,
                batch_size=self.spin_batch_size.value(),
                threshold=self.slider_threshold.value() / 100
            )
        self.display_results(duplicates)

    def compare_folders(self):
        if not self.folder_path1 or not self.folder_path2:
            self.results_text_edit.append('Please select both folders first.')
            return

        self.results_text_edit.append('Comparing Folder 1 and Folder 2...')
        folder1 = ImageLoader.load_folder(self.folder_path1)
        folder2 = ImageLoader.load_folder(self.folder_path2)

        if self.radio_hash.isChecked():
            duplicates = DuplicateFinder.compare_folders(folder1, folder2)
            self.display_results(duplicates)
        elif self.radio_cnn.isChecked():
            self.results_text_edit.append('This method has no implementation of '
                                          'finding duplicates between two folders.')

    def display_results(self, duplicates):
        self.results_text_edit.append(f'Found {len(duplicates)} duplicates.')
        if self.radio_hash.isChecked():
            for img1, img2 in duplicates:
                self.results_text_edit.append(f'Duplicate: {img1.path} and {img2.path}')
        elif self.radio_cnn.isChecked():
            for img1, img2 in duplicates:
                self.results_text_edit.append(f'Duplicate: {img1} and {img2}')
        self.visualize_duplicates(duplicates)

    def visualize_duplicates(self, duplicates):
        rows = min(len(duplicates), 100)
        cols = 2

        fig, axes = plt.subplots(rows, cols, figsize=(10, 5 * rows))

        if rows == 1:
            axes = [axes]
        if self.radio_hash.isChecked():
            for i, (img1, img2) in enumerate(duplicates[:100]):
                file1_name = img1.path.split('\\')[-1]
                file2_name = img2.path.split('\\')[-1]
                path1 = img1.path
                path2 = img2.path

                axes[i][0].imshow(PILImage.open(img1.path))
                axes[i][0].axis('off')
                axes[i][0].set_title(f"File: {file1_name}\nPath: {path1}", fontsize=8, pad=20)

                axes[i][1].imshow(PILImage.open(img2.path))
                axes[i][1].axis('off')
                axes[i][1].set_title(f"File: {file2_name}\nPath: {path2}", fontsize=8, pad=20)

            plt.tight_layout()
            canvas = FigureCanvas(fig)
            canvas.setMinimumHeight(5 * rows * 100)
            self.scroll_area.setWidget(canvas)
            plt.close()
        elif self.radio_cnn.isChecked():
            for i, (img1, img2) in enumerate(duplicates[:100]):
                file1_name = img1.split('\\')[-1]
                file2_name = img2.split('\\')[-1]
                path1 = img1
                path2 = img2

                axes[i][0].imshow(PILImage.open(img1))
                axes[i][0].axis('off')
                axes[i][0].set_title(f"File: {file1_name}\nPath: {path1}", fontsize=8, pad=20)

                axes[i][1].imshow(PILImage.open(img2))
                axes[i][1].axis('off')
                axes[i][1].set_title(f"File: {file2_name}\nPath: {path2}", fontsize=8, pad=20)

            plt.tight_layout()
            canvas = FigureCanvas(fig)
            canvas.setMinimumHeight(5 * rows * 100)
            self.scroll_area.setWidget(canvas)
            plt.close()

    def update_threshold_label(self):
        threshold = self.slider_threshold.value() / 100
        self.label_threshold_value.setText(f'{threshold:.2f}')

    def clear_results(self):
        self.results_text_edit.clear()
