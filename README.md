## AudioCommons Timbral Models
This work is part of the [AudioCommons project](https://www.audiocommons.org).
This distribution contains Python scripts developed for extracting timbral attributes of audio files.

More detailed explanations of how the models function can be found in Deliverable D5.6: Second prototype of timbral characterisation tools for semantically annotating non-musical content, available: http://www.audiocommons.org/materials/


## Installing the package
The timbral_models package can be installed using the pip command.  This will handle most dependencies.
```
pip install timbral_models
```
Note that during test installing the package with only basic python installed, an error occurred when installing dependencies.  This can be overcome by first installing numpy, followed by timbral_models.
```
pip install numpy
pip install timbral_models
```

Additionally, the code requires the use of the Essentia library.  Documentation for the installation of Essentia can be found at (http://essentia.upf.edu/documentation/installing.html).  


## Dependencies
The script can also be downloaded manually from the github repository (https://github.com/AudioCommons/timbral_models).  If doing this, dependencies will need to be manually installed.  The timbral models rely on several other easily accessible python packages: `numpy`, `soundfile`, `librosa`, `sklearn`, and `scipy`.  These are all easily installed using the `pip install` command.  e.g.
```
$ pip install numpy
$ pip install soundfile
$ pip install librosa
$ pip install scipy
$ pip install sklearn
```

The Essentia library will also need to be installed using this manual installation.  Documentation for the installation of Essentia can be found at (http://essentia.upf.edu/documentation/installing.html).


## Using the models
The models are written as a package which can be imported into a Python script.  Within the package are seven methods that predict the *hardness*, *depth*, *brightness*, *warmth*, *sharpness*, *booming*, and *roughness* of an audio file.  These are named `timbral_xxx(fname)`, where `xxx` represents the timbral model.

To calculate the timbral attribute, give the method a string of the file name.  The method will then read in the audio file internally and return the timbral characteristic, as described below.


## Model output
The *hardness*, *depth*, *brightness*, and *warmth* models predict subjective ratings of their respective attributes.  Each model returns a float.  These models were trained on subjective ratings ranging from 0 to 100, but can extend beyond this range.  See Deliverbale D5.6 for full documentation on implementation and optional parameters.

The *roughness*, *sharpness*, and *booming* models return a float representing their subjective attribute for the audio file.  The minimum value is 0.0, but there is no upper limit on the maximum value.


## Example usage

```
from timbral_models import timbral_brightness 

# generic file location
fname = '/Users/User/Music/AudioFileToTest.wav'

# calculate brightness
brightness = timbral_brightness(fname) 
```


## Version History
This section documents the version history of the timbral models.  To download a specific version of the model that relate to a specific deliverable, please check this section and download the most recent version from that date.

2018/07/26 - Version 0.2 of timbral models, relates to Audio Commons Deliverable D5.6.  This version of the repository relates to the software version 0.2 on PyPI. 

2017/09/05 - Version 0.1 of timbral models, relates to Audio Commons Deliverable D5.3.  This version of the repository relates to the software version 0.1 on PyPI.

2017/04/27 - Version 0.0 of the timbral models, relates to Audio Commons Deliverable D5.2. 
