import UserAuthenticate
from CENTRAL_SERVER import SlideApplication
from CENTRAL_SERVER import simpleslideinterface
import unittest
from datetime import datetime
import sys

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
    
    def test_sending(self):
        self.assertTrue(SlideApplication.OpenSlide('8808-04Ep', 'Cell seed detection and counting', datetime.now(), 'admin'))
        
if __name__ == '__name__':
    unittest.main()