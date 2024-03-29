# Drowsiness detection in car with internet of things. 
## Problem and Solution
Vehicle crash in Indonesia increase from 95.906 to 109.215 in the years of 2014-2018 in indonesia (www.bps.go.id/linkTableDinamis/view/id/1134).Moreover in 2010-2016, crash because of the human error reachs 69.7% from all the crashes happen (Komite Nasional dan Keselamatan Informasi). In addition, in U.S. there are 396.000 crashes that related to drowsy of the drivers (NHTSA).  
  
  People who drowsy have an intent to close their eye. (Siswanto, Romy Loice, & The, 2014). The average of people blink is 100-400ms (Caffier, Erdmann, & Ulsperger, 2005). Therefore, if people blink more than 400 ms we can classify that they are sleepy.  
    
From the problem, one of the solution to make instrument with drowsiness detection. I used Convolutuional Neural Network here which applied on raspberry PI 4. 

## The CNN making process
### Closed eyes and opened eyes dataset for training : 
http://mrl.cs.vsb.cz/eyedataset![image]  
https://user-images.githubusercontent.com/95922228/151928769-86772ef7-e7e1-402c-996a-de9790f0a9b4.png  
http://parnec.nuaa.edu.cn/_upload/tpl/02/db/731/template731/pages/xtan/ClosedEyeDatabases.html  
https://user-images.githubusercontent.com/95922228/151928790-850e7863-31f6-4651-a24d-0f39befec849.png  

### Processing the picture
From the dataset, all pictures have various size, so we have to make the same size and dimension to 32 x 32 x 3 and labelling it. 
![mataprocess](https://user-images.githubusercontent.com/95922228/207498294-d4411d8b-43a2-4e2d-b9d3-a592fe535884.png)

### CNN Architecture
I build CNN architecture with only a few weights in order to fit the peformance of Raspberry PI 4

![Screen Shot 2022-12-14 at 10 30 09](https://user-images.githubusercontent.com/95922228/207498507-68cbf293-4c58-40d1-9b52-1832b2623476.png)


### CNN Training
I used Adam Optimizer with the data spil 70% for the training and 30% for the validation.

### Drowsiness Detection test
Haarcascade classifier was used. In order to peform better, picture was changed from RGB to gray. After we got the Region of Interest(The eye), we resize it to 32 x 32 which the same size as trained CNN model.
![Screen Shot 2022-12-14 at 10 31 14](https://user-images.githubusercontent.com/95922228/207498644-2d42dfdf-c6ae-445e-ac18-e76cdf7b689f.png)
![Screen Shot 2022-12-14 at 10 32 11](https://user-images.githubusercontent.com/95922228/207498820-106f1b66-cb28-4e33-88ba-1bf3d694a22e.png)

## Results
The model has 0.997% accuracy with validation reach 0.984%. On the other hand, the accuration loss only 0.0068%. In addtion, the Receive of Operating (ROC) curve reachs 0.999%.  
![Screen Shot 2022-12-14 at 10 32 41](https://user-images.githubusercontent.com/95922228/207498931-2eedcded-a87e-4260-9553-73ed17f2564a.png)
![Screen Shot 2022-12-14 at 10 32 54](https://user-images.githubusercontent.com/95922228/207498956-39efe44d-285f-4f54-85ea-a5a424c5c187.png)
![Screen Shot 2022-12-14 at 10 33 28](https://user-images.githubusercontent.com/95922228/207499001-e401e158-76fd-48dc-b732-392950eea6c3.png)

when CNN model applied to raspberry Pi with Pi camera version 2, the fps peformance was 1-2 fps. The real time test in the car, 14 times the blink tested, the tool succeed to detect all closes eye. But 3 times the tool detect the open eyes for clos eyes because of lack of lights. 

![Screen Shot 2022-12-14 at 10 34 05](https://user-images.githubusercontent.com/95922228/207499074-49ccdc4a-93ca-4165-9675-ea609e283d27.png)


