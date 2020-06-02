from pynwb import NWBFile

from rec_to_nwb.processing.tools.beartype.beartype import beartype


class DeviceInjector:

    @beartype
    def inject_all_devices(self, nwb_content: NWBFile, devices: list):
        for device in devices:
            self.__inject_device(nwb_content, device)

    @staticmethod
    def __inject_device(nwb_content, device):
        nwb_content.add_device(device)