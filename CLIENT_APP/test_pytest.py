import UserAuthenticate

def loginTest1():
    assert UserAuthenticate.LoginAuthenticate('','') == False
    
def loginTest2():
    assert UserAuthenticate.LoginAuthenticate('admin','aojsndiasd') == False

def loginTest3():
    assert UserAuthenticate.LoginAuthenticate('ajsndasbid','admin') == False
    
def loginTest4():
    assert UserAuthenticate.LoginAuthenticate('aecacad','efefawfwef') == False
    
def loginTest5():
    assert UserAuthenticate.LoginAuthenticate('','sdvcewavf') == False
    
def loginTest1():
    assert UserAuthenticate.LoginAuthenticate('FEFAEWGREGAE','') == False
    
def loginTest1():
    assert UserAuthenticate.LoginAuthenticate('admin','admin') == True