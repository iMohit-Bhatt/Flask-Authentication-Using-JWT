from app import app, Resource, ns, fields
from flask import request, make_response, render_template
from Login.service import Login
from CommonFunc.ReturnFunc import ReturnFunc
from CommonFunc.CustomException import CustomException
from datetime import datetime, timedelta

import logging, requests, jwt

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

rf = ReturnFunc()
login = Login()


@ns.route('/dashboard', methods=['GET'])
class LoginRoutes(Resource):
    
    def login_required(func):
        def wrapper(*args, **kwargs):
            try:
                token = request.headers.get('Authorization')
                    
                if not token:
                    raise CustomException("please send the Authorization Bearer token in the headers", 400)
                
                if 'Bearer' not in token:
                    raise CustomException("Send Bearer token", 403)
                
                token = token.split(' ')[1]

                try:
                    decoded_token = jwt.decode(token, app.config['SECRET_KEY'], 'HS256')

                    if decoded_token['expiration'] < str(datetime.utcnow()):
                        raise jwt.ExpiredSignatureError
                
                except jwt.ExpiredSignatureError:
                    raise CustomException("Token is expired", 403)
                
                except jwt.InvalidSignatureError:
                    raise CustomException("Invalid Signation", 403)

                except jwt.DecodeError:
                    raise CustomException("Invalid token error", 403)
                
                return func(*args, **kwargs)
                
            except CustomException as e:
                return make_response(rf.return_func(data="", error="True", code=e.status_code, message=f"{e}", details=""), e.status_code) 
                
            except Exception as e:
                logger.debug(str(e))
                return make_response(rf.return_func(data="", error="True", code="500", message="Got an unexpected error", details=""), 500)

        return wrapper

    @login_required
    def get(self):
        try:
            
            return make_response(rf.return_func(data="Welcome to the Dashboard", error="False", code="", message="", details=""), 200) 
        
        except CustomException as e:
            return make_response(rf.return_func(data="", error="True", code=e.status_code, message=f"{e}", details=""), e.status_code) 
            
        except Exception as e:
            logger.debug(str(e))
            return make_response(rf.return_func(data="", error="True", code="500", message="Got an unexpected error", details=""), 500)

