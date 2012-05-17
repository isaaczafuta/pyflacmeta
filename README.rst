pyflacmeta
==========

Pure Python3 FLAC Metadata Reader

Reads tags (vorbis comments) from FLAC files.

Example usage:

::

    >>> import pyflacmeta
    >>> flacfile = pyflacmeta.FLAC("test.flac")
    >>> flacfile.keys()
    dict_keys([b'album', b'title', b'tracknumber',...])
    >>> flacfile["album"]
    Tigermilk
    >>> flacfile["artist"]
    Belle and Sebastian