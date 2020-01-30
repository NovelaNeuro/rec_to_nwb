class DeviceInjector():
    def __init__(self, nwb_content):
        self.nwb_content = nwb_content


    def join_device(self, device):
        self.nwb_content.add_device(device)