
<html>
	<head>
		<title><?php echo $title; ?></title>
		<meta http-equiv="content-type" content="text/html;charset=utf-8" />
		<meta name="generator" content="Geany 1.33" />
		<link rel="stylesheet" type="text/css" href="Styles/Stylesheet.css">
	</head>
	<body> 
		<div id="wrapper" style = "background-color:black;">
			<div id="banner" style = "background:url(huraaa.png);background-size: 100%;">
				
			</div>
			
			<nav id="navigation" style = "background:url(blackas.png);background-size: 100%;">
				<ul id="nav">
					<li><a href="index.php">Dashboard</a></li>
					<li><a href="table.php">Tabel</a></li>
					<li><a href="gambar.php">ScreenCap</a></li>
				</ul>
			</nav>
			<div id="content_area">
				<?php echo $content;?>
			</div>
		</div>
	</body>
</html>
