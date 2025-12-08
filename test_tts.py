#!/usr/bin/env python3
"""Test script for TTS endpoint."""
import requests
import json
from pathlib import Path

BASE_URL = "http://localhost:8000"
TTS_ENDPOINT = f"{BASE_URL}/api/tts"

def test_basic_tts():
    """Test basic TTS conversion."""
    print("Test 1: Basic TTS request")
    response = requests.post(
        TTS_ENDPOINT,
        json={"text": "Hello, this is a test of the text to speech endpoint."}
    )
    
    if response.status_code == 200:
        # Save audio file
        output_file = Path("test_audio.mp3")
        output_file.write_bytes(response.content)
        print(f"✓ Success! Audio saved to {output_file}")
        print(f"  Content-Type: {response.headers.get('Content-Type')}")
        print(f"  Content-Length: {len(response.content)} bytes")
    else:
        print(f"✗ Failed with status {response.status_code}")
        print(f"  Response: {response.text}")

def test_custom_parameters():
    """Test TTS with custom parameters."""
    print("\nTest 2: TTS with custom parameters")
    response = requests.post(
        TTS_ENDPOINT,
        json={
            "text": "This is a test with custom voice settings.",
            "voice_id": "JBFqnCBsd6RMkjVDRZzb",
            "model_id": "eleven_turbo_v2",
            "output_format": "mp3_44100_128"
        }
    )
    
    if response.status_code == 200:
        output_file = Path("test_audio_custom.mp3")
        output_file.write_bytes(response.content)
        print(f"✓ Success! Audio saved to {output_file}")
    else:
        print(f"✗ Failed with status {response.status_code}")
        print(f"  Response: {response.text}")

def test_error_cases():
    """Test error handling."""
    print("\nTest 3: Error case - empty text")
    response = requests.post(
        TTS_ENDPOINT,
        json={"text": ""}
    )
    print(f"  Status: {response.status_code}")
    print(f"  Response: {response.json()}")
    
    print("\nTest 4: Error case - text too long")
    long_text = "a" * 5001
    response = requests.post(
        TTS_ENDPOINT,
        json={"text": long_text}
    )
    print(f"  Status: {response.status_code}")
    print(f"  Response: {response.json()}")

def test_health_check():
    """Test health endpoint."""
    print("\nTest 5: Health check")
    response = requests.get(f"{BASE_URL}/api/health")
    print(f"  Status: {response.status_code}")
    print(f"  Response: {json.dumps(response.json(), indent=2)}")

if __name__ == "__main__":
    print("=" * 50)
    print("TTS Endpoint Testing")
    print("=" * 50)
    
    try:
        # Check if server is running
        health_response = requests.get(f"{BASE_URL}/api/health", timeout=2)
        if health_response.status_code != 200:
            print("⚠ Server might not be running properly")
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to server!")
        print("  Make sure the server is running:")
        print("  python web/run_server.py")
        exit(1)
    
    # Run tests
    test_basic_tts()
    test_custom_parameters()
    test_error_cases()
    test_health_check()
    
    print("\n" + "=" * 50)
    print("Testing complete!")
    print("=" * 50)

