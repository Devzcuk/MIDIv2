'''
Main Entry Point for the MIDI Song Generator Application

This file serves as the main entry point for the MIDI Song Generator application. 
It initialises the  - logging 
                    - sets up the application environment
                    - displays a splash screen
                    - launches the main GUI window (MidiGeneratorApp)

It also handles application-level error logging and ensures a smooth user experience during startup.

'''

import logging
import os
import time
from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from modules.ui import MidiGeneratorApp
from logging.handlers import RotatingFileHandler
import pygame 
from pygame import mixer

# Ensure the logs directory exists
# This creates a directory named "logs" if it doesn't already exist
log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Initialize basic logging configuration
# Logs are written to "app.log" in the "logs" directory
logging.basicConfig(
    filename=os.path.join(log_dir, "app.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Initialize logging with rotation
# RotatingFileHandler ensures that log files do not exceed 5 MB, keeping up to 3 backups
log_file = os.path.join(log_dir, "app.log")
handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=3)  # 5 MB per file, 3 backups
logging.basicConfig(
    handlers=[handler],
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Initialize pygame.mixer
try:
    mixer.init()
    logging.info("Pygame mixer initialized successfully.")
except Exception as e:
    logging.error(f"Failed to initialize pygame mixer: {e}")
    raise

# Main entry point of the application
if __name__ == "__main__":
    try:
        # Log the start of the application
        logging.info("Starting MIDI Song Generator application.")

        # Create the QApplication instance
        app = QApplication([])

        # Check for the splash screen image
        splash_image_path = "resources/splash.png"
        if not os.path.exists(splash_image_path):
            # Log a warning if the splash screen image is missing
            logging.warning(f"Splash screen image not found: {splash_image_path}")
            # Create a blank placeholder image if the splash image is missing
            splash_pix = QPixmap(400, 300)
            splash_pix.fill(Qt.white)  # Fill the placeholder with white color
        else:
            # Load the splash screen image
            splash_pix = QPixmap(splash_image_path)

        # Display the splash screen
        splash = QSplashScreen(splash_pix)
        splash.show()
        app.processEvents()  # Ensure the splash screen is displayed immediately

        # Simulate loading time (e.g., for initializing resources)
        time.sleep(2)

        # Initialize and display the main application window
        window = MidiGeneratorApp()
        window.show()
        splash.finish(window)  # Close the splash screen once the main window is ready

        # Start the application's event loop
        app.exec_()

        # Log the closure of the application
        logging.info("Application closed.")
    except Exception as e:
        # Log any unexpected errors that occur during execution
        logging.error(f"An unexpected error occurred: {e}")