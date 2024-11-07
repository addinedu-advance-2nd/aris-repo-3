from faster_whisper import WhisperModel

# Whisper 모델 로드 (여기서는 "base" 모델을 사용)
model = WhisperModel("base", device="cpu")

# 변환할 오디오 파일 경로
audio_file = "./audiofiles/output_speech.wav"  # VAD로 처리한 오디오 파일 경로

# 음성 파일을 텍스트로 변환
segments, info = model.transcribe(audio_file, language="ko")

# 변환된 텍스트 출력
print("Transcription:")
#print(result)

for segment in segments:
    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))