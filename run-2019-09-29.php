<?php
error_reporting(E_ALL & ~E_NOTICE);

//$file = "BATAM.txt";
$file = "LMSMRTM.txt";
//$file = "LMNTRIX.txt";
//$file = "BATAM_UAT.txt";

read_source($file);

function read_source($file) {
    $fname_data_all = "./data.new/data.txt";
    if(file_exists($fname_data_all)) {
        unlink($fname_data_all);
    }

    $temp = file_get_contents("./".$file);
    $exp = explode("\n",$temp);

    //echo "<pre>";
    //print_r($exp);
    //echo "</pre>";

    $prev_CIF = "";

    foreach ($exp as $key => $val) {
        //echo $val."<br>";
        $check = strpos($val, "\f CABANG :");
        if($check > 0) {

            $get_line_CIF = $exp[$key + 3];
            $get_CIF = substr($get_line_CIF,120,10);
            //echo "CIF : ". $get_CIF . "<br>";

            if($get_CIF != $prev_CIF) {

                $get_line_CUSTOMER_NAME = $exp[$key + 4];
                $get_CUSTOMER_NAME = substr($get_line_CUSTOMER_NAME,0,45);

                $get_line_NOMOR_REKENING = $exp[$key + 4];
                $get_NOMOR_REKENING = substr($get_line_NOMOR_REKENING,118,14);

                $get_line_CURRENCY = $exp[$key + 5];
                $get_CURRENCY = trim(substr($get_line_CURRENCY,118,3));

                $get_line_PAGE = $exp[$key + 8];
                $get_PAGE = substr($get_line_PAGE, 119, 5);


                //echo "<hr>";
                //echo "IDENTIFIER : <b>" . $get_CIF . "</b><br>";
                //echo "CUSTOMER NAME : <b>" . $get_CUSTOMER_NAME . "</b><br>";
                //echo "NO REKENING : <b>" . $get_NOMOR_REKENING . "</b><br>";
                //echo "HALAMAN " . $get_PAGE.  " - W/ NO-REK :" . $get_NOMOR_REKENING . " | MATA-UANG : " . $get_CURRENCY. "<br>";

                echo "\n";
                echo "IDENTIFIER : " . $get_CIF . "\n";
                echo "CUSTOMER NAME : " . $get_CUSTOMER_NAME . "\n";
                echo "NO REKENING : " . $get_NOMOR_REKENING . "\n";
                echo "HALAMAN " . $get_PAGE.  " - W/ NO-REK :" . $get_NOMOR_REKENING . " | MATA-UANG : " . $get_CURRENCY. "\n";

                reformat_data($exp,$key,$get_CIF,"w");

                $prev_CIF = $get_CIF;

            }
            else {

                $get_line_NOMOR_REKENING = $exp[$key + 4];
                $get_NOMOR_REKENING = substr($get_line_NOMOR_REKENING,118,14);

                $get_line_CURRENCY = $exp[$key + 5];
                $get_CURRENCY = trim(substr($get_line_CURRENCY,118,3));

                $get_line_PAGE = $exp[$key + 8];
                $get_PAGE = substr($get_line_PAGE, 119, 5);

                echo "HALAMAN " . $get_PAGE.  " - W/ NO-REK :" . $get_NOMOR_REKENING . " | MATA-UANG : " . $get_CURRENCY. "<br>";

                reformat_data($exp,$key,$get_CIF,"a");
            }
        }
    }
    make_data_new();
}

function reformat_data($exp,$key,$get_CIF,$fopen_type) {

    //echo "<pre>";
    //print_r($data);
    //echo "</pre>";

    $get_line_CUSTOMER_NAME = $exp[$key + 4];
    $get_CUSTOMER_NAME = substr($get_line_CUSTOMER_NAME,0,45);

    $statement_type = "NORMAL";

    $get_line_HEADER = array();

    for($line = 0; $line <= 25; $line++) {

        switch ($line)
        {
            case 0 :
                $first_line = explode("",$exp[$key + $line]);
                $get_line_HEADER[$line] = $first_line[1];
                break;

            case 23 :
                $check_naration = $exp[$key + $line];
                if(strpos($check_naration,"RINGKASAN REKENING GABUNGAN ANDA DI BII") > 0) {
                    $statement_type = "PENGGABUNGAN";
                }
                else {
                    $statement_type = "NORMAL";
                }
                //$get_line_HEADER[16] = $exp[$key + $line];
                $get_line_HEADER[$line] = $exp[$key + $line];
                break;

            default :
                $get_line_HEADER[$line] = $exp[$key + $line];
                break;
        }

        $fname = trim($get_CIF)."-".trim(str_replace("/","",$get_CUSTOMER_NAME));


    }

    $get_line_DATA = array();

    switch ($statement_type) {

        case "NORMAL":
            while(true) {
                if($exp[$key + $line] == null) {
                    break;
                }
                $read_line = $exp[$key + $line];
                if($last_pos = strpos($read_line,"\f CABANG :") > 0 || $last_pos = strpos($read_line,"\f BRANCH :") || $last_pos = strpos($read_line,"CABANG :  ") || $last_pos = strpos($read_line,"\f")) {
                    //$last_line = explode("\f CABANG :",$read_line);
                    break;
                }
                array_push($get_line_DATA,$read_line);
                //array_push($get_line_DATA,$last_line[0]);
                $line++;
            }

            break;

        case "PENGGABUNGAN":

            /*
            $current_HEADER = 17;
            while(true) {
                if($exp[$key + $line] == null) {
                    break;
                }
                $read_line = $exp[$key + $line];
                if($last_pos = strpos($read_line,"\f CABANG :") > 0 || $last_pos = strpos($read_line,"\f BRANCH :") || $last_pos = strpos($read_line,"CABANG :  ") || $last_pos = strpos($read_line,"\f")) {
                    $last_line = explode("\f CABANG :",$read_line);
                    $get_line_HEADER[$current_HEADER] = $last_line[0];
                    break;
                }
                $get_line_HEADER[$current_HEADER] = $read_line;
                $current_HEADER++;
                $line++;
            }
            */

            while(true) {
                if($exp[$key + $line] == null) {
                    break;
                }
                $read_line = $exp[$key + $line];
                if($last_pos = strpos($read_line,"\f CABANG :") > 0 || $last_pos = strpos($read_line,"\f BRANCH :") || $last_pos = strpos($read_line,"CABANG :  ") || $last_pos = strpos($read_line,"\f")) {
                    //$last_line = explode("\f CABANG :",$read_line);
                    break;
                }
                array_push($get_line_DATA,$read_line);
                //array_push($get_line_DATA,$last_line[0]);
                $line++;
            }

            break;

        default:
            break;
    }

    write_format($fname,$get_line_HEADER,$get_line_DATA,$statement_type,$fopen_type);
}


function write_format($fname,$header,$data,$type,$fopen_type) {

    //echo $type."<br>";
    //echo "<pre>";
    print_r($header);
    print_r($data);
    //echo "</pre>";



    switch ($type) {

        case "NORMAL" :

            $file_normal = fopen("./data.new/temp-".$fname.".txt", $fopen_type) or die("Unable to open file!");
            //HEADER
            foreach ($header as $k => $v) {
                fwrite($file_normal, str_pad($k+1,2,"0",STR_PAD_LEFT).$v."\n");
            }
            //DATA
            foreach ($data as $k => $v) {
                fwrite($file_normal, "DD".$v."\n");
            }
            fclose($file_normal);
            break;

        case "PENGGABUNGAN" :

            $file_union = fopen("./data.new/temp-".$fname.".txt", "w") or die("Unable to open file!");
            //HEADER
            foreach ($header as $k => $v) {
                fwrite($file_union, str_pad($k+1,2,"0",STR_PAD_LEFT).$v."\n");
            }
            //DATA
            foreach ($data as $k => $v) {
                fwrite($file_union, "DD".$v."\n");
            }
            fclose($file_union);
            break;

        default :
            break;
    }


}


function make_data_new() {
    $fname_data_all = "./data.new/data.txt";
    $file_data_all = fopen($fname_data_all,"w") or die("Unable to open file!");

    $all_temp_files = scandir("./data.new/");
    echo "DATA-NEW-FILES:\n";
    foreach ($all_temp_files as $k => $v) {
        if($v == "." || $v == ".." || strtolower($v) == ".ds_store" || $v == "data.txt" || substr($v,0,1) == ".") {
        }
        else {
            echo "file:".$v."\n";
            $content = file_get_contents("./data.new/".$v);
            fwrite($file_data_all,$content);
            unlink("./data.new/".$v);
        }

    }
    echo "\n";
    fclose($file_data_all);
}
?>
