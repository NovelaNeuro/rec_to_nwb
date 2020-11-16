class FlHeaderDevice:

    def __init__(self, name, global_configuration_dict):
        self.name = name
        for parameter in global_configuration_dict:
            if global_configuration_dict[parameter] is None:
                global_configuration_dict[parameter] = ''
        self.global_configuration = global_configuration_dict

