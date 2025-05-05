''' 
MIDI Generator Module for programmatic music composition for MIDI Song Generator Application

This file contains the core logic for generating MIDI files for the application. 
It includes functions for creating:-
                - scale notes
                - chord progressions
                - melodies
                - harmonies
                - rhythmic patterns and percussion. 
                                    
The module supports genre-specific rules and features such as:- 
                - tempo changes
                - key modulation
                
this module integrates the midiutil library and configuration mappings to produce customisable MIDI compositions.

'''
import sys
import os
# Add the project root directory to sys.path (troubleshooting whilst experiencing execution problems)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
from modules.configuration import (
    INSTRUMENT_MAP, KEY_MAP, SCALE_INTERVALS, GENRE_CHORD_MAPS, GENRE_DEFAULTS, GENRE_SECTIONS
)
from midiutil import MIDIFile
import random
import time
import logging

random.seed(time.time())  # Seed the random number generator with the current time

BEATS_PER_BAR = 4  # Number of beats in one bar (default for 4/4 time signature)

# 1. Generate Scale Notes
def generate_scale_notes(key, scale):
    """
    Generate MIDI note numbers for the given key and scale.
    """
    if key not in KEY_MAP:
        raise ValueError(f"Invalid key: {key}. Valid keys are: {list(KEY_MAP.keys())}")
    if scale not in SCALE_INTERVALS:
        raise ValueError(f"Invalid scale: {scale}. Valid scales are: {list(SCALE_INTERVALS.keys())}")

    root_note = KEY_MAP.get(key, 60)
    intervals = SCALE_INTERVALS.get(scale, SCALE_INTERVALS["Major"])
    return [root_note + interval for interval in intervals]

# 2. Generate Chord Progression
def generate_chord_progression(scale_notes, genre, progression=None):
    """
    Generate MIDI note numbers for a given chord progression with genre-specific rules.

    Args:
        scale_notes (list): Notes in the scale.
        genre (str): The musical genre (e.g., "Pop", "Jazz").
        progression (list): Optional predefined chord progression.

    Returns:
        list: A list of chords, where each chord is a list of MIDI note numbers.
    """
    if genre not in GENRE_CHORD_MAPS:
        logging.warning(f"Genre '{genre}' not found. Falling back to 'Pop'.")
        genre = "Pop"  # Fallback to a default genre

    chord_map = GENRE_CHORD_MAPS.get(genre, GENRE_CHORD_MAPS["Pop"])
    if progression is None or not progression:
        progression = random.choices(list(chord_map.keys()), k=4)  # Generate a random 4-chord progression

    chords = []
    for chord_name in progression:
        chord_intervals = chord_map[chord_name]
        chord = [scale_notes[i % len(scale_notes)] for i in chord_intervals]

        # Apply genre-specific rules
        if genre == "Jazz":
            # Add 7ths, 9ths, or 13ths to chords
            if random.random() > 0.5:
                chord.append(chord[0] + 10)  # Add a minor 7th
            if random.random() > 0.7:
                chord.append(chord[0] + 14)  # Add a major 9th
            if random.random() > 0.9:
                chord.append(chord[0] + 21)  # Add a 13th
        elif genre == "Classical":
            # Keep chords simple (triads) and occasionally add a suspension
            chord = chord[:3]
            if random.random() > 0.8:
                chord[1] = chord[0] + 5  # Replace the third with a fourth (suspension)
        elif genre == "Pop":
            # Occasionally add a 7th or a sus2/sus4
            if random.random() > 0.8:
                chord.append(chord[0] + 10)  # Add a minor 7th
            if random.random() > 0.9:
                chord[1] = chord[0] + 2  # Replace the third with a second (sus2)
            elif random.random() > 0.9:
                chord[1] = chord[0] + 5  # Replace the third with a fourth (sus4)
        elif genre == "Rock":
            # Use power chords (root and fifth) and occasionally add an octave
            chord = [chord[0], chord[0] + 7]
            if random.random() > 0.7:
                chord.append(chord[0] + 12)  # Add an octave
        elif genre == "Electronic":
            # Add wide intervals and dissonance
            if random.random() > 0.5:
                chord.append(chord[0] + 11)  # Add a major 7th
            if random.random() > 0.7:
                chord.append(chord[0] + 13)  # Add a minor 9th
        elif genre == "Folk":
            # Keep chords simple and diatonic, occasionally add a sixth
            if random.random() > 0.8:
                chord.append(chord[0] + 9)  # Add a sixth
        elif genre == "Hip-Hop":
            # Use minor chords with added 7ths and 9ths for a jazzy feel
            chord = chord[:3]
            if random.random() > 0.5:
                chord.append(chord[0] + 10)  # Add a minor 7th
            if random.random() > 0.7:
                chord.append(chord[0] + 14)  # Add a major 9th
        elif genre == "Blues":
            # Use dominant 7th chords
            chord = chord[:3]
            chord.append(chord[0] + 10)  # Add a minor 7th
            if random.random() > 0.6:
                chord.append(chord[0] + 14)  # Add a major 9th

        # Randomly apply inversions
        if random.random() > 0.5:
            chord = chord[1:] + [chord[0] + 12]  # First inversion
        elif random.random() > 0.5:
            chord = chord[2:] + [chord[0] + 12, chord[1] + 12]  # Second inversion

        chords.append(chord)
    return chords

# 3. Generate Genre-Specific Melody
def generate_genre_specific_melody(genre, scale_notes, length):
    """
    Generate genre-specific melodic patterns with randomness and variation.
    """
    melody = []
    for _ in range(length):
        if random.random() < 0.15:  # 15% chance to add a rest
            melody.append(None)  # Represent a rest with None
            continue

        note = random.choice(scale_notes)
        if genre == "Jazz":
            note += random.randint(-2, 2)  # Add chromatic tones
        elif genre == "Classical":
            note += random.randint(-1, 1)  # Add subtle variations
        elif genre == "Rock":
            note = random.choice([scale_notes[0], scale_notes[3], scale_notes[4]])  # Power chord notes
        elif genre == "Electronic":
            note += random.randint(-3, 3)  # Add wide variations
        elif genre == "Pop":
            note = random.choice([scale_notes[0], scale_notes[2], scale_notes[4]])  # Triad notes
        elif genre == "Folk":
            note = random.choice(scale_notes)  # Folk melodies are simple and scale-based
            if random.random() < 0.3:  # 30% chance to add an octave variation
                note += random.choice([-12, 12])

        melody.append(note)
    return melody

# 4. Add Dynamics
def add_dynamics(base_velocity, section_progress, crescendo=True):
    """
    Apply crescendos, decrescendos, and random velocity variations.
    """
    variation = random.randint(-10, 20)  # Reduce variation for more subtle changes
    if crescendo:
        return max(0, min(127, base_velocity + int(30 * section_progress) + variation))
    else:
        return max(0, min(127, base_velocity - int(30 * section_progress) + variation))

# 5. Note duration variations 
def add_melody(midi, track, channel, melody, start_time, base_duration, velocity):
    """
    Add a melody to the MIDI file with varied note durations.
    """
    for i, note in enumerate(melody):
        if note is not None:  # Skip rests
            duration = base_duration * random.choice([0.5, 1, 1.5, 2, 2.5, 3])  # Add variation
            midi.addNote(track, channel, note, start_time + i, duration, velocity)

# 6. Modulate Key
def modulate_key(scale_notes, steps):
    """
    Modulate the key by shifting all notes in the scale by a number of steps.

    Args:
        scale_notes (list): The original scale notes.
        steps (int): The number of semitone steps to shift.

    Returns:
        list: The modulated scale notes.
    """
    return [note + steps for note in scale_notes]

# 7. Randomly add ornamentation to notes
def add_ornamentation(note, genre):
    """
    Add ornamentation to a note based on the genre.
    """
    if genre == "Classical" and random.random() < 0.5:  # 30% chance for trills
        return [note, note + 1, note]
    elif genre == "Jazz" and random.random() < 0.2:  # 20% chance for grace notes
        return [note - 1, note]
    elif genre == "Pop" and random.random() < 0.2:  # 20% chance for grace notes
        return [note - 1, note]
    elif genre == "Rock" and random.random() < 0.4:  # 20% chance for grace notes
        return [note - 1, note]
    return [note]

# 8. Generate Percussion Pattern
def generate_musical_percussion_pattern(genre, length_in_beats):
    """
    Generate musical percussion patterns for the given genre with structured rhythms and dynamic variations.
    """
    genre_patterns = {
        "Rock": {
            "kick": [1, 0, 1, 0],  # Kick on beats 1 and 3
            "snare": [0, 1, 0, 1],  # Snare on beats 2 and 4
            "hihat": [1, 1, 1, 1]  # Hi-hat on all beats
        },
        "Jazz": {
            "ride": [1, 0.5, 1, 0.5],  # Swing ride pattern
            "snare": [0, 0.5, 0, 0.5],  # Light snare accents
            "kick": [1, 0, 0, 0]  # Sparse kick hits
        },
        "Electronic": {
            "kick": [1, 0, 1, 0],  # Kick on beats 1 and 3
            "clap": [0, 1, 0, 1],  # Clap on beats 2 and 4
            "hihat": [1, 1, 1, 1]  # Hi-hat on all beats
        },
        "Pop": {
            "kick": [1, 0, 1, 0],  # Kick on beats 1 and 3
            "snare": [0, 1, 0, 1],  # Snare on beats 2 and 4
            "hihat": [1, 1, 1, 1]  # Hi-hat on all beats
        },
        "Folk": {
            "kick": [1, 0, 0, 0],  # Kick on beat 1
            "shaker": [1, 1, 1, 1],  # Shaker on all beats
            "tambourine": [0, 1, 0, 1]  # Tambourine on beats 2 and 4
        },
        "Classical": {
            "timpani": [1, 0, 0, 1],  # Timpani on beats 1 and 4
            "cymbals": [0, 0, 1, 0],  # Cymbals on beat 3
            "bass_drum": [1, 0, 0, 0],  # Bass drum on beat 1
            "triangle": [0, 1, 0, 1]  # Triangle on beats 2 and 4
        }
    }

    pattern = genre_patterns.get(genre, genre_patterns["Pop"])
    percussion = []

    for beat in range(length_in_beats):
        # Add timpani
        if pattern.get("timpani", [])[beat % 4]:
            percussion.append(47)  # Timpani
        else:
            percussion.append(None)

        # Add cymbals
        if pattern.get("cymbals", [])[beat % 4]:
            percussion.append(49)  # Cymbals
        else:
            percussion.append(None)

        # Add bass drum
        if pattern.get("bass_drum", [])[beat % 4]:
            percussion.append(35)  # Bass drum
        else:
            percussion.append(None)

        # Add triangle
        if pattern.get("triangle", [])[beat % 4]:
            percussion.append(81)  # Triangle
        else:
            percussion.append(None)

    logging.debug(f"Generated percussion pattern for genre '{genre}': {percussion}")
    return percussion

# 9. Generate Countermelody
def generate_countermelody(scale_notes, length):
    """
    Generate a countermelody that complements the main melody.
    """
    countermelody = []
    for i in range(length):
        note = random.choice(scale_notes) + random.choice([-12, 0, 12])  # Add octave variation
        countermelody.append(note)
    return countermelody

# 10. Add Melody
def add_melody(midi, track, channel, melody, start_time, duration, velocity):
    """
    Add a melody to the MIDI file.
    """
    for i, note in enumerate(melody):
        if note is not None:  # Skip rests
            midi.addNote(track, channel, note, start_time + i, duration, velocity)

# 11. Add Harmony
def add_harmony(midi, track, channel, chords, start_time, duration, base_velocity, genre=None):
    """
    Add harmonies (chords) to the MIDI file with dynamic velocity and genre-specific variations.

    Args:
        midi (MIDIFile): The MIDI file object.
        track (int): The track number for harmony.
        channel (int): The MIDI channel for harmony.
        chords (list): A list of chords, where each chord is a list of MIDI note numbers.
        start_time (float): The start time for the harmony.
        duration (float): The duration of each chord.
        base_velocity (int): The base velocity (volume) of the notes.
        genre (str): The musical genre (optional, for genre-specific harmonic rules).
    """
    previous_chord = None
    for i, chord in enumerate(chords):
        # Apply voice leading: minimize movement between notes
        if previous_chord:
            chord = sorted(chord, key=lambda note: min(abs(note - prev) for prev in previous_chord))

        # Apply genre-specific harmonic variations
        if genre == "Jazz":
            # Add extensions like 9ths, 11ths, or 13ths
            if random.random() > 0.5:
                chord.append(chord[0] + 14)  # Add a major 9th
            if random.random() > 0.7:
                chord.append(chord[0] + 17)  # Add an 11th
            if random.random() > 0.9:
                chord.append(chord[0] + 21)  # Add a 13th
        elif genre == "Classical":
            # Use inversions to create smoother transitions
            if random.random() > 0.5:
                chord = chord[1:] + [chord[0] + 12]  # First inversion
            elif random.random() > 0.5:
                chord = chord[2:] + [chord[0] + 12, chord[1] + 12]  # Second inversion
        elif genre == "Pop":
            # Add occasional sus2 or sus4 chords
            if random.random() > 0.8:
                chord[1] = chord[0] + 2  # Replace the third with a second (sus2)
            elif random.random() > 0.8:
                chord[1] = chord[0] + 5  # Replace the third with a fourth (sus4)
        elif genre == "Rock":
            # Use power chords (root and fifth) with occasional octaves
            chord = [chord[0], chord[0] + 7]
            if random.random() > 0.7:
                chord.append(chord[0] + 12)  # Add an octave

        # Add each note in the chord to the MIDI file
        for note in chord:
            velocity = base_velocity + random.randint(-10, 10)  # Add slight velocity variation
            midi.addNote(track, channel, note, start_time + i * duration, duration, velocity)

        # Update the previous chord for voice leading
        previous_chord = chord

# 12. Add Percussion
def add_percussion(midi, track, channel, percussion_pattern, start_time, duration, velocity):
    logging.debug(f"Adding percussion: track={track}, channel={channel}, pattern={percussion_pattern}, "
                  f"start_time={start_time}, duration={duration}, velocity={velocity}")   
    """
    Add percussion patterns to the MIDI file.
    """
    for i, hit in enumerate(percussion_pattern):
        if hit is not None:  # Only add notes where the pattern specifies a hit
            midi.addNote(track, channel, hit, start_time + i, duration, velocity)


            logging.debug(f"Added percussion note: {hit} at time {start_time + i} with velocity {velocity}")

''' TEST FUINCTION '''

# Test the imports from configuration.py (troulbeshooting due to execution problems)
# This function checks if all the required functions and data are accessible from the mconfiguration module.
# It will raise an AssertionError if any of the functions are not callable or not imported correctly.
def test_imports_from_configuration():

    try:
        # Test if the imported variables exist and are of the correct type
        assert isinstance(INSTRUMENT_MAP, dict), "INSTRUMENT_MAP is not a dictionary"
        assert isinstance(KEY_MAP, dict), "KEY_MAP is not a dictionary"
        assert isinstance(SCALE_INTERVALS, dict), "SCALE_INTERVALS is not a dictionary"
        assert isinstance(GENRE_CHORD_MAPS, dict), "GENRE_CHORD_MAPS is not a dictionary"
        assert isinstance(GENRE_DEFAULTS, dict), "GENRE_DEFAULTS is not a dictionary"
        assert isinstance(GENRE_SECTIONS, dict), "GENRE_SECTIONS is not a dictionary"

        # Log success
        logging.info("All variables imported successfully from configuration.py")
        print("All variables imported successfully from configuration.py")

    except AssertionError as e:
        logging.error(f"Import test failed: {e}")
        print(f"Import test failed: {e}")

# Run the test if this script is executed directly
if __name__ == "__main__":
    test_imports_from_configuration()