pyflacmeta
==========

Pure Python3 FLAC Metadata Reader

Reads tags (vorbis comments) from FLAC files.

Example usage:

::

    >>> import pyflacmeta
    >>> flacfile.keys()
    dict_keys(['album', 'DISCTOTAL', 'artist', 'title', 'tracktotal', 'date', 'tracknumber', 'DISCNUMBER'])
    >>> flacfile['artist']
    'David Bowie'
    >>> flacfile['title']
    'Life on Mars?'
    >>> flacfile.tags()
    {'album': 'Hunky Dory', 'DISCTOTAL': '1', 'artist': 'David Bowie', 'title': 'Life on Mars?', 'tracktotal': '11', 'date': '1971-12', 'tracknumber': '4', 'DISCNUMBER': '1'}
