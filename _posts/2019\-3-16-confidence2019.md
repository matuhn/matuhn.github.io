---
layout: post
title: CONFidence CTF 2019 Teaser
---
# CONFidence CTF 2019 Teaser
Giải do team p4 tổ chức, có khá nhiều bài hay :))) Nhưng là mới chỉ là Teaser thôi nên mình vẫn chưa ngập hành. 


![alt text](https://raw.githubusercontent.com/matuhn/matuhn.github.io/master/images/con1.png "CONFidence CTF 2019")

## My admin panel
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
