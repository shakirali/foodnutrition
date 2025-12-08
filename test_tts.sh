#!/bin/bash
# Test script for TTS endpoint

# Test 1: Basic request
echo "Test 1: Basic TTS request"
curl -X POST "http://localhost:8000/api/tts" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, this is a test of the text to speech endpoint."}' \
  --output test_audio.mp3

echo -e "\n✓ Audio saved to test_audio.mp3"
echo "Play it with: open test_audio.mp3 (macOS) or your audio player"

# Test 2: With custom parameters
echo -e "\nTest 2: TTS with custom parameters"
curl -X POST "http://localhost:8000/api/tts" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "This is a test with custom voice settings.",
    "voice_id": "JBFqnCBsd6RMkjVDRZzb",
    "model_id": "eleven_turbo_v2",
    "output_format": "mp3_44100_128"
  }' \
  --output test_audio_custom.mp3

echo -e "\n✓ Audio saved to test_audio_custom.mp3"

# Test 3: Error case - empty text
echo -e "\nTest 3: Error case - empty text"
curl -X POST "http://localhost:8000/api/tts" \
  -H "Content-Type: application/json" \
  -d '{"text": ""}' \
  -w "\nHTTP Status: %{http_code}\n"

# Test 4: Error case - text too long
echo -e "\nTest 4: Error case - text too long"
curl -X POST "http://localhost:8000/api/tts" \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"$(python3 -c 'print("a" * 5001)')\"}" \
  -w "\nHTTP Status: %{http_code}\n"

