import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def get_p(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048))
        except Exception as e:
            print(f"Error en connect: {e}")
            return None

    def send(self, data):
        try:
            serialized_data = pickle.dumps(data)
            self.client.send(serialized_data)
            
            # Recibir datos en partes
            full_data = b''
            while True:
                part = self.client.recv(2048)
                if not part:
                    break
                full_data += part
                if len(part) < 2048:
                    break
                    
            return pickle.loads(full_data)
        except socket.error as e:
            print(f"Error en send: {e}")
            raise e
    
