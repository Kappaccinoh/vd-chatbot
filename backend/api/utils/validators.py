def validate_audio_file(file):
    allowed_types = [
        'audio/wav', 
        'audio/x-wav', 
        'audio/mp3',
        'audio/webm',
        'audio/webm;codecs=opus'  # Add this for opus codec
    ]
    print(f"Received file type: {file.content_type}")  # Debug print
    if file.content_type not in allowed_types:
        raise ValueError(f'Invalid audio file type: {file.content_type}. Allowed types: {allowed_types}')