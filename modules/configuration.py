"""
Configuration module file for MIDI Song Generator Application.

This file defines constants, default settings, and helper functions for the MIDI Song Generator Application. 

It includes mappings for    - musical keys 
                            - scales
                            - instruments
                            - genre-specific defaults
                            - chord progressions and song sections. 

These configurations are designed to ensure modularity and flexibility, 
which enables the application to adapt to various musical styles and user preferences.

"""
# Import necessary modules
import logging


# Musical Keys
# List of all valid musical keys
KEYS = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

# Common Scales
# List of common musical scales supported by the application
SCALES = [
    "Major", "Minor", "Dorian", "Mixolydian", "Phrygian", "Lydian",
    "Harmonic Minor", "Melodic Minor", "Pentatonic Major", "Pentatonic Minor",
    "Blues", "Hungarian Minor", "Arabic", "Japanese", "Whole Tone", "Chromatic",
]

# Default Settings for Each Genre
# Dictionary defining default settings for various genres
GENRE_DEFAULTS = {
    "Pop": {
        "time_signature": "4/4",
        "scale": "Major",
        "key": "C",
        "instruments": ["Electric Piano", "Guitar", "Synth", "Bass", "Vocal Pad"]
    },
    "Rock": {
        "time_signature": "4/4",
        "scale": "Minor",
        "key": "E",
        "instruments": ["Electric Guitar (Distorted)", "Electric Guitar (Clean)", "Bass", "Drums", "Synth Pad"]
    },
    "Jazz": {
        "time_signature": "4/4",
        "scale": "Dorian",
        "key": "G",
        "instruments": ["Saxophone", "Piano", "Double Bass", "Drums", "Trumpet"]
    },
    "Classical": {
        "time_signature": "3/4",
        "scale": "Major",
        "key": "F",
        "instruments": ["String Ensemble", "Violin", "Piano", "Cello", "Harpsichord"]
    },
    "Electronic": {
        "time_signature": "4/4",
        "scale": "Mixolydian",
        "key": "A",
        "instruments": ["Synth Lead", "Synth Pad", "Synth Bass", "Drums", "Percussion"]
    },
    "Hip-Hop": {
        "time_signature": "4/4",
        "scale": "Minor",
        "key": "D",
        "instruments": ["808 Bass", "Drums", "Synth Lead", "Strings", "Percussion"]
    },
    "Folk": {
        "time_signature": "6/8",
        "scale": "Pentatonic Major",
        "key": "G",
        "instruments": ["Acoustic Guitar", "Violin", "Flute", "Double Bass", "Percussion"]
    },
    "User": {
        "time_signature": "4/4",
        "scale": "Major",
        "key": "C",
        "instruments": ["Piano", "Bass", "Drums"]
    },
}

# Default Sections for Each Genre
# Dictionary defining default song sections for each genre
GENRE_SECTIONS = {
    "Pop": [("Intro", 8), ("Verse", 16), ("PreChorus", 8), ("Chorus", 8), ("Verse", 16), ("Chorus", 8), ("Bridge", 8), ("Outro", 8)],
    "Rock": [("Intro", 4), ("Verse", 16), ("PreChorus", 8), ("Chorus", 8), ("Verse", 16), ("Chorus", 8), ("Solo", 8), ("Bridge", 8), ("Chorus", 8), ("Outro", 8)],
    "Jazz": [("Head", 8), ("Solo", 16), ("Head", 8), ("Outro", 4)],
    "Classical": [("Exposition", 16), ("Development", 16), ("Recapitulation", 16), ("Coda", 8)],
    "Electronic": [("Build-up", 16), ("Drop", 16), ("Verse", 16), ("Outro", 8)],
    "Hip-Hop": [("Intro", 4), ("Verse", 16), ("Chorus", 8), ("Outro", 4)],
    "Folk": [("Intro", 16), ("Verse", 16), ("Chorus", 8), ("Verse", 16), ("Chorus", 8), ("Bridge", 8), ("Outro", 16)],
    "User": [("Intro", 8), ("Verse", 8), ("Chorus", 16), ("Bridge", 8), ("Outro", 16)],
}

# Song Sections (Customizable)
# List to store user-defined song sections
SONG_SECTIONS = []

def load_default_sections(genre):
    """
    Load default sections for a given genre into SONG_SECTIONS.

    Args:
        genre (str): The genre name.
    """
    global SONG_SECTIONS
    SONG_SECTIONS.clear()  # Clear existing sections
    default_sections = GENRE_SECTIONS.get(genre, [])
    SONG_SECTIONS.extend(default_sections)
    logging.info(f"Loaded sections for genre '{genre}': {SONG_SECTIONS}")

def add_section(name, length):
    """
    Add a new section to SONG_SECTIONS.

    Args:
        name (str): The name of the section.
        length (int): The length of the section in bars.
    """
    SONG_SECTIONS.append((name, length))

def remove_section(index):
    """
    Remove a section from SONG_SECTIONS by index.

    Args:
        index (int): The index of the section to remove.
    """
    if 0 <= index < len(SONG_SECTIONS):
        SONG_SECTIONS.pop(index)

def get_song_sections():
    """
    Retrieve the current song sections.

    Returns:
        list: A list of the current song sections.
    """
    return SONG_SECTIONS

# Chord Definitions
# Dictionary defining chord progressions for each genre
GENRE_CHORD_MAPS = {
    "Pop": {
        "I": [0, 2, 4],
        "ii": [1, 3, 5],
        "IV": [3, 5, 0],
        "V": [4, 6, 1],
        "vi": [5, 0, 2],
    },
    "Rock": {
        "I": [0, 2, 4],
        "bIII": [2, 4, 6],
        "IV": [3, 5, 0],
        "V": [4, 6, 1],
        "bVI": [5, 7, 9],
        "bVII": [6, 8, 10],
    },
    "Jazz": {
        "ii": [1, 3, 5],
        "V": [4, 6, 1],
        "I": [0, 2, 4],
        "vi": [5, 0, 2],
        "maj7": [0, 4, 7, 11],
        "m7": [0, 3, 7, 10],
    },
    "Classical": {
        "I": [0, 2, 4],
        "ii": [1, 3, 5],
        "iii": [2, 4, 6],
        "IV": [3, 5, 0],
        "V": [4, 6, 1],
        "vi": [5, 0, 2],
        "vii°": [6, 1, 3],
    },
    "Electronic": {
        "i": [0, 3, 7],
        "III": [4, 7, 11],
        "VI": [9, 0, 4],
        "VII": [11, 2, 5],
        "v": [7, 10, 2],
    },
    "Hip-Hop": {
        "i": [0, 3, 7],
        "iv": [5, 8, 0],
        "v": [7, 10, 2],
        "VI": [9, 0, 4],
        "VII": [11, 2, 5],
    },
    "Folk": {
        "I": [0, 2, 4],
        "IV": [3, 5, 0],
        "V": [4, 6, 1],
        "vi": [5, 0, 2],
        "ii": [1, 3, 5],
    },
    "User": {
        "I": [0, 2, 4],
        "IV": [3, 5, 0],
        "V": [4, 6, 1],
        "vi": [5, 0, 2],
    },
}

# MIDI Instrument Mappings
# Dictionary mapping instrument names to MIDI program numbers
INSTRUMENT_MAP = {
    # Piano and Keyboard
    "Piano": 0,
    "Bright Acoustic Piano": 1,
    "Electric Grand Piano": 2,
    "Honky-tonk Piano": 3,
    "Electric Piano 1": 4,
    "Electric Piano 2": 5,
    "Electric Piano": 4,
    "Harpsichord": 6,
    "Clavinet": 7,

    # Guitars
    "Acoustic Guitar": 24,
    "Electric Guitar (Clean)": 26,
    "Electric Guitar (Distorted)": 30,
    "Nylon Guitar": 25,

    # Strings
    "Violin": 40,
    "Viola": 41,
    "Cello": 42,
    "Double Bass": 43,
    "Harp": 46,
    "String Ensemble": 48,

    # Woodwinds
    "Flute": 73,
    "Clarinet": 71,
    "Oboe": 68,
    "Bassoon": 70,
    "Saxophone": 65,

    # Brass
    "Trumpet": 56,
    "Trombone": 57,
    "French Horn": 60,
    "Tuba": 58,

    # Synths
    "Synth Lead": 80,
    "Synth Pad": 88,
    "Synth Bass": 38,
    "Synth Pluck": 81,

    # Percussion
    "Drums": 0,  # Drums use channel 9
    "Timpani": 47,
    "Marimba": 12,
    "Xylophone": 13,
    "Vibraphone": 11,
    "Timpani": 47,
    "Cymbals": 49,
    "Bass Drum": 35,
    "Triangle": 81,

    # World Instruments
    "Sitar": 104,
    "Shamisen": 105,
    "Koto": 106,
    "Steel Drums": 114,
    "Taiko Drum": 117,

    # Bass
    "Electric Bass": 33,
    "Acoustic Bass": 32,
    "Slap Bass": 36,
    "Fretless Bass": 35,
    "808 Bass": 33,

    # Additional Instruments
    "Accordion": 21,
    "Harmonica": 22,
    "Kalimba": 108,
    "Hang Drum": 116,
    "Vocal Pad": 88,
}

# MIDI Note Numbers for Keys
# Dictionary mapping musical keys to their MIDI note numbers
KEY_MAP = {
    "C": 60, "C#": 61, "D": 62, "D#": 63, "E": 64, "F": 65, "F#": 66,
    "G": 67, "G#": 68, "A": 69, "A#": 70, "B": 71,
}

# Intervals for Scales
# Dictionary mapping scale names to their corresponding intervals in semitones
SCALE_INTERVALS = {
    "Major": [0, 2, 4, 5, 7, 9, 11],
    "Minor": [0, 2, 3, 5, 7, 8, 10],
    "Dorian": [0, 2, 3, 5, 7, 9, 10],
    "Mixolydian": [0, 2, 4, 5, 7, 9, 10],
    "Phrygian": [0, 1, 3, 5, 7, 8, 10],
    "Lydian": [0, 2, 4, 6, 7, 9, 11],
    "Harmonic Minor": [0, 2, 3, 5, 7, 8, 11],
    "Melodic Minor": [0, 2, 3, 5, 7, 9, 11],
    "Pentatonic Major": [0, 2, 4, 7, 9],
    "Pentatonic Minor": [0, 3, 5, 7, 10],
    "Blues": [0, 3, 5, 6, 7, 10],
    "Hungarian Minor": [0, 2, 3, 6, 7, 8, 11],
    "Arabic": [0, 1, 4, 5, 7, 8, 11],
    "Japanese": [0, 1, 5, 7, 8],
    "Whole Tone": [0, 2, 4, 6, 8, 10],
    "Chromatic": list(range(12)),
}

# Helper Functions 
def is_valid_key(key):
    """
    Check if the given key is valid.

    Args:
        key (str): The musical key to validate.

    Returns:
        bool: True if the key is valid, False otherwise.
    """
    return key in KEY_MAP

def is_valid_scale(scale):
    """
    Check if the given scale is valid.

    Args:
        scale (str): The scale name to validate.

    Returns:
        bool: True if the scale is valid, False otherwise.
    """
    return scale in SCALE_INTERVALS

def is_valid_genre(genre):
    """
    Check if the given genre is valid.

    Args:
        genre (str): The genre name to validate.

    Returns:
        bool: True if the genre is valid, False otherwise.
    """
    return genre in GENRE_DEFAULTS

def is_valid_instrument(instrument):
    """
    Check if the given instrument is valid.

    Args:
        instrument (str): The instrument name to validate.

    Returns:
        bool: True if the instrument is valid, False otherwise.
    """
    return instrument in INSTRUMENT_MAP

def get_genre_defaults(genre):
    """
    Retrieve default settings for a given genre, with fallback to 'Default'.

    Args:
        genre (str): The genre name for which to retrieve defaults.

    Returns:
        dict: A dictionary containing default settings for the genre.
    """
    return GENRE_DEFAULTS.get(genre, GENRE_DEFAULTS["Default"])