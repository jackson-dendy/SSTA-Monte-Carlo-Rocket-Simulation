import numpy as np

def cf(from_unit, to_unit):
    """Returns the conversion factor from one unit to another."""
    units_conversion_dict = {
        # Units of length. Meter "m" is the base unit.
        "mm": 1e3,
        "cm": 1e2,
        "dm": 1e1,
        "m": 1,
        "dam": 1e-1,
        "hm": 1e-2,
        "km": 1e-3,
        "ft": 1 / 0.3048,
        "in": 1 / 0.0254,
        "mi": 1 / 1609.344,
        "nmi": 1 / 1852,
        "yd": 1 / 0.9144,
        # Units of velocity. Meter per second "m/s" is the base unit.
        "m/s": 1,
        "km/h": 3.6,
        "knot": 1.9438444924406047,
        "mph": 2.2369362920544023,
        "ft/s": 1 / 0.3048,
        # Units of acceleration. Meter per square second "m/s^2" is the base unit.
        "m/s^2": 1,
        "grav": 1 / 9.80665,
        "ft/s^2": 1 / 3.2808399,
        # Units of pressure. Pascal "Pa" is the base unit.
        "Pa": 1,
        "hPa": 1e-2,
        "kPa": 1e-3,
        "MPa": 1e-6,
        "bar": 1e-5,
        "atm": 1.01325e-5,
        "mmHg": 1 / 133.322,
        "inHg": 1 / 3386.389,
        # Units of time. Seconds "s" is the base unit.
        "s": 1,
        "min": 1 / 60,
        "h": 1 / 3600,
        "d": 1 / 86400,
        # Units of mass. Kilogram "kg" is the base unit.
        "mg": 1e-6,
        "g": 1e-3,
        "kg": 1,
        "lb": 2.20462,
        # Units of angle. Radian "rad" is the base unit.
        "rad": 1,
        "deg": 1 / 180 * np.pi,
        "grad": 1 / 200 * np.pi,
    }
    try:
        incoming_factor = units_conversion_dict[to_unit]
    except KeyError:
        raise ValueError(f"Unit {to_unit} is not supported.")
    try:
        outgoing_factor = units_conversion_dict[from_unit]
    except KeyError:
        raise ValueError(f"Unit {from_unit} is not supported.")

    return incoming_factor / outgoing_factor