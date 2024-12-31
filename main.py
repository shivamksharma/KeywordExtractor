import os
import re
import time
import json
import csv
from tqdm import tqdm
from pydub import AudioSegment
from pydub.utils import make_chunks
import speech_recognition as sr

# Convert audio file to WAV format
def convert_to_wav(audio_file):
    try:
        sound = AudioSegment.from_file(audio_file)
        wav_file = audio_file.replace(os.path.splitext(audio_file)[1], ".wav")
        sound.export(wav_file, format="wav")
        return wav_file
    except Exception as e:
        print(f"Error converting audio file: {e}")
        return None

# Extract text from audio with timestamps
def extract_text_with_timestamps(audio_file, chunk_size=5000):  # chunk_size in milliseconds
    recognizer = sr.Recognizer()
    audio = AudioSegment.from_file(audio_file)
    chunks = make_chunks(audio, chunk_size)
    results = []
    for i, chunk in enumerate(chunks):
        with sr.AudioFile(chunk.export(format="wav")) as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data)
                if text:
                    start_time = i * chunk_size / 1000  # Convert to seconds
                    results.append({"text": text, "start_time": start_time})
            except sr.UnknownValueError:
                continue
    return results

# Search for multiple keywords in the extracted text
def search_multiple_keywords(keywords, audio_file):
    results = {keyword: [] for keyword in keywords}
    text_with_timestamps = extract_text_with_timestamps(audio_file)
    for entry in text_with_timestamps:
        for keyword in keywords:
            if keyword.lower() in entry["text"].lower():
                results[keyword].append({
                    "text": entry["text"],
                    "start_time": entry["start_time"]
                })
    return results

# Save results to JSON, CSV, or TXT
def save_results(results, output_file, format="json"):
    try:
        if format == "json":
            with open(output_file, 'w') as file:
                json.dump(results, file, indent=4)
        elif format == "csv":
            with open(output_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Keyword", "Text", "Start Time (s)"])
                for keyword, occurrences in results.items():
                    for occurrence in occurrences:
                        writer.writerow([keyword, occurrence["text"], occurrence["start_time"]])
        elif format == "txt":
            with open(output_file, 'w') as file:
                for keyword, occurrences in results.items():
                    file.write(f"Keyword: {keyword}\n")
                    for occurrence in occurrences:
                        file.write(f"Text: {occurrence['text']}\n")
                        file.write(f"Start Time: {occurrence['start_time']}s\n\n")
        print(f"Results saved to {output_file}.")
    except Exception as e:
        print(f"Error saving results to file: {e}")

# Real-time audio processing
def real_time_audio_processing(keywords):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening... (Press Ctrl+C to stop)")
        try:
            while True:
                audio = recognizer.listen(source)
                try:
                    text = recognizer.recognize_google(audio)
                    for keyword in keywords:
                        if keyword.lower() in text.lower():
                            print(f"Found keyword '{keyword}': {text}")
                except sr.UnknownValueError:
                    print("Could not understand audio.")
                except sr.RequestError:
                    print("API request failed.")
        except KeyboardInterrupt:
            print("Real-time processing stopped.")

# Main function
def main():
    print("\n=== Welcome to Audio Text Analyzer ===\n")
    mode = input("Choose mode: (1) File Analysis, (2) Real-Time Processing: ").strip()
    
    if mode == "1":
        # File Analysis Mode
        audio_file = input("Enter the path of the audio file: ").strip()
        if not os.path.isfile(audio_file):
            print("File not found.")
            return

        if not audio_file.endswith(".wav"):
            print("Converting audio file to WAV format...")
            audio_file = convert_to_wav(audio_file)
            if not audio_file:
                return

        keywords = input("Enter keywords to search (comma-separated): ").strip().split(",")
        results = search_multiple_keywords(keywords, audio_file)

        output_format = input("Enter output format (json/csv/txt): ").strip().lower()
        output_file = f"results.{output_format}"
        save_results(results, output_file, format=output_format)

    elif mode == "2":
        # Real-Time Processing Mode
        keywords = input("Enter keywords to search (comma-separated): ").strip().split(",")
        real_time_audio_processing(keywords)

    else:
        print("Invalid mode selected.")

if __name__ == "__main__":
    main()