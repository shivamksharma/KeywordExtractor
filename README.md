# Keyword Extractor

This project draws inspiration from the 2007 movie **Live Free or Die Hard** where hackers intercept various communication signals like radio, phone calls, etc., to track down specific names swiftly, such as **Matt Farrell** or **John McClane**.

---

## Overview

The Keyword Extractor is a tool designed to scan and analyze various communication channels for specific keywords or phrases, mimicking the concept seen in the movie. It aims to efficiently parse and extract relevant information containing predefined keywords, allowing quick identification and response.

---

## Features

- **Keyword Monitoring:** Scan audio files or real-time microphone input for specific names or phrases.
- **Real-Time Analysis:** Provides real-time analysis of intercepted communication data.
- **Multiple Keyword Search:** Search for multiple keywords simultaneously.
- **Timestamp Extraction:** Add timestamps to keyword occurrences in audio files.
- **Export Results:** Save results in JSON, CSV, or TXT formats for further analysis.
- **Customizable Filters:** Allows customization of keywords or phrases to monitor.

---

## Installation

To install and run the Keyword Extractor:

1. Clone this repository:
   ```bash
   git clone https://github.com/shivamksharma/KeywordExtractor.git
   cd KeywordExtractor
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

Run the script:
```bash
python main.py
```

### **Modes**
1. **File Analysis Mode**:
   - Enter the path to an audio file.
   - Provide comma-separated keywords to search.
   - Choose the output format (JSON, CSV, or TXT).

2. **Real-Time Processing Mode**:
   - Provide comma-separated keywords to search.
   - The program listens to the microphone and prints detected keywords in real-time.

---

## Example

### File Analysis Mode
```
=== Welcome to Audio Text Analyzer ===

Choose mode: (1) File Analysis, (2) Real-Time Processing: 1
Enter the path of the audio file: example.mp3
Converting audio file to WAV format...
Enter keywords to search (comma-separated): John McClane, Matt Farrell
Enter output format (json/csv/txt): json
Results saved to results.json.
```

### Real-Time Processing Mode
```
=== Welcome to Audio Text Analyzer ===

Choose mode: (1) File Analysis, (2) Real-Time Processing: 2
Enter keywords to search (comma-separated): hello, world
Listening... (Press Ctrl+C to stop)
Found keyword 'hello': Hello, how are you?
Found keyword 'world': Welcome to the world of Python.
```

---

## Output Formats

### JSON (`results.json`)
```json
{
    "John McClane": [
        {
            "text": "John McClane is a hero",
            "start_time": 0.0
        }
    ]
}
```

### CSV (`results.csv`)
```
Keyword,Text,Start Time (s)
John McClane,"John McClane is a hero",0.0
```

### TXT (`results.txt`)
```
Keyword: John McClane
Text: John McClane is a hero
Start Time: 0.0s
```

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

