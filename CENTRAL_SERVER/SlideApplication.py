import simpleslideinterface
import json
import numpy as np
from numpy import asarray
import cv2
import os

def OpenSlide(directoryName, jobId, date, user):
    
    base_url='http://localhost:5120/'
    ssi = simpleslideinterface.MinimalWrapper(base_url=base_url, raise_for_status=True)
    
    slide_path = f'C:\\Users\\sasdi\\Documents\\Szakdolgozat_Project\\FILE_SERVER\\slides\\{directoryName}\\{directoryName}'
    #slide_path = f'media\\nfs\\slides\\{directoryName}\\{directoryName}'
    slide_token = ssi.post('slide/open/local/{}', slide_path, readonly=True).json()
    print(f'Created slide token: [{slide_token}]')
    
    print('Slide Properties:')
    properties = ssi.get('slide/{}/base_properties', slide_token).json()
    print(json.dumps(properties, indent=4))
    
    #used only for the unit tests
    #return properties
    
    GetTilesFromSlide(ssi, slide_token, properties, jobId, directoryName, date, user)
    

def GetTilesFromSlide(ssi, slide_token, properties, jobId, directoryName, date, user):
    
    if jobId == 'Cell seed detection and counting':
        
        seedNum = 0
        
        width = int(int(properties['Width']) / 256 / 2)
        height = int(int(properties['Height']) / 256 / 2)
      
        for i  in range(width):
            for j in range(height):
                
                image = ssi.get_image('slide/{}/tile', slide_token, encoding='BMP_RAW', x1=i, y1=j, x2=i, y2=j, magnification=1)
                numpyArray= asarray(image)
                
                if np.mean(numpyArray) == 255:
                    print(f'---PROCESSING--- {i + 1}/{width} - {j + 1}/{height} ', end = '\r')

                    continue
                else:
                    gray = cv2.cvtColor(numpyArray, cv2.COLOR_BGR2GRAY)

                    thresh_for_seeds = cv2.threshold(gray, 135, 255, cv2.THRESH_TOZERO_INV)[1]

                    cnts_for_seeds = cv2.findContours(thresh_for_seeds, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                    cnts_for_seeds = cnts_for_seeds[0] if len(cnts_for_seeds) == 2 else cnts_for_seeds[1]

                    min_area = 1
                    black_dots = []

                    for c in cnts_for_seeds:
                        area = cv2.contourArea(c)
                        if area > min_area:
                            cv2.drawContours(numpyArray, [c], -1, (36, 255, 12), 1)
                            black_dots.append(c)
                            
                    #cv2.imwrite(f'C:\\Users\\sasdi\\Documents\\Szakdolgozat_Project\\CENTRAL_SERVER\\contours\\{i}_{j}.jpg', numpyArray) 
                    
                    seedNum += len(black_dots)
        
        path = 'C:\\Users\\sasdi\\Documents\\Szakdolgozat_Project\\FILE_SERVER\\results\\results.txt'
        
        check_file = os.path.exists(path)
        
        if not check_file:
            result = open('C:\\Users\\sasdi\\Documents\\Szakdolgozat_Project\\FILE_SERVER\\results\\results.txt', 'w')
            result.write(f'{date} - {user} - {directoryName} - {jobId} :: {str(seedNum)}\n')
            print('[SERVER] Finished!')
        else:
            result.write(f'{date} - {user} - {directoryName} - {jobId} :: {str(seedNum)}\n')
            print('[SERVER] Finished!')
        
        #result = open(f'media\\nfs\\results\\{directoryName}.txt', 'w')