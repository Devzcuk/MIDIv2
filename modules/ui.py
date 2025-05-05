import sys
import os

# Add the project root directory to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import necessary modules
from modules.midi_generator import create_midi
from modules.configuration import GENRE_DEFAULTS, GENRE_SECTIONS, SONG_SECTIONS, KEYS, SCALES
from modules.configuration import load_default_sections

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QGroupBox,
    QPushButton, QSlider, QComboBox, QCheckBox, QListWidget, QMessageBox, QWidget, QSpinBox
)
from pygame import mixer
import logging

''' GRAPHIC USER INTERFACE '''

# This class creates the GUI for the MIDI song generator application.
class MidiGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MIDI Song Generator")
        self.setGeometry(100, 100, 800, 600)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Initialise attributes
        self.main_layout = QVBoxLayout(self.central_widget)
        self.instrument_comboboxes = []  # list for instrument comboboxes
        self.setup_ui()

    def setup_ui(self):
        """Set up the user interface."""
        # Initialize genre_combobox
        self.genre_combobox = QComboBox()
        self.genre_combobox.addItems(list(GENRE_DEFAULTS.keys()))  # Populate genres dynamically
        logging.info(f"Genre combobox initialized with items: {self.genre_combobox.count()} genres")

        # File Settings Group
        file_settings_group = QGroupBox("File Settings")
        file_settings_layout = QVBoxLayout()
        file_name_layout = QHBoxLayout()
        file_name_layout.addWidget(QLabel("File Name:"))
        self.file_name_input = QLineEdit("output.mid")
        file_name_layout.addWidget(self.file_name_input)
        file_settings_layout.addLayout(file_name_layout)
        file_settings_group.setLayout(file_settings_layout)
        self.main_layout.addWidget(file_settings_group)
        self.genre_combobox.currentIndexChanged.connect(self.update_genre_data)
        

        ''' BPM and Time Signature Group '''
        bpm_time_group = QGroupBox("Tempo and Time Signature")
        bpm_time_layout = QVBoxLayout()
        bpm_layout = QHBoxLayout()
        bpm_layout.addWidget(QLabel("BPM:"))
        self.bpm_slider = QSlider(Qt.Horizontal)
        self.bpm_slider.setMinimum(60)
        self.bpm_slider.setMaximum(240)
        self.bpm_slider.setValue(120)
        self.bpm_slider.setToolTip("Adjust the tempo of the MIDI file (60-240 BPM).")
        self.bpm_slider.valueChanged.connect(self.update_bpm_label)
        bpm_layout.addWidget(self.bpm_slider)
        self.bpm_label = QLabel("120")
        bpm_layout.addWidget(self.bpm_label)
        bpm_time_layout.addLayout(bpm_layout)
    
        time_signature_layout = QHBoxLayout()
        time_signature_layout.addWidget(QLabel("Time Signature:"))
        self.time_signature_combobox = QComboBox()
        self.time_signature_combobox.addItems(["4/4", "3/4", "6/8"])
        time_signature_layout.addWidget(self.time_signature_combobox)
        bpm_time_layout.addLayout(time_signature_layout)
        bpm_time_group.setLayout(bpm_time_layout)
        self.main_layout.addWidget(bpm_time_group)
    
        ''' Genre and Sections Group '''
        genre_sections_group = QGroupBox("Genre and Sections")
        genre_sections_layout = QVBoxLayout()
        genre_layout = QHBoxLayout()
        genre_layout.addWidget(QLabel("Genre:"))

        # Initialise genre combobox with default genres
        self.genre_combobox = QComboBox()
        self.genre_combobox.addItems(list(GENRE_DEFAULTS.keys()))  # Populate genres dynamically
        genre_layout.addWidget(self.genre_combobox)

        # connect signal for genre selection
        self.genre_combobox.currentIndexChanged.connect(self.update_instruments)  # Connect signal for instruments
        self.genre_combobox.currentIndexChanged.connect(self.update_sections)  # Connect signal for sections
        self.genre_combobox.currentIndexChanged.connect(self.update_genre_data)  # Update scale, key, sections, etc.
        genre_sections_layout.addLayout(genre_layout)
        genre_layout.addWidget(self.genre_combobox)
        genre_sections_layout.addLayout(genre_layout)

        ''' Scale and Key Selection '''
        scale_key_layout = QHBoxLayout()
        scale_key_layout.addWidget(QLabel("Scale:"))
        self.scale_combobox = QComboBox()
        self.scale_combobox.addItems(SCALES)  # Populate with all scales
        scale_key_layout.addWidget(self.scale_combobox)

        scale_key_layout.addWidget(QLabel("Key:"))
        self.key_combobox = QComboBox()
        self.key_combobox.addItems(KEYS)  # Populate with all keys
        scale_key_layout.addWidget(self.key_combobox)
        genre_sections_layout.addLayout(scale_key_layout)

        genre_sections_group.setLayout(genre_sections_layout)
        self.main_layout.addWidget(genre_sections_group)
        
        '''Section List and Add Section Button '''
        section_list_layout = QVBoxLayout()
        section_list_layout.addWidget(QLabel("Sections:"))
        self.section_list = QListWidget()
        section_list_layout.addWidget(self.section_list)
    
        add_section_layout = QHBoxLayout()
        self.section_name_dropdown = QComboBox()
        self.update_section_dropdown()  # Initialise with default genre sections
        add_section_layout.addWidget(self.section_name_dropdown)
    
        self.section_length_input = QSpinBox()
        self.section_length_input.setMinimum(1)
        self.section_length_input.setMaximum(32)
        self.section_length_input.setValue(8)
        add_section_layout.addWidget(self.section_length_input)
    
        add_section_button = QPushButton("Add Section")
        add_section_button.clicked.connect(self.add_section)
        add_section_layout.addWidget(add_section_button)
        section_list_layout.addLayout(add_section_layout)
        genre_sections_layout.addLayout(section_list_layout)
        genre_sections_group.setLayout(genre_sections_layout)
        self.main_layout.addWidget(genre_sections_group)
    
        ''' Instruments Group '''
        instruments_group = QGroupBox("Instruments")
        instruments_layout = QVBoxLayout()
        instruments_layout.addWidget(QLabel("Instruments:"))
        self.instrument_layout = QVBoxLayout()
        instruments_layout.addLayout(self.instrument_layout)
        instruments_group.setLayout(instruments_layout)
        self.main_layout.addWidget(instruments_group)
    
        ''' Generate and Preview Buttons '''
        button_layout = QHBoxLayout()
        generate_button = QPushButton("Generate MIDI")
        generate_button.clicked.connect(self.generate_midi)
        generate_button.setToolTip("Generate a MIDI file based on the current settings.")
        button_layout.addWidget(generate_button)
    
        self.preview_button = QPushButton("Preview MIDI")
        self.preview_button.clicked.connect(self.preview_midi)
        self.preview_button.setToolTip("Preview the generated MIDI file.")
        button_layout.addWidget(self.preview_button)
        self.main_layout.addLayout(button_layout)

        ''' Add Reset Button '''
        reset_button = QPushButton("Reset")
        reset_button.clicked.connect(self.reset_ui)
        reset_button.setToolTip("Reset the UI to its default state.")
        button_layout.addWidget(reset_button)

    def reset_ui(self):
        """Reset the UI to its default state."""
        self.genre_combobox.setCurrentIndex(0)
        self.update_genre_data()
        self.file_name_input.setText("output.mid")
        self.bpm_slider.setValue(120)
        self.time_signature_combobox.setCurrentIndex(0)
        logging.info("UI reset to default state.")
    
        # Initialize sections, instruments, scale, and key based on the default genre
        self.update_genre_data()

    def update_bpm_label(self):
        self.bpm_label.setText(str(self.bpm_slider.value()))

    def update_instruments(self):
        """Update the instrument comboboxes based on the selected genre."""
        # Clear existing comboboxes
        for combobox in self.instrument_comboboxes:
            self.instrument_layout.removeWidget(combobox)
            combobox.deleteLater()
        self.instrument_comboboxes.clear()

        # Get the selected genre
        selected_genre = self.genre_combobox.currentText()
        default_instruments = GENRE_DEFAULTS.get(selected_genre, {}).get("instruments", [])

        # Add comboboxes for the default instruments
        for instrument in default_instruments:
            combobox = QComboBox()
            combobox.addItems(default_instruments)
            combobox.setCurrentText(instrument)
            self.instrument_comboboxes.append(combobox)
            self.instrument_layout.addWidget(combobox)

    def update_sections(self):
        """Update the section list and dropdown based on the selected genre."""
        # Clear existing sections in the section list
        self.section_list.clear()
    
        # Get the selected genre
        selected_genre = self.genre_combobox.currentText()
        logging.info(f"Updating sections for genre: {selected_genre}")
    
        # Load default sections for the selected genre
        load_default_sections(selected_genre)
    
        # Log the contents of SONG_SECTIONS for debugging
        logging.info(f"SONG_SECTIONS after loading: {SONG_SECTIONS}")
    
        # Populate the section list with default sections
        for section in SONG_SECTIONS:
            try:
                section_name, length = section[:2]  # Unpack only the first two elements
                self.section_list.addItem(f"{section_name}: {length} bars")
            except ValueError:
                logging.error(f"Invalid section format: {section}")
                continue
    
        # Update the section name dropdown
        self.update_section_dropdown()
    
        # Update the section name dropdown
        self.update_section_dropdown()

    def update_section_dropdown(self):
        """Update the section name dropdown based on the selected genre."""
        selected_genre = self.genre_combobox.currentText()
        sections = GENRE_SECTIONS.get(selected_genre, [])
        self.section_name_dropdown.clear()
        self.section_name_dropdown.addItems([name for name, _ in sections])

    def add_section(self):
        """Add a new section to the section list."""
        section_name = self.section_name_dropdown.currentText()
        section_length = self.section_length_input.value()
        if section_name:
            self.section_list.addItem(f"{section_name}: {section_length} bars")

    def update_genre_data(self):
        """Update scale, key, sections, and instruments based on the selected genre."""
        if not hasattr(self, 'genre_combobox'):
            logging.error("genre_combobox is not initialized!")
            return
    
        # Get the selected genre
        selected_genre = self.genre_combobox.currentText()
        logging.info(f"Updating genre data for selected genre: {selected_genre}")
    
        # Update scale and key
        self.update_scale_and_key(selected_genre)
    
        # Update sections
        self.update_sections()
    
        # Update instruments
        self.update_instruments()
    
    def update_scale_and_key(self, genre):
        """Update the scale and key dropdowns based on the selected genre."""
        genre_defaults = GENRE_DEFAULTS.get(genre, {})
        default_scale = genre_defaults.get("scale", "Major")
        default_key = genre_defaults.get("key", "C")
    
        # Reset scale and key to defaults
        self.scale_combobox.setCurrentText(default_scale)
        self.key_combobox.setCurrentText(default_key)
    
        logging.info(f"Scale and key reset to defaults for genre '{genre}': Scale={default_scale}, Key={default_key}")
    ''' MIDI FILE CREATION AND MIDI SONG PREVIEW '''

    # This function generates a MIDI file based on the user inputs and settings.
    def generate_midi(self):
        """Generate a MIDI file based on the current settings."""
        file_name = self.file_name_input.text()
        if not file_name.endswith(".mid"):
            file_name += ".mid"

        bpm = self.bpm_slider.value()
        time_signature = self.time_signature_combobox.currentText()
        genre = self.genre_combobox.currentText()

        # Get instruments from comboboxes
        instruments = [combobox.currentText() for combobox in self.instrument_comboboxes]

        # Get sections from the section list
        sections = []
        for i in range(self.section_list.count()):
            section_item = self.section_list.item(i).text()  # Properly retrieve the section item
            try:
                section_name, length = section_item.split(":")
                sections.append((section_name.strip(), int(length.split()[0])))
            except ValueError:
                QMessageBox.warning(self, "Warning", f"Invalid section format: {section_item}")
                logging.warning(f"Generate failed: Invalid section format: {section_item}")
                return

        # Validate inputs
        if not instruments:
            QMessageBox.warning(self, "Warning", "No instruments selected.")
            logging.warning("Generate failed: No instruments selected.")
            return

        if not sections:
            QMessageBox.warning(self, "Warning", "No sections added.")
            logging.warning("Generate failed: No sections added.")
            return

        scale = self.scale_combobox.currentText()
        key = self.key_combobox.currentText()

        try:
            logging.info("Generating MIDI file...")
            # Generate the MIDI file
            create_midi(
                file_name=file_name,
                bpm=bpm,
                time_signature=time_signature,
                scale=scale,
                key=key,
                genre=genre,
                instruments=instruments,
                sections=sections
            )
            QMessageBox.information(self, "Success", f"MIDI file generated: {file_name}")
            logging.info(f"MIDI file generated: {file_name}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to generate MIDI file: {e}")
            logging.error(f"Failed to generate MIDI file: {e}")

    def preview_midi(self):
        """Preview the generated MIDI file."""
        file_name = "preview.mid"

        # Ensure mixer is initialized
        if not mixer.get_init():
            QMessageBox.critical(self, "Error", "Audio mixer is not initialized.")
            logging.error("Audio mixer is not initialized.")
            return

        # Stop playback if already playing
        if mixer.music.get_busy():
            self.stop_preview()
            return

        # Retrieve values from the UI
        bpm = self.bpm_slider.value()
        time_signature = self.time_signature_combobox.currentText()
        genre = self.genre_combobox.currentText()

        # Get instruments from comboboxes
        instruments = [combobox.currentText() for combobox in self.instrument_comboboxes]

        # Get sections from the section list
        sections = []
        for i in range(self.section_list.count()):
            section_item = self.section_list.item(i).text()  # Properly retrieve the section item
            try:
                section_name, length = section_item.split(":")
                sections.append((section_name.strip(), int(length.split()[0])))
            except ValueError:
                QMessageBox.warning(self, "Warning", f"Invalid section format: {section_item}")
                logging.warning(f"Preview failed: Invalid section format: {section_item}")
                return

        # Validate inputs
        if not instruments:
            QMessageBox.warning(self, "Warning", "No instruments selected.")
            logging.warning("Preview failed: No instruments selected.")
            return

        if not sections:
            QMessageBox.warning(self, "Warning", "No sections added.")
            logging.warning("Preview failed: No sections added.")
            return

        scale = self.scale_combobox.currentText()
        key = self.key_combobox.currentText()

        try:
            logging.info("Generating MIDI file for preview...")
            # Call create_midi with all required arguments
            create_midi(
                file_name=file_name,
                bpm=bpm,
                time_signature=time_signature,
                scale=scale,
                key=key,
                genre=genre,
                instruments=instruments,
                sections=sections
            )
            logging.info(f"MIDI file written to {file_name}")

            # Play the generated MIDI file
            mixer.music.load(file_name)
            mixer.music.play()
            self.preview_button.setText("Stop Preview")
            logging.info("MIDI preview started.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to preview MIDI file: {e}")
            logging.error(f"Failed to preview MIDI file: {e}")

    ''' END OF UI.PY SCRIPT '''
