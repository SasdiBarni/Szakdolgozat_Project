import simpleslideinterface
import json

base_url='http://localhost:5120/'
ssi = simpleslideinterface.MinimalWrapper(base_url=base_url, raise_for_status=True)

#! change local path to path on file server, add directory name to end
def OpenSlide(ssi, directory_name):
    
    slide_path = 'C:\\Users\\sasdi\\Documents\\Szakdolgozat_Project\\CLIENT_APP\\8808-04Ep\\8808-04Ep' #*Change path here
    slide_token = ssi.post('slide/open/local/{}', slide_path, readonly=True).json()
    print('Created slide token:', slide_token)
    
    print('Properties:')
    properties = ssi.get('slide/{}/base_properties', slide_token).json()
    print(json.dumps(properties, indent=4))
    
    GetTilesFromSlide(ssi, slide_token, properties)

def GetTilesFromSlide(ssi, slide_token, properties):
    
    width = int(int(properties['Width']) / 256 / 2)
    height = int(int(properties['Height']) / 256 / 2)
    
    #! Change the save path here later
    
    for i  in range(width):
        for j in range(height):
            image = ssi.get_image('slide/{}/tile', slide_token, encoding='BMP_RAW', x1=i, y1=j, x2=i, y2=j, magnification=1)
            image.save('C:\\Users\\sasdi\\Documents\\Szakdolgozat_Project\\CENTRAL_SERVER\\TILES\\' + slide_token + '__'+ str(i) + '__' + str(j) + '.bmp') #*Change the save path here
