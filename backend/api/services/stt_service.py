from google.cloud import speech_v1

class STTService:
    def __init__(self):
        self.client = speech_v1.SpeechClient()
    
    def transcribe(self, audio_file):
        try:
            # Read the audio content
            content = audio_file.read()
            
            audio = speech_v1.RecognitionAudio(content=content)
            config = speech_v1.RecognitionConfig(
                encoding=speech_v1.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,  # Adjust based on your audio
                language_code="en-US",
                enable_automatic_punctuation=True
            )
            
            response = self.client.recognize(config=config, audio=audio)
            
            if response.results:
                return response.results[0].alternatives[0].transcript
            return ""
            
        except Exception as e:
            print(f"STT Error: {str(e)}")
            raise e