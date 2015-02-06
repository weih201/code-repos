# Camera Image Capture and Vector Display

This is designed to capture monochrome images from a CMOS image chip (with a digital interface) and display them on the VGA monitor. The camera module is OV7620, the resolution is (640x480). The captured image is held in a double-buffered Frame Buffer, so that capturing and displaying image can happen independently and simultaneously,  ….