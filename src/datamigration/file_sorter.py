class FileSorter:
    def sort_filenames(self, filenames):
        filenames.sort(key=lambda item: (len(item), item))
        return filenames
