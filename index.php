<?php
$title = "dashboard";
$content = "<H2>Status Mobil</H2>";

include 'header.php';
?>
<html>
<body style = "background:url(background.png);background-repea:no-repeat;backgrond-sizer:100% 100%">
</body>
</html>
<table border="3" class ='content_area'>
    
    <tr>
        <th>No</th>
        <th>Waktu</th>
        <th>Latitude</th>
        <th>Longitude</th>
        <th>Roll</th>
        <th>Pitch</th>
    </tr>
    
    
    <?php
    
    $host    = "localhost";
    $user    = "phpmyadmin";
    $pass    = "arsenal4life";
    $db_name = "Database Kecelakaan";

    $connection = mysqli_connect($host, $user, $pass, $db_name);


    $DataSQL = mysqli_query($connection,"select * from Status ORDER BY No DESC LIMIT 10 ");
    while ($datasensor = mysqli_fetch_array($DataSQL)){
        echo "
        <tr>
            <td>$datasensor[No]</td>
            <td>$datasensor[waktu]</td>
            <td>$datasensor[Latitude]</td>
            <td>$datasensor[Longitude]</td>
            <td>$datasensor[Roll]</td>
            <td>$datasensor[Pitch]</td>
        </tr>";
    }
    ?>
</table>
<?php
    $files = glob("*.jpg");
    usort($files, function($a, $b){
        return (filemtime($a) < filemtime($b));
    });

    $files = array_slice($files, 0, 1);

    foreach($files as $file)
        echo "<p class='kanan'>$file </p><br>";
        echo "<img src='" . $file. "' alt='code'class ='imgRight'>";

?>
<footer style="background:url(hitam.png);background-size: 100%;">
<p>Kotak Pengemudi : 08xxxxxxxxxx</p>
</footer>
