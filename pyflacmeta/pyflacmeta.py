import struct


class ReadError(Exception):
    pass


class InvalidFLACError(Exception):
    pass


class MetadataBlock(object):
    def __init__(self, fp):
        self.header = MetadataBlockHeader(fp)
        self.last = self.header.last
        self.type = self.header.type
        size = self.header.size
        self.data = MetadataBlockTypes[self.type](fp, size)


class MetadataBlockHeader(object):
    def __init__(self, fp):
        headersize = 4
        data = fp.read(headersize)
        unpacked = struct.unpack('!I', data)[0]
        self.last = bool(unpacked >> 31)
        self.type = (unpacked >> 24) & 0x7f
        self.size = unpacked & 0xffffff


class MetadataBlockData(object):
    def __init__(self, fp, size):
        data = fp.read(size)


class MetadataBlockStreamInfo(object):
    def __init__(self, fp, size):
        data = fp.read(size)
        fields = struct.unpack('!2HIH2I16B', data)
        self.minblocksize = fields[0]
        self.maxblocksize = fields[1]
        self.minframesize = fields[2] >> 8
        self.maxframesize = (fields[2] & 0xff) + fields[3]
        self.samplerate = fields[4] >> 12
        self.channels = ((fields[4] >> 9) & 0x7) + 1
        self.bitspersample = ((fields[4] >> 4) & 0x1f) + 1
        self.samples = ((fields[4] & 0x0f) << 24) + fields[5]
        md5 = 0
        for md5_byte in fields[6:]:
            md5 = (md5 << 8) + md5_byte
        self.md5 = md5


class MetadataBlockVorbisComment(object):
    def __init__(self, fp, size):
        data = fp.read(size)
        vendor_string_length, = struct.unpack('<I', data[:4])
        vendor_format = '<%ss' % vendor_string_length
        vendor_data = data[4:4 + vendor_string_length]
        self.vendor_string, = struct.unpack(vendor_format, vendor_data)
        metadata_offset = vendor_string_length + 4
        meta_count_data = data[metadata_offset:metadata_offset + 4]
        meta_count, = struct.unpack('<I', meta_count_data)
        self.metadata = {}
        offset = metadata_offset + 4
        for _ in range(meta_count):
            length, = struct.unpack('<I', data[offset:offset + 4])
            value = data[offset + 4:offset + length + 4]
            splittag = value.split(b'=')
            key, value = splittag[0], b'='.join(splittag[1:])
            key = str(key, 'ascii')
            self.metadata[key] = str(value, 'utf-8')
            offset += length + 4


class FLAC(object):
    def __init__(self, filename):
        with open(filename, 'rb') as fp:
            self.read(fp)

    def read(self, fp):
        streammarker = b'fLaC'
        if fp.read(len(streammarker)) != streammarker:
            raise InvalidFLACError
        self.metadatablocks = []
        self.metadatablocks.append(MetadataBlock(fp))
        while not self.metadatablocks[-1].last:
            self.metadatablocks.append(MetadataBlock(fp))

    def _get_vorbis_comment(self):
        for metadatablock in self.metadatablocks:
            if metadatablock.type == 4:
                return metadatablock.data

    def _get_streaminfo(self):
        for metadatablock in self.metadatablocks:
            if metadatablock.type == 0:
                return metadatablock.data

    def streaminfo(self):
        streaminfo = self._get_streaminfo()
        if streaminfo:
            return {
                "minblocksize": streaminfo.minblocksize,
                "maxblocksize": streaminfo.maxblocksize,
                "minframesize": streaminfo.minframesize,
                "maxframesize": streaminfo.maxframesize,
                "samplerate": streaminfo.samplerate,
                "channels": streaminfo.channels,
                "bitspersample": streaminfo.bitspersample,
                "samples": streaminfo.samples,
                "md5": streaminfo.md5
            }
        else:
            return {}

    def __getitem__(self, key):
        vorbiscomment = self._get_vorbis_comment()
        if not vorbiscomment:
            raise KeyError
        try:
            value = vorbiscomment.metadata[key]
        except KeyError:
            value = vorbiscomment.metadata[key.lower()]
        return value

    def keys(self):
        tags = self.tags()
        if not tags:
            return None
        return tags.keys()

    def tags(self):
        vorbiscomment = self._get_vorbis_comment()
        if not vorbiscomment:
            return None
        return vorbiscomment.metadata

MetadataBlockTypes = {
    0: MetadataBlockStreamInfo,
    1: MetadataBlockData,
    2: MetadataBlockData,
    3: MetadataBlockData,
    4: MetadataBlockVorbisComment,
    5: MetadataBlockData,
    6: MetadataBlockData
}
