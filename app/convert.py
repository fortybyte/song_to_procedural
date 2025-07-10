"""Audio conversion utilities."""

from pydub import AudioSegment
import numpy as np
import json


def audio_to_js_array(input_file: str, frame_ms: int = 100):
    """Return a list of [frequency, duration] pairs for the given audio file."""
    sound = AudioSegment.from_file(input_file).set_channels(1)
    sample_rate = sound.frame_rate
    samples = np.array(sound.get_array_of_samples())
    frame_len = int(sample_rate * frame_ms / 1000)

    frequencies = []
    durations = []

    for start in range(0, len(samples), frame_len):
        frame = samples[start : start + frame_len]
        if len(frame) == 0:
            break
        spectrum = np.abs(np.fft.rfft(frame))
        freq_bins = np.fft.rfftfreq(len(frame), d=1 / sample_rate)
        freq = float(freq_bins[np.argmax(spectrum)])
        if frequencies and abs(freq - frequencies[-1]) < 1.0:
            durations[-1] += frame_ms / 1000
        else:
            frequencies.append(freq)
            durations.append(frame_ms / 1000)

    return [[round(f, 2), round(d, 2)] for f, d in zip(frequencies, durations)]


def convert_to_js(input_file: str, output_file: str) -> None:
    """Write a JavaScript array of frequencies and durations to ``output_file``."""
    data = audio_to_js_array(input_file)
    with open(output_file, "w") as f:
        f.write("export default ")
        json.dump(data, f)
        f.write(";\n")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Convert audio to a compressed JavaScript frequency array"
    )
    parser.add_argument("input", help="Input audio file")
    parser.add_argument("output", help="Output .js file")
    args = parser.parse_args()
    convert_to_js(args.input, args.output)
