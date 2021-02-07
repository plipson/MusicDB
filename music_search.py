# -*- coding: utf-8 -*-
"""
    Music Search 
    
    will traverse a folder hierarchy to create artist/album/song directories
    
"""

import os
import sys

'''
    Song
'''
class Song(object):
    # maybe allow both a path & fn, or just a full fn
    def __init__(self, name, record, size = -1):
        self.title = name[:-4]
        self.album = record

    def is_song(name):
        return len(name) > 4 and name[-4:].lower() == '.mp3'
    
    def __str__(self):
        return f'{self.title} \ton:{self.album.title} \tby:{self.album.artist.name}'

    def __repr__(self):
        return f"Song('{self.title}', Album('{self.album.title}', Artist('{self.album.artist.name}')))"

'''
    Album
'''
class Album(object):
    # maybe allow a folder instead
    def __init__(self, name, band):
        self.title = name
        self.artist = band
        self.songs = {}
        
    def add_song(self, name):
        if name in self.songs:
            print(f'WARNING: adding {name} to {self.title} by {self.artist.name} again!')
            return
        self.songs[name] = Song(name, self)
        
    def tracks(self):
        return [song.title for song in self.songs]
      
    def __str__(self):
        return f'{self.title} \tby:{self.artist.name} - {len(self.songs)} songs'

    def __repr__(self):
        return f"Album('{self.title}', Artist('{self.artist.name}'))"

'''
    Artist
'''      
class Artist(object):
    def __init__(self, band):
        self.name = band
        self.albums = {}
        
    def albums(self):
        return [album.title for album in self.albums]
        
    def find_record(self, key):
        if key in self.albums:
            return self.albums[key]
        entry = Album(key, self)
        self.albums[key] = entry
        return entry
    
    def add_song(self, name, album):
        album.add_song(name)
    
    def __str__(self):
        return f'{self.name} has {len(self.albums)} records'

    def __repr__(self):
        return f"Artist('{self.name}')"

'''
    Music DB
'''
class MusicDB(object):
    def __init__(self):
        self.artist_dir = {}
        self.song_list = set()
        
        # NOTE: add some way to collect aliases for a given artist
        #  -- or cross-reference them to multiple bands
        
    def get_key(parts, indx):
        return parts[indx] if len(parts) > -indx else '<unknown>'
        
    def find_artist(self, key):
        if key in self.artist_dir:
            return self.artist_dir[key]
        entry = Artist(key)
        self.artist_dir[key] = entry
        return entry        

    # if any songs are in it, create an album of the folder
    def process(self, folder, files):
        songs = [f for f in files if Song.is_song(f)]
        if len(songs):
            parts = folder.replace('\\','/').split('/')
            band_name = MusicDB.get_key(parts, -2)
            band = self.find_artist(band_name)
            record_name = MusicDB.get_key(parts, -1)
            album = band.find_record(record_name)
            for song in songs:
                band.add_song(song, album)
            
    def __str__(self):
        return f'MusicDB has {len(self.artist_dir)} records'

    def __repr__(self):
        return f"MusicDB()')"
           
    
## TEST
def test(folder):
    ct = 0
    mdb = MusicDB()
    for root,dirs,fnames in os.walk(folder):
        mdb.process(root, fnames)
        ct += 1
        print(f'at {root} are {len(dirs)} dirs and {len(fnames)} files')
        dirs[:] = dirs[:-2]
    print(f'done counted {ct}...')
    return mdb
        
        