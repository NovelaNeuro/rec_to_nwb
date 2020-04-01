import inspect

class NameExtractor:

    @staticmethod
    def extract_name(method):
        return inspect.getfullargspec(method)[0]
