import json
import os

def store_jyhq_GD(data, year, path):
    out = os.path.join(path, f"jyhq_{year}_GD.json")
    with open(out, "w") as outfile:
        json.dump(data, outfile)
    print("file saved in " + out + "!")