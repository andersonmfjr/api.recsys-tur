from flask_restplus import Resource
import socket


class GetIp(Resource):
    def get(self):
        ip = socket.gethostbyname(socket.gethostname())
        return ip
