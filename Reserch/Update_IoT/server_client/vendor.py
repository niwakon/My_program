import socket
import random
import hashlib
from web3 import Web3,HTTPProvider
from eth_account.messages import encode_defunct

web3 = Web3(HTTPProvider('rinkebyのinfuraのアドレス'))

sk = bytes.fromhex("ベンダーの秘密鍵")
pk = "ベンダーの公開鍵"
eth_address = "ベンダーのEthereumアドレス"

h_f ={"0x52d1b856e53afba25b7cc7ebd4b2870d04165fb2818c14d89e8fc8bb31ad8e95":"original1.txt", "0xc5a99e3fb7eed332c6502097b997e6aa69ee83539590ec93846111b53a3d0297":"sc382_104.bin"}

class Server:
    """Server側のクラスを設定"""
    def __init__(self, server_ip, server_port):
        """初期化関数"""
        #ソケットを設定
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #ブロッキングモードに設定
        self.socket.setblocking(True)
        self.socket.bind((server_ip, server_port))
        self.socket.listen(1)

    def start(self):
        client, addr = self.socket.accept()
        print("connection_by" + str(client))
        print("connection addr" + str(addr))
        while True:
            # ダウンロードリクエストを受信
            data = client.recv(1024).decode()
            req, dist_addr = data.split(",")
            print('data: ', data)
            if req not in h_f:
                client.close()
                break
            f_name = h_f[req]
            # 署名生成・送信
            print(dist_addr, "\n", req)
            sign = self.Sig(dist_addr, req)
            client.send(sign.hex().encode())
            print("send sign")
            print(sign.hex())
            # ファームウェア送信
            f = open('./'+f_name, "rb")
            l = f.read(1024)
            while l:
                client.send(l)
                l = f.read(1024)
            f.close()
            print("send file")
            client.close()
            break
            
            if not data:
                client.close()
                break
    
    def Sig(self, adder_dis, hash_f):
        hash = web3.soliditySha3(
              ["address", "bytes32"],
              [adder_dis, hash_f]
              ).hex()
        message = encode_defunct(hexstr=hash)
        return web3.eth.account.sign_message(message,private_key=sk).signature

ip = '192.168.11.25'
port = int('9000')
server = Server(ip, port)
while True:
    server.start()