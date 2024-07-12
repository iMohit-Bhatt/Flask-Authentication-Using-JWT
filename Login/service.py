from app import db
from flask import request, make_response, render_template
from Login.interface import LoginInterface
from Login.model import *
from CommonFunc.CustomException import CustomException
from CommonFunc.ReturnFunc import ReturnFunc
import uuid, logging, hashlib, jwt
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

rf = ReturnFunc()

class Login(LoginInterface):
    
    def user_login(self, data):
        try:
            if 'user_name' in data:
                user = Users().query.filter_by(user_name = data['user_name']).first()
            elif 'email' in data:
                user = Users().query.filter_by(email = data['email']).first()
            elif 'mobile':
                user = Users().query.filter_by(user_name = data['mobile']).first()
            else:
                pass

            if not user:
                raise CustomException(f"User not found", 404)
            
            salt = user.salt
            hashed_pass = user.password
            
            if 'password' not in data:
                raise CustomException(f"please enter password in password field", 400)
            
            user_pass = data['password'] + str(salt)

            user_hashed_pass = hashlib.md5(user_pass.encode()).hexdigest()

            if user_hashed_pass == hashed_pass:

                key = next((k for k in ['user_name', 'email', 'mobile'] if k in data), 'mobile')
                value = data.get(key)

                token = jwt.encode(
                    {key: value, "expiration" : str(datetime.utcnow() + timedelta(seconds= 120))},
                    app.config['SECRET_KEY']
                )

                response = {"token": token}
                return make_response(rf.return_func(data=response, error="False", code="200", message="", details=""), 200)
            
            else:
                raise CustomException("Worng Credentials", 400)

        except CustomException as e:
            return make_response(rf.return_func(data="", error="True", code=e.status_code, message=f"{e}", details=""), e.status_code) 
            
        except Exception as e:
            logger.debug(str(e))
            return make_response(rf.return_func(data="", error="True", code="500", message="Got an unexpected error", details=""), 500)