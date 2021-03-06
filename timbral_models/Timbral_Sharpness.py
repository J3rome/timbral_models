from __future__ import division
import numpy as np
import soundfile as sf
from . import timbral_util


def sharpness_Fastl(loudspec):
    """
      Calculates the sharpness based on FASTL (1991)
      Expression for weighting function obtained by fitting an
      equation to data given in 'Psychoacoustics: Facts and Models'
      using MATLAB basic fitting function
      Original Matlab code by Claire Churchill Sep 2004
      Transcoded by Andy Pearce 2018
    """
    n = len(loudspec)
    gz = np.ones(140)
    z = np.arange(141,n+1)
    gzz = 0.00012 * (z/10.0) ** 4 - 0.0056 * (z/10.0) ** 3 + 0.1 * (z/10.0) ** 2 -0.81 * (z/10.0) + 3.5
    gz = np.concatenate((gz, gzz))
    z = np.arange(0.1, n/10.0+0.1, 0.1)

    sharp = 0.11 * np.sum(loudspec * gz * z * 0.1) / np.sum(loudspec * 0.1)
    return sharp


def timbral_sharpness(fname, dev_output=False, phase_correction=False):
    """
     This is an implementation of the matlab sharpness function found at:
     https://www.salford.ac.uk/research/sirc/research-groups/acoustics/psychoacoustics/sound-quality-making-products-sound-better/accordion/sound-quality-testing/matlab-codes

     This function calculates the apparent Sharpness of an audio file.

     Version 0.2

     Originally coded by Claire Churchill Sep 2004
     Transcoded by Andy Pearce 2018

     Required parameter
    :param fname:                   Audio filename to be analysed, including full file path and extension.

    Optional parameters
    :param dev_output:              Bool, when False return the warmth, when True return all extracted features (currently none)
    :param phase_correction:        If the inter-channel phase should be estimated when performing a mono sum.
                                    Defaults to False.

    :return                         Apparent sharpness of the audio file.


    Copyright 2018 Andy Pearce

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

    """

    # use pysoundfile to read audio
    audio_samples, fs = sf.read(fname, always_2d=False)
    audio_samples = timbral_util.channel_reduction(audio_samples, phase_correction=phase_correction)

    # normalise audio
    audio_samples /= max(abs(audio_samples))

    # calculate the specific loudness
    N_entire, N_single = timbral_util.specific_loudness(audio_samples, Pref=100.0, fs=fs, Mod=0)

    # estimate sharpness
    sharpness = sharpness_Fastl(N_single)

    return sharpness
