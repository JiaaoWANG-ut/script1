import os

def read_file(file_path):
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        return None

    with open(file_path, "r") as f:
        lines = f.readlines()
        # remove any leading/trailing whitespaces and newlines
        lines = [line.strip() for line in lines]

        if not lines:
            print(f"File {file_path} has no content.")
            return None

        # create a string containing all lines, separated by a newline character
        data = " ".join(lines)
        return data

file_path = "type_map.raw"
data = read_file(file_path)

if data is not None:
    print(data)
else:
    print("File could not be read.")







import json

data = {
    "_comment": " model parameters",
    "model": {
        "type_map":     ["O", "H"],
        "descriptor" :{
            "type":             "se_e2_a",
            "sel":              [46, 92],
            "rcut_smth":        0.50,
            "rcut":             6.00,
            "neuron":           [25, 50, 100],
            "resnet_dt":        False,
            "axis_neuron":      16,
            "seed":             1,
            "_comment":         " that's all"
        },
        "fitting_net" : {
            "neuron":           [240, 240, 240],
            "resnet_dt":        True,
            "seed":             1,
            "_comment":         " that's all"
        },
        "_comment":     " that's all"
    },

    "learning_rate" :{
        "type":         "exp",
        "decay_steps":  5000,
        "start_lr":     0.001,
        "stop_lr":      3.51e-8,
        "_comment":     "that's all"
    },
    "loss" :{
        "type":         "ener",
        "start_pref_e": 0.02,
        "limit_pref_e": 1,
        "start_pref_f": 1000,
        "limit_pref_f": 1,
        "start_pref_v": 0,
        "limit_pref_v": 0,
        "_comment":     " that's all"
    },

    "training" : {
        "training_data": {
            "systems":          ["."],
            "batch_size":       1,
            "_comment":         "that's all"
        },
        "validation_data":{
            "systems":          ["."],
            "batch_size":       1,
            "numb_btch":        1,
            "_comment":         "that's all"
        },
        "numb_steps":   1000000,
        "seed":         10,
        "disp_file":    "lcurve.out",
        "disp_freq":    100,
        "save_freq":    1000,
        "_comment":     "that's all"
    },

    "_comment":         "that's all"
}

# convert the data to JSON format


type_map_list = lines
data["model"]["type_map"] = type_map_list

sel=96
sel_list=[sel] * len(type_map_list)
data["model"]["descriptor"]["sel"] = sel_list

json_data = json.dumps(data, indent=4)

# print the JSON data
print(json_data)

with open("input.json", "w") as f:
    f.write(json_data)