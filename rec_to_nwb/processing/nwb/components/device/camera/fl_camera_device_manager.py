from rec_to_nwb.processing.nwb.components.device.camera.fl_camera_device_builder import FlCameraDeviceBuilder
from rec_to_nwb.processing.tools.beartype.beartype import beartype
from rec_to_nwb.processing.tools.validate_parameters import validate_parameters_not_none


class FlCameraDeviceManager:

    @beartype
    def __init__(self, metadata: dict):
        self.metadata = metadata

    def get_fl_device_manager(self) -> list:
        return [
            self.__build_single_camera_device(camera_metadata)
            for camera_metadata in self.metadata['cameras']
        ]

    @staticmethod
    def __build_single_camera_device(camera_metadata):
        validate_parameters_not_none(
            __name__,
            camera_metadata.get('id', None),
            camera_metadata.get('meters_per_pixel', None)
        )

        return FlCameraDeviceBuilder.build(
            name=str(camera_metadata['id']),
            meters_per_pixel=float(camera_metadata['meters_per_pixel'])
        )
