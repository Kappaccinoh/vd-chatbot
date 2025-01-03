from google.cloud import speech_v1

class STTService:
    def __init__(self):
        print("Initializing STT Service...")
        self.client = speech_v1.SpeechClient()
    
    def transcribe(self, audio_file):
        try:
            print(f"\nSTT Debug:")
            print(f"Audio file type: {audio_file.content_type}")
            print(f"Audio file size: {audio_file.size} bytes")
            
            # Read the audio content
            content = audio_file.read()
            print(f"Read {len(content)} bytes from file")
            
            # Configure audio and recognition settings
            audio = speech_v1.RecognitionAudio(content=content)
            
            config = speech_v1.RecognitionConfig(
                encoding=speech_v1.RecognitionConfig.AudioEncoding.WEBM_OPUS,  # Changed from LINEAR16
                sample_rate_hertz=48000,  # Common sample rate for web audio
                language_code="en-US",
                enable_automatic_punctuation=True
            )
            
            print("Sending request to Google STT...")
            response = self.client.recognize(config=config, audio=audio)
            print(f"Received response: {response}")
            
            if response.results:
                transcript = response.results[0].alternatives[0].transcript
                confidence = response.results[0].alternatives[0].confidence
                print(f"Transcript: '{transcript}'")
                print(f"Confidence: {confidence}")
                return transcript
            else:
                print("No transcription results returned")
                return ""
                
        except Exception as e:
            print(f"STT Error: {str(e)}")
            print("Full error:")
            import traceback
            traceback.print_exc()
            raise e