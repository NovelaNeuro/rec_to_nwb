class ElectrodesHeaderExtensionCreator:
    @staticmethod
    def create_electrodes_header_extension(header):
        hw_chan = []
        for spike_n_trode in header.configuration.spike_configuration.spike_n_trodes:
            for spike_channel in spike_n_trode.spike_channels:
                hw_chan.append(spike_channel.hw_chan)
        return hw_chan
