def validate_audio_file(file):
    allowed_types = ['audio/wav', 'audio/x-wav', 'audio/mp3']
    if file.content_type not in allowed_types:
        raise ValueError('Invalid audio file type')