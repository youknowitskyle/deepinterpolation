import os
from deepinterpolation.generic import JsonSaver, ClassLoader
import pathlib

generator_param = {}
inferrence_param = {}

# We are reusing the data generator for training here.
generator_param["type"] = "generator"
generator_param["name"] = "SingleTifGenerator"
generator_param["pre_post_frame"] = 30
generator_param["pre_post_omission"] = 0
generator_param[
    "steps_per_epoch"
] = -1  # No steps necessary for inference as epochs are not relevant. -1 deactivate it.

generator_param["train_path"] = os.path.join(
    pathlib.Path(__file__).parent.absolute(),
    "..",
    "test",
    "combine.tif",
)

generator_param["batch_size"] = 5
generator_param["start_frame"] = 0
generator_param["end_frame"] = -1  # -1 to go until the end.
generator_param[
    "randomize"
] = 0  # This is important to keep the order and avoid the randomization used during training


inferrence_param["type"] = "inferrence"
inferrence_param["name"] = "core_inferrence"

# Replace this path to where you stored your model
inferrence_param[
    "model_path"
] = "ENTER PATH HERE"

# Replace this path to where you want to store your output file
inferrence_param[
    "output_file"
] = "/content/deepinterpolation/test/ophys_tiny_continuous_deep_interpolation.h5"

jobdir = "/content/deepinterpolation/test"

try:
    os.mkdir(jobdir)
except:
    print("folder already exists")

path_generator = os.path.join(jobdir, "generator.json")
json_obj = JsonSaver(generator_param)
json_obj.save_json(path_generator)

path_infer = os.path.join(jobdir, "inferrence.json")
json_obj = JsonSaver(inferrence_param)
json_obj.save_json(path_infer)

generator_obj = ClassLoader(path_generator)
data_generator = generator_obj.find_and_build()(path_generator)

inferrence_obj = ClassLoader(path_infer)
inferrence_class = inferrence_obj.find_and_build()(path_infer, data_generator)

# Except this to be slow on a laptop without GPU. Inference needs parallelization to be effective.
inferrence_class.run()
