<?php
/**
 * Created by PhpStorm.
 * User: naikorasu
 * Date: 22/03/19
 * Time: 10.24
 */

$data = file_get_contents("./target.sql");


$arr_lines = explode("\n", $data);

//echo "<pre>";
//print_r($arr_lines);
//echo "</pre>";;

$seeder = "";

foreach ($arr_lines as $line) {
    $line = substr($line,1,-2);
    //echo $line."<br/>";
    $arr_columns = explode("', '", $line);

    $code_acc = $arr_columns[0];
    $code_acb = $arr_columns[1];
    $code_cab = $arr_columns[2];
    $name = $arr_columns[3];
    $address = $arr_columns[4];
    $city = $arr_columns[5];
    $phone_1 = $arr_columns[6];
    $phone_2 = $arr_columns[7];
    $tu_name = $arr_columns[8];
    $ks_name = $arr_columns[9];

    $seeder .= "
    DB::table('prm_school_units')->insert([
            <br>'code_acc' => $code_acc',
            <br>'code_acb' => '$code_acb',
            <br>'code_cab' => '$code_cab',
            <br>'name' => '$name',
            <br>'address' => '$address',
            <br>'city' => '$city',
            <br>'phone_1' => '$phone_1',
            <br>'phone_2' => '$phone_2',
            <br>'tu_name' => '$tu_name',
            <br>'ks_name' => '$ks_name',
        <br>]);
    ";

    $seeder .= "<br/><br/>";

}

echo $seeder;