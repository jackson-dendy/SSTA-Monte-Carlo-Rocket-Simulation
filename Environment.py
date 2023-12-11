from rocketpy import Environment

env = Environment(
    date=(2020, 6, 10, 18),
    latitude=35.3467755,
    longitude=-117.80820,
    elevation=630,
    datum="WGS84",
    max_expected_height=26000
)

env.set_atmospheric_model(
    type="Windy",
    file="GFS"
)

