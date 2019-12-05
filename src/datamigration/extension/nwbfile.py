from pynwb import NWBFile


class FLNWBFile(NWBFile):

    def __init__(self, **kwargs):
        super(FLNWBFile, self).__init__(**kwargs)

    def __repr__(self):
        return "COS"

    def __str__(self):
        return 'cos'
