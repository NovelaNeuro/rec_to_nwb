from datetime import datetime

from dateutil.tz import tzlocal

from src.datamigration.nwb_file_creator import NWBFileCreator

nwb_builder = NWBFileCreator('John the experimenter',
                             'novela lab', 'novela institution',
                             'our novela experiment',
                             'description of the novela session',
                             datetime(2019, 10, 31, tzinfo=tzlocal()),
                             'some novela indentifier'
                             )
nwb_builder.build()
