import os
import platform
import re
import time
from enum import Enum
from typing import List, Tuple

import music_tag
import requests

from const import SANITIZE, ARTIST, TRACKTITLE, ALBUM, YEAR, DISCNUMBER, TRACKNUMBER, ARTWORK, \
    WINDOWS_SYSTEM


class MusicFormat(str, Enum):
    MP3 = 'mp3',
    OGG = 'ogg',
    

def create_download_directory(download_path: str) -> None:
    os.makedirs(download_path, exist_ok=True)


def wait(seconds: int = 3) -> None:
    """ Pause for a set number of seconds """
    for second in range(seconds)[::-1]:
        print(f'\rWait for {second + 1} second(s)...', end='')
        time.sleep(1)


def split_input(selection) -> List[str]:
    """ Returns a list of inputted strings """
    inputs = []
    if '-' in selection:
        for number in range(int(selection.split('-')[0]), int(selection.split('-')[1]) + 1):
            inputs.append(number)
    else:
        selections = selection.split(',')
        for i in selections:
            inputs.append(i.strip())
    return inputs


def splash() -> None:
    """ Displays splash screen """
    print("""
███████ ███████ ██████   ██████  ████████ ██ ███████ ██    ██
   ███  ██      ██   ██ ██    ██    ██    ██ ██       ██  ██
  ███   ███████ ██████  ██    ██    ██    ██ █████     ████
 ███         ██ ██      ██    ██    ██    ██ ██         ██
███████ ███████ ██       ██████     ██    ██ ██         ██
    """)


def clear() -> None:
    """ Clear the console window """
    if platform.system() == WINDOWS_SYSTEM:
        os.system('cls')
    else:
        os.system('clear')


def sanitize_data(value) -> str:
    """ Returns given string with problematic removed """
    for pattern in SANITIZE:
        value = value.replace(pattern, '')
    return value.replace('|', '-')


def set_audio_tags(filename, artists, name, album_name, release_year, disc_number, track_number) -> None:
    """ sets music_tag metadata """
    tags = music_tag.load_file(filename)
    tags[ARTIST] = conv_artist_format(artists)
    tags[TRACKTITLE] = name
    tags[ALBUM] = album_name
    tags[YEAR] = release_year
    tags[DISCNUMBER] = disc_number
    tags[TRACKNUMBER] = track_number
    tags.save()


def conv_artist_format(artists) -> str:
    """ Returns converted artist format """
    return ', '.join(artists)


def set_music_thumbnail(filename, image_url) -> None:
    """ Downloads cover artwork """
    img = requests.get(image_url).content
    tags = music_tag.load_file(filename)
    tags[ARTWORK] = img
    tags.save()


def regex_input_for_urls(search_input) -> Tuple[str, str, str, str, str, str]:
    """ Since many kinds of search may be passed at the command line, process them all here. """
    track_uri_search = re.search(
        r'^spotify:track:(?P<TrackID>[0-9a-zA-Z]{22})$', search_input)
    track_url_search = re.search(
        r'^(https?://)?open\.spotify\.com/track/(?P<TrackID>[0-9a-zA-Z]{22})(\?si=.+?)?$',
        search_input,
    )

    album_uri_search = re.search(
        r'^spotify:album:(?P<AlbumID>[0-9a-zA-Z]{22})$', search_input)
    album_url_search = re.search(
        r'^(https?://)?open\.spotify\.com/album/(?P<AlbumID>[0-9a-zA-Z]{22})(\?si=.+?)?$',
        search_input,
    )

    playlist_uri_search = re.search(
        r'^spotify:playlist:(?P<PlaylistID>[0-9a-zA-Z]{22})$', search_input)
    playlist_url_search = re.search(
        r'^(https?://)?open\.spotify\.com/playlist/(?P<PlaylistID>[0-9a-zA-Z]{22})(\?si=.+?)?$',
        search_input,
    )

    episode_uri_search = re.search(
        r'^spotify:episode:(?P<EpisodeID>[0-9a-zA-Z]{22})$', search_input)
    episode_url_search = re.search(
        r'^(https?://)?open\.spotify\.com/episode/(?P<EpisodeID>[0-9a-zA-Z]{22})(\?si=.+?)?$',
        search_input,
    )

    show_uri_search = re.search(
        r'^spotify:show:(?P<ShowID>[0-9a-zA-Z]{22})$', search_input)
    show_url_search = re.search(
        r'^(https?://)?open\.spotify\.com/show/(?P<ShowID>[0-9a-zA-Z]{22})(\?si=.+?)?$',
        search_input,
    )

    artist_uri_search = re.search(
        r'^spotify:artist:(?P<ArtistID>[0-9a-zA-Z]{22})$', search_input)
    artist_url_search = re.search(
        r'^(https?://)?open\.spotify\.com/artist/(?P<ArtistID>[0-9a-zA-Z]{22})(\?si=.+?)?$',
        search_input,
    )

    if track_uri_search is not None or track_url_search is not None:
        track_id_str = (track_uri_search
                        if track_uri_search is not None else
                        track_url_search).group('TrackID')
    else:
        track_id_str = None

    if album_uri_search is not None or album_url_search is not None:
        album_id_str = (album_uri_search
                        if album_uri_search is not None else
                        album_url_search).group('AlbumID')
    else:
        album_id_str = None

    if playlist_uri_search is not None or playlist_url_search is not None:
        playlist_id_str = (playlist_uri_search
                           if playlist_uri_search is not None else
                           playlist_url_search).group('PlaylistID')
    else:
        playlist_id_str = None

    if episode_uri_search is not None or episode_url_search is not None:
        episode_id_str = (episode_uri_search
                          if episode_uri_search is not None else
                          episode_url_search).group('EpisodeID')
    else:
        episode_id_str = None

    if show_uri_search is not None or show_url_search is not None:
        show_id_str = (show_uri_search
                       if show_uri_search is not None else
                       show_url_search).group('ShowID')
    else:
        show_id_str = None

    if artist_uri_search is not None or artist_url_search is not None:
        artist_id_str = (artist_uri_search
                         if artist_uri_search is not None else
                         artist_url_search).group('ArtistID')
    else:
        artist_id_str = None

    return track_id_str, album_id_str, playlist_id_str, episode_id_str, show_id_str, artist_id_str
