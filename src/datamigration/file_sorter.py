class FileSorter:
    def sort_filenames(self, filenames):
        max_filename_length = len(max(filenames, key=len))
        min_filename_length = len(min(filenames, key=len))
        sorted_files = []
        for i in range(min_filename_length, max_filename_length + 1):
            temp_data = [file for file in filenames if len(file) == i]
            temp_data.sort()
            sorted_files = sorted_files + temp_data
        return sorted_files
