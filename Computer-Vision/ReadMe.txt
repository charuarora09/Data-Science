Enhancing the algorithm to capture wink and silence in live video and images using haar cascades in C++ using OpenCv.


1.	Approach used to detect a wink

Program file: DetectWink.cpp



First, I convert the image to grayscale and try to detect the face. Once detected, I check for open eyes in the upper half of the face. Once detected, the program counts the number of eyes and if only one is found, it outputs that a wink has been detected, else it is not considered a wink.

Parameter used to detect the face - 
Scale factor: 1.1
minNeighbors: 4
 flags: 0|CV_HAAR_SCALE_IMAGE
size in pixels of smallest allowed detection: Size(15, 15)

Parameters used to detect the eyes:
Scale factor: 1.1
minNeighbors: 8
 flags: 0|CV_HAAR_SCALE_IMAGE
size in pixels of smallest allowed detection: Size(20, 20)



Using this approach on the images provided, the program was not able to detect winks in 4 of the images (for which ever image a face was detected). Out of these 4 images, one of them had the second eye half opened, which is why it considered it to be completely open, giving a wrong result. For two of the images out of these 4, the eyes were way too small to be detected. And for the 4th image, there is a glare in the spectacles of the person in the image which is why it could not detect the eyes. 


2.	Approach used to detect silence

Program file: DetectSilence.cpp




First, I convert the image to grayscale and try to detect the face. Once detected, I check for a mouth in the lower half of the face. If a mouth is detected, it checks the ratio of the mouth found and the lower part of the face. 
If ratio is greater than 0.30, it then checks if the mouth is placed in the center of the face by checking the percentage of ‘the distance between the points on the left side of the mouth and lower face’ and ‘the distance between the points on the right side of the mouth and lower face’ with ‘the width of the lower part of the face’. 

Formula: 
abs(norm(left1-left2)-norm(right1-right2))/ mouth.width*100 >25

If this is greater than 25, that means the mouth detected is not in the center of the lower part of the face.

Parameter used to detect the face - 
Scale factor: 1.1
minNeighbors: 3
 flags: 0|CV_HAAR_SCALE_IMAGE
size in pixels of smallest allowed detection: Size(30, 30)

Parameters used to detect the mouth:
Scale factor: 1.2
minNeighbors: 3
 flags: 0|CV_HAAR_SCALE_IMAGE
size in pixels of smallest allowed detection: Size(10, 10)



Using this approach on the images provided, the program detected all the images with Silence with no false positives (for which ever image a face was detected). 
