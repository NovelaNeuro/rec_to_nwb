from rec_to_nwb.processing.nwb.components.device.camera.fl_camera_device import FlCameraDevice
from rec_to_nwb.processing.tools.beartype.beartype import beartype


class FlCameraDeviceBuilder:

    @staticmethod
    @beartype
    def build(name: str, meters_per_pixel: float):
        return FlCameraDevice(
            name=name,
            meters_per_pixel=meters_per_pixel
        )
