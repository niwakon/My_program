pragma solidity ^0.7.4;

contract ContactTrace{
    mapping(address=>bool) public vendors; //登録者が許可されてるベンダーか
    mapping(address=>address) public device_maker; // 登録されているdevice 公開鍵->販売者(vendor)のアドレス？
    mapping(address=>traceLog[]) public log_GPS; // ログ
    mapping(address=>keyLog[]) public log_Key;
    
    constructor() public {}
    
    event RegistDevice(address indexed vendor, address[] pubkey);
    event logGPS(address indexed sender, address indexed reciever, string gps, bytes ghash, string time);
    event logKey(address indexed sender, bytes key, bytes iv);
    
    struct traceLog{
        address sender;
        address reciever;
        string gps;
        bytes ghash;
        string time;
    }
    
    struct keyLog{
        bytes key;
        bytes iv;
    }
    
    // modelに対応したdeviceの登録 (とりあえず1つずつ)
    function registDevice(address[] memory _pubkey, uint256 len) public{
        //require(vendors[msg.sender]);
        for(uint256 i = 0; i < len; i++){
            //require(device_maker[_pubkey[i] == address(0)])
            // 二重登録防止
            require(device_maker[_pubkey[i]] == address(0));
            device_maker[_pubkey[i]] = msg.sender;
        }
        //num_device[_model] += len;
        emit RegistDevice(msg.sender, _pubkey);
    }
    
    // 位置情報等の記録
    function reportGPS(address _reciever, bytes memory _signature, string memory _time, string memory _gps, bytes memory _ghash, uint256 _nonce) public payable{
        address addr = getAddrfromSign(_signature, _time,_ghash, _nonce);
        // 登録されてるアドレスかつ自分で作ったものでない事を確認
        require(addr == _reciever);
        require(device_maker[addr] != address(0));
        require(addr != msg.sender);
        
        traceLog memory tLog = traceLog(msg.sender,addr, _gps, _ghash,  _time);
        log_GPS[msg.sender].push(tLog);
        emit logGPS(msg.sender, addr, _gps, _ghash, _time);
    }
    
    // 暗号鍵の記録(AES-CBCモード用)
    function storeKey(bytes memory _key, bytes memory _iv) public payable{
        keyLog memory kLog = keyLog(_key, _iv);
        log_Key[msg.sender].push(kLog);
        emit logKey(msg.sender, _key, _iv);
        
    }
    
    // 公開鍵からアドレス生成
    function calculateAddress(bytes memory pub) public pure returns (address addr) {
        bytes32 hash = keccak256(pub);
        assembly {
            mstore(0, hash)
            addr := mload(0)
        }
        return addr;
    }
    
    
    //署名からアドレス取得
    function getAddrfromSign(bytes memory signature, string memory time, bytes memory _ghash, uint256 nonce) public pure returns(address){
        bytes32 message = prefixed(keccak256(abi.encodePacked(time, _ghash, nonce)));
        return recoverSigner(message, signature);
    }
    /*
    //署名からアドレス取得
    function getAddrfromSign(bytes memory signature, string memory time, string memory lo, string memory la, uint256 nonce) public pure returns(address){
        bytes32 message = prefixed(keccak256(abi.encodePacked(time, lo, la, nonce)));
        return recoverSigner(message, signature);
    }*/
    
    /// signature methods.
    function splitSignature(bytes memory sig) internal pure returns (uint8 v, bytes32 r, bytes32 s) {
        require(sig.length == 65);
        assembly {
            // first 32 bytes, after the length prefix.
            r := mload(add(sig, 32))
            // second 32 bytes.
            s := mload(add(sig, 64))
            // final byte (first byte of the next 32 bytes). 
            v := byte(0, mload(add(sig, 96)))
        }
        return (v, r, s);
    }
    
    function recoverSigner(bytes32 message, bytes memory sig) internal pure returns (address) {
        (uint8 v, bytes32 r, bytes32 s) = splitSignature(sig); 
        return ecrecover(message, v, r, s);
    }
    /// builds a prefixed hash to mimic the behavior of eth_sign.
    function prefixed(bytes32 hash) internal pure returns (bytes32) {
        return keccak256(abi.encodePacked("\x19Ethereum Signed Message:\n32", hash));
    }
}
