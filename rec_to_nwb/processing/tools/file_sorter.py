
class FileSorter:
    @staticmethod
    def sort_filenames(filenames):
        # Check if these are mda files
        # There can be a log file along with mda files, so check whether any file is an mda file
        filenames_mda = [i for i in filenames if '.mda' in i]
        if len(filenames_mda) > 0: # if at least one mda file
            # sort by length first because the ntrode numbers are 1,2,.., 10, ...
            filenames.sort(key=lambda item: (len(item), item))
        else:
            filenames.sort(key=lambda item: (item, len(item)))
        #print('IN FILESORTER') ##########
        #print('filenames:', filenames) ##############
        return filenames
