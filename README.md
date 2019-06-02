# compliment-inator
### Simple Face Recognition Program, That compliments you each time it sees you on webcam!

Open source project made by Jakub Podolak, based on [face_recognition](https://github.com/ageitgey/face_recognition) module and [gTTS](https://pypi.org/project/gTTS/). I suggest going through those libraries first, to get familiar with them and install all required stuff.

### What is it?
This is very simple - `face_finder.py` uses face_recognition module to detect your face, saves your name to log file, from which another program: `sayer.py` can take it, and synthesize a compliment (or any other text) for you!

### How to get it working?
0. Install all needed libraries:
```
gtts
playsound
configparser
face_recognition
cv2
numpy
```

1. Download all files from this repository  
2. Add your photo with `.jpg` extension, e.g. `myface.jpg`
3. Specify it in `config_face.ini` file in `[FACES]` section like this:  
```
myName = myface.jpg  
Thomas = thomas_photo.jpg
```
4. Add your text (currently only one sentence for each person) in `config_sayer.ini` in `[SAYINGS]` section like this:  
```
myName = My text that will be synthesized
Thomas = You looking good, Thomas!
```
5. Tinker with additional settings specified in both config files  
6. Run two programs with `./RUN.sh` command
