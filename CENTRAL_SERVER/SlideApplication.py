import simpleslideinterface
import json
import numpy as np

base_url='http://localhost:5120/'
ssi = simpleslideinterface.MinimalWrapper(base_url=base_url, raise_for_status=True)

#! ADD TO FRONT OF PATH '\\\\192.168.0.1\\' SERVER IP
def OpenSlide(ssi, directoryName):
    
    slide_path = f'C:\\Users\\sasdi\\Documents\\Szakdolgozat_Project\\FILE_SERVER\\slides\\{directoryName}\\{directoryName}'
    slide_token = ssi.post('slide/open/local/{}', slide_path, readonly=True).json()
    print('Created slide token:', slide_token)
    
    print('Properties:')
    properties = ssi.get('slide/{}/base_properties', slide_token).json()
    print(json.dumps(properties, indent=4))
    
    GetTilesFromSlide(ssi, slide_token, properties)

def GetTilesFromSlide(ssi, slide_token, properties):
    
    width = int(int(properties['Width']) / 256 / 2)
    height = int(int(properties['Height']) / 256 / 2)
    
    #! Saving is not needed for tiles    
    for i  in range(width):
        for j in range(height):
            image = ssi.get_image('slide/{}/tile', slide_token, encoding='BMP_RAW', x1=i, y1=j, x2=i, y2=j, magnification=1)
            
            if np.mean(image) == 255:
                print()
            else:
                print()
                #else ágon lesz a feldolgozás
                
            #image.save('C:\\Users\\sasdi\\Documents\\Szakdolgozat_Project\\CENTRAL_SERVER\\TILES\\' + slide_token + '__'+ str(i) + '__' + str(j) + '.bmp')
