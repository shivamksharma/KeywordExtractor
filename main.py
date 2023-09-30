import moviepy.editor as mp
import os
import speech_recognition as sr
import re
import time

def extract_text_from_audio(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
        text = recognizer.recognize_google(audio)
        return text

def search_text_in_audio(text_to_search, audio_file):
    text = extract_text_from_audio(audio_file)
    sentences = text.split(".")
    occurrences = [sentence for sentence in sentences if text_to_search.lower() in sentence.lower()]
    return occurrences

def highlight_keyword(text, keyword):
    return re.sub(f'(?i){re.escape(keyword)}', f'**{keyword.upper()}**', text)

def save_results_to_file(results, output_file, keyword):
    with open(output_file, 'w') as file:
        for result in results:
            highlighted_result = highlight_keyword(result, keyword)
            file.write(highlighted_result + '\n')

def prompt_user_for_file():
    while True:
        file_path = input("Enter the path of the audio file (or 'q' to quit): ")
        if file_path.lower() == 'q':
            return None
        if os.path.isfile(file_path):
            return file_path
        else:
            print("File not found. Please enter a valid path.")

def main():
    print("\n=== Welcome to Audio Text Analyzer ===\n")
    verbose = input("Enable verbose mode? (yes/no): ").lower() == 'yes'
    
    audio_file = prompt_user_for_file()
    if not audio_file:
        return

    if verbose:
        print(f"\nAnalyzing audio file '{audio_file}'...")
    text_to_search = input("Enter the text to search for: ")
    output_file = 'results.txt'

    if os.path.exists(output_file):
        action = input("The results file 'results.txt' already exists. Do you want to (o)verwrite, (r)eplace, or (c)reate a new file? ").lower()
        if action == 'o':
            pass
        elif action == 'r':
            os.remove(output_file)
        elif action == 'c':
            count = 1
            while os.path.exists(f"results_{count}.txt"):
                count += 1
            output_file = f"results_{count}.txt"
        else:
            print("Invalid choice. Using existing file.")
    
    print("Searching for keyword...")
    time.sleep(2)  # Simulating a search process

    occurrences = search_text_in_audio(text_to_search, audio_file)

    if verbose:
        print(f"\nAnalysis complete. Found {len(occurrences)} occurrences of '{text_to_search}' in the audio.")
        print(f"\nSaving results to {output_file}...")
    
    save_results_to_file(occurrences, output_file, text_to_search)

    if verbose:
        print(f"\nResults saved to {output_file}.\n")

if __name__ == "__main__":
    main()

