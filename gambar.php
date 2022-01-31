<?php
$title = "Kondisi Pengemudi";
include 'header.php';
?>
<html>
<body style = "background-color: lightblue">


<?php
    echo '<div class="kiri">';
        echo "<h1>Kondisi Pengemudi</h1>";
        foreach (glob("*.jpg") as $filename){
            echo '<div class="kiri">';
                echo "<p>$filename </p><br>";
                echo "<img src='$filename' alt= '$filename' class ='kiri'/>";
            echo '</div>';
    echo '</div>';

}
    
?>
</body>
</html>
