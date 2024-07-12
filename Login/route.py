from app import app, Resource, ns, fields
from flask import request, make_response
from Login.service import Login
from CommonFunc.ReturnFunc import ReturnFunc
from CommonFunc.CustomException import CustomException

import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

rf = ReturnFunc()
login = Login()


@ns.route('/user/login', methods=['POST'])
class LoginRoutes(Resource):
    
    def post(self):
        try:
            unknown_query_params = set(request.args.keys()) - {'limit', 'from', 'sort', 'order'}

            if unknown_query_params:
                raise CustomException(f'Unknown query parameter(s): {", ".join(unknown_query_params)}', 400)
            
            return login.user_login(request.json)
        
        except CustomException as e:
            return make_response(rf.return_func(data="", error="True", code=e.status_code, message=f"{e}", details=""), e.status_code) 
            
        except Exception as e:
            logger.debug(str(e))
            return make_response(rf.return_func(data="", error="True", code="500", message="Got an unexpected error", details=""), 500)