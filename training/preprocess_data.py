import json
import pandas as pd
import numpy as np

N_KPTS = 133
N_FRAMES = 60

print("Loading files...")
with open('data/2Dto3D_train_part1.json', 'r') as file:
    data1 = json.load(file)

with open('data/2Dto3D_train_part2.json', 'r') as file:
    data2 = json.load(file)

with open('data/2Dto3D_train_part3.json', 'r') as file:
    data3 = json.load(file)

with open('data/2Dto3D_train_part4.json', 'r') as file:
    data4 = json.load(file)

with open('data/2Dto3D_train_part5.json', 'r') as file:
    data5 = json.load(file)

def preprocess_data(value, split="input"):
    input, output = value['keypoints_2d'], value['keypoints_3d']
    res = [0] * N_KPTS
    
    if split == "input":
        for i in range(N_KPTS):
            res[i] = [input[str(i)]['x'], input[str(i)]['y']]
    else:
        for i in range(N_KPTS):
            res[i] = [output[str(i)]['x'], output[str(i)]['y'], output[str(i)]['z']]

    return res

print("Creating train and test splits...")
train_dict = data1.copy()
train_dict.update(data2)
train_dict.update(data3)
train_dict.update(data4)

train = list(train_dict.values())
test = list(data5.values())

print("Separating train dataset into input and output...")
train_input = [preprocess_data(x, split="input") for x in train]
train_output = [preprocess_data(x, split="output") for x in train]

print("Separating test dataset into input and output...")
test_input = [preprocess_data(x, split="input") for x in test]
test_output = [preprocess_data(x, split="output") for x in test]

print(f"Splitting into sets of {N_FRAMES}")
num_full_chunks = (len(train_input) // 60) * 60
trimmed = train[:num_full_chunks]
train_input = [trimmed[i:i + 60] for i in range(0, len(trimmed), 60)]

num_full_chunks = (len(train_output) // 60) * 60
trimmed = train[:num_full_chunks]
train_output = [trimmed[i:i + 60] for i in range(0, len(trimmed), 60)]

num_full_chunks = (len(test_input) // 60) * 60
trimmed = train[:num_full_chunks]
test_input = [trimmed[i:i + 60] for i in range(0, len(trimmed), 60)]

num_full_chunks = (len(test_output) // 60) * 60
trimmed = train[:num_full_chunks]
test_output = [trimmed[i:i + 60] for i in range(0, len(trimmed), 60)]

print("Build dataframes...")
train_df = pd.DataFrame({
    'Input': train_input,
    'Output': train_output
})

test_df = pd.DataFrame({
    'Input': test_input,
    'Output': test_output
})

print("Save CSVs...")
train_df.to_csv('data/train.csv', index=False)
test_df.to_csv('data/test.csv', index=False)