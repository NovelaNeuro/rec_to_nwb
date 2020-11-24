class FileSorter:

    @staticmethod
    def sort_filenames(filenames):
        filenames.sort(key=lambda item: (item, len(item)))
        return filenames
