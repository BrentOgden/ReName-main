import sys
import shutil
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QProgressBar, QSplashScreen, QHBoxLayout, QDialog, QTextEdit, QStyle, QFileDialog, QTextBrowser
from PyQt6.QtCore import Qt, QTimer, QCoreApplication, QPropertyAnimation, QPoint, QEasingCurve, QSize
from PyQt6.QtGui import QLinearGradient, QColor, QPalette, QPixmap, QPainter, QPainterPath, QBrush
from scriptThread import ScriptThread
from pathlib import Path
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# Define the SplashScreen class
class SplashScreen(QSplashScreen):
    def __init__(self, pixmap):
        super().__init__(pixmap, Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.FramelessWindowHint)
        self.showMessage("Loading...", Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter, Qt.GlobalColor.white)

        # Set the size of the splash screen to match the size of the main window
        main_window = QApplication.activeWindow()
        if main_window:
            self.resize(main_window.size())

class CustomProgressBar(QProgressBar):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QProgressBar {
                border: 1px solid grey;
                text-align: center;
                border-radius: 5px;
                background-color: #ffffff;
                margin-top: 20px;
                margin-bottom: 10px;
            }
            QProgressBar::chunk {
                background-color: #1D1B7D;
                width: 10px;
                margin: .5px;
            }
            QProgressBar::text {
                color: #FF0000 !important;  /* Red color for text */
                padding-top: 5px;
                font-size: 20px;  /* Increased font size */
                font-weight: bold; 
            }
        """)
         # Set the text color using QPalette
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Text, QColor("#ffffff"))
        self.setPalette(palette)
        
        # Add these lines to set the font size
        font = self.font()  # get the current font
        font.setPointSize(16)  # set the font size
        self.setFont(font)  # set the font back
        
        # Vertically and Horizontally center the text
        self.setTextVisible(True)  # Show the percentage text
        self.setAlignment(Qt.AlignmentFlag.AlignRight)
        
    def text(self):
        default_text = super().text()
        return "\n\n" + default_text  # Add a newline to the beginning
    
class ResizableLabel(QWidget):
    def __init__(self, pixmap, parent=None):
        super().__init__(parent)
        self._pixmap = pixmap
        self._scale_factor = 1.0
        self.setFixedSize(pixmap.width(), pixmap.height())  # This sets the initial fixed size of the widget

    def paintEvent(self, event):
        painter = QPainter(self)
        target_width = self._pixmap.width() * self._scale_factor
        target_height = self._pixmap.height() * self._scale_factor
        scaled_pixmap = self._pixmap.scaled(target_width, target_height, Qt.AspectRatioMode.KeepAspectRatio)
        painter.drawPixmap(0, 0, scaled_pixmap)

class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Setting the dialog to be modal
        self.setModal(True)
        
        # Creating a QTextEdit to show the help information
        text_browser = QTextBrowser(self)
        text_browser.setOpenExternalLinks(True)  # This will allow the hyperlinks to be opened by external applications (like email clients)

        # Determine the paths for the images
        logo_path = resource_path('logo.png')
        screenshot_drag_path = resource_path('screenshot_drag.png')
        screenshot_export_path = resource_path('screenshot_export.png')
        # Sample HTML content with styled text and an image
        html_content = f"""
        <div align='center' margin-bottom='10px' margin-top='10px'>
        <h2>ReNAME:</h2>
        <h4>PDF/DOCX File Renamer</h4>
        </div>
        <div align='center' margin-bottom='10px' margin-top='10px'>
        <img src='{logo_path}' width='100' align='center' margin-left='auto' margin-right='auto' padding='10px'>
        </div>
        <h3>Introduction</h3>
        <p>This application allows the user to group batches of PDF and DOCX files by status and quickly rename them according to the following naming convention:</p>
        <p align='center'><strong><i>VendorName_AgreementType_STATUS_Date.pdf</i></strong></p>
        <h3>How it Works</h3>
        <ol>
        <li>Drag the desired files for each status type from their location on your machine into the appropriate boxes. You will see the box will highlight and their will be a badge at the top left with the total number of files dropped in each section.</li>
        <div align='center' margin-bottom='10px' margin-top='10px'>
        <img src='{screenshot_drag_path}' width='250'>
        </div>
        <li>Once you have selected the desired number of files for each status, click "Rename Files" to proceed with renaming the files. You will see a progress bar and messaging that will update as the ReNAME is being performed.  </li>
        <li>When the process has completed, you will see the progress bar at 100% and the application will say that the files have been renamed. These renamed files can be found in the location that you selected, grouped by their status. Any files that were missing an attribute, such as Agreement Type, will be sent to the "Incomplete" folder with "UnknownType" in the filename. The missing type can then be added manually.  </li>
        </ol>
        <div align='center' margin-bottom='10px' margin-top='10px'>
        <img src='{screenshot_export_path}' width='250'>
        </div>
        <h3>Things to Know</h3>
        <ul>
        <li>Accuracy of the rename <u>may vary</u> depending on the quailty of the document being used. PDFs that are scanned at poor quality are harder to read by the OCR tool and may result in the application being unable to find a given attribute. </li>
        <li>Since the application scans each document and extracts specific attributes, the processing time can vary if there are a significant amount of files processed at once. </li>
        <li>There may be instances where an Agreement Type or Vendor may not match exactly to what is desired. This may happen if there are multiple vendors present in the document and the model is unsure which to use. </li>
        <li>There is a folder to house files for which an attribute was not found. These files will be sent to the "Incomplete" folder so that the missing attribute can be added manually.</li>
         <li>Encrypted files are unable to be scanned and will be sent to the "Incomplete" folder. They can then be named manually. </li>
         <li>Only English files can be processed</li>
         <li>For Support: <a href="mailto:clm-support@dish.com" target="_blank">clm-support@dish.com</a> | <a href="mailto:clm-admin@dish.com" target="_blank">clm-admin@dish.com</a>
        </ul>


        """

        text_browser.setHtml(html_content)
        text_browser.setReadOnly(True)
        
        # Styling the dialog
        self.setStyleSheet("background-color: #3879E7; border: 2px solid #555; border-radius: 5px; font: 16px 'Arial';")
        text_browser.setStyleSheet('''
            QTextEdit {
                border: 2px dashed #000000;
                background-color: #ECF0F1;
                border-radius: 3px;
                font-size: 14px;
            }

            /* Styling the vertical scrollbar background */
            QTextEdit QScrollBar:vertical {
                border: 2px solid #999999;
                background: white;
                width: 15px;
                margin: 15px 0 15px 0;
            }
            
            /* Styling the handle */
            QTextEdit QScrollBar::handle:vertical {
                background: #30A9DE;
                min-height: 20px;
            }
            
            /* Styling the groove */
            QTextEdit QScrollBar::groove:vertical {
                border: 1px solid #999999;
                background: #F1F1F1;
            }
        ''')


        text_browser.setStyleSheet('''
            border: 2px dashed #000000;
            background-color: #ECF0F1;
            border-radius: 3px;
            padding: 10px;
            color: #000000;
            font-size: 14px;
        ''')
        
        
        # Setting the layout
        layout = QVBoxLayout(self)
        layout.addWidget(text_browser)
        self.setLayout(layout)
        self.setWindowTitle("Help")
        self.resize(420, 700)

    
        


class App(QMainWindow):
    class DropArea(QLabel):
        def __init__(self, folder_path, parent=None):
            super(App.DropArea, self).__init__(parent)
            self.folder_path = folder_path
            self.setAcceptDrops(True)
            self.setAlignment(Qt.AlignmentFlag.AlignCenter)
            
             # Initialize the counter
            self.file_count = 0
            self.files_present = False
            
            # Add a QLabel for the bubble display
            self.bubble_label = QLabel(self)
            self.bubble_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.bubble_label.setStyleSheet("""
                background-color: lightgrey;
                border-radius: 10px;
                color: black; 
                padding: 3px 4px;
                position: absolute;
                right: 5px;
                top: 5px;
            """)
            self.bubble_label.setText("25")
            self.bubble_label.adjustSize()
            self.bubble_label.hide()  # Hide it initially
            
            self.update_display()

            # Store the default style sheet for later use
            self.default_stylesheet = """
                background-color: #ECF0F1;
                border: 2px dashed black;
                padding: 20px;
                color: #000000;
                border-radius: 5px;
                font-weight: bold;
                font-size: 2rem;
            """
            
            # Connect the dragEnterEvent and dragLeaveEvent
            self.setMouseTracking(True)
            self.dragEnterEvent = self.on_drag_enter
            self.dragLeaveEvent = self.on_drag_leave
            
        def reset_style_and_hide_bubble(self):
            self.setStyleSheet(self.default_stylesheet)
            self.bubble_label.hide()
            self.file_count = 0  # Reset the file count
            self.files_present = False  # Reset the files_present flag
            self.update_display()  # Update the label's display


        def update_display(self):
            # Extract the final directory name from the folder_path and set the text
            final_directory_name = self.folder_path.name
            if self.file_count == 0:
                self.setText(f"Drop {final_directory_name} files here")
            else:
                self.setText(f"{final_directory_name} FILES")

            # Update the bubble label size after setting the text
            self.adjust_bubble_size()

            # Update the bubble label visibility based on file count
            if self.file_count > 0:
                self.bubble_label.setText(str(self.file_count))
                self.bubble_label.show()
            else:
                self.bubble_label.hide()

        def lock(self):
            self.setAcceptDrops(False)

        def unlock(self):
            self.setAcceptDrops(True)
    
        def adjust_bubble_size(self):
            # Get the width of the text
            text_width = self.bubble_label.fontMetrics().boundingRect(self.bubble_label.text()).width()

            # Add some padding to the width and set a fixed height
            adjusted_width = max(text_width + 12, 25)  # Ensure a minimum width
            self.bubble_label.setFixedWidth(adjusted_width)
            self.bubble_label.setFixedHeight(25)  # Adjust as needed
            self.bubble_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

 
        def dragMoveEvent(self, event):
            event.acceptProposedAction()

        def on_drag_enter(self, event):
            event.acceptProposedAction()
            # Change the style when files are dragged over the area
            if not self.files_present:  # Only update the style if no files are present
                self.setStyleSheet("""
                    background-color: #3879E7;  /* Change the background color */
                    border: 2px dashed #3a46c9;  /* Change the border color */
                    color: #ffffff;
                    padding: 20px;
                    border-radius: 5px;
                    font-weight: bold;
                    font-size: 2rem;
                """)

        def on_drag_leave(self, event):
            # Restore the default style when files are no longer dragged over the area
            if not self.files_present:
                self.setStyleSheet(self.default_stylesheet)

        def dragEnterEvent(self, event):
            mime_data = event.mimeData()
            if mime_data.hasUrls():
                event.acceptProposedAction()

        def dropEvent(self, event):
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                try:
                    shutil.move(file_path, self.folder_path)
                    self.file_count += 1
                    self.files_present = True
                    self.update_display()
                except Exception as e:
                    pass
                
        def update_file_count(self):
            self.file_count = len(list(self.folder_path.iterdir()))        

        


    def show_help_dialog(self):
        help_dialog = HelpDialog(self)
        help_dialog.exec()

            
    def __init__(self):
        super().__init__()
        # Prompt the user to select a directory when the app starts
        selected_directory = QFileDialog.getExistingDirectory(self, "Select Starting Directory")
        QApplication.instance().aboutToQuit.connect(self.on_app_exit)
        # If the user cancels the directory selection, use the Desktop as the default directory
        self.base_directory = selected_directory if selected_directory else os.path.expanduser('~/Desktop')

        self.path = QPainterPath()
        self.initUI()
        self.script_running = False  # Flag to indicate whether the script is running
        # Within your App class after selecting the directory
        self.thread = ScriptThread(base_directory=self.base_directory)

        # Delay directory creation until after GUI is displayed
        QTimer.singleShot(0, self.lazy_create_directories)

    def lazy_create_directories(self):
        documents_folder = Path(self.base_directory)

   

        # Provided paths
        main_dirs = [
            documents_folder / 'Renamed Files' / 'export' / 'DRAFT',
            documents_folder / 'Renamed Files' / 'export' / 'EXECUTED',
            documents_folder / 'Renamed Files' / 'export' / 'FOR APPROVAL',
            documents_folder / 'Renamed Files' / 'export' / 'PARTIALLY EXECUTED'
        ]

        output_dir = documents_folder / 'Renamed Files' / 'export' / 'output'

        # Create main directories
        for dir_path in main_dirs:
            dir_path.mkdir(parents=True, exist_ok=True)

        # Create corresponding subdirectories in the output directory
        for dir_path in main_dirs:
            sub_output_dir = output_dir / dir_path.name
            sub_output_dir.mkdir(parents=True, exist_ok=True)

    def initUI(self):
        self.setWindowTitle('ReNAME')
        self.setGeometry(100, 100, 400, 600)  # Set the window size and position
        self.setFixedSize(400, 800)
        documents_folder = Path(self.base_directory)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

         
        
        # # Set the background gradient for the central widget
        # self.set_background_gradient(central_widget)
        self.set_background_image(central_widget, resource_path('background2.jpg'))

        layout = QVBoxLayout(central_widget)

        icon = self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarContextHelpButton)
        help_button = QPushButton(self)
        help_button.setIcon(icon)
        help_button.setIconSize(QSize(24, 24))  # Adjust size as needed
        help_button.setFixedSize(30, 30)  # Set fixed size for the button to be a circle

        help_button.setStyleSheet("""
        QPushButton {
            background-color: #ddd;   /* Circle's background color */
            border: 2px solid #aaa;   /* Circle's border color */
            border-radius: 15px;      /* Half of the button's size for a perfect circle */
        }
        QPushButton:hover {
            background-color: #bbb;  /* Change the background color on hover */
        }
    """)
        help_button.clicked.connect(self.show_help_dialog)
        top_layout = QHBoxLayout()
        top_layout.addStretch(1)
        top_layout.addWidget(help_button)
        
        layout.addLayout(top_layout)
        
        progress_widget = QWidget()
        progress_layout = QVBoxLayout(progress_widget)
        layout.addWidget(progress_widget)

        # Add an image above the progress bar
        image_label = QLabel()
        pixmap = QPixmap(resource_path('rename_logo2.png'))

        


        # Resize the image to a specific width and height (e.g., 100x100 pixels)
        desired_width = 210
        desired_height = 210
        pixmap = pixmap.scaled(desired_width, desired_height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

        # Set the alignment to center
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_label.setPixmap(pixmap)
        progress_layout.addWidget(image_label)

        # Create a custom QProgressBar
        self.progress_bar = CustomProgressBar()
        progress_layout.addWidget(self.progress_bar)

        # Check if folder image is loaded
        folder_pixmap = QPixmap("folder.png")

        # Using QLabel to display the folder image directly
        self.folder_label = QLabel()
        self.folder_label.setPixmap(folder_pixmap)
        max_width = int(folder_pixmap.width() * 1.5)
        max_height = int(folder_pixmap.height() * 1.5)
        self.folder_label.setFixedSize(max_width, max_height)

        # Initialize the scaling animation for the folder label
        self.scale_animation = QPropertyAnimation(self.folder_label, b"scale_factor")
        self.scale_animation.setStartValue(1.0)
        self.scale_animation.setKeyValueAt(0.5, 1.5)  # Mid-point expansion
        self.scale_animation.setEndValue(1.0)  # Contract back to original size
        self.scale_animation.setDuration(2500)
        self.scale_animation.setLoopCount(-1)  # Continuous loop
        self.scale_animation.setEasingCurve(QEasingCurve.Type.InOutSine)
        self.scale_animation.valueChanged.connect(self.set_image_scale)

        # Create a QWidget to hold the folder label
        folder_widget = QWidget()
        folder_layout = QVBoxLayout(folder_widget)
        folder_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        progress_layout.addWidget(self.folder_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Add the folder label to the folder layout
        folder_layout.addWidget(self.folder_label)
        self.folder_label.setVisible(False)
        

        # Add the folder widget to the progress layout
        progress_layout.addWidget(folder_widget)

        # Create a widget to hold the progress label
        progress_label_widget = QWidget()
        progress_label_layout = QVBoxLayout(progress_label_widget)

        self.progress_label = QLabel("Processing Files...", self)
        self.progress_label.setVisible(False)
        self.progress_label.setStyleSheet("""
        text-align: left;
        font-weight: bold;
        font-size: 14px;
        padding-left: 0px;
        margin-left: 0px;
        color: #ffffff;
        """)
        self.progress_label.setFixedHeight(30)

        # For the Layout
        progress_label_layout.setContentsMargins(0, 0, 0, 0)  # (left, top, right, bottom)
        progress_label_layout.addWidget(self.progress_label)
        progress_label_layout.addWidget(self.progress_label)

        # Create a widget to hold both the progress label and the folder widget in a horizontal layout
        progress_and_folder_widget = QWidget()
        progress_and_folder_layout = QHBoxLayout(progress_and_folder_widget)
        progress_and_folder_layout.addWidget(progress_label_widget)
        progress_and_folder_layout.addWidget(folder_widget)

        # Add the progress and folder widget to the progress layout
        progress_layout.addWidget(progress_and_folder_widget)

        # Determine the base directory
        documents_folder = Path(self.base_directory)

        # # Check if the script is running as a bundled executable or as a script
        # if getattr(sys, 'frozen', False):
        #     base_dir = documents_folder
        # else:
        #     base_dir = documents_folder

        # Using the base directory in the paths
        self.drop_area1 = self.DropArea(documents_folder / 'Renamed Files' / 'export' / 'DRAFT', central_widget)
        self.drop_area2 = self.DropArea(documents_folder / 'Renamed Files' / 'export' / 'EXECUTED', central_widget)
        self.drop_area3 = self.DropArea(documents_folder / 'Renamed Files' / 'export' / 'FOR APPROVAL', central_widget)
        self.drop_area4 = self.DropArea(documents_folder / 'Renamed Files' / 'export' / 'PARTIALLY EXECUTED', central_widget)

        self.drop_area1.setStyleSheet(self.drop_area1.default_stylesheet)  # Set the default style
        self.drop_area2.setStyleSheet(self.drop_area2.default_stylesheet)  # Set the default style
        self.drop_area3.setStyleSheet(self.drop_area3.default_stylesheet)  # Set the default style
        self.drop_area4.setStyleSheet(self.drop_area4.default_stylesheet)  # Set the default style

        # Add drop areas to the progress layout
        progress_layout.addWidget(self.drop_area1)
        progress_layout.addWidget(self.drop_area2)
        progress_layout.addWidget(self.drop_area3)
        progress_layout.addWidget(self.drop_area4)

        # Button to run script, disabled by default
        self.button = QPushButton('Rename Files', central_widget)
        self.button.clicked.connect(self.run_script)
        self.button.setStyleSheet("""
            QPushButton {
                padding: 15px; color: white; background-color: #1D1B7D; border: 1px blue; border-radius: 5px; font-size: 18px;
            }

            QPushButton:hover {
                background-color: white;  /* Change the background color on hover */
                color: blue;  /* Change the text color on hover */
            }
        """)
        layout.addWidget(self.button)

        # Enable the button by default
        self.button.setEnabled(True)

    def set_image_scale(self, scale_factor):
        pixmap = QPixmap(resource_path('folder.png'))
        new_width = int(pixmap.width() * scale_factor)
        new_height = int(pixmap.height() * scale_factor)
        scaled_pixmap = pixmap.scaled(new_width, new_height, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.folder_label.setPixmap(scaled_pixmap)

    # def set_background_gradient(self, widget):
    #     gradient = QLinearGradient(0, 0, 0, widget.height())
    #     gradient.setColorAt(0, QColor(67, 73, 193))  # Start color (Level 1)
    #     gradient.setColorAt(0.33, QColor(128, 148, 208))  # Color at 25% (Level 2)
    #     gradient.setColorAt(0.5, QColor(165, 174, 216))  # Color at 50% (Level 3)
    #     gradient.setColorAt(1, QColor(164, 171, 249))  # End color (Level 4)
    #     widget.setAutoFillBackground(True)
    #     palette = widget.palette()
    #     palette.setBrush(QPalette.ColorRole.Window, gradient)
    #     widget.setPalette(palette)
    def set_background_image(self, widget, image_path):
        widget.setAutoFillBackground(True)
        palette = widget.palette()
        pixmap = QPixmap(image_path)
        palette.setBrush(QPalette.ColorRole.Window, QBrush(pixmap))
        widget.setPalette(palette)


    def run_script(self):
        # Lock the drop areas
        self.drop_area1.lock()
        self.drop_area2.lock()
        self.drop_area3.lock()
        self.drop_area4.lock()
        if not self.script_running:
            self.script_running = True
        self.progress_label.setVisible(True)  # Make the progress label visible
        self.folder_label.setVisible(True)
        # Start the scale animation
        self.scale_animation.start()
        self.thread.progress_signal.connect(self.update_progress)
        self.thread.status_signal.connect(self.update_status)
        self.thread.error_signal.connect(self.show_errors)
        self.thread.finished.connect(self.stop_animation)
         # Start the script thread
        self.thread.start()
        
        

    def stop_animation(self):
        self.script_running = False
        # Stop the scale animation
        self.scale_animation.stop()
        
        # Reset the style and hide the bubble for each drop area
        self.drop_area1.reset_style_and_hide_bubble()
        self.drop_area2.reset_style_and_hide_bubble()
        self.drop_area3.reset_style_and_hide_bubble()
        self.drop_area4.reset_style_and_hide_bubble()
        
        # Unlock the drop areas
        self.drop_area1.unlock()
        self.drop_area2.unlock()
        self.drop_area3.unlock()
        self.drop_area4.unlock()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    

    def get_total_files(self):
        # Calculate the total number of files based on the file_count in drop areas
        total_files = (
            self.drop_area1.file_count +
            self.drop_area2.file_count +
            self.drop_area3.file_count +
            self.drop_area4.file_count
        )
        return total_files
    
    def update_status(self, message):
        self.progress_label.setVisible(True)
        total_files = self.get_total_files()
        message_with_total = f"{message}\n({total_files} total files)"
        self.progress_label.setText(message_with_total)


    def show_errors(self, errors):
        if errors:
            error_message = "\n".join(errors)
            QMessageBox.critical(self, "Errors Encountered", error_message)
         
    def on_app_exit(self):
        documents_folder = Path(self.base_directory)
        old_directory_path = documents_folder / 'Renamed Files' / 'export' / 'output'
        print(f"Attempting to delete directory: {old_directory_path}")  # Debugging print statement
        try:
            shutil.rmtree(old_directory_path)
            print(f"Deleted directory: {old_directory_path}")
        except Exception as e:
            # logging.exception('Error encountered:')
            print(f"Failed to delete {old_directory_path}. Reason: {e}")
    
    
if __name__ == '__main__':
    QCoreApplication.processEvents()
    app = QApplication(sys.argv)
    
     # Create and show the splash screen

    splash_pixmap = QPixmap(resource_path('wireless_splash.png'))
    splash = SplashScreen(splash_pixmap)
    splash.show()
    ex = App()
    ex.show()
    sys.exit(app.exec())
