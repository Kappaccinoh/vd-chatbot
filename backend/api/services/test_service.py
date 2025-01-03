from google.cloud import texttospeech
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/reluvate/Desktop/exercises/vd-chatbot/backend/focal-pager-446702-m9-dd9090f58de4.json"

try:
    print("Initializing Text-to-Speech client...")
    client = texttospeech.TextToSpeechClient()

    print("Preparing synthesis input...")
    synthesis_input = texttospeech.SynthesisInput(text="Hello, Google Cloud!")
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    print("Synthesizing speech...")
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

    print("Writing audio content to file...")
    with open("output.mp3", "wb") as out:
        out.write(response.audio_content)
        print("Audio content written to file 'output.mp3'")

except Exception as e:
    print(f"An error occurred: {e}")
