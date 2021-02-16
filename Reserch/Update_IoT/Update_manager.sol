pragma solidity ^0.5.12;

contract Update_mager{
    
    mapping(address=>UpLog_ven[]) public log_ven; // vendorのリリースログ
    mapping(address=>UpLog_IoT[]) public log_update; // IoTのアップデートログ, 鍵で個別認証
    mapping(string=>uint256) public version; // デバイスの最新バージョン
    mapping(string=>mapping(uint256=>bytes32)) public firmware;
    mapping(string=>mapping(uint256=>string[])) public URL; // リポジトリの一覧
    mapping(string=>address) public eth_addr_URL; // URL に対応した ethreumアドレス
    mapping(address=>string) public list_device; // modelに対応したdevice 公開鍵->model名
    mapping(address=>mapping(uint256=>uint256)) public done_update; // update済みかどうか 公開鍵->ver->0 or 1
    mapping(string=>uint) public num_device; // デバイス数
    mapping(bytes32=>uint) public reward; //アップデート報酬(合計) H(firmware) -> 
    mapping(bytes32=>uint) public reward_pay; //アップデート報酬(支払い) H(frimware) -> 
    mapping(string=>address) public vendor; // modelに対応したvendorアドレス
    mapping(bytes32=>uint256) public period; // 報酬の配布期間 H(firmware) -> timestamp
    
    struct UpLog_ven{
        string model;
        uint256 ver;
        bytes32 hash_u;
    }
    
    struct UpLog_IoT{
        address distributor;
        string model;
        uint256 ver;
        bytes32 hash_u;
    }
    
    event RegistDevice(address indexed vendor, string model, address[] pubkey);
    event RegistURL(address indexed distributer, string URL, string model, uint256 ver);
    event NewVer(address indexed vendor, string model, uint256 indexed ver, bytes32 hash);
    event ReportUpdate(address indexed device, address indexed distributor, string model, uint256 ver, bytes32 hash_u);
    
    constructor() public {}
    
    // ハッシュ関数(文字列 -> ハッシュ値)　文字列の比較に使用
    function getHash(string memory _var) internal pure returns (bytes32){
        byte b = 0x00;
        uint8 i = 0;
        return keccak256(abi.encodePacked(b, i, _var));
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
    
    // modelに対応したdeviceの登録 (とりあえず1つずつ)
    function registDevice(string memory _model, address[] memory _pubkey, uint256 len) public{
        // 自身のmodelに関してのみ登録可能
        if(vendor[_model] == address(0)){
            vendor[_model] = msg.sender;
        }
        require(vendor[_model] == msg.sender);
        for(uint256 i = 0; i < len; i++){
            // 二重登録防止
            require(getHash(list_device[_pubkey[i]]) == getHash(""));
            list_device[_pubkey[i]] = _model;
        }
        num_device[_model] += len;
        
        emit RegistDevice(msg.sender, _model, _pubkey);
    } 
    
    // vendorが更新情報をアップ
    function upVendor(string memory _model, uint256 _ver, bytes32 _hash, string memory url) public payable{
        // 自身の製品の更新情報のみ許可
        require(vendor[_model] == msg.sender);
        
        UpLog_ven memory uven = UpLog_ven(_model, _ver, _hash);
        log_ven[msg.sender].push(uven);
        reward[_hash] = msg.value;
        reward_pay[_hash] = msg.value / num_device[_model];
        URL[_model][_ver].push(url);
        eth_addr_URL[url] = msg.sender;
        firmware[_model][_ver] = _hash;
        version[_model] = _ver;
        // 報酬配布期間の設定(とりあえず12時間)
        period[_hash] = block.timestamp + 12 hours;
         
        emit NewVer(msg.sender, _model, _ver, _hash);
    }

    // 配布者がurlを登録
     function registURL(string  memory _url, string memory _model, uint256 _ver, bytes memory sign) public {
        bytes32 h_u = firmware[_model][_ver];
        // 開発者の電子署名がないと登録できないようにする
        require(verifyDistributor(vendor[_model], sign, h_u));
        URL[_model][_ver].push(_url);
        eth_addr_URL[_url] = msg.sender;
        emit RegistURL(msg.sender, _url, _model, _ver);
    }
    
    // solidity で乱数できないので乱数渡す
    function getURL(string memory _model, uint256 _ver, uint256 num) public view returns (string memory, address){
        string memory url = URL[_model][_ver][num];
        return (url, eth_addr_URL[url]);
    }
    
    // UpLog_ven の数を取得
    function getNumUpLog(address _vendor) public view returns (uint256) {
        UpLog_ven[] memory ul = log_ven[_vendor];
        return ul.length;
    }
    
    // model の最新バージョン番号を取得
    function getVersion(string memory _model) public view returns (uint256, bytes32) {
        uint256 ver = version[_model];
        return (ver, firmware[_model][ver]);
    }
    
    // 最新のアップデート情報の入手
    function getInfo(address _vendor) public view returns (string memory, uint256, bytes32){
        uint256 len = log_ven[_vendor].length; 
        UpLog_ven memory ul = log_ven[_vendor][len-1];
        return (ul.model, ul.ver, ul.hash_u);
    }

    // device が アップデート済 か調べる
    function checkDevice(address pk_d, uint256 ver) public view returns(bool){
       return(done_update[pk_d][ver] == 0);
    }
    
    // アップデート報告 署名検証 + 報酬付与
    function reportUpdate(string memory model, uint256 ver, bytes memory signature, address pk_d, uint256 ts) public payable{
        bytes32 h_u = firmware[model][ver];
        bool check = verify_Update3(model, ver, pk_d, signature, h_u, ts);
        require(check); // 署名が正しいかどうか
        require(getHash(model) == getHash(list_device[pk_d])); // アップデート対象かどうか
        require(done_update[pk_d][ver] == 0); // まだアップデートしていないことの確認
        // 報酬が残っており署名をもらってから１時間以内であれば報酬を支払う
        if(reward[h_u] >= reward_pay[h_u] && block.timestamp <= (ts + 1 hours)){
            // 報酬支払い
            msg.sender.transfer(reward_pay[h_u]);
            reward[h_u] -= reward_pay[h_u];
        }
        // アップデートログ生成
        done_update[pk_d][ver] = 1;
        UpLog_IoT memory ulog = UpLog_IoT(msg.sender, model, ver, h_u);
        log_update[pk_d].push(ulog);
        
        emit ReportUpdate(pk_d, msg.sender, model, ver, h_u);
    }
    
    function verifyDistributor(address _vendor,bytes memory signature, bytes32 h_u) public view returns(bool){
        // this recreates the message that was signed on the client
        bytes32 message = prefixed(keccak256(abi.encodePacked(msg.sender, h_u)));
        return (recoverSigner(message, signature) == _vendor);
    }

    function verify_Update3(string memory model, uint256 ver, address pk_d, bytes memory signature, bytes32 h_u, uint256 ts) public view returns(bool){
        bytes32 message = prefixed(keccak256(abi.encodePacked(msg.sender, model, ver, h_u, ts)));
        return (recoverSigner(message, signature) == pk_d);
    }
    
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
    
    // ベンダーが残った報酬を引き出す
    function withdrawFunds(string memory _model, uint256 _ver, bytes32 _hash) public payable{
        require(block.timestamp > period[_hash]); //配布期間が過ぎてる場合のみ実行可能
        require(vendor[_model] == msg.sender); // 自身の管理するモデルのみ実行可能
        require(firmware[_model][_ver] == _hash); // 対応しているか
        msg.sender.transfer(reward[_hash]);
    }
    
}