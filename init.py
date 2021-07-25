import subprocess
import os
print("Thank you for using Ball Caller!")
print("Please take a picture of your tennis ball laying on the court so I can calibrate Ball Caller for your match.")
path = input("Please pass an absolute or relative path to your image:\n")
bashCommand = " run paint " + path
input("Excellent. An MSPaint window will be opened now. Please use the select tool to draw a circle around the ball.\n Press any key to continue.")
paintPath = os.path.splitdrive(os.path.expanduser("~"))[0]+r"\WINDOWS\system32\mspaint.exe"
subprocess.Popen([paintPath, path])
input("Press any key to confirm that you have saved the image.")
os.system("python recordvid.py " + path)
