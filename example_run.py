import json
import pandas as pd
from tortoise import TortoiseExperiment

df = pd.read_csv("example_data.csv")

exp = TortoiseExperiment(
    target_column="failure",
    time_column="time",
    feature_columns=["sensor_a", "sensor_b", "sensor_c"],
    horizons=(1, 3, 7, 23),
    random_state=23,
)

result = exp.run(df)
print(json.dumps(result, indent=2))
