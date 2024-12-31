import json
import os
import re
import time

import speech_recognition as sr
from fuzzywuzzy import process
from pydub import AudioSegment
from tqdm import tqdm


# Convert audio file to WAV format (required by speech_recognition)
def convert_to_wav(audio_file):
    try:
        sound = AudioSegment.from_file(audio_file)
        wav_file = audio_file.replace(os.path.splitext(audio_file)[1], ".wav")
        sound.export(wav_file, format="wav")
        return wav_file
    except Exception as e:
        print(f"Error converting audio file: {e}")
        return None


# Extract text from audio using Google Speech Recognition
def extract_text_from_audio(audio_file):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
            return text
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""


# Search for a keyword in the extracted text
def search_text_in_audio(text_to_search, audio_file):
    text = extract_text_from_audio(audio_file)
    if not text:
        return []
    sentences = text.split(".")
    occurrences = [
        sentence.strip()
        for sentence in sentences
        if text_to_search.lower() in sentence.lower()
    ]
    return occurrences


# Highlight the keyword in the text
def highlight_keyword(text, keyword):
    return re.sub(f"(?i){re.escape(keyword)}", f"**{keyword.upper()}**", text)


# Save results to a JSON file
def save_results_to_json(results, output_file, keyword):
    data = {"keyword": keyword, "occurrences": results}
    try:
        with open(output_file, "w") as file:
            json.dump(data, file, indent=4)
        print(f"Results saved to {output_file}.")
    except Exception as e:
        print(f"Error saving results to file: {e}")


# Prompt the user for an audio file path
def prompt_user_for_file():
    while True:
        file_path = input("Enter the path of the audio file (or 'q' to quit): ").strip()
        if file_path.lower() == "q":
            return None
        if os.path.isfile(file_path):
            return file_path
        else:
            print("File not found. Please enter a valid path.")


# Main function to orchestrate the program
def main():
    print("\n=== Welcome to Audio Text Analyzer ===\n")
    verbose = input("Enable verbose mode? (yes/no): ").lower() == "yes"

    # Prompt user for audio file
    audio_file = prompt_user_for_file()
    if not audio_file:
        return

    # Convert audio file to WAV format if necessary
    if not audio_file.endswith(".wav"):
        if verbose:
            print("Converting audio file to WAV format...")
        audio_file = convert_to_wav(audio_file)
        if not audio_file:
            return

    # Prompt user for keyword to search
    text_to_search = input("Enter the text to search for: ").strip()
    if not text_to_search:
        print("No keyword provided. Exiting.")
        return

    # Handle existing results file
    output_file = "results.json"
    if os.path.exists(output_file):
        action = input(
            "The results file 'results.json' already exists. Do you want to (o)verwrite, (r)eplace, or (c)reate a new file? "
        ).lower()
        if action == "o":
            pass
        elif action == "r":
            os.remove(output_file)
        elif action == "c":
            count = 1
            while os.path.exists(f"results_{count}.json"):
                count += 1
            output_file = f"results_{count}.json"
        else:
            print("Invalid choice. Using existing file.")

    # Simulate search process with a progress bar
    print("Searching for keyword...")
    for _ in tqdm(range(10), desc="Processing audio"):
        time.sleep(0.1)

    # Search for keyword in audio
    occurrences = search_text_in_audio(text_to_search, audio_file)

    # Display results
    if verbose:
        print(
            f"\nAnalysis complete. Found {len(occurrences)} occurrences of '{text_to_search}' in the audio."
        )
        if occurrences:
            print("\nOccurrences:")
            for occurrence in occurrences:
                print(f"- {highlight_keyword(occurrence, text_to_search)}")

    # Save results to file
    save_results_to_json(occurrences, output_file, text_to_search)


if __name__ == "__main__":
    main()
