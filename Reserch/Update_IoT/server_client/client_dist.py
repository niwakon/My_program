import socket
import random
import hashlib
from multiprocessing import Process
from time import sleep
from web3 import Web3,HTTPProvider
from eth_account.messages import encode_defunct

web3 = Web3(HTTPProvider('rinkebyのinfuraアドレス'))

address = bytes.fromhex("スマートコントラクトのethereumアドレス")
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

sk = bytes.fromhex("配布者の秘密鍵(ECDSA)")
pk = "配布者の公開鍵"
eth_address = "配布者のEthereumアドレス"
#firmware = {'0x52d1b856e53afba25b7cc7ebd4b2870d04165fb2818c14d89e8fc8bb31ad8e95':"firmware.txt"} #ファイル名
#f_info = {'52d1b856e53afba25b7cc7ebd4b2870d04165fb2818c14d89e8fc8bb31ad8e95':('type1', 1)} # ファームウェア情報
num_Log = {'0xc8ef0d029f8ee878b951e6bd8cdd346700c8e517':0}
firmware={}
f_info={}
addr_vendor = bytes.fromhex("ベンダーのethereumアドレス")


def Sig_M2(self, c):
	message = encode_defunct(text=c)
	singed_m = web3.eth.account.sign_message(message,private_key=sk)
	print("sig: ", singed_m.signature)
	return singed_m.signature

def client(ip, port, h_f, model, ver):
    socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
    socket1.connect((ip, port))
    while True:
        # リクエスト(ハッシュ、ethreumアドレス送信)
        data = ('0x'+h_f.hex() + "," + eth_address).encode()
        socket1.send(data)
        print("send: ",data)
		# 署名受信
        sign = socket1.recv(1024).decode()
        # ファームウェア受信
        f_name = 'firmware'+str(len(firmware))+".txt"
        f = open(f_name,'wb')
        while True:
            l = socket1.recv(1024)
            while l:
                f.write(l)
                l = socket1.recv(1024)
            break
        f.close()
        socket1.close()
        sleep(5)
        #　正しくファイルを入手できた検証
        f_h = fileHash(f_name)
        print("f_h:", f_h, "\n h_f: ", h_f.hex())
        if f_h != h_f.hex():
            return False
        firmware[h_f] = f_name
        tr = mycontract.functions.registURL("127.0.0.1:8000", model, ver, sign).buildTransaction({
                        "from": eth_address,
                        "nonce": web3.eth.getTransactionCount(eth_address),
                        "gas": 5000000,
                        "gasPrice": web3.eth.gasPrice,
                        "value": 0
                        })
        signed_txn = web3.eth.account.signTransaction(tr, sk)
        tx = web3.eth.sendRawTransaction(signed_txn.rawTransaction) 
        print("done: ",tx.hex())
        return True

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

# 更新情報の取得及びファイルの取得
def monitorBC():
    print("monitorBC")
    print(num_Log["0xc8ef0d029f8ee878b951e6bd8cdd346700c8e517"])
    len_log = mycontract.functions.getNumUpLog(addr_vendor).call()
    print(len_log)
    if len_log > num_Log["0xc8ef0d029f8ee878b951e6bd8cdd346700c8e517"]:
        up_model, new_ver, hash_u = mycontract.functions.getInfo(addr_vendor).call()
        url, address_dis = mycontract.functions.getURL(up_model, new_ver, 0).call()
        ip, port = url.split(":")
        port = int(port)
        success = client(ip, port, hash_u, up_model, new_ver)
        if success:
            num_Log["0xc8ef0d029f8ee878b951e6bd8cdd346700c8e517"] = len_log
            f_info[hash_u] = (up_model, new_ver)
            print("len_log: ", len_log)
            print(f_info[hash_u])
            print(firmware)
        print("monitor end")


while True:
	monitorBC()
	sleep(10)

