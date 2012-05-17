pyflacmeta
==========

Pure Python3 FLAC Metadata Reader

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