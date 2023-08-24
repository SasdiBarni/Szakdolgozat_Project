import simpleslideinterface
import CellSeedDetection as CDet
import json
import numpy as np
from numpy import asarray

base_url='http://localhost:5120/'
ssi = simpleslideinterface.MinimalWrapper(base_url=base_url, raise_for_status=True)


def OpenSlide(ssi, directoryName, jobId):
    
    #! ADD TO FRONT OF PATH '\\\\192.168.0.1\\' SERVER IP AND CHANGE ROUTE
    slide_path = f'C:\\Users\\sasdi\\Documents\\Szakdolgozat_Project\\FILE_SERVER\\slides\\{directoryName}\\{directoryName}'
    slide_token = ssi.post('slide/open/local/{}', slide_path, readonly=True).json()
    print(f'Created slide token: [{slide_token}]')
    
    print('Slide Properties:')
    properties = ssi.get('slide/{}/base_properties', slide_token).json()
    print(json.dumps(properties, indent=4))
    
    GetTilesFromSlide(ssi, slide_token, properties, jobId, directoryName)

def GetTilesFromSlide(ssi, slide_token, properties, jobId, directoryName):
    
    if jobId == 'Cell seed detection and counting':
        
        seedNum = 0
        
        width = int(int(properties['Width']) / 256 / 2)
        height = int(int(properties['Height']) / 256 / 2)
      
        for i  in range(width):
            for j in range(height):
                
                #converting img to npArray to filter out all white images
                image = ssi.get_image('slide/{}/tile', slide_token, encoding='BMP_RAW', x1=i, y1=j, x2=i, y2=j, magnification=1)
                numpyArray= asarray(image)
                
                if np.mean(numpyArray) == 255:
                    print(f'{i + 1}/{width} - {j + 1}/{height}')
                    continue
                else:
                    #!CELL SEED DETECTION, PUT HERE
                    seedNum += CDet.CellSeedDetectAndCount(image)
                    
        result = open(f'C:\\Users\\sasdi\\Documents\\Szakdolgozat_Project\\FILE_SERVER\\results\\{directoryName}.txt', 'w')
        
        result.write(str(seedNum))
                
    #image.save('C:\\Users\\sasdi\\Documents\\Szakdolgozat_Project\\CENTRAL_SERVER\\TILES\\' + slide_token + '__'+ str(i) + '__' + str(j) + '.bmp')
