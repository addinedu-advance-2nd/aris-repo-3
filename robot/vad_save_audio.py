import webrtcvad
import wave
import numpy as np
import os

# VAD 객체 생성 (모드 1~3, 3이 가장 민감)
vad = webrtcvad.Vad(3)

# WAV 파일을 읽고 음성 구간을 감지합니다
def read_wave(filename):
    with wave.open(filename, 'rb') as wf:
        sample_rate = wf.getframerate()
        frames = wf.readframes(wf.getnframes())
    return sample_rate, frames

def frame_generator(frame_duration_ms, audio, sample_rate):
    frame_size = int(sample_rate * frame_duration_ms / 1000.0 * 2)  # 프레임 크기 계산 (16-bit이므로 *2)
    for i in range(0, len(audio), frame_size):
        frame = audio[i:i+frame_size]
        if len(frame) < frame_size:
            # 패딩을 추가하여 프레임을 원하는 길이로 만듭니다.
            frame += b'\x00' * (frame_size - len(frame))
        yield frame

# 오디오 파일에서 음성 구간 감지
def detect_speech(filename):
    sample_rate, audio = read_wave(filename)
    frames = frame_generator(10, audio, sample_rate)  # 30ms 단위로 분할
    speech_frames = []

    for frame in frames:
        is_speech = vad.is_speech(frame, sample_rate)  # 음성 여부 판별
        if is_speech:
            speech_frames.append(frame)
    
    return speech_frames, sample_rate

# 새로운 오디오 파일로 저장
def save_audio(speech_frames, sample_rate, output_filename):
    with wave.open(output_filename, 'wb') as wf:
        wf.setnchannels(1)  # 모노 채널 (1)
        wf.setsampwidth(2)  # 16비트 샘플 폭
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(speech_frames))  # 음성 프레임들을 합쳐서 저장

# 사용 예시
audio_file = './audiofiles/sample_audio_16000_16bit_3.wav'
speech_frames, sample_rate = detect_speech(audio_file)

# 감지된 음성 구간을 새로운 WAV 파일로 저장
output_file = './audiofiles/output_speech.wav'
save_audio(speech_frames, sample_rate, output_file)

print(f"새로운 오디오 파일이 저장되었습니다: {output_file}")
