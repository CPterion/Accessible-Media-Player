# Accessible Media Player
An assistive technology for users with motor impairments. The user can control their music or video player (play, pause, or change volume) by making distinct facial gestures like turning your head, tilting, or opening their mouth.

## Requirements
- Python==3.12.3: Programming language
- MediaPipe==0.10.21: for creating a face mesh
- KivyMD==1.2.0: for the ready-made video player
- FFPyPlayer==4.5.3: for playing videos
- OpenCV==4.11.0.86: Webcam and image processing
```
pip install -r requirements.txt
```

## Usage
```
python video_player.py
```
This video player is controlled by facial expressions and actions. A well-lit environment is recommended, though it can also work in moderately-lit surroundings. Drag the file to the window to load a video. It plays the video when a face is detected, and pauses it when you look away or leave the computer. This feature can be disabled by opening your mouth. To control the volume, tilt your head to the left or right. You can also rewind or seek forward the video by turning your head in the direction you want to move the playback position.

### Controls
- Head tilt: audio control (left ay decrease, right ay increase)
- Head turn: playback seek (left ay rewind, right ay seek forward)
- Face detection: for playing of video (kunwari umalis ka, magpopause yung player kung saka magpeplay ulit kung may nadetect nanaman na face)
- Open mouth: to disable the last feature (toggle command ito)
