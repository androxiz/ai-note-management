from passlib.context import CryptContext

pwd_cnxt = CryptContext(schemes='bcrypt', deprecated='auto')

class Hash:
    def hash(password:str):
        return pwd_cnxt.hash(password)
    
    def verify(hashed_password:str, plain_password:str):
        return pwd_cnxt.verify(plain_password, hashed_password)