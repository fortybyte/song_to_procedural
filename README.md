# Song to Procedural (Game Boy Style)

This project converts any audio file into a highly compressed representation.
The result is a JavaScript array of `[frequency, duration]` pairs that can be
used to recreate the melody procedurally.

## Usage

### Command line

```bash
python convert.py input_song.mp3 output.js
```

### Web app

Install dependencies and run the Flask application:

```bash
pip install -r requirements.txt
python app/app.py
```

Ensure FFmpeg is installed on your system so that pydub can decode various
audio formats.

Open your browser at `http://localhost:5000` to upload a song and download the
generated JavaScript file.
