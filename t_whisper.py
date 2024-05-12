import os

from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

with open("samples/quantile-trick.mp3", "rb") as f:
    transcription = client.audio.transcriptions.create(model="whisper-1", file=f)

if transcription.text:
    with open("out.txt", "w") as f:
        f.write(transcription.text)

print(transcription.text)
