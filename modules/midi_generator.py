''' 
MIDI Generator Module to create MIDI for MIDI Song Generator Application
                
this module integrates the midiutil library and configuration mappings to produce customisable MIDI compositions.

'''

import sys
import os
# Add the project root directory to sys.path (troubleshooting whilst experiencing execution problems)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from modules.music_program import (
    generate_scale_notes, generate_chord_progression, generate_genre_specific_melody,
    add_dynamics, add_melody, modulate_key, add_ornamentation,
    generate_musical_percussion_pattern, generate_countermelody, add_harmony, add_percussion
)

from midiutil import MIDIFile
from modules.music_program import generate_scale_notes, generate_chord_progression, generate_genre_specific_melody, add_dynamics, add_melody, modulate_key, add_ornamentation, generate_musical_percussion_pattern, generate_countermelody, add_harmony, add_percussion
import random
import time
import logging

random.seed(time.time())  # Seed the random number generator with the current time

BEATS_PER_BAR = 4  # Number of beats in one bar (default for 4/4 time signature)

# Create MIDI 
def create_midi(file_name, bpm, time_signature, scale, key, genre, instruments, sections,
                enable_dynamic_tempo=False, enable_dynamics=False, enable_modulation=False,
                enable_ornamentation=False, enable_countermelody=False, enable_percussion=True):
    """
    Create a MIDI file based on the given parameters.
    """
    # Validate inputs
    if not sections:
        raise ValueError("The 'sections' list is empty. Please provide at least one section.")
    if not instruments:
        raise ValueError("The 'instruments' list is empty. Please provide at least one instrument.")

    # Calculate the number of tracks
    num_tracks = len(instruments)
    if enable_countermelody:
        num_tracks += 1  # Add one track for countermelody
    if enable_percussion:
        num_tracks += 1  # Add one track for percussion

    midi = MIDIFile(num_tracks)
    start_time = 0  # Start time for the first note

    # Parse the time signature
    beats_per_bar, beat_unit = map(int, time_signature.split("/"))

    # Generate scale notes and chord progression
    scale_notes = generate_scale_notes(key, scale)
    if not scale_notes:
        raise ValueError(f"Failed to generate scale notes for key '{key}' and scale '{scale}'.")

    chords = generate_chord_progression(scale_notes, genre)

    for section_name, length in sections:
        section_length_in_beats = length * beats_per_bar

        # Apply dynamic tempo changes if enabled
        if enable_dynamic_tempo:
            if section_name.lower() == "intro":
                current_bpm = bpm - 10
            elif section_name.lower() == "outro":
                current_bpm = bpm - 20
            else:
                current_bpm = bpm
        else:
            current_bpm = bpm
        midi.addTempo(0, start_time, current_bpm)

        # Apply key modulation if enabled
        if enable_modulation and section_name.lower() == "bridge":
            scale_notes = modulate_key(scale_notes, 2)  # Modulate up by 2 semitones

        # Add melody to the MIDI file
        melody = generate_genre_specific_melody(genre, scale_notes, section_length_in_beats)
        if enable_ornamentation:
            melody = add_ornamentation(melody, genre)
        add_melody(midi, 0, 0, melody, start_time, 1, 100)  # Track 0 for melody

        # Add harmony to the MIDI file
        if enable_dynamics:
            harmony = add_dynamics(chords, section_length_in_beats)
        else:
            harmony = chords
        add_harmony(midi, 1, 1, harmony, start_time, 1, 80)  # Track 1 for harmony

        # Add rhythm to the MIDI file
        if len(instruments) > 2:
            rhythm_pattern = generate_genre_specific_melody(genre, scale_notes, section_length_in_beats)
            add_melody(midi, 2, 2, rhythm_pattern, start_time, 1, 90)  # Track 2 for rhythm

        # Add bass to the MIDI file
        if len(instruments) > 3:
            bass_line = [chord[0] for chord in chords]  # Use the root note of each chord
            add_melody(midi, 3, 3, bass_line, start_time, 1, 70)  # Track 3 for bass

        # Generate percussion pattern
        percussion_pattern = generate_musical_percussion_pattern(genre, section_length_in_beats)
        if percussion_pattern:
            add_percussion(midi, num_tracks - 1, 9, percussion_pattern, start_time, 1, 70)
        else:
            logging.warning("The percussion pattern is empty. Skipping percussion.")

        # Generate and add countermelody
        if enable_countermelody:
            countermelody = generate_countermelody(scale_notes, section_length_in_beats)
            if countermelody:
                add_melody(midi, num_tracks - 1, 0, countermelody, start_time, 1, 90)
            else:
                logging.warning("The countermelody is empty. Skipping countermelody.")

        start_time += section_length_in_beats

    # Write the MIDI file
    with open(file_name, "wb") as output_file:
        midi.writeFile(output_file)

''' TEST FUNCTION '''

# Test the imports from music_program.py (troulbeshooting due to execution problems)
# This function checks if all the required functions and data are accessible from the music_program module.
# It will raise an AssertionError if any of the functions are not callable or not imported correctly.
def test_imports_from_music_program():

    try:
        # Test function imports
        assert callable(generate_scale_notes), "generate_scale_notes is not callable"
        assert callable(generate_chord_progression), "generate_chord_progression is not callable"
        assert callable(generate_genre_specific_melody), "generate_genre_specific_melody is not callable"
        assert callable(add_dynamics), "add_dynamics is not callable"
        assert callable(add_melody), "add_melody is not callable"
        assert callable(modulate_key), "modulate_key is not callable"
        assert callable(add_ornamentation), "add_ornamentation is not callable"
        assert callable(generate_musical_percussion_pattern), "generate_musical_percussion_pattern is not callable"
        assert callable(generate_countermelody), "generate_countermelody is not callable"
        assert callable(add_harmony), "add_harmony is not callable"
        assert callable(add_percussion), "add_percussion is not callable"

        # Log success
        logging.info("All functions imported successfully from music_program.py")
        print("All functions imported successfully from music_program.py")

    except AssertionError as e:
        logging.error(f"Import test failed: {e}")
        print(f"Import test failed: {e}")

# Run the test if this script is executed directly
if __name__ == "__main__":
    test_imports_from_music_program()