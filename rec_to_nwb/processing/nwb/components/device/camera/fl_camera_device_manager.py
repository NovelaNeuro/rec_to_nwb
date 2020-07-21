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
            camera_metadata.get('meters_per_pixel', None),
            camera_metadata.get('manufacturer', None),
            camera_metadata.get('model', None),
            camera_metadata.get('lens', None),
            camera_metadata.get('camera_name', None)
        )

        return FlCameraDeviceBuilder.build(
            name='camera_device ' + str(camera_metadata['id']),
            meters_per_pixel=float(camera_metadata['meters_per_pixel']),
            manufacturer=str(camera_metadata['manufacturer']),
            model=str(camera_metadata['model']),
            lens=str(camera_metadata['lens']),
            camera_name=str(camera_metadata['camera_name'])
        )
