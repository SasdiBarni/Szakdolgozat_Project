import UserAuthenticate
from CENTRAL_SERVER import SlideApplication
import simpleslideinterface
import unittest
from datetime import datetime
import sys, os

class Test_LoginTests(unittest.TestCase):
    
    def test_login1(self):
        self.assertFalse(UserAuthenticate.LoginAuthenticate('',''))
    
    def test_login2(self):
        self.assertFalse(UserAuthenticate.LoginAuthenticate('admin','aojsndiasd'))

    def test_login3(self):
        self.assertFalse(UserAuthenticate.LoginAuthenticate('ajsndasbid','admin'))
    
    def test_login4(self):
        self.assertFalse(UserAuthenticate.LoginAuthenticate('ajsndasbid',''))
    
    def test_login5(self):
        self.assertFalse(UserAuthenticate.LoginAuthenticate('','asdwcewvef'))
    
    def test_login6(self):
        self.assertFalse(UserAuthenticate.LoginAuthenticate('ajsndasbid','afaweggrrg'))
    
    def test_login7(self):
        self.assertTrue(UserAuthenticate.LoginAuthenticate('admin','admin'))

class Test_FileSendingAndOpeningTest(unittest.TestCase):
    
    sys.path.insert(0, 'C:\\Users\\sasdi\\Documents\\Szakdolgozat_Project\\CLIENT_APP')
    
    def test_notEmpty(self):
        self.assertNotEqual(SlideApplication.OpenSlide('8808-04Ep', 'Cell seed detection and counting', datetime.now(), 'admin'), '')
    
    def test_name(self):
        self.assertEqual(SlideApplication.OpenSlide('8808-04Ep', 'Cell seed detection and counting', datetime.now(), 'admin')['OriginalName'], '8808-04Ep')
        
    def test_width(self):
        self.assertEqual(str(SlideApplication.OpenSlide('8808-04Ep', 'Cell seed detection and counting', datetime.now(), 'admin')['Width']), '67584')
    
    def test_height(self):
        self.assertEqual(str(SlideApplication.OpenSlide('8808-04Ep', 'Cell seed detection and counting', datetime.now(), 'admin')['Height']), '153856')
        
    def test_size(self):
        self.assertEqual(int(SlideApplication.OpenSlide('8808-04Ep', 'Cell seed detection and counting', datetime.now(), 'admin')['Size']), 60376325)
        
    def test_correctSending(self):
        
        path1 = 'C:\\Users\\sasdi\\Documents\\Szakdolgozat_Project\\CLIENT_APP\\8808-04Ep'
        files1 = sorted(os.listdir(path1))
        
        print(files1)
        
        path2 = 'C:\\Users\\sasdi\\Documents\\Szakdolgozat_Project\\FILE_SERVER\\slides\\8808-04Ep'
        files2 = sorted(os.listdir(path2))
        
        self.assertEqual(files1, files2)
        
        
if __name__ == '__name__':
    unittest.main()