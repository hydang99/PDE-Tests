# WoundHealing Project
Would Healing Project - Deep Learning &amp; Mathematics <newline>
In this research project, we use 2 main methods which are Partial Differential Equations to study the healing process of the wound as well as Deep Learning to retrieve the boundary of the pictures of wounds.
  
## 1. Big Idea: 
  We want to analyze the wound healing process by using mathematical models. We treat the way protein, keratin, covers at a wound as a diffusion process. There are many ways to solve this numerical problem. However, we believe that ADI method is the good way to do that.
  Our problem will be divided into two main tasks: 
  - 1. Working with the wound images. 
  - 2. Working with the mathematical model.
## Working with tasks
### 1. Working with the wound images. 
  Recognizing the wounds in the image and mapping images with different time to the same scale because each image is captured in different angle and different distances from the wound. Thus, we want to align all of them in the same scales. (zoom, rotate)
  - Dataset: We receive the dataset which contains multiple images of the wounds of patients. (One patient have different images in different times). 
  #### Subtask 1. Recognizing the wounds in the images. 
  For this task, we want to use Deep Learning, there have been many works that involving this type of segmentation. Most common approach is using "Encoder-Decoder" models. We have tried to use different Deep Learning models to implement this task. So these are the results of two models which are U-Net and Residual U-Net model. 
  Problems encountered: Lack of data. -> Residual U-Net performs worse than U-Net Model.
  Loss function : pixel-wise cross entropy loss, dice coefficient. 
 #### Subtask 2. Aligning the wounds in the images. 
  Finding the correct zoom factor and rotation factor between two images. 
  1. Finding center of mass of the wound 
  2. Getting the small windows of images
  3. Getting the frame of images
  4. Try different combinations of rotation and angle to identify maximum number of matches pixels between two images. 
### 2. Working with the mathematical model. 

