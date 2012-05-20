pyflacmeta
==========

Pure Python3 FLAC Metadata Reader

Reads tags (vorbis comments) from FLAC files.

Example usage:

::

    >>> import pyflacmeta
    >>> flacfile = pyflacmeta.FLAC("test.flac")
    >>> flacfile.keys()
    dict_keys(['album', 'artist', 'title', ...])
    >>> flacfile['artist']
    'David Bowie'
    >>> flacfile['title']
    'Life on Mars?'
    >>> flacfile.tags()
    {'album': 'Hunky Dory', 'artist': 'David Bowie', 'title': 'Life on Mars?',...}
