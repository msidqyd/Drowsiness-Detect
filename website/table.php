<?php
$title = "Tabel";
$content = "<H1>Tabel Informasi Mobil</H1>";

include 'header.php';
?>
<body style = "background:url(background.png);background-repea:no-repeat;backgrond-sizer:100% 100%">
</body>
</html>


<table border="3" class ='kiri'>
    
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


    $DataSQL = mysqli_query($connection,"select * from Status ORDER BY No DESC");
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

