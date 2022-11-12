import time
import os
import pytube
import whisper
from typing import Iterator, TextIO


def srt_format_timestamp(seconds: float):
    assert seconds >= 0, "non-negative timestamp expected"
    milliseconds = round(seconds * 1000.0)

    hours = milliseconds // 3_600_000
    milliseconds -= hours * 3_600_000

    minutes = milliseconds // 60_000
    milliseconds -= minutes * 60_000

    seconds = milliseconds // 1_000
    milliseconds -= seconds * 1_000

    return f"{hours}:" + f"{minutes:02d}:{seconds:02d},{milliseconds:03d}"


def write_md(transcript: Iterator[dict], file: TextIO):
    for segment in transcript:
        print(
            f"- [ {{{{youtube-timestamp {(srt_format_timestamp(segment['start']))}}}}} --> {{{{youtube-timestamp {srt_format_timestamp(segment['end'])}}}}} ]   "
            f"{segment['text'].replace('-->', '->').strip()}\n",
            file=file,
            flush=True,
        )


video = 'https://www.youtube.com/watch?v=Og-ah5UIeHY&t=1385'
data = pytube.YouTube(video)

# get the name of the video
video_name = data.title

# Converting and downloading as 'MP4' file
name = video_name + str(time.time())

# download video
video = data.streams.get_highest_resolution()
video.download(filename=name + '.mp4')

model = whisper.load_model("base")
text = model.transcribe(name + '.mp4', fp16=False, verbose=True)

# save md file
with open(name + '.md', 'w') as srt:
    write_md(text["segments"], file=srt)

# delete the  file
os.remove(name + '.mp4')
