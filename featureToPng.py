
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



FEATURE = 'spectral_rolloff'

                  
def hash_feature(feature) :
    """hash_feature [a function that generate spectograms of fetures] ########## you need to be in the folder of songs

    Args:
        feature ([string]): [special feature to be extracted]
    """    
    


    
    

    for filename in os.listdir():
        if filename.endswith(".mp3"):
        
            
            mp3_audio = AudioSegment.from_file(filename, format="mp3")[:60000]  # read mp3
            wname = mktemp('.wav')  # use temporary file
            mp3_audio.export(wname, format="wav")  # convert to wav
            # Read the wav file (mono)
            wavsong,samplingFrequency =librosa.load(wname)

            pylab.axis('off')  # no axis
            pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[])  # Remove the white edge
            if 'spectral_centroid' == feature :
                SavePath = 'Hashes_centroid/'+os.path.splitext(os.path.basename(filename))[0]+'HASH_centroid.png'

                featured= librosa.feature.spectral_centroid(y=wavsong, sr=samplingFrequency)
                librosa.display.specshow(featured.T,sr=samplingFrequency )
                pylab.savefig(SavePath, bbox_inches=None, pad_inches=0)
                pylab.close()
            elif 'spectral_rolloff' == FEATURE :
                SavePath = 'Hashes_RollOff/'+os.path.splitext(os.path.basename(filename))[0]+'HASH_rolloff.png'
                featured= librosa.feature.spectral_rolloff(y=wavsong, sr=samplingFrequency)
                librosa.display.specshow(featured.T,sr=samplingFrequency )
                pylab.savefig(SavePath, bbox_inches=None, pad_inches=0)
                pylab.close()
            else :
                return 

    return none
hash_feature(FEATURE)
