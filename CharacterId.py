from extractSilhouette import extractSilhouette
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np
from scipy.stats import pearsonr
import cv2
import time

directory = 'Database'
pathlist = Path(directory).rglob('*.jpg')
                              
dataSize = 100


pathInd = 0
pathNames = []
for path in pathlist:
    pathNames.append(path.parts[1])
    print(str(path))
    # because path is object not strin
    if pathInd == 0:
        output, _ = extractSilhouette(str(path))
        dataMat = output
    else:
        output, _ = extractSilhouette(str(path))
        dataMat = np.c_[dataMat,output]
    pathInd += 1
    #print(path_in_str)
    plt.plot(output)
    

plt.legend(pathNames)
plt.show()
row,cols = dataMat.shape

results = np.zeros(cols,'float')

# define a video capture object 
vid = cv2.VideoCapture(0)
frame_rate = 1
prev = 0

while(True): 
      
    # Capture the video frame 
    # by frame 
    time_elapsed = time.time() - prev
    ret, frame = vid.read() 
    
    if time_elapsed > 1./frame_rate:
        prev = time.time()
        frame = frame[300:700,450:850]
        
        
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      
        # Display the resulting frame 
        
          
        # the 'q' button is set as the 
        # quitting button you may use any 
        # desired button of your choice 
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break
      
        extractSilhouette(frame)
        for i in range(cols):
            output, edges = extractSilhouette(frame)
            temp = np.correlate(output,dataMat[:,i])
            results[i] = temp[0]
            
        plt.plot(output)
        plt.show()

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame,str(pathNames[np.argmax(results)]),(10,30),font, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imshow('frame', frame) 
        
        cv2.imshow('edges', edges) 
    
        print(np.argmax(results))
        print(pathNames[np.argmax(results)])
    
# After the loop release the cap object 
vid.release() 
# Destroy all the windows 
cv2.destroyAllWindows() 
