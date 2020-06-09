pragma solidity ^0.5.8;

contract OreOreCoin {
    // 変数の宣言
    string public name;
    string public symbol;
    uint8 public decimals;

    uint256 public totalSupply;
    mapping (address => uint256) public balanceOf;
    address public owner;
    
    // 修飾子
    modifier onlyOwner() { if (msg.sender != owner) revert(); _; }

    // イベント通知
    event Transfer(address indexed from, address indexed to, uint256 value);

    //  コンストラクト
    constructor(uint256 _supply, string memory _name, string memory _symbol, uint8 _decimals) public{
        balanceOf[msg.sender] = _supply;
        name = _name;
        symbol = _symbol;
        decimals = _decimals;
        totalSupply = _supply;
        owner = msg.sender;
    }
    
    function getbalanceOf(address _addr) view public returns (uint256) {
        return balanceOf[_addr];
    }
    

    // 送金
    function transfer(address _sender, address _to, uint256 _value) public{
        //　不正送金チェック
        if (balanceOf[_sender] < _value) revert();
        if (balanceOf[_to] + _value < balanceOf[_to]) revert();
    
        balanceOf[_sender] -= _value;
        balanceOf[_to] += _value;
            
        emit Transfer(_sender, _to, _value);
    }
}

contract ContentsManage2 {
    OreOreCoin public token;
    address[] public saller;
    mapping(address => string[]) public contents; //コンテンツ
    mapping(address => string[]) public names; //　コンテンツの名前
    mapping(address => mapping(string => bytes32)) public content_from_name; // 名前からコンテンツを取得(ハッシュ値)
    mapping(bytes32 => uint256) public minprice; // ハッシュ値を渡す予定なので被らないはず
    mapping(bytes32 => mapping(address => bool)) public allow_list; //コンテンツへのアクセス許可者
    mapping(bytes32 => address) public contents_owner; // コンテンツのオーナー(著作権保護)
    mapping(address => uint256[]) public depts; // 転売のペナルティ(この割合だけ売り上げを他の人へ送金)
    mapping(address => address[]) public creditor; // 転売しようとしたコンテンツのオーナー(オリジナル)
    
    event UpContent(string content, uint256 minprice);
    event BuyContent(address saller, uint256 pay, string name);
    event FindResale(address resaler, address original, string content);
    event GetDept(address resaler, address original, uint256 dept);
    event Repayment(address depter, address payee, uint256 dept);
    
    constructor(OreOreCoin _token) public{
        token = _token;
    }
    
    // 所持金の確認
    function getbalanceOf() public view returns(uint256){
        OreOreCoin oc = OreOreCoin(token);
        return oc.getbalanceOf(msg.sender);
    }
    
    // ハッシュ関数(文字列 -> ハッシュ値)
    function getHash(string memory _var) public pure returns (bytes32){
        byte b = 0x00;
        uint8 i = 0;
        return keccak256(abi.encodePacked(b, i, _var));
    }
    
    // コンテンツのアップロード
    function upContent(string memory _content, string memory _name, uint256 _minprice) public {
        // 売値の確認
        if(_minprice < 0) revert("値段設定がおかしいです");
        
        bytes32 hash = getHash(_content);
        
        /* 他人のコンテンツを出してないか確認
          転売した場合、商品分のお金をオリジナルの出品者に送金
          足りない場合は、借金とし、自分の入金をオリジナルの出品者に送金するようにする*/
        if(contents_owner[hash] != address(0) && contents_owner[hash] != msg.sender){
            uint256 balance = getbalanceOf();
            uint256 dept = minprice[hash] + 100;
            if(balance >= dept){
                token.transfer(msg.sender, contents_owner[hash], minprice[hash]);
            }else if (balance > 0){
                token.transfer(msg.sender, contents_owner[hash], balance);
                dept -= balance;
                depts[msg.sender].push(dept);
                creditor[msg.sender].push(contents_owner[hash]);
                
                emit GetDept(msg.sender, contents_owner[hash], dept);
            }else{
                depts[msg.sender].push(dept);
                creditor[msg.sender].push(contents_owner[hash]);
                
                emit GetDept(msg.sender, contents_owner[hash], dept);
            }
            emit FindResale(msg.sender, contents_owner[hash], _content);
            return;
        }else if(contents_owner[hash] != address(0)){
            revert("既に出品しています");
        }
        
        //同じ名前の物を出していないか確認
        if(content_from_name[msg.sender][_name] != 0) revert("同じ名前の物を既に公開してます");
        
        //出品者リストに追加
        if(contents[msg.sender].length == 0) saller.push(msg.sender);
        
        contents[msg.sender].push(_content);
        names[msg.sender].push(_name);
        content_from_name[msg.sender][_name] = hash;
        minprice[hash] = _minprice;
        contents_owner[hash] = msg.sender;
        allow_list[hash][msg.sender] = true; // 自分のコンテンツは入手可能
        
        
        emit UpContent(_content, _minprice);
    }
    
    // コンテンツの購入
    function buyContent(address _addr, uint256 _pay, string memory _name) public {
        bytes32 content_hash = content_from_name[_addr][_name];
        if(contents_owner[content_hash] != _addr) revert("出品者はこの商品を出品してません");
        // 最低価格よりも少ない額なら例外
        if (_pay < minprice[content_hash]) revert("金額が不足しています");
        
        // 支払先が借金している場合は支払先を変更
        if(creditor[_addr].length != 0){
            address payee = creditor[_addr][0];
            uint256 dept = depts[_addr][0];
            token.transfer(msg.sender, payee, _pay);
            if(_pay >= dept){
                delete depts[_addr][0];
                delete creditor[_addr][0];
                
                emit Repayment(_addr, payee, dept);
            }else{
                depts[_addr][0] = dept - _pay;
            }
        }else{
            token.transfer(msg.sender, _addr, _pay);
        }
        allow_list[content_hash][msg.sender] = true;
        emit BuyContent(_addr, _pay, _name);
    }
    
    // コンテンツの取得
    function getContent(address _addr, uint _num) public view returns (string memory){
        bytes32 content_hash = getHash(contents[_addr][_num]);
        if(!allow_list[content_hash][msg.sender]) revert("購入してください");
        return contents[_addr][_num];
    }
    
    // 出品者及びその出品物の一覧の補助関数1(出品者数)
    function getSallers() public view returns (address[] memory){
        return saller;
    }
    
    // 出品者及びその出品物の一覧の補助関数2(出品者のコンテンツ数)
    function getNumContents(address _addr) public view returns (uint256){
        return names[_addr].length;
    }
    
    // 出品者の出品物の一覧
    function getInfo(address _addr, uint256 _num) public view returns (string memory, uint256 ){
        string memory _name = names[_addr][_num];
        bytes32 _hash = content_from_name[_addr][_name];
        uint256 _minprice = minprice[_hash]; 
        return (names[_addr][_num], _minprice);
    }
    
}