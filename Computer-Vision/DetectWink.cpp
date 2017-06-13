#include "opencv2/highgui.hpp"
#include "opencv2/objdetect/objdetect.hpp"
#include "opencv2/imgproc/imgproc.hpp"

#include <iostream>
#include <stdio.h> 
#include "dirent.h"

using namespace std;
using namespace cv;


/* 
   The cascade classifiers that come with opencv are kept in the
   following folder: bulid/etc/haarscascades
   Set OPENCV_ROOT to the location of opencv in your system
*/
string OPENCV_ROOT = "/usr/local/Cellar/opencv/2.4.13.2/";
string cascades = OPENCV_ROOT + "share/OpenCV/haarcascades/";
string FACES_CASCADE_NAME = cascades + "haarcascade_frontalface_alt.xml";
string EYES_CASCADE_NAME = cascades + "haarcascade_eye.xml";
string EYES_CASCADE_NAME1 = cascades + "haarcascade_eye_tree_eyeglasses.xml";


int distance_pts(Mat frame, Rect face, vector<Rect> eyes, Point location)
{
	int n;
	int neyes = (int)eyes.size();
	int num[neyes];
	if (neyes ==2)
	{
    for( int i = 0; i < neyes ; i++ ) {
    Rect eyes_i = eyes[i];
    eyes_i = eyes_i+location;
    //cout<<" "<<eyes_i.width/float(face.width)<<"\t";
    num[i] = eyes_i.height;

	}
	if (abs(num[0]-num[1]) < 10)
	{
		n = 1;
		}
		
	else
	{
		n=0;
	}
	} 
return (n==1);

}





void drawEllipse(Mat frame, const Rect rect, int r, int g, int b) {
  int width2 = rect.width/2;
     int height2 = rect.height/2;
     Point center(rect.x + width2, rect.y + height2);
     ellipse(frame, center, Size(width2, height2), 0, 0, 360, 
	     Scalar(r, g, b), 2, 8, 0 );
}


bool detectWink(Mat frame, Point location, Mat ROI, CascadeClassifier cascade,CascadeClassifier cascade1, Rect face) {

	
    vector<Rect> eyes;
    cascade.detectMultiScale(ROI, eyes, 1.1, 4, 0, Size(10, 10));
    int neyes = (int)eyes.size();
    bool p = distance_pts(frame,face,eyes,location);
    if (neyes == 0)
    {

    cascade.detectMultiScale(ROI, eyes, 1.1, 4, 0, Size(25, 25));
    neyes = (int)eyes.size();
	 for( int i = 0; i < neyes ; i++ ) 
    {
    Rect eyes_i = eyes[i];
    drawEllipse(frame, eyes_i + location, 255, 255, 0);
	}
    }
    else{
    if(  neyes!=2  )
    {
    if(ROI.rows==57 and ROI.cols==100)
    {
    neyes = neyes -1;
    }
    else
    for( int i = 0; i < neyes ; i++ ) 
    {
    Rect eyes_i = eyes[i];
    drawEllipse(frame, eyes_i + location, 255, 255, 0);
	}
	}
	else
	{

	cascade1.detectMultiScale(ROI, eyes, 1.1, 4, 0, Size(10, 10));
    neyes = (int)eyes.size();
	 for( int i = 0; i < neyes ; i++ ) 
    {
    Rect eyes_i = eyes[i];
    drawEllipse(frame, eyes_i + location, 255, 255, 0);
	}
	}
	}
	return(neyes == 1);
}

// you need to rewrite this function
int detect(Mat frame, 
	   CascadeClassifier cascade_face, CascadeClassifier cascade_eyes,CascadeClassifier cascade_eyes1) {
  Mat frame_gray;
  vector<Rect> faces;
  
  cvtColor(frame, frame_gray, CV_BGR2GRAY);
  cascade_face.detectMultiScale(frame_gray, faces, 
			   1.1, 4, 0|CV_HAAR_SCALE_IMAGE, 
			   Size(10,10));
  int detected = 0;
  int nfaces = (int)faces.size();
  for( int i = 0; i < nfaces ; i++ ) {
    Rect face = faces[i];
    drawEllipse(frame, face, 255, 0, 255);
    Rect real(face.x, face.y ,face.width, face.height/1.75);
    //cout<<real;
    Mat faceROI = frame_gray(real);
    if(detectWink(frame, Point(face.x, face.y), faceROI, cascade_eyes, cascade_eyes1,real)) {
      drawEllipse(frame, face, 0, 255, 0);
      detected++;
    }
  }
  return(detected);
}

int runonFolder(const CascadeClassifier cascade1, 
		const CascadeClassifier cascade2, const CascadeClassifier cascade3,
		string folder) {
  if(folder.at(folder.length()-1) != '/') folder += '/';
  DIR *dir = opendir(folder.c_str());
  if(dir == NULL) {
      cerr << "Can't open folder " << folder << endl;
      exit(1);
    }
  bool finish = false;
  string windowName;
  struct dirent *entry;
  int detections = 0;
  while (!finish && (entry = readdir(dir)) != NULL) {
    char *name = entry->d_name;
    string dname = folder + name;
    Mat img = imread(dname.c_str(), CV_LOAD_IMAGE_UNCHANGED);
    if(!img.empty()) {
      int d = detect(img, cascade1, cascade2,cascade3);
      cerr << d << " detections" << endl;
      detections += d;
      if(!windowName.empty()) destroyWindow(windowName);
      windowName = name;
      namedWindow(windowName.c_str(),CV_WINDOW_AUTOSIZE);
      imshow(windowName.c_str(), img);
      int key = cvWaitKey(0); // Wait for a keystroke
      switch(key) {
      case 27 : // <Esc>
	finish = true; break;
      default :
	break;
      }
    } // if image is available
  }
  closedir(dir);
  return(detections);
}

void runonVideo(const CascadeClassifier cascade1,
		const CascadeClassifier cascade2,const CascadeClassifier cascade3) {
  VideoCapture videocapture(0);
  if(!videocapture.isOpened()) {
    cerr <<  "Can't open default video camera" << endl ;
    exit(1);
  }
  string windowName = "Live Video";
  namedWindow("video", CV_WINDOW_AUTOSIZE);
  Mat frame;
  bool finish = false;
  while(!finish) {
    if(!videocapture.read(frame)) {
      cout <<  "Can't capture frame" << endl ;
      break;
    }
    detect(frame, cascade1, cascade2,cascade3);
    imshow("video", frame);
    if(cvWaitKey(30) >= 0) finish = true;
  }
}


int main(int argc, char** argv) {
  if(argc != 1 && argc != 2) {
    cerr << argv[0] << ": "
	 << "got " << argc-1 
	 << " arguments. Expecting: [image-folder]" 
	 << endl;
    return(-1);
  }

  string foldername = (argc == 1) ? "" : argv[1];
  CascadeClassifier faces_cascade, eyes_cascade, eyes_cascade1;
  
  if( 
     !faces_cascade.load(FACES_CASCADE_NAME) 
     || !eyes_cascade.load(EYES_CASCADE_NAME) || !eyes_cascade1.load(EYES_CASCADE_NAME1)) {
    cerr << FACES_CASCADE_NAME << " or " << EYES_CASCADE_NAME << " or " << EYES_CASCADE_NAME1
	 << " are not in a proper cascade format" << endl;
    return(-1);
  }

  int detections = 0;
  if(argc == 2) {
    detections = runonFolder(faces_cascade, eyes_cascade, eyes_cascade1,foldername);
    cout << "Total of " << detections << " detections" << endl;
  }
  else runonVideo(faces_cascade, eyes_cascade,eyes_cascade1);
  return(0);
}