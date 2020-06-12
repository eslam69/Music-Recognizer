# Music Recognizer

To install required dependencies please run :
```python
 pip install -r requirements.txt
```

## Description
* The Database consists of 223 songs, recognition is based on songs spectrograms or the spectral features : <br/>
( spectral centroids & spectral rolloff ), hashing the data is done with a Perceptual Hashing algorithm.
* Two audio files can be loaded into the application, you can mix the 2 files as a testing mechanism.
* The results are populted into the table and sorted according to their similarity index

![ Mix your Song and it will try to recognize the Output](res/Screenshot.png)
