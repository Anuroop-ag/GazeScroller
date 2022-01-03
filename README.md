# GazeScroller

Using Facial Movements to perform Hands-free Gesture on the system

# Abstract

As our world is getting digitized on an fast rate, every person is having a device that is making life better. Also, there is a considerate amount of the society that do not have interactions as others to these devices. One such example are the quadriplegic people (people suffering from paralysis) which constitute to 5.4 million people people in the world*. Our aim here is to make them interact with the digital world. In this project, facial movements of the person's face is fed to the system on real-time and a certain list of operations can be performed on the system using these facial actions.Additionally, we will extend this system to mini-games on the internet like the Dino Game. Finally, I have evaluated the system by five people and found that they have positively to the system. These results imply that we can generalise this system to the entire world.

# Approach
The project captures live stream of the video via webcam of the system. It then maps the face to 68 landmark points via the library Dlib. The movements of the points corresponding to the eye and nose are monitored continously.
The functionalities covered in the project include :
• Detect blink of one eye to enable/disable scrolling.
• Detect the scroll movement based on the movement of the point on the nose.
Using Blink to toggle scroll and head direction to scroll
 
# Background Study
Blinking is an involuntary action of a human being.Blinks can be spontaneous, reflex and voluntary, and eye blink rate depends on various factors including environmental factors, type of activity.
 
In order to segregate natural blink of the eye with the intentional blink of one eye of the user for functionality 1 as discussed above, I have studied the eye width ratios of by conducting experiments study over 5 users with each subject testing for 10 times.
This data analysis is used to understand to difference in the eye width ratio between both the eyes to when a user blinks one of the eye.
Secondly, the intentional blink of the eye is put on a threshold for 3 frames to detect blink.
These procedures helped detect the intentional one eye blink from the natural blink of the eyes.
The information from the Fig 1 gives us the details of the eye ratio and the delta (difference between the eye ratios). We take the mean and use them as a reference in our code as threshold.

# Technical Tools :
• Dlib - a library used to detect face per frame via webcam
• Python - language to write the code
• landmarksPoints.dat file - this file is used to superimpose landmarks onto the face
detected.
• pynput - library to invoke keyboard and mouse keys.
  
# System Setup :
By using the tools of mentioned above, we get the face of the user per frame superimposed by landmark points.
Calculations for each frame include :

rightEyeWidthRatio = height of the right eye/ width of the right eye leftEyeWidthRatio = height of the left eye/ width of the left eye delta = abs(leftEyeWidthRatio - rightEyeWidthRatio)
Whenever a user blinks one eye, following cases are checked
• Check 1 : if delta > threshold of delta taken from fig.1
• Check 2 : if leftEyeWidthRatio < threshold value of blink and frame count is 3.
• If Check 1 and Check 2 true , trigger Blink and enable scrolling.
UX Aspects :
Trigger notifications in the system when scrolling is toggled.

# Discussion & Future Scope:
In the present work I have not made much effort into perfectly the model and in CV. I have worked towards the thresholds and correlating to the use case I mentioned in the abstract. If substantial work is detecting the exact eye wink using ML models, the system would be much better.
The false blinks being recorded is because we lack a model here.
In the future scope , we can use this feature to build interactive games to the quadriplegic people to improve their psychological status too.


#  Conclusion :
All the subjects who have tested responded positively to the system and felt good about it.
Therefore, we can say that our system is performing good to scroll pages using the nose and to capture the blink of the eye as a toggle gesture.
 
Hence, such a model will be beneficial to quadriplegic people and help them to interact with the digital world.Since the false blinks are low, the system is good to be used. It can be further perfected with ML models to give better accuracy to be used by the quadriplegic people.
    
