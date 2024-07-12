from flask import jsonify

class ReturnFunc():
    def return_func(self, data, error, code, message, details):
        if error == 'False':
            success = True
            code = None
            message = None
            details = None
        else:
            success = False
            data= None

        return jsonify({
                    "success": success,             
                    "data": data,               
                    "error": {
                        "code": code,              
                        "message": message,           
                        "details": details           
                    }
            })
