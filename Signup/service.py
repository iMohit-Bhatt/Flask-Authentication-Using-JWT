from app import db
from flask import request, make_response
from Signup.interface import SignupInterface
from Login.model import *
from CommonFunc.CustomException import CustomException
from CommonFunc.ReturnFunc import ReturnFunc

import uuid, logging, random, hashlib, re

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

rf = ReturnFunc()

class Signup(SignupInterface):

    users_column_names = [column.name for column in Users.__table__.columns]
    required_keys = ["name", "user_name", "password", "mobile", "email"]
    neglected_keys = ['id', 'created_on', 'salt', 'modified_on']

    def user_signup(self, data):
        try:

            payload_keys = [key for key in data]   

            for key in self.required_keys:
                if key not in payload_keys:
                    raise CustomException(f"Plese send required keys: {self.required_keys}", 400)
            
            users = Users()

            for key, value in data.items():

                if key not in self.users_column_names or (key in self.users_column_names and key in self.neglected_keys):
                    raise CustomException(f"{key} is not a valid key", 400)
                
                elif key == 'password':
                    password = value

                elif key == 'user_name':
                    user_found = Users().query.filter_by(user_name = value).first()
                    if user_found:
                        raise CustomException(f"{value} is not available", 400)

                elif key == 'mobile':
                    pattern = re.compile(r'^[789]\d{9}$')
                    if not pattern.match(value):
                       raise CustomException(f"Enter a valid mobile number without country code", 400)
                    
                    user_found = Users().query.filter_by(mobile = value).first()
                    if user_found:
                        raise CustomException(f"{value} already exsist", 400)

                elif key == 'email':
                    pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
                    if not pattern.match(value):
                       raise CustomException(f"Enter a valid email id", 400) 
                    
                    user_found = Users().query.filter_by(email = value).first()
                    if user_found:
                        raise CustomException(f"{value} already exsist", 400)
                
                setattr(users, key, value)
            
            salt = random.randint(100000, 999999)
            users.salt = salt

            password = str(password) + str(salt)
            hashed_password = hashlib.md5(password.encode()).hexdigest()
            
            users.password = hashed_password

            db.session.add(users)
            db.session.commit()

            return make_response(rf.return_func(data="User created successfully", error="False", code=200, message="", details=""), 200)

        except CustomException as e:
            return make_response(rf.return_func(data="", error="True", code=e.status_code, message=f"{e}", details=""), e.status_code) 
            
        except Exception as e:
            logger.debug(str(e))
            return make_response(rf.return_func(data="", error="True", code="500", message="Got an unexpected error", details=""), 500)