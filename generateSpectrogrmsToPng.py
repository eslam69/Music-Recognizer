
import matplotlib.pyplot as plot
import librosa 
from pydub import AudioSegment
from tempfile import mktemp
import sklearn
import librosa.display
import numpy as np
from sklearn.feature_selection import SelectKBest, chi2
import os
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from PIL import Image
import imagehash
import pylab

for filename in os.listdir():   ################################### you need to be in the folder of songs
    if filename.endswith(".mp3"):
    
        
        mp3_audio = AudioSegment.from_file(filename, format="mp3")[:60000]  # read mp3
        wname = mktemp('.wav')  # use temporary file
        mp3_audio.export(wname, format="wav")  # convert to wav
        # Read the wav file (mono)
        wavsong,samplingFrequency =librosa.load(wname)

        Spectro_Path = 'spectros/'+os.path.splitext(os.path.basename(filename))[0]+'.png'
        pylab.axis('off')  # no axis
        pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[])  # Remove the white edge
        D = librosa.amplitude_to_db(np.abs(librosa.stft(wavsong)), ref=np.max)
        librosa.display.specshow(D, y_axis='linear')
        pylab.savefig(Spectro_Path, bbox_inches=None, pad_inches=0)
        pylab.close()

 
        # For plotting headlessly

        
        

