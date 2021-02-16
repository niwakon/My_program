import socket
import random
import hashlib
from time import sleep
from web3 import Web3,HTTPProvider
from eth_account.messages import encode_defunct

web3 = Web3(HTTPProvider('rinkebyのinfuraアドレス'))
address = bytes.fromhex("コントラクトのアドレス")
abi = [
	{
		"inputs": [],
		"payable": False,
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "vendor",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "model",
				"type": "string"
			},
			{
				"indexed": True,
				"internalType": "uint256",
				"name": "ver",
				"type": "uint256"
			},
			{
				"indexed": False,
				"internalType": "bytes32",
				"name": "hash",
				"type": "bytes32"
			}
		],
		"name": "NewVer",
		"type": "event"
	},
	{
		"constant": False,
		"inputs": [
			{
				"internalType": "string",
				"name": "_model",
				"type": "string"
			},
			{
				"internalType": "address[]",
				"name": "_pubkey",
				"type": "address[]"
			},
			{
				"internalType": "uint256",
				"name": "len",
				"type": "uint256"
			}
		],
		"name": "registDevice",
		"outputs": [],
		"payable": False,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "vendor",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "model",
				"type": "string"
			},
			{
				"indexed": False,
				"internalType": "address[]",
				"name": "pubkey",
				"type": "address[]"
			}
		],
		"name": "RegistDevice",
		"type": "event"
	},
	{
		"constant": False,
		"inputs": [
			{
				"internalType": "string",
				"name": "_url",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_model",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "_ver",
				"type": "uint256"
			},
			{
				"internalType": "bytes",
				"name": "sign",
				"type": "bytes"
			}
		],
		"name": "registURL",
		"outputs": [],
		"payable": False,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "distributer",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "URL",
				"type": "string"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "model",
				"type": "string"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "ver",
				"type": "uint256"
			}
		],
		"name": "RegistURL",
		"type": "event"
	},
	{
		"constant": False,
		"inputs": [
			{
				"internalType": "string",
				"name": "model",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "ver",
				"type": "uint256"
			},
			{
				"internalType": "bytes",
				"name": "signature",
				"type": "bytes"
			},
			{
				"internalType": "address",
				"name": "pk_d",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "ts",
				"type": "uint256"
			}
		],
		"name": "reportUpdate",
		"outputs": [],
		"payable": True,
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": True,
				"internalType": "address",
				"name": "device",
				"type": "address"
			},
			{
				"indexed": True,
				"internalType": "address",
				"name": "distributor",
				"type": "address"
			},
			{
				"indexed": False,
				"internalType": "string",
				"name": "model",
				"type": "string"
			},
			{
				"indexed": False,
				"internalType": "uint256",
				"name": "ver",
				"type": "uint256"
			},
			{
				"indexed": False,
				"internalType": "bytes32",
				"name": "hash_u",
				"type": "bytes32"
			}
		],
		"name": "ReportUpdate",
		"type": "event"
	},
	{
		"constant": False,
		"inputs": [
			{
				"internalType": "string",
				"name": "_model",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "_ver",
				"type": "uint256"
			},
			{
				"internalType": "bytes32",
				"name": "_hash",
				"type": "bytes32"
			},
			{
				"internalType": "string",
				"name": "url",
				"type": "string"
			}
		],
		"name": "upVendor",
		"outputs": [],
		"payable": True,
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"constant": False,
		"inputs": [
			{
				"internalType": "string",
				"name": "_model",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "_ver",
				"type": "uint256"
			},
			{
				"internalType": "bytes32",
				"name": "_hash",
				"type": "bytes32"
			}
		],
		"name": "withdrawFunds",
		"outputs": [],
		"payable": True,
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [
			{
				"internalType": "bytes",
				"name": "pub",
				"type": "bytes"
			}
		],
		"name": "calculateAddress",
		"outputs": [
			{
				"internalType": "address",
				"name": "addr",
				"type": "address"
			}
		],
		"payable": False,
		"stateMutability": "pure",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [
			{
				"internalType": "address",
				"name": "pk_d",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "ver",
				"type": "uint256"
			}
		],
		"name": "checkDevice",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "done_update",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"name": "eth_addr_URL",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "firmware",
		"outputs": [
			{
				"internalType": "bytes32",
				"name": "",
				"type": "bytes32"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [
			{
				"internalType": "address",
				"name": "_vendor",
				"type": "address"
			}
		],
		"name": "getInfo",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			},
			{
				"internalType": "bytes32",
				"name": "",
				"type": "bytes32"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [
			{
				"internalType": "address",
				"name": "_vendor",
				"type": "address"
			}
		],
		"name": "getNumUpLog",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [
			{
				"internalType": "string",
				"name": "_model",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "_ver",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "num",
				"type": "uint256"
			}
		],
		"name": "getURL",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [
			{
				"internalType": "string",
				"name": "_model",
				"type": "string"
			}
		],
		"name": "getVersion",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			},
			{
				"internalType": "bytes32",
				"name": "",
				"type": "bytes32"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "list_device",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "log_update",
		"outputs": [
			{
				"internalType": "address",
				"name": "distributor",
				"type": "address"
			},
			{
				"internalType": "string",
				"name": "model",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "ver",
				"type": "uint256"
			},
			{
				"internalType": "bytes32",
				"name": "hash_u",
				"type": "bytes32"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "log_ven",
		"outputs": [
			{
				"internalType": "string",
				"name": "model",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "ver",
				"type": "uint256"
			},
			{
				"internalType": "bytes32",
				"name": "hash_u",
				"type": "bytes32"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"name": "num_device",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [
			{
				"internalType": "bytes32",
				"name": "",
				"type": "bytes32"
			}
		],
		"name": "period",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [
			{
				"internalType": "bytes32",
				"name": "",
				"type": "bytes32"
			}
		],
		"name": "reward",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [
			{
				"internalType": "bytes32",
				"name": "",
				"type": "bytes32"
			}
		],
		"name": "reward_pay",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "URL",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"name": "vendor",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [
			{
				"internalType": "string",
				"name": "model",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "ver",
				"type": "uint256"
			},
			{
				"internalType": "address",
				"name": "pk_d",
				"type": "address"
			},
			{
				"internalType": "bytes",
				"name": "signature",
				"type": "bytes"
			},
			{
				"internalType": "bytes32",
				"name": "h_u",
				"type": "bytes32"
			},
			{
				"internalType": "uint256",
				"name": "ts",
				"type": "uint256"
			}
		],
		"name": "verify_Update3",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [
			{
				"internalType": "address",
				"name": "_vendor",
				"type": "address"
			},
			{
				"internalType": "bytes",
				"name": "signature",
				"type": "bytes"
			},
			{
				"internalType": "bytes32",
				"name": "h_u",
				"type": "bytes32"
			}
		],
		"name": "verifyDistributor",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"name": "version",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	}
]
mycontract = web3.eth.contract(address=address, abi=abi)

sk = bytes.fromhex("配布者の秘密鍵")
pk = "配布者の公開鍵"
eth_address = "配布者のEthereumアドレス"
firmware = {'0x52d1b856e53afba25b7cc7ebd4b2870d04165fb2818c14d89e8fc8bb31ad8e95':"firmware.txt"} #ファイル名
f_info = {'52d1b856e53afba25b7cc7ebd4b2870d04165fb2818c14d89e8fc8bb31ad8e95':('model1', 1)} # ファームウェア情報
num_Log = {'0xc8ef0d029f8ee878b951e6bd8cdd346700c8e517':1}
addr_vendor = bytes.fromhex("ベンダーのアドレス")

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
		"""実行関数"""
		client, addr = self.socket.accept()
		print("connection_by" + str(client))
		print("connection addr" + str(addr))
		while True:
			# ダウンロードリクエスト受信
			data = client.recv(1024).decode()
			if not data:
				client.close()
				break
			sig, ver, h_u, pk_IoT = data.split(',')
			ver = int(ver)
			adder_IoT = mycontract.functions.calculateAddress(pk_IoT).call()
			model = mycontract.functions.list_device(adder_IoT).call()
			# 署名検証
			msg = encode_defunct(text=(str(ver)+","+h_u))
			check = (web3.eth.account.recover_message(msg, signature= bytes.fromhex(sig[2:])) == adder_IoT)
			print("sig2")
			print(check)
			# 通信相手がアップデート対象かどうか検証
			check1 = f_info[h_u][0] == model and f_info[h_u][1] == ver
			check2 = mycontract.functions.checkDevice(adder_IoT, ver).call()
			if not (check1 and check2):
				print("unkown device")
				client.close()
				break
			if check:
				# sign(Uid, eth_address, adder_IoT)送信
				Uid = fileHash("firmware.txt")
				print("file hash: ",Uid)
				m = Uid + eth_address + adder_IoT
				sign_m = self.Sig_M2(m)
				data = (sign_m.hex() + "," + eth_address).encode()					
				print("data_send: ", data)
				client.send(data)
				# ファームウェア送信
				f = open('./firmware.txt', "rb")
				l = f.read(1024)
				while l:
					client.send(l)
					l = f.read(1024)
				f.close()
				print("send file")
				#証拠受け取り
				data = client.recv(1024).decode()
				sign_d, ts = data.split(",")
				ts = int(ts)
				print(sign_d, ts)
				print(model,"\n pk: ",adder_IoT,"\ndata: ",data, "\nuid: ",Uid)
				print(mycontract.functions.verify_Update3(model, ver, adder_IoT, sign_d, Uid, ts).call({"from": eth_address}))
				# トランザクション送信
				tr = mycontract.functions.reportUpdate(model, ver, sign_d, adder_IoT, ts).buildTransaction({
                    "from": eth_address,
                    "nonce": web3.eth.getTransactionCount(eth_address),
                    "gas": 5000000,
                    "gasPrice": web3.eth.gasPrice,
                    "value": 0
                    })
				signed_txn = web3.eth.account.signTransaction(tr, sk)
				tx = web3.eth.sendRawTransaction(signed_txn.rawTransaction) 
				print("done: ", tx.hex())
			client.close()
			print('close')
			break
		
	def Sig_M2(self, c):
		message = encode_defunct(text=c)
		singed_m = web3.eth.account.sign_message(message,private_key=sk)
		print("sig: ", singed_m.signature)
		return singed_m.signature

def fileHash(path):
		algo = 'sha256'
		h = hashlib.new(algo)
		Length = hashlib.new(algo).block_size * 0x800
		with open(path, 'rb') as f:
			BinaryData = f.read(Length)
			
			while BinaryData:
				h.update(BinaryData)
				BinaryData = f.read(Length)
		return h.hexdigest()

if __name__ == '__main__':
	ip = '127.0.0.1'
	port = int('8000')
	server = Server(ip, port)
	while True:
		server.start()