<?php
//error_reporting(E_ALL & ~E_NOTICE);

$folder = $argv[1];
$format_file = $argv[2];
$folder_output = $argv[3];

//$folder = "./";
//$format_file = "*.CDIMSTME*.txt";

var_dump($argv);
//$file = "BATAM.txt";
//$file = "LMNTRIX.txt";
//$file = "BATAM_UAT.txt";

//echo $file;
//exit;

$arr_seq = array();

$files = glob($folder."/".$format_file);

//echo "<pre>";
echo "SOURCE :\n";
print_r($files);
//echo "</pre>";

read_source($files[0]);

function read_source($file) {
    $fname_data_all = "./data.temp/data.txt";
    if(file_exists($fname_data_all)) {
        unlink($fname_data_all);
    }
	
	

    $temp = file_get_contents($file);
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
            $get_CIF = substr($get_line_CIF,118,10);
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
                echo "IDENTIFIER : " . $get_CIF . "\n";
                echo "CUSTOMER NAME : " . $get_CUSTOMER_NAME . "\n";
                echo "NO REKENING : " . $get_NOMOR_REKENING . "\n";
                echo "HALAMAN " . $get_PAGE.  " - W/ NO-REK :" . $get_NOMOR_REKENING . " | MATA-UANG : " . $get_CURRENCY. "\n\n";

                reformat_data($exp,$key,$get_CIF,"w");

                $prev_CIF = $get_CIF;
				
				$arr_detail = array();
				$arr_detail['CIF'] = $get_CIF;
				$arr_detail['NAME'] = $get_CUSTOMER_NAME;
				
				array_push($GLOBALS['arr_seq'], $arr_detail); 

            }
            else {

                $get_line_NOMOR_REKENING = $exp[$key + 4];
                $get_NOMOR_REKENING = substr($get_line_NOMOR_REKENING,118,14);

                $get_line_CURRENCY = $exp[$key + 5];
                $get_CURRENCY = trim(substr($get_line_CURRENCY,118,3));

                $get_line_PAGE = $exp[$key + 8];
                $get_PAGE = substr($get_line_PAGE, 119, 5);

                echo "HALAMAN " . $get_PAGE.  " - W/ NO-REK :" . $get_NOMOR_REKENING . " | MATA-UANG : " . $get_CURRENCY. "\n\n";

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

        //$fname = trim($get_CIF)."-".trim(str_replace("/","",$get_CUSTOMER_NAME));
		$fname = trim($get_CIF);

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
    //print_r($header);
    //print_r($data);
	echo "\n".$fname . " SPLIT PROCESS.....\n\n\n";
    //echo "</pre>";



    switch ($type) {

        case "NORMAL" :

            $file_normal = fopen("./data.temp/".$fname.".txt", $fopen_type) or die("Unable to open file!");
            //HEADER
            foreach ($header as $k => $v) {
                fwrite($file_normal, str_pad($k+1,2,"0",STR_PAD_LEFT).$v."\n");
            }
            //DATA
            foreach ($data as $k => $v) {
                fwrite($file_normal, "DD".$v."\n");
            }
			
			fwrite($file_normal, "AT"."\n");
			fwrite($file_normal, "AM"."\n");
			fwrite($file_normal, "XX"."\n");
            fclose($file_normal);
            break;

        case "PENGGABUNGAN" :

            $file_union = fopen("./data.temp/".$fname.".txt", "w") or die("Unable to open file!");
            //HEADER
            foreach ($header as $k => $v) {
                fwrite($file_union, str_pad($k+1,2,"0",STR_PAD_LEFT).$v."\n");
            }
            //DATA
            foreach ($data as $k => $v) {
                fwrite($file_union, "DD".$v."\n");
            }
			
			fwrite($file_union, "AT"."\n");
			fwrite($file_union, "AM"."\n");
			fwrite($file_union, "XX"."\n");
			
            fclose($file_union);
            break;

        default :
            break;
    }


}


function make_data_new() {
	echo "SEQUENCES : \n";
	print_r($GLOBALS['arr_seq']);
	
    $fname_data_all = "./data.temp/data.txt";
    $file_data_all = fopen($fname_data_all,"w") or die("Unable to open file!");

    $all_temp_files = scandir("./data.temp/");
	
	foreach ($GLOBALS['arr_seq'] as $n => $val) {
		
		$cif = $GLOBALS['arr_seq'][$n]['CIF'];
		$gen_cif_text = $cif.".txt";
		
		foreach ($all_temp_files as $k => $v) {
		if($v == "." || $v == ".." || strtolower($v) == ".ds_store" || $v == "data.txt" || substr($v,0,1) == ".") {
		}
		else {
				
			if($gen_cif_text == $v) {
				
				echo "file:".$v."\n";
				$content = file_get_contents("./data.temp/".$v);
				fwrite($file_data_all,$content);
				unlink("./data.temp/".$v);
			}
		}

	}
		
	}
	
	
	
    fclose($file_data_all);
	
	$newfile = $GLOBALS['folder_output']."/output/e-billing/data.new";

	if (!copy($fname_data_all, $newfile)) {
		echo "failed to copy";
	}
	
}
?>
