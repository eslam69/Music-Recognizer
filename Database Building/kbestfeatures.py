import matplotlib.pyplot as plot
import librosa 
from pydub import AudioSegment
from tempfile import mktemp
import sklearn
import librosa.display
import numpy as np
from sklearn.feature_selection import SelectKBest, chi2
import os

songName = 'massaregbari_saheb_music_17.mp3'
mp3_audio = AudioSegment.from_file(songName, format="mp3")[:60000]  # read mp3
wname = mktemp('.wav')  # use temporary file
mp3_audio.export(wname, format="wav")  # convert to wav
# Read the wav file (mono)
wavsong,samplingFrequency =librosa.load(wname)
#print(wavsong)
# Plot the signal read from wav file
#plot.subplot(211) 

array= plot.specgram(wavsong,Fs=samplingFrequency)
print(type(array))
plot.xlabel('Time')
plot.ylabel('Frequency')
plot.show()

# zero_crossing #feature 1
n0 = 9000
n1 = 9100
zero_crossings = librosa.feature.zero_crossing_rate(wavsong)
print(zero_crossings.shape)

#plot.show()
#spectral centroid -- centre of mass -- weighted mean of the frequencies present in the sound #feature 2

spectral_centroids = librosa.feature.spectral_centroid(wavsong,sr=samplingFrequency)
spectral_centroids.shape# Computing the time variable for visualization
frames = range(len(spectral_centroids))
t = librosa.frames_to_time(frames)
# Normalising the spectral centroid for visualisation
def normalize(x, axis=0):
    return sklearn.preprocessing.minmax_scale(x, axis=axis)
#Plotting the Spectral Centroid along the waveform
librosa.display.waveplot(wavsong,sr=samplingFrequency, alpha=0.4)
#plot.subplot(211)
#plot.plot(t, normalize(spectral_centroids), color='r')

#spectral rolloff #feature 3
spectral_rolloff = librosa.feature.spectral_rolloff(wavsong, sr=samplingFrequency)
print(spectral_rolloff.shape)
librosa.display.waveplot(wavsong,sr=samplingFrequency, alpha=0.4)
#plot.subplot(212)
#plot.plot(t, normalize(spectral_rolloff), color='g')
#mfssc #feature 4
mfccs = librosa.feature.mfcc(wavsong, sr=samplingFrequency)
print(mfccs.shape)#Displaying  the MFCCs:
#librosa.display.specshow(mfccs, sr=samplingFrequency, x_axis='time')
#plot.show()


#kbest 
x = np.concatenate((zero_crossings,spectral_centroids,spectral_rolloff))
y = ('zero_crossings','spectral_centroids','spectral_rolloff')
X_new = SelectKBest(chi2, k=2).fit_transform(x, y)
print(X_new)
# so the best to use is spectral_centroids & spectral_rolloff ##############################################################################################

window_size = 1024
window = np.hanning(window_size)
stft  = librosa.core.spectrum.stft(wavsong, n_fft=window_size, hop_length=512, window=window)
out = 2 * np.abs(stft) / np.sum(window)

# For plotting headlessly
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

fig = plot.Figure(frameon=False)
plot.axis('off')
canvas = FigureCanvas(fig)
ax = fig.add_subplot(111)
p = librosa.display.specshow(librosa.amplitude_to_db(out, ref=np.max), ax=ax, y_axis='log', x_axis='time')
#p = librosa.display.specshow(wavsong)

fig.savefig('spectros/'+os.path.splitext(os.path.basename(songName))[0]+'.png')

'''
################ Hashing the features of a song  ##########
from PIL import Image
import imagehash
features = [spectral_centroids , mfccs ]
print("perceptual hash of features is")
for feature in features :
    otherhash = imagehash.phash(Image.fromarray(feature) )
    print(otherhash)

print("\n average hash of features is")
for feature in features :
    otherhash = imagehash.average_hash(Image.fromarray(feature) )
    print(otherhash)
    '''
