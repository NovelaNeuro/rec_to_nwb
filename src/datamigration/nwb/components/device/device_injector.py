class DeviceInjector:

    def inject_all_devices(self, nwb_content, devices):
        for device in devices:
            self.inject_device(nwb_content, device)

    @staticmethod
    def inject_device(nwb_content, device):
        nwb_content.add_device(device)