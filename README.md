# Detection and Sorting of Lego Bricks using OpenCV

A simple machine vision system for detection and sorting of lego bricks.

The program identifies the colour of the lego bricks using HSV colour thresholding together with area and aspect ratio values. The program identifies the size of the lego bricks using the colour identified together with area and aspect ratio values. With the colour and size of the lego bricks identified, it is able to properly identify the exact lego bricks present in a video, which is used to update the table.

OpenCV was used to read images, create a video using images, converting colour space, colour thresholding, binary image bitwise operations, contour detection, contour area calculation, finding rotated rectangle of minimum area, finding vertices of rotated rectangle, draw contours, draw circle, add text to image, blur images and find circles in grayscale image using Hough transform.

### Lego detection:

<img width="577" height="302" alt="lego detection" src="https://github.com/user-attachments/assets/df005655-352c-4a53-9805-3e8abf47779d" />

### Contour detection:

<img width="575" height="300" alt="contour detection" src="https://github.com/user-attachments/assets/dbf15533-00be-4fb5-abc6-6e9916f3c9a3" />

### Circle detection:

<img width="561" height="293" alt="circle detection" src="https://github.com/user-attachments/assets/9aebb7c1-159f-410c-838f-b01b8b72c525" />

### Center detection:

<img width="570" height="297" alt="center detection" src="https://github.com/user-attachments/assets/d1c48a56-5dc7-42c9-a09f-1d3005aa482a" />

## Overall workflow:
<img width="1551" height="758" alt="image" src="https://github.com/user-attachments/assets/592a9c53-541f-434a-91ac-1adefe463878" />

The flowchart above shows the whole computer vision approach flow, from the input to the output. The green boxes represent the input and output. The blue boxes represent the Lego Detection, Contour Detection, Circle Detection and Center Detection. The grey boxes represent the detection of only grey coloured lego bricks. The white boxes represent the normal flow each input goes through to reach the output.
