class FileSorter:
    def sort_filenames(self, filenames):
        max_filename_length = len(filenames[0])
        min_filename_length = len(filenames[0])
        for filename in filenames:
            if len(filename) > max_filename_length:
                max_filename_length = len(filename)
            elif len(filename) < min_filename_length:
                min_filename_length = len(filename)

        sorted_files = []
        for i in range(min_filename_length, max_filename_length):
            temp_data = []
            for filename in filenames:
                if len(filename) == i:
                    temp_data.append(filename)
            temp_data.sort()
            sorted_files = sorted_files + temp_data
        return sorted_files
