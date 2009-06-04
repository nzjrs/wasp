def calculate_dt_seconds(then, now):
    d = now - then
    return d.seconds + d.microseconds / 1000000.0

def has_elapsed_time_passed(then, now, dt):
    ds = calculate_dt_seconds(then, now)
    if ds > dt:
        return now, True, ds
    else:
        return then, False, ds
