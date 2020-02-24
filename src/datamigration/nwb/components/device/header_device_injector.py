class HeaderDeviceInjector:

    @staticmethod
    def inject_header_device(nwb_content, header_device):
        nwb_content.add_device(header_device)
