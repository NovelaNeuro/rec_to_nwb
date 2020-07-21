from rec_to_nwb.processing.nwb.components.device.camera.fl_camera_device import FlCameraDevice
from rec_to_nwb.processing.tools.beartype.beartype import beartype


class FlCameraDeviceBuilder:

    @staticmethod
    @beartype
    def build(name: str, meters_per_pixel: float, manufacturer: str, model: str, lens: str, camera_name: str):
        return FlCameraDevice(
            name=name,
            meters_per_pixel=meters_per_pixel,
            manufacturer=manufacturer,
            model=model,
            lens=lens,
            camera_name=camera_name
        )
