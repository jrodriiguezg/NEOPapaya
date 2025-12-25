#!/usr/bin/env python3
import wave
import struct
import math
import sys
import os

def analyze_wav(filename):
    if not os.path.exists(filename):
        print(f"File not found: {filename}")
        return

    print(f"--- Analyzing {filename} ---")
    try:
        with wave.open(filename, 'rb') as wf:
            channels = wf.getnchannels()
            width = wf.getsampwidth()
            rate = wf.getframerate()
            frames = wf.getnframes()
            duration = frames / float(rate)
            
            print(f"Format: {rate}Hz, {channels}ch, {width*8}bit")
            print(f"Duration: {duration:.2f}s")
            
            raw_data = wf.readframes(frames)
            
            if width == 2:
                fmt = f"{frames * channels}h"
            else:
                print("Only 16-bit supported for analysis")
                return

            samples = struct.unpack(fmt, raw_data)
            
            # 1. Max Amplitude
            max_amp = max(abs(s) for s in samples)
            print(f"Max Amplitude: {max_amp} / 32767")
            
            # 2. RMS Amplitude (Volume)
            sum_squares = sum(s**2 for s in samples)
            rms = math.sqrt(sum_squares / len(samples))
            print(f"RMS Amplitude: {rms:.2f}")
            
            # 3. Simple Silence Check
            if max_amp == 0:
                print("RESULT: DIGITAL SILENCE (Mic not working or muted)")
            elif rms < 100:
                print("RESULT: EXTREMELY QUIET (Mic gain too low)")
            elif rms < 500:
                print("RESULT: QUIET (Might need boost)")
            else:
                print("RESULT: SIGNAL DETECTED (Likely valid audio or loud noise)")
                
    except Exception as e:
        print(f"Error analyzing file: {e}")

if __name__ == "__main__":
    target = "debug_last_audio.wav"
    if len(sys.argv) > 1:
        target = sys.argv[1]
    
    analyze_wav(target)
