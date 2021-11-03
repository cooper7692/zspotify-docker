import argparse

from app import client



if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='zspotify',
        description='A Spotify downloader needing only a python interpreter and ffmpeg.')
    parser.add_argument('-ns', '--no-splash',
                        action='store_true',
                        help='Suppress the splash screen when loading.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('urls',
                       type=str,
                       # action='extend',
                       default='',
                       nargs='*',
                       help='Downloads the track, album, playlist, podcast episode, or all albums by an artist from a url. Can take multiple urls.')
    group.add_argument('-ls', '--liked-songs',
                       dest='liked_songs',
                       action='store_true',
                       help='Downloads all the liked songs from your account.')
    group.add_argument('-p', '--playlist',
                       action='store_true',
                       help='Downloads a saved playlist from your account.')
    group.add_argument('-s', '--search',
                       dest='search_spotify',
                       action='store_true',
                       help='Loads search prompt to find then download a specific track, album or playlist')

    parser.set_defaults(func=client)

    args = parser.parse_args()
    args.func(args)
