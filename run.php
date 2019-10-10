<?php
/**
 * Created by PhpStorm.
 * User: naikorasu
 * Date: 29/08/19
 * Time: 11.59
 */

error_reporting(E_ALL & ~E_NOTICE);
echo "\n\n\n\n";

var_dump($argv);
$folder = $argv[1];
$format_file = $argv[2];
$folder_output = $argv[3];

$arr_seq = array();

//$folder = "./";
//$format_file = "*.CDIMSTME*.txt";
//$file = "BATAM.txt";
//$file = "LMNTRIX.txt";
//$file = "BATAM_UAT.txt";
//echo $file;

$open_config = file_get_contents("c:/xampp/cgi-bin/snm/tHeInterPasw.psw");
$config = explode(',',$open_config);
$dbname = $config[0];
$username = $config[1];
$password = $config[2];
$host = $config[3];
echo "CONFIG :\n";
var_dump($config);
echo "END-CONFIG :\n";
echo "\n\n";


$mysqli = new mysqli($host, $username, $password, $dbname);

/* check connection */
if ($mysqli->connect_errno) {
    printf("Connect failed: %s\n", $mysqli->connect_error);
    exit();
}

$search = $folder."/".$format_file;
$files = glob($search);
//echo "<pre>";
echo "SOURCE :\n";
var_dump($search);
echo "END-SOURCE :\n";
echo "FILES :\n";
var_dump($files);
echo "END-FILES :\n";
//echo "</pre>";

$open_convert = file_get_contents("./convert.cfg");
$convert = explode("\n", $open_convert);
foreach ($convert as $line) {
    if(strlen($line) > 0) {
        $liner = explode(chr(9),$line);
        $var = $liner[0];
        $val = $liner[1];
        $variable = "cfg".$var;
        $$variable = $val;
        echo $variable.":".$$variable."\n";
    }
}
$databulan = $cfgperiod;
echo "\nDATA-BULAN:".$databulan."\n";


$sql = "
DELETE FROM CUST_MasterPrintClean
WHERE cust_product_id='$cfgproduct'
AND cust_region_id='$cfgregion'";
$mysqli->query($sql);

$sql = "
DELETE FROM TEMP_PointerClean
WHERE cust_spinid like '%datark%'
AND cust_regionid='$cfgregion'";
$mysqli->query($sql);

$sql = "
DELETE FROM SPLIT_FileException 
WHERE split_product_id='$cfgproduct'
AND split_region_id='$cfgregion'";
$mysqli->query($sql);

$sql = "
DELETE FROM SPLIT_NorekException 
WHERE split_product_id='$cfgproduct'
AND split_region_id='$cfgregion'";
$mysqli->query($sql);

$sql = "SELECT control_htdocs_dir FROM TblControl";
$query = $mysqli->query($sql);
if ($query) {
    $result = $query->fetch_array();
    $query->close();
}
//var_dump($result);
$fixhtdir = $result[0];

$sql = "SELECT system_value FROM TblSystem
WHERE system_product_id='$cfgproduct'
AND system_id='varsharedir'";
$query = $mysqli->query($sql);
if ($query) {
    $result = $query->fetch_array();
    $query->close();
}
//var_dump($result);
$datatemp = explode(";",$result[0]);
//var_dump($datatemp);
$cfgsharedir = $datatemp[0];
$cfgmapdir = $datatemp[1];


$sql = "SELECT system_value FROM TblSystem
WHERE system_product_id='$cfgproduct'
AND system_id='varposfile'";
$query = $mysqli->query($sql);
if ($query) {
    $result = $query->fetch_array();
    $query->close();
}
//var_dump($result);
$cfgposfile = $result[0];

$datatemp = explode("/",$cfgposfile);
//var_dump($datatemp);
$cfgdbspin = "";
for ($ki=0;$ki<count($datatemp) - 2;$ki++)
{
    $cfgdbspin .= $datatemp[$ki] . "/";
}

$cfgdbspin .= "data" . "/" . substr($datatemp[count($datatemp)-1],0,strlen($datatemp[count($datatemp)-1])-4) . ".db";
//var_dump($cfgdbspin);

$sql = "SELECT system_value FROM TblSystem
WHERE system_product_id='$cfgproduct'
AND system_id='varspindir'";
$query = $mysqli->query($sql);
if ($query) {
    $result = $query->fetch_array();
    $query->close();
}
//var_dump($result);
$cfgunixdir = $result[0];
$cfgdosdir = $result[0];
//$cfgdosdir =~ "tr/\//\\\\/";

/*
$promoid = array();
$promoname = array();

$sql = "SELECT promo_id,promo_tray_name FROM PROMO_BrochureHead
WHERE promo_product_id='$cfgproduct'
AND TO_DAYS('$vartemp')>=TO_DAYS(promo_date_start)
AND TO_DAYS('$vartemp')<=TO_DAYS(promo_date_end)";
$query = $mysqli->query($sql);
if ($query) {
    $result = $query->fetch_array();
    if($query->num_rows > 0) {
        foreach ($result as $k => $v) {
            array_push($promoid, $result[0]);
            array_push($promoname, $result[1]);
        }
    }
    $query->close();
}
//var_dump($result);

$sql = "SHOW TABLES LIKE 'TEMP_Pointer$databulan'";
$query = $mysqli->query($sql);
if($query) {
    $result = $query->fetch_array();
    $query->close();
}
//var_dump($result);
//echo "\nCOUNT:".count($result)."\n";
if(count($result) == 0) {
    $create = "CREATE TABLE TEMP_Pointer$databulan(cust_product_number char(30) not null,
		cust_spinid char(50) not null, cust_spincnt int(7) not null,
		cust_spinsrc char(30) not null, cust_spintxn int(5) not null,
		cust_spinpage int(3) not null, cust_pointer decimal(15,0) not null, 
		cust_spinrec int(4) not null,cust_regionid char(10) not null,
		primary key(cust_product_number),
		index(cust_product_number))
		ENGINE=MYISAM";
    $mysqli->query($create);
}

$sql = "SHOW TABLES LIKE 'CUST_EBS$databulan'";
$query = $mysqli->query($sql);
if($query) {
    $result = $query->fetch_array();
    $query->close();
}
//var_dump($result);
//echo "\nCOUNT:".count($result)."\n";
if(count($result) == 0) {
    $create = "CREATE TABLE CUST_EBS$databulan (cust_prod_master char(30) not null,
	  		cust_prod_no char(30) not null, cust_timestamp datetime not null,
	  		cust_region_id char(3) not null, cust_product_id char(3) not null, 
	  		cust_email char(100), cust_status char(1), cust_errcode char(10),
	  		cust_user char(100),
	  		PRIMARY KEY(cust_prod_master,cust_prod_no,cust_timestamp), index(cust_prod_no))
	  		ENGINE=MYISAM";
    $mysqli->query($create);
}

$sql = "SHOW TABLES LIKE 'CUST_MasterPrint$databulan'";
$query = $mysqli->query($sql);
if($query) {
    $result = $query->fetch_array();
    $query->close();
}
//var_dump($result);
//echo "\nCOUNT:".count($result)."\n";
if(count($result) == 0) {
    $create = "CREATE TABLE CUST_MasterPrint$databulan (cust_dok_id char(20) not null,
		  cust_product_id char(5) not null, cust_region_id char(5) not null,
		  cust_prod_no char(30) not null, cust_nama char(60) not null,
		  cust_alamat char(200) not null, cust_kelurahan char(30) not null,
		  cust_city char(30) not null, cust_zipcode char(10) not null,
		  cust_id char(15) not null, cust_segmen char(10) not null,
		  cust_total_bill decimal(15,2) not null, cust_sheet int(4) not null,
		  cust_sequence char(40), cust_currency_id char(10),
		  cust_vendor char(40), cust_courier char(40), 
		  cust_branch_id char(10), cust_region char(10),
		  cust_timestamp datetime not null, cust_flag char(5),
		  cust_prod_master char(30) not null, cust_prod_no_real char(30),
		  PRIMARY KEY(cust_product_id,cust_prod_no),
	  	  index(cust_prod_no))
	  	  ENGINE=MYISAM";
    $mysqli->query($create);
}


$sql = "SHOW TABLES LIKE 'SPLIT_MasterPage$cfgproduct'";
$query = $mysqli->query($sql);
if($query) {
    $result = $query->fetch_array();
    $query->close();
}
//var_dump($result);
//echo "\nCOUNT:".count($result)."\n";
if(count($result) == 0) {
    $create = "CREATE TABLE SPLIT_MasterPage$cfgproduct(prod_no char(30) not null, 
   		prod_page decimal(5,0) not null,
	  	PRIMARY KEY(prod_no), index(prod_no))
	  	ENGINE=MYISAM";
    $mysqli->query($create);
}


$sql = "SHOW TABLES LIKE 'SPLIT_MasterPoint$cfgproduct'";
$query = $mysqli->query($sql);
if($query) {
    $result = $query->fetch_array();
    $query->close();
}
//var_dump($result);
//echo "\nCOUNT:".count($result)."\n";
if(count($result) == 0) {
    $create = "CREATE TABLE SPLIT_MasterPoint$cfgproduct(point_master char(30) not null, 
   		point_number char(30) not null, point_expired char(10) not null,
   		point_total decimal(14,0) not null, point_redeemed decimal(14,0) not null,
   		point_balance decimal(14,0) not null,
	  	PRIMARY KEY(point_master,point_number), index(point_number))
	  	ENGINE=MYISAM";
    $mysqli->query($create);
}

$sql = "SHOW TABLES LIKE 'SPLIT_MasterTicket$cfgproduct'";
$query = $mysqli->query($sql);
if($query) {
    $result = $query->fetch_array();
    $query->close();
}
//var_dump($result);
//echo "\nCOUNT:".count($result)."\n";
if(count($result) == 0) {
    $create = "CREATE TABLE SPLIT_MasterTicket$cfgproduct(product_master char(30) not null, 
   		product_number char(30) not null, product_flags char(15) not null,
   		product_id char(3) not null, product_region char(3) not null,
   		product_vendor char(6), product_segment char(10),
   		product_courier char(6), cust_data_one char(50),
   		cust_data_two text, cust_data_three char(50),
   		cust_pri_code char(20), cust_pri_region char(30),
   		cust_pri_propinsi char(30), cust_pri_kota char(30),
   		cust_pri_branch char(40),
   		cust_sex char(20), cust_name char(100), cust_subproduct char(50),   		
	  	PRIMARY KEY(product_master,product_number), index(product_number))
	  	ENGINE=MYISAM";
    $mysqli->query($create);

}
//var_dump($result);
//echo "\nCOUNT:".count($result)."\n";

$sql = "SHOW TABLES LIKE 'SPLIT_MarketingTicket$cfgproduct'";
$query = $mysqli->query($sql);
if ($query) {
    $result = $query->fetch_array();
    $query->close();
}
if (count($result) == 0) {
    $create = "CREATE TABLE SPLIT_MarketingTicket$cfgproduct(product_field char(20) not null, 
    product_number char(30) not null, product_flags char(20) not null,
    product_id char(200),
    PRIMARY KEY(product_number), index(product_number))
    ENGINE=MYISAM";
    $mysqli->query($create);
}

$sql = "SHOW TABLES LIKE 'SPLIT_VendorSort$cfgproduct'";
$query = $mysqli->query($sql);
if ($query) {
    $result = $query->fetch_array();
    $query->close();
}
//var_dump($result);
//echo "\nCOUNT:".count($result)."\n";
if (count($result) == 0) {
    $create = "CREATE TABLE SPLIT_VendorSort$cfgproduct(document_id char(20) not null, 
    product_segment char(10) not null, 
    product_number char(30) not null, cust_name char(40) not null,
    cust_comp char(40), cust_addr1 char(40),
    cust_addr2 char(40), cust_addr3 char(40), 
    cust_addr4 char(40), cust_addr5 char(40), 
    cust_telp_r char(40), cust_seqnumber char(20), 
    cust_nokartu char(50), cust_city char(30), 
    cust_zipcode char(5), cust_nfile char(30), cust_wil char(50),
    cust_status char(20), cust_barcode char(40), 
    cust_request char(20), cust_cstaff char(10),
    cust_ckurir char(20), 
    cust_ckode char(30), cust_cregion char(30),
    cust_cpropinsi char(30), cust_ckota char(30),
    cust_cbranch char(40), cust_flag char(50),
    PRIMARY KEY(product_number), index(product_number))
    ENGINE=MYISAM";
    $mysqli->query($create);
}

$sql = "SHOW TABLES LIKE 'SPLIT_SPINDB$cfgproduct'";
$query = $mysqli->query($sql);
if ($query) {
    $result = $query->fetch_array();
    $query->close();
}
//var_dump($result);
//echo "\nCOUNT:".count($result)."\n";
if (count($result) == 0) {
    $create = "CREATE TABLE SPLIT_SPINDB$cfgproduct(thecounter int(6) not null, 
    thefilename char(20) not null, thesequence char(1),
    thecourier char(1),theprior char(1),
    theflagbrosur char(1), thefilesource char(20), 
    thetxn int(4), thecount int(4), 
    thepointer decimal(15,0), thecardnumber char(30) not null, 
    thenotused char(1),
    PRIMARY KEY(thecardnumber), INDEX(thecardnumber))
    ENGINE=MYISAM";
    $mysqli->query($create);
}

//596
if ($cfghold != "") {

    $sql = "SHOW TABLES LIKE 'SPLIT_MasterHOLD$cfgproduct'";
    $query = $mysqli->query($sql);
    if ($query) {
        $result = $query->fetch_array();
        $query->close();
    }
//var_dump($result);
//echo "\nCOUNT:".count($result)."\n";
    if (count($result) == 0) {
        $create = "CREATE TABLE SPLIT_MasterHOLD$cfgproduct(product_number char(30) not null,
        PRIMARY KEY(product_number), index(product_number))
        ENGINE=MYISAM";
        $mysqli->query($create);
    }

    $sql = "UPDATE SPLIT_MasterHOLD$cfgproduct SET product_number=REPLACE(product_number,'\r','')";
    $mysqli->query($sql);

    $sql = "UPDATE SPLIT_MasterHOLD$cfgproduct SET product_number=REPLACE(product_number,'\n','')";
    $mysqli->query($sql);

    $sql = "UPDATE SPLIT_MasterHOLD$cfgproduct SET product_number=REPLACE(product_number,'\r\n','')";
    $mysqli->query($sql);

    $sql = "UPDATE SPLIT_MasterHOLD$cfgproduct SET product_number=REPLACE(product_number,'\n\r','')";
    $mysqli->query($sql);
}
*/

//658
/*
if ($cfglistkurvskota != "")
{
    $sql = "SHOW TABLES LIKE 'TblKurirVSKota'";
    $query = $mysqli->query($sql);
    if ($query) {
        $result = $query->fetch_array();
        $query->close();
    }
    $create = "CREATE TABLE TblKurirVSKota(nid int(4) not null, 
    nkota char(50) not null, nfile char(50),
    nkurir char(50))
    ENGINE=MYISAM";
    $mysqli->query($create);

    $sql = "SHOW TABLES LIKE 'TEMP_TblKurirVSKota'";
    $query = $mysqli->query($sql);
    if ($query) {
        $result = $query->fetch_array();
        $query->close();
    }
    $create = "CREATE TABLE TEMP_TblKurirVSKota(nid int(4) not null, 
    nkota char(50) not null, nfile char(50),
    nkurir char(50))
    ENGINE=MYISAM";
    $mysqli->query($create);


}
*/

     

//READ_SOURCE
read_source($files[0]);
$check_data_finish = "SELECT * FROM TblFinishSPLITTING WHERE splitting_product_id = '$cfgproduct' AND splitting_region_id = '$cfgregion' AND splitting_period = '$cfgperiod'";
$query = $mysqli->query($sql);
if($query) {
    $result = $query->fetch_array();
    $query->close();
}

if (count($result) == 0) {
    $sql = "INSERT INTO TblFinishSPLITTING VALUES('$cfgproduct','$cfgregion','$cfgperiod',NOW())";
    $mysqli->query($sql);
    echo "\n\nFINISH-SPLITTING(I)\n\n";
}
else {
    $sql = "UPDATE TblFinishSPLITTING SET splitting_time = NOW() WHERE splitting_product_id = '$cfgproduct' AND splitting_region_id = '$cfgregion' AND splitting_period = '$cfgperiod')";
    $mysqli->query($sql);
    echo "\n\nFINISH-SPLITTING(U)\n\n";
}


$mysqli->close();
exit;


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

            $get_line_BRANCH = $exp[$key + 2];
            $get_BRANCH = trim(substr($get_line_BRANCH,0,5));
            //echo "BRANCH : ". $get_BRANCH."\n";
            
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

                $get_line_ADDRESS_1 = $exp[$key + 4 + 1];
                $get_ADDRESS_1 = substr($get_line_ADDRESS_1,0,45);

                $get_line_ADDRESS_2 = $exp[$key + 4 + 2];
                $get_ADDRESS_2 = substr($get_line_ADDRESS_2,0,45);

                $get_line_ADDRESS_3 = $exp[$key + 4 + 3];
                $get_ADDRESS_3 = substr($get_line_ADDRESS_3,0,45);

                $get_line_ADDRESS_4 = $exp[$key + 4 + 4];
                $get_ADDRESS_4 = substr($get_line_ADDRESS_4,0,45);

                $get_line_ADDRESS_5 = $exp[$key + 4 + 5];
                $get_ADDRESS_5 = substr($get_line_ADDRESS_5,0,45);


                //echo "<hr>";
                echo "IDENTIFIER : " . $get_CIF . "\n";
                echo "CUSTOMER NAME : " . $get_CUSTOMER_NAME . "\n";
                echo "NO REKENING : " . $get_NOMOR_REKENING . "\n";
                echo "HALAMAN " . $get_PAGE.  " - W/ NO-REK :" . $get_NOMOR_REKENING . " | MATA-UANG : " . $get_CURRENCY. "\n";

                reformat_data($exp,$key,$get_CIF,"w");

                $prev_CIF = $get_CIF;

                $arr_detail = array();
                $arr_detail['CIF'] = $get_CIF;
                $arr_detail['BRANCH'] = $get_BRANCH;
                $arr_detail['NAME'] = $get_CUSTOMER_NAME;
                $arr_detail['REK'] = $get_NOMOR_REKENING;
                $arr_detail['CURR'] = $get_CURRENCY;
                $arr_detail['ADDR_1'] = $get_ADDRESS_1;
                $arr_detail['ADDR_2'] = $get_ADDRESS_2;
                $arr_detail['ADDR_3'] = $get_ADDRESS_3;
                $arr_detail['ADDR_4'] = $get_ADDRESS_4;
                $arr_detail['ADDR_5'] = $get_ADDRESS_5;

                array_push($GLOBALS['arr_seq'], $arr_detail);

            }
            else {

                $get_line_UNION_STARS = $exp[$key + 11];
                $get_UNION_STARS = trim(substr($get_line_UNION_STARS,0,22));

                if(strpos($get_UNION_STARS, "*** PENGGABUNGAN ***") !== false) {
                    echo "*** PENGGABUNGAN ***\n";
                    $get_line_CURRENCY = $exp[$key + 12];
                    $get_CURRENCY = trim(substr($get_line_CURRENCY,118,3));

                    $get_line_NOMOR_REKENING = $exp[$key + 11];
                    $get_NOMOR_REKENING = substr($get_line_NOMOR_REKENING,118,14);

                }
                else {
                    $get_line_CURRENCY = $exp[$key + 5];
                    $get_CURRENCY = trim(substr($get_line_CURRENCY,118,3));

                    $get_line_NOMOR_REKENING = $exp[$key + 4];
                    $get_NOMOR_REKENING = substr($get_line_NOMOR_REKENING,118,14);
                }

                if($get_CURRENCY == "") {
                    $get_CURRENCY = "IDR";
                }

                $get_line_PAGE = $exp[$key + 8];
                $get_PAGE = substr($get_line_PAGE, 119, 5);

                echo "HALAMAN " . $get_PAGE.  " - W/ NO-REK :" . $get_NOMOR_REKENING . " | MATA-UANG : " . $get_CURRENCY. "\n";
          
                $arr_detail['TOTAL_PAGE'] = $get_PAGE;
                //array_push($GLOBALS['arr_seq'], $arr_detail);

                reformat_data($exp,$key,$get_CIF,"a");
            }
        }
    }

    make_log_sc();
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
    echo $fname . " SPLIT PROCESS.....\n\n";
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


function make_log_sc() {

    $open_convert = file_get_contents("./convert.cfg");
    $convert = explode("\n", $open_convert);
    foreach ($convert as $line) {
        if(strlen($line) > 0) {
            $liner = explode(chr(9),$line);
            $var = $liner[0];
            $val = $liner[1];
            $variable = "cfg".$var;
            $$variable = $val;
            echo $variable.":".$$variable."\n";
        }
    }

    $fname_log_sc = $GLOBALS['folder_output']."/output/vendor/SCNasabah.txt";
    $file_log_sc = fopen($fname_log_sc,"w") or die("Unable to open file!");

    $all_temp_files = scandir("./data.temp/");

    $header = "seqno" . chr(9) . "segment" . chr(9) . "cc" . chr(9) . "nama" . chr(9). "company" . chr(9) . "alamat1" . chr(9) . "alamat2" . chr(9) . "alamat3" . chr(9) . "alamat4" . chr(9) . "alamat5" . chr(9) . "telr" . chr(9) . "telk" . chr(9) . "nokartu" . chr(9) . "kota" . chr(9) . "kodepos" . chr(9) . "nfile" . chr(9) . "wil" . chr(9) . "status" . chr(9) . "barcode" . chr(9) . "request" . chr(9) . "cstaff" . chr(9) . "ckurir" . chr(9) . "prikode" . chr(9) . "priregion" . chr(9) . "priprop" . chr(9) . "pricity" . chr(9) . "pribranch" . chr(9) . "totalpage" . chr(9) . "\n";
    //echo $header."\n";
    fwrite($file_log_sc, $header);

    foreach ($GLOBALS['arr_seq'] as $n => $val) {

        $cif = $GLOBALS['arr_seq'][$n]['CIF'];
        $rekening = $GLOBALS['arr_seq'][$n]['REK'];
        $branch = $GLOBALS['arr_seq'][$n]['BRANCH'];
        $currency = $GLOBALS['arr_seq'][$n]['CURR'];
        $name = $GLOBALS['arr_seq'][$n]['NAME'];
        $address_1 = $GLOBALS['arr_seq'][$n]['ADDR_1'];
        $address_2 = $GLOBALS['arr_seq'][$n]['ADDR_2'];
        $address_3 = $GLOBALS['arr_seq'][$n]['ADDR_3'];
        $address_4 = $GLOBALS['arr_seq'][$n]['ADDR_4'];
        $address_5 = $GLOBALS['arr_seq'][$n]['ADDR_5'];
        $total_page = $GLOBALS['arr_seq'][$n]['TOTAL_PAGE'];
        $gen_cif_text = $cif.".txt";

        foreach ($all_temp_files as $k => $v) {
            if($v == "." || $v == ".." || strtolower($v) == ".ds_store" || $v == "data.txt" || substr($v,0,1) == ".") {
            }
            else {

                if($gen_cif_text == $v) {

                    $hitcust = $n;
                    $tempbarcode = substr($varnow,9-1,2) . substr($varnow,6-1,2) . substr($varnow,3-1,2)  . $hitcust;

                    $pad = str_pad($hitcust,10,"0");
                    $custseq = $cfgproduct . $pad;
                    $custseqnumber = $pad . $hitcust;
                    $custname = $name;
                    $custaddr1 = $address_1;
                    $custaddr2 = $address_2;
                    $custaddr3 = $address_3;
                    $custaddr4 = $address_4;
                    $custaddr5 = $address_5;
                    $custtelpr = "";
                    $custnokartu = $rekening;
                    $custcurrency = $currency;
                    $custbranch = $branch;
                    $custstatus = $custcurrency . "," . $custbranch;
                    $custcomp = "COMPANY-NAME";
                    $cust_cstaff = "";
                    
                    $productnumber = trim($rekening).trim($currency);
                    $prodsegment = "";

                    $seqkota = "";
                    $seqwil = "";
                    $seqbarcode = "";
                    $seqrequest = "";
                    $seqnfile = $total_page;

                    $seqcbranch = $branch;
                    $seqcregion = $cfgregion;
                    $seqckurir = "DEFCOU";
                    $seqckode = "";
                    $seqcpropinsi = "";
                    $seqckota = "";

                    $varzipcode = "";
                    $flagtotalpage = $total_page;
                    $flagtotalamplop = ceil($total_page/6);


                    $content = $custseq . chr(9) . $prodsegment . chr(9) . $productnumber . chr(9) . $custname . chr(9). $custcomp . chr(9) . $custaddr1 . chr(9) . $custaddr2 . chr(9) . $custaddr3 . chr(9) . $custaddr4 . chr(9) . $custaddr5 . chr(9) . $custtelpr . chr(9) . $custseqnumber . chr(9) . $custnokartu . chr(9) . $seqkota . chr(9) . $varzipcode . chr(9) . strtoupper($seqnfile) . chr(9) . $seqwil . chr(9) . $custstatus . chr(9) . $seqbarcode . chr(9) . $seqrequest . chr(9) . $cust_cstaff . chr(9) . $seqckurir . chr(9) . $seqckode . chr(9) . $seqcregion . chr(9) . $seqcpropinsi . chr(9) . $seqckota . chr(9) . $seqcbranch . chr(9) . $flagtotalpage . "," . $flagtotalamplop . chr(9) . "\n";
                    //echo $content."\n";
                    fwrite($file_log_sc, $content);
                }
            }

        }

    }

           
}


function make_data_new() {
    //echo "SEQUENCES : \n";
    //print_r($GLOBALS['arr_seq']);

    $fname_data_all = "./data.temp/data.txt";
    $file_data_all = fopen($fname_data_all,"w") or die("Unable to open file!");

    $all_temp_files = scandir("./data.temp/");

    echo "DATA-NEW-FILES:\n";

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
                    //unlink("./data.temp/".$v);
                }
            }

        }

    }

    $leave_files = array('data.txt');

    foreach( glob("./data.temp/*") as $file ) {
        if( !in_array(basename($file), $leave_files) )
            unlink($file);
    }

    echo "\n";
    fclose($file_data_all);

    $newfile = $GLOBALS['folder_output']."/output/e-billing/data.new";

    if (!copy($fname_data_all, $newfile)) {
        echo "failed to copy";
    }

}
?>
