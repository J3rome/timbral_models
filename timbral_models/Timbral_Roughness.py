from __future__ import division
import numpy as np
import soundfile as sf
from . import timbral_util


def plomp(f1, f2):
    b1 = 3.51
    b2 = 5.75
    xstar = 0.24
    s1 = 0.0207
    s2 = 18.96
    s = np.tril(xstar / ((s1 * np.minimum(f1, f2)) + s2))
    pd = np.exp(-b1 * s * np.abs(f2 - f1)) - np.exp(-b2 * s * np.abs(f2 - f1))
    return pd


def timbral_roughness(fname, dev_output=False, phase_correction=False):
    """
     This function is an implementation of the Vassilakis [2007] model of roughness.
     The peak picking algorithm implemented is based on the MIR toolbox's implementation.

     Version 0.2


     Vassilakis, P. 'SRA: A Aeb-based researh tool for spectral and roughness analysis of sound signals', Proceedings
     of the 4th Sound and Music Computing Conference, Lefkada, Greece, July, 2007.

    Required parameter
    :param fname:                   Audio filename to be analysed, including full file path and extension.

    Optional parameters
    :param dev_output:              Bool, when False return the roughness, when True return all extracted features
                                    (current none).
    :param phase_correction:        If the inter-channel phase should be estimated when performing a mono sum.
                                    Defaults to False.

    :return:        Roughness of the audio signal.

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

    audio_samples /= np.max(np.abs(audio_samples))


    # reshape audio
    audio_len = len(audio_samples)
    time_step = 0.05
    step_samples = int(fs * time_step)
    nfft = step_samples
    window = np.hamming(nfft + 2)
    window = window[1:-1]
    olap = nfft / 2
    num_frames = int((audio_len)/(step_samples-olap))
    next_pow_2 = np.log(step_samples) / np.log(2)
    next_pow_2 = 2 ** int(next_pow_2 + 1)

    reshaped_audio = np.zeros([next_pow_2, num_frames])

    i = 0
    start_idx = int((i * (nfft / 2.0)))

    # get all the audio
    while start_idx+step_samples <= audio_len:
        audio_frame = audio_samples[start_idx:start_idx+step_samples]

        # apply window
        audio_frame = audio_frame * window

        # append zeros
        reshaped_audio[:step_samples, i] = audio_frame

        # increase the step
        i += 1
        start_idx = int((i * (nfft / 2.0)))

    spec = np.fft.fft(reshaped_audio, axis=0)
    spec_len = int(next_pow_2/2) + 1
    spec = spec[:spec_len, :]
    spec = np.absolute(spec)

    freq = fs/2 * np.linspace(0, 1, spec_len)

    # normalise
    norm_spec = (spec - np.min(spec)) / (np.max(spec) - np.min(spec))

    ''' Peak picking algorithm '''
    cthr = 0.01  # threshold for peak picking

    _, no_segments = np.shape(spec)

    allpeakpos = []
    allpeaklevel = []
    allpeaktime = []

    for i in range(0, no_segments):
        d = norm_spec[:, i]
        d_un = spec[:, i]

        # find peak candidates
        peak_pos, peak_level, peak_x = timbral_util.detect_peaks(d, cthr=cthr, unprocessed_array=d_un, freq=freq)

        allpeakpos.append(peak_pos)
        allpeaklevel.append(peak_level)
        allpeaktime.append(peak_x)

    ''' get the roughness '''
    allroughness = []
    # for each frame
    for frame in range(len(allpeaklevel)):
        frame_freq = allpeaktime[frame]
        frame_level = allpeaklevel[frame]

        if len(frame_freq) > 1:
            f2 = np.kron(np.ones([len(frame_freq), 1]), frame_freq)
            f1 = f2.T
            v2 = np.kron(np.ones([len(frame_level), 1]), frame_level)
            v1 = v2.T

            X = v1 * v2
            Y = (2 * v2) / (v1 + v2)
            Z = plomp(f1, f2)
            rough = (X ** 0.1) * (0.5 * (Y ** 3.11)) * Z

            allroughness.append(np.sum(rough))
        else:
            allroughness.append(0)

    mean_roughness = np.mean(allroughness)

    if dev_output:
        return [mean_roughness]
    else:
        return mean_roughness


