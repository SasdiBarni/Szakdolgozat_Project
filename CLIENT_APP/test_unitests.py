import UserAuthenticate
import CENTRAL_SERVER
import unittest

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
        self.assertEqassertFalseual(UserAuthenticate.LoginAuthenticate('ajsndasbid','afaweggrrg'))
    
    def test_login7(self):
        self.assertTrue(UserAuthenticate.LoginAuthenticate('admin','admin'))

class Test_FileSendingAndOpeningTest(unittest.TestCase):
    
    def test_sending(self):
        self.assertEqual(CENTRAL_SERVER.SlideApplicaion.OpenSlide())
        
if __name__ == '__name__':
    unittest.main()