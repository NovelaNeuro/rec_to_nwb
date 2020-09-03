import os


class AssociatedFilesExistanceValidator:

    def __init__(self, associated_files):
        self.associated_files = associated_files

    def files_exist(self):
        for associated_file in self.associated_files:
            if not os.path.isfile(associated_file["path"]):
                return False
        return True
