"""This is client.py"""
import socket
import sys
import hashlib
from web3 import Web3,HTTPProvider
from eth_account.messages import encode_defunct
# rinkeby でブロックナンバー取るためのおまじない
from web3.middleware import geth_poa_middleware

web3 = Web3(HTTPProvider('rinnkebyのinfuraのアドレス'))
# rinkeby でブロックナンバー取るためのおまじない
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

address = bytes.fromhex("コントラクトアドレス")
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

pk = "IoT機器の公開鍵"
eth_address = "IoT機器のehtereumアドレス"
model = "model1"
version = 0
vendor_address = bytes.fromhex("ベンダーのEthereumアドレス")
# 更新情報
new_ver = 0
hash_u = ""

# solidity で検証用
# 例) m = Sig_M(int(data))
#    data = (m.hex() +"," +pk).encode()
def Sig_done(adder_dis, model_up, ver_new, hash_f, ts):
    sk = bytes.fromhex("IoT機器の秘密鍵")
    hash_c = web3.soliditySha3(
              ["address", "string", "uint256", "bytes32", "uint256"],
              [adder_dis, model_up, ver_new, hash_f, ts]
              ).hex()
    message = encode_defunct(hexstr=hash_c)
    return web3.eth.account.sign_message(message,private_key=sk).signature

# local(web3.eth.account.recover_messageで検証可能)
def Sig_M2(c):
    sk = bytes.fromhex("IoT機器の秘密鍵")
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

# ver を上手く更新できない為
def updateVer(new_ver):
	version = new_ver

def main():
    # 最新の更新情報を取得
	new_ver, hash_u = mycontract.functions.getVersion(model).call()
	print( new_ver, hash_u)
	print(version, model)
	if version <= new_ver:
		# url を元に接続する
		url, address_dis = mycontract.functions.getURL(model, new_ver, 1).call({'from': eth_address})
		print(address_dis)
		ip, port = url.split(":")
		port = int(port)
		# # """This is a program when it comes to crient"""
		socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    
		socket1.connect((ip, port))
		while True:
			# ダウンロードリクエスト(ver, pk, hash_u, sig(ver,pk,hash_u)) を送信
			data = str(new_ver)+","+hash_u.hex() 
			m = Sig_M2(data)
			data = (m.hex() + "," + data +","+ pk).encode()
			print("client: ", data)
			socket1.send(data)
			# ファームウェア受け取り: 署名受信
			data = socket1.recv(1024).decode()
			if not data:
				socket1.close()
				break
			sig, address_check = data.split(',')
			if address_check != address_dis:
				print("not addr:", address_check)
				socket1.close()
				break
			print("sig: ",sig, "\n address_d:", address_dis)
			# 署名検証
			msg = encode_defunct(text=(hash_u.hex() + address_dis + eth_address))
			adder = web3.eth.account.recover_message(msg, signature = bytes.fromhex(sig[2:]))
			check = (adder == address_dis)
			print(check)
			if check:
				# ファームウェア受信
				f = open('Get_file.txt','wb') #ファームウェアのファイル名
				while True:
					l = socket1.recv(1024)
					while l:
						f.write(l)
						if len(l) != 1024:
							break
						l = socket1.recv(1024)
					break
				f.close()
				print("get file")
				# ファームウェア検証
				f_h = fileHash("Get_file.txt")
				check = (f_h == hash_u.hex())
				print(f_h)
				print(hash_u.hex())
				print("f_h:",check )
				if check:
					# 証拠署名の送信 sign(address of distributer, model, ver, timestamp)
					msg = address_dis + model + str(new_ver)
					latest = web3.eth.blockNumber - 10
					ts = web3.eth.getBlock(latest).timestamp					
					print(ts)
					sig = Sig_done(address_dis, model, new_ver, ("0x"+f_h), ts)
					data = (sig.hex() + "," + str(ts)).encode()
					print(sig.hex())
					socket1.send(data)
					updateVer(new_ver)
			socket1.close()
			break
			if not data:
				socket1.close()
				break

if __name__ == '__main__':
	main()
