#import the pyplot and wavfile modules 
from PyQt5 import QtWidgets ,QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QFileDialog, QAction,QTableWidget
from gui import Ui_MainWindow
import os
import sys
import matplotlib.pyplot as plot
import librosa 
from pydub import AudioSegment
from tempfile import mktemp
#import sklearn
import librosa.display
import numpy as np
from PIL import Image
import imagehash
import pylab
class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self) 

        ############################################# Control Lists #############################################
        self.Buttons= [self.ui.BrowseFile1 , self.ui.BrowseFile2 , self.ui.Search]
        self.RadioButtons = [self.ui.radioButton , self.ui.radioButton_2]

        ############################################# ############# #############################################



        #############################################   UI initial settings #####################################
        self.Buttons[1].setDisabled(True) 
        self.Buttons[2].setDisabled(True) 
        self.ui.horizontalSlider.setDisabled(True) 
        self.ui.horizontalSlider.setMaximum(100)
        self.ui.horizontalSlider.setMinimum(0)
        self.ui.horizontalSlider.setSingleStep(1)
        self.ui.horizontalSlider.setValue(0)

        self.OpenAgain_flag1  = False 
        self.OpenAgain_flag2 = False 


        ############################################# ############# #############################################



        #############################################   UI signals #####################################
        self.ui.BrowseFile1.clicked.connect(lambda : self.mp3Converter(1) )
        self.ui.BrowseFile2.clicked.connect(lambda : self.mp3Converter(2) )
        self.ui.horizontalSlider.sliderReleased.connect(lambda : self.mixer())
        self.ui.Search.clicked.connect(lambda : self.compare()  )
       
        #self.ui.horizontalSlider.valueChanged.connect(self.mixer)
     
    def mp3Converter(self,songNumber):
      fname= QFileDialog.getOpenFileName( self, 'choose the signal', os.getenv('HOME') ,"mp3(*.mp3)" ) 
      self.path = fname[0] 
      if self.path =="" :
          return
      mp3_audio = AudioSegment.from_file( self.path , format="mp3")[:60000]  # read mp3
      wname = mktemp('.wav')  # use temporary file
      mp3_audio.export(wname, format="wav")  # convert to wav
      if 1 == songNumber :
        self.ui.label_2.setText(os.path.splitext(os.path.basename(self.path))[0])
        self.Buttons[1].setDisabled(False) 
        self.wavsong1,self.samplingFrequency1 =librosa.load(wname)
        self.OpenAgain_flag1  =  True


        print("file1 read ")
      elif 2 == songNumber :
        self.ui.label_3.setText(os.path.splitext(os.path.basename(self.path))[0])
        #self.Buttons[2].setDisabled(False) 
        
        self.ui.horizontalSlider.setDisabled(False)  
        self.wavsong2,self.samplingFrequency2 =librosa.load(wname)
        self.OpenAgain_flag2  = True

        print("file2 read")
      self.ui.tableWidget.clearContents()



    def mixer(self) :
      """mixer [applies the mixing ratio taken from the GUI slider and then calls the spectrogram() function and pass to it the output of mixing ]
      """
      sliderRatio = self.ui.horizontalSlider.value()/100
      self.outputSong = self.wavsong1 * sliderRatio + self.wavsong2 * (1-sliderRatio)
      self.Buttons[2].setDisabled(False) 
      #print(self.output)
      self.spectrogram()

      
    def spectrogram (self):
        """spectrogram [Makes the spectrogram of a song , calls a function to hash the the spectro. and a function to extract the features of the song]
        """
        Spectro_Path = 'mixSpectrogram.png'
        pylab.axis('off')  # no axis
        pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[])  # Remove the white edge
        D = librosa.amplitude_to_db(np.abs(librosa.stft(self.outputSong)), ref=np.max)
        librosa.display.specshow(D, y_axis='linear')
        pylab.savefig(Spectro_Path, bbox_inches=None, pad_inches=0)
        pylab.close()
        self.SongHash = self.hashing(Spectro_Path) 
        self.features()

    def hashing(self,filename) :
      """hashing [function that hashes a spectrogram]

      Args:
          filename ([string]): [the file of the image of a spectrogram to be hashed]
      Return:
          string
      """
      hashcode = imagehash.phash(Image.open(filename) ) #We will use Perceptual hashing 
      return(str(hashcode))

    def features (self): 
      """features [a function that do feature extraction on the mixed song , 
      
      return globally :(spectral_centroids,spectral_rolloff)]

      """      
      #spectral centroid 
      pylab.axis('off')  
      pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[])
      SavePath = 'HASH_centroid.png'
      featured1= librosa.feature.spectral_centroid(y=self.outputSong, sr=self.samplingFrequency1)
      librosa.display.specshow(featured1.T,sr=self.samplingFrequency1 )
      pylab.savefig(SavePath, bbox_inches=None, pad_inches=0)
      pylab.close()

      #spectral_RollOff
      pylab.axis('off') 
      pylab.axes([0., 0., 1., 1.], frameon=False, xticks=[], yticks=[]) 
      SavePath ='HASH_rolloff.png'
      featured2= librosa.feature.spectral_rolloff(y=self.outputSong, sr=self.samplingFrequency1)
      librosa.display.specshow(featured2.T,sr=self.samplingFrequency1 )
      pylab.savefig(SavePath, bbox_inches=None, pad_inches=0)
      pylab.close()


      #hashing the 2 features
      self.centroidHash= self.hashing('HASH_centroid.png')
      self.rolloffHash= self.hashing('HASH_rolloff.png')
      print(self.SongHash,self.centroidHash ,self.rolloffHash )
      ### kda ana 3ndy 3 hash codes b3d el function de -----> 1)self.SongHash        2)self.centroidHash        3)self.rolloffHash 


    def compare(self ) :
      """ compare [ This function checks the mode of Identinfication of the song, either:by Spectrogram or By Features
      then calculates the hamming distances and shows the result in the UI table
      ]
      """
      if self.OpenAgain_flag1 or self.OpenAgain_flag2 : #### UI signals Flow opimization 
        self.mixer()
        self.OpenAgain_flag1 = False
        self.OpenAgain_flag2 =False


      if self.RadioButtons[0].isChecked() ==True : ######### spectrogram mode #########
        song_index_pair = dict()
        # iterate over hashes of spectrograms , make Dictionary: "song_index_pair" which has "song name" as key and "hamming index between this song and the mixed song" as value
        for filename in os.listdir('spectros/hashes') : 
          f = open('spectros/hashes/'+filename,"r")
          HASH = f.read()
          NAME = os.path.splitext(os.path.basename(filename))[0] 
          #Calculating the number of different Bits (using bitwise XOR)
          hamming_index= bin( int(self.SongHash,16)^int(HASH,16) ).count('1') 
          print("hamming index =   ",hamming_index)
          song_index_pair.update({NAME : hamming_index} )
          f.close()
        # Now we create two lists ine for keys and the other for values of the Dictionary
        keys= list(song_index_pair.keys())
        values = list(song_index_pair.values())
        #then we sort them ascendingly according to hamming index (Note: lower index means more similar to the song) 
        values, keys = (list(t) for t in zip(*sorted(zip(values, keys))))
        #We will choose the top 10 song to show on the result table 
        self.TopTen = keys[:10]
        for row in range(10) :
          
          item = QtWidgets.QTableWidgetItem(self.TopTen[row])
          self.ui.tableWidget.setItem(row,0,item)
      else : ######### Features Mode #########
        #Creating 2 dictionaries to hold the song_index pair for each song feature
        song_index_pair1 = dict() #for spectral centroid
        song_index_pair2 = dict() #for spectral rolloff
        # iterate over hashes files in the directory of 'Hashes_Centroid/hashes' FEATURE 1
        for filename in os.listdir('Hashes_Centroid/hashes') :  
          f = open('Hashes_Centroid/hashes/'+filename,"r")
          HASH = f.read()
          NAME = os.path.splitext(os.path.basename(filename))[0][:-13] 
          hamming_index1= bin( int(self.centroidHash,16)^int(HASH,16) ).count('1') 
          print("hamming index1 =   ",hamming_index1)
          song_index_pair1.update({NAME : hamming_index1} )
          f.close()
        # iterate over hashes files in the directory of 'Hashes_RollOff/hashes' FEATURE 2
        for filename in os.listdir('Hashes_RollOff/hashes') : 
          f = open('Hashes_RollOff/hashes/'+filename,"r")
          HASH = f.read()
          NAME = os.path.splitext(os.path.basename(filename))[0][0:-12]  ####edit name here
          hamming_index2= bin( int(self.rolloffHash,16)^int(HASH,16) ).count('1') 
          print("hamming index2 =   ",hamming_index2)
          song_index_pair2.update({NAME : hamming_index2} )
          f.close()

        values1= np.asarray(list(song_index_pair1.values()) )
        values2= np.asarray(list(song_index_pair2.values()) )
        averageValues = values1*0.5 + values2*0.5 #taking a weighted average of the 2 features lists element wise 

        #list songs Names to be showed on the UI table
        keys = list(song_index_pair1.keys())
        #sorting the Results
        values, keys = (list(t) for t in zip(*sorted(zip(averageValues, keys))))
        self.TopTen = keys[:10]
        for row in range(10) :
          
          item = QtWidgets.QTableWidgetItem(self.TopTen[row])
          self.ui.tableWidget.setItem(row,0,item)
          
        




      #print(keys)
         






def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    app.exec_()
if __name__ == "__main__":
    main()
