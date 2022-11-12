import time
import os
import pytube
import whisper

from typing import Iterator, TextIO

# from whisper.utils import write_srt


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


# write a function for from str timestamp to youtube timestamp
def str_to_youtube_timestamp(time_str):
    time_str = time_str.split(':')
    time_str = [int(i) for i in time_str]
    return time_str[0]*60*60 + time_str[1]*60 + time_str[2]


def write_srt(transcript: Iterator[dict], file: TextIO):
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
# audio = data.streams.get_audio_only()
# save the file with the time stamp
name = video_name + str(time.time())
# audio.download(filename=name)

# download video
video = data.streams.get_highest_resolution()
video.download(filename=name + '.mp4')

model = whisper.load_model("base")
text = model.transcribe(name + '.mp4', fp16=False, verbose=True)

# save str to file
# save VTT
with open(name + '.md', 'w') as srt:
    write_srt(text["segments"], file=srt)

# create a text file and write the output
# with open(name + '.txt', 'w') as f:
#     f.write(text['segments'][0]['text'])

# delete the  file
os.remove(name+'.mp4')
