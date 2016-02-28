# coding: utf-8

import subprocess
import os

import celery
import music21

from models import Song


@celery.task
def write(song_key):
    song = Song.objects.get(key=song_key)

    score = music21.converter.parse(song.song)
    midi = music21.midi.translate.streamToMidiFile(score)

    if not os.path.exists(song.store_path):
        os.makedirs(song.store_path)

    midi.open(song.midi_file, 'wb')
    midi.write()
    midi.close()

    writer_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'writer.sh')
    subprocess.call([writer_script, song.midi_file, song.mp3_file])
