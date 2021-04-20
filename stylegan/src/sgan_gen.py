# Copyright (c) 2019, NVIDIA CORPORATION. All rights reserved.
#
# This work is licensed under the Creative Commons Attribution-NonCommercial
# 4.0 International License. To view a copy of this license, visit
# http://creativecommons.org/licenses/by-nc/4.0/ or send a letter to
# Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.

"""Minimal script for generating an image using pre-trained StyleGAN generator."""

import os
import pickle
import numpy as np
import PIL.Image
import dnnlib.tflib as tflib
import config
import glob
import random
import time
import gc
import redis
import io

MODEL = os.environ['MODEL']

def load_Gs(filepath):
    # Load pre-trained network.
    model_file = glob.glob(filepath)
    if len(model_file) == 1:
        model_file = open(model_file[0], "rb")
    else:
        raise Exception('Failed to find the model')
    _G, _D, Gs = pickle.load(model_file)
    # Print network details.
    #Gs.print_layers()
    model_file.close()
    return Gs

def main():
    # Initialize TensorFlow.
    tflib.init_tf()
    print(MODEL)
    # Subscribe to the Redis queue
    r = redis.Redis(host='redis', port=6379, db=0)
    p = r.pubsub(ignore_subscribe_messages=True)
    p.subscribe('stylegan-request')

    while True:
        #Get a message from the queue
        message = p.get_message()
        print(message)
        if(message):
            seed = random.randint(0,10000)
            # Generate Image   
            Gs = load_Gs(MODEL)
            rnd = np.random.RandomState(seed)
            latents = rnd.randn(1, Gs.input_shape[1])
            fmt = dict(func=tflib.convert_images_to_uint8, nchw_to_nhwc=True)
            print('\n * Generating...'*6)
            images = Gs.run(latents, None, truncation_psi=0.5, randomize_noise=True, output_transform=fmt)
            print('\n * Done'*10)
            
            # Save image.
            with io.BytesIO() as photos:
                PIL.Image.fromarray(images[0], 'RGB').save(photos, 'PNG')
                contents = photos.getvalue()
                r.publish('stylegan-photos', contents)

            #free memory
            del Gs
            del rnd
            del latents
            del images
            gc.collect()

        time.sleep(10)
        


if __name__ == "__main__":
    main()
