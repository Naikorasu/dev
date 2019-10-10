<?php
/**
 * Created by PhpStorm.
 * User: naikorasu
 * Date: 07/08/19
 * Time: 02.14
 */
ob_clean();
$content = $_POST['mytextarea'];
/*
$myfile = fopen("html_template.html", "w") or die("Unable to open file!");
fwrite($myfile, $content);
fclose($myfile);
*/
header('Content-Description: File Transfer');
header('Content-Type: application/octet-stream');
header('Content-Disposition: attachment; filename=html_template.html');
header('Content-Transfer-Encoding: binary');
header('Connection: Keep-Alive');
header('Expires: 0');
header('Cache-Control: must-revalidate, post-check=0, pre-check=0');
header('Pragma: public');
header('Content-Length: ' . strlen($content)*8);
echo $content;
?>