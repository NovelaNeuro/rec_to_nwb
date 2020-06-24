from rec_to_nwb.processing.tools.beartype.beartype import beartype


def get_times_period_multiplier(metadata):
    times_period_multiplier = metadata.get('times_period_multiplier', '1.5')
    return return_validated_period(times_period_multiplier)


@beartype
def return_validated_period(period: (int, float, str)) -> float:
    return float(period)
