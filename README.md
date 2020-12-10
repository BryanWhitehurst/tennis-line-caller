# tennis-line-caller
A python script that uses OpenCV to make "In" or "Out" line calls in Tennis.

Using OpenCV functionality, the script
1. reads in a video file of the ball hitting the ground
2. uses binary search to find the frame where the ball is touching the ground
3. calls the ball "In" or "Out"
4. Prints the result to an image called "result.jpg"
