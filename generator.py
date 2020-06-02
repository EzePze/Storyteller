#!/usr/bin/env python3
import os
import fire
import json
import numpy as np
import tensorflow as tf

import model
import sample
import encoder
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

# Ensures that the entire script can be used as a library instead of a standalone program


def interact_model(
    custom,
    raw_text,
    model_name='124M',
    seed=None,
    nsamples=1,
    batch_size=1,
    length=None,
    temperature=1,
    top_k=40,
    top_p=1,
    models_dir='models',
):

    # ====================================== PARAMETERS ====================================
    # model_name : String, which model to use

    # seed : Integer seed for random number generators

    # nsamples : Number of samples to return total

    # batch_size : Number of batches (only affects speed/memory).  Must divide nsamples.

    # length : Number of tokens in generated text, if None (default), is determined by model hyperparameters

    # temperature : Float value controlling randomness in boltzmann distribution. Lower temperature results in less random completions. As the temperature approaches zero, the model will become deterministic and repetitive. Higher temperature results in more random completions.

    # top_k : Integer value controlling diversity. 1 means only 1 word is considered for each step (token), resulting in deterministic completions, while 40 means 40 words are considered at each step. 0 (default) is a special setting meaning no restrictions. 40 generally is a good value.

    # models_dir : path to parent folder containing model subfolders (i.e. contains the <model_name> folder)
    # ======================================================================================

    # Does not need to take in custom prompt if the user didn't choose 'custom' in main
    if not custom:
        print('\nGenerating text with prompt:\n\n "%s"\n\n\n' % (raw_text))

    # Finds the directory that contains the models to be used, depending on the complexity the user has chosen
    models_dir = os.path.expanduser(os.path.expandvars(models_dir))

    # batch_size affects the speed and memory use in token generation, no need for user to interact or change it
    if batch_size is None:
        batch_size = 1
    assert nsamples % batch_size == 0

    # Get the encoder for the chosen model and initialise hyper-parameters
    enc = encoder.get_encoder(model_name, models_dir)
    hparams = model.default_hparams()
    with open(os.path.join(models_dir, model_name, 'hparams.json')) as f:
        hparams.override_from_dict(json.load(f))

    # Determines the number of tokens in the generated text. By default, it is determined by the hyper-parameters
    if length is None:
        length = hparams.n_ctx // 2
    elif length > hparams.n_ctx:
        raise ValueError(
            "Can't get samples longer than window size: %s" % hparams.n_ctx)

    # Initialise the tensorflow session graph; a method of representing the computations of the model as a dataflow gragh
    with tf.Session(graph=tf.Graph()) as sess:

        # Create the placeholder to hold the context tokens once generated
        context = tf.placeholder(tf.int32, [batch_size, None])

        # Randomise the seed
        np.random.seed(seed)
        tf.set_random_seed(seed)

        # Define the sequence to be used for the output, based on the parameters either defined by the user or by the default settings
        output = sample.sample_sequence(
            hparams=hparams, length=length,
            context=context,
            batch_size=batch_size,
            temperature=temperature, top_k=top_k, top_p=top_p
        )

        # Not really necessary for this major, but this allows the model to save where it was up to in the training process and return to it later
        saver = tf.train.Saver()
        ckpt = tf.train.latest_checkpoint(os.path.join(models_dir, model_name))
        saver.restore(sess, ckpt)

        # If the user chose custom input, prompt them
        if custom:
            custom_text = input("\nModel prompt >>> ")
            while not custom_text:
                print('Prompt should not be empty!')
                custom_text = input("\nModel prompt >>> ")
            raw_text += ' ' + custom_text
            print('Generating text with prompt:\n\n "%s"\n\n\n' % (custom_text))

        # Using the encoder, generate context tokens. This is one of the factors that causes the software to take so long
        context_tokens = enc.encode(raw_text)

        # Using the context tokens, generate text sequentially using the tensorflow session graph
        generated = 0
        for _ in range(nsamples // batch_size):
            out = sess.run(output, feed_dict={
                context: [context_tokens for _ in range(batch_size)]
            })[:, len(context_tokens):]
            for i in range(batch_size):
                generated += 1
                text = enc.decode(out[i])
                print("=" * 80)
                print(text)
        print("=" * 80)


# Allows the script to be used on its own; does not need to be used by main.py
if __name__ == '__main__':
    fire.Fire(interact_model)
