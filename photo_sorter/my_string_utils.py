#-----------------------------------------------------------------------------# 
def xp_decode(t):
    """
    Takes a exif XPKeywords tag and decodes it to a text string
    """
    b = bytes(t)
    return b[:-2].decode('utf-16-le')

#-----------------------------------------------------------------------------#
def xp_encode(s):
    """
    Takes a text string and encodes it as an exif XPKeywords tag
    """
    b = s.encode('utf-16-le') + b'\x00\x00'
    return tuple([int(i) for i in b])