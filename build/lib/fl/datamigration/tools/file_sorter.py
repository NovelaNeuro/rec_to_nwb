class FileSorter:

    @staticmethod
    def sort_filenames(filenames):
        filenames.sort(key=lambda item: (len(item), item))
        return filenames
