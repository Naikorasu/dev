<?php
ini_set('max_execution_time', 300);
$temp = file_get_contents("BATAM.txt");
//$temp = file_get_contents("LMNTRIX.txt");
//$temp = file_get_contents("BATAM_UAT.txt");

require_once __DIR__ . '/vendor/autoload.php';




$exp = explode("\n",$temp);

//echo "<pre>";
//print_r($exp);
//echo "</pre>";

$prev_CIF = "";

foreach ($exp as $key => $val) {
    //echo $val."<br>";

    //$check = substr($val,0,10);
    $check = strpos($val, "KEPADA YTH :");
    if($check > 0) {

        $get_CIF = substr($val,120,10);
        //echo $val."<br>";
        //echo "CIF : ". $get_CIF . "<br>";

        if($get_CIF != $prev_CIF) {

            $get_line_CUSTOMER_NAME = $exp[$key + 1];
            $get_CUSTOMER_NAME = substr($get_line_CUSTOMER_NAME,0,45);

            $get_line_NOMOR_REKENING = $exp[$key + 1];
            $get_NOMOR_REKENING = substr($get_line_NOMOR_REKENING,118,14);

            $get_line_ADDRESS_1 = $exp[$key + 2];
            $get_line_ADDRESS_2 = $exp[$key + 3];
            $get_line_ADDRESS_3 = $exp[$key + 4];
            $get_line_ADDRESS_4 = $exp[$key + 5];

            $get_ADDRESS_1 = substr($get_line_ADDRESS_1,0,80);
            $get_ADDRESS_2 = substr($get_line_ADDRESS_2,0,80);
            $get_ADDRESS_3 = substr($get_line_ADDRESS_3,0,80);
            $get_ADDRESS_4 = substr($get_line_ADDRESS_4,0,80);

            $get_line_START_BALANCE = $exp[$key + 13];
            $get_line_AVERAGE_BALANCE = $exp[$key + 13];
            $get_line_END_BALANCE = $exp[$key + 18];

            $get_START_BALANCE = substr($get_line_START_BALANCE,30,21);
            $get_AVERAGE_BALANCE = substr($get_line_AVERAGE_BALANCE,109,21);
            $get_END_BALANCE = substr($get_line_END_BALANCE,30,21);

            $get_line_STATEMENT_DATE = $exp[$key + 3];
            $get_STATEMENT_DATE = substr($get_line_STATEMENT_DATE,118,10);

            $get_line_CURRENCY = $exp[$key + 2];
            $get_CURRENCY = trim(substr($get_line_CURRENCY,118,3));

            //$get_CURRENCY = "ZZZ";

            $fname = trim($get_CIF);

            $template_data_page = file_get_contents("./template/template_data_page.html");

            $template_data_page = str_replace("__CUSTOMER_NAME__",$get_CUSTOMER_NAME,$template_data_page);
            $template_data_page = str_replace("__CIF__",$get_CIF,$template_data_page);
            $template_data_page = str_replace("__ADDRESS_1__",$get_ADDRESS_1,$template_data_page);
            $template_data_page = str_replace("__ADDRESS_2__",$get_ADDRESS_2,$template_data_page);
            $template_data_page = str_replace("__ADDRESS_3__",$get_ADDRESS_3,$template_data_page);
            $template_data_page = str_replace("__ADDRESS_4__",$get_ADDRESS_4,$template_data_page);

            $template_data_page = str_replace("__STATEMENT_DATE__",$get_STATEMENT_DATE,$template_data_page);
            $template_data_page = str_replace("__CURRENCY__",$get_CURRENCY,$template_data_page);

            $template_data_page = str_replace("__START_BALANCE__",$get_START_BALANCE,$template_data_page);
            $template_data_page = str_replace("__AVG_BALANCE__",$get_AVERAGE_BALANCE,$template_data_page);
            $template_data_page = str_replace("__END_BALANCE__",$get_END_BALANCE,$template_data_page);

            $template_last_page = file_get_contents("./template/template_last_page.html");


            $mpdf = new \Mpdf\Mpdf();
            //$mpdf->SetProtection(array(), '123456', '123456');
            $mpdf->SetDisplayMode('fullpage');

            $mpdf->WriteHTML($template_data_page);

            $mpdf->AddPage("P");
            $mpdf->WriteHTML($template_last_page);

            $mpdf->Output("./output/".$fname.".pdf",\Mpdf\Output\Destination::FILE);

            echo "<hr>";
            echo "IDENTIFIER : <b>" . $get_CIF . "</b><br>";
            echo "CUSTOMER NAME : <b>" . $get_CUSTOMER_NAME . "</b><br>";
            echo "NO REKENING : <b>" . $get_NOMOR_REKENING . "</b><br>";
            echo "MATA UANG : <b>" . $get_CURRENCY . "</b><br>";



            $get_halaman = $exp[$key + 5];
            $exp_halaman = explode("HALAMAN                     :",$get_halaman);
            echo "HALAMAN " . $exp_halaman[1].  " - W/ NO-REK :" . $exp_CUST_NOREK[1] ."<br>";

            $prev_CIF = $get_CIF;


        }
        else if ($get_CIF == $prev_CIF) {
            //echo "IDENTIFIER SAME : " . $get_CIF ."<br>";

            $get_halaman = $exp[$key + 5];
            $exp_halaman = explode("HALAMAN                     :",$get_halaman);

            $get_penggabungan = $exp[$key + 8];
            $check_penggabungan = strpos($get_penggabungan,"*** PENGGABUNGAN ***          ");
            if($check_penggabungan > 0) {
                $get_line_CUST_NOREK_PENGGABUNGAN = $get_penggabungan;
                $exp_CUST_NOREK = explode("NOMOR REKENING              : ",$get_line_CUST_NOREK_PENGGABUNGAN);
                echo "HALAMAN " . $exp_halaman[1].  " - PENGGABUNGAN W/ NO-REK :" . $exp_CUST_NOREK[1] ."<br>";
            }
            else {
                echo "HALAMAN " . $exp_halaman[1].  " - W/ NO-REK :" . $exp_CUST_NOREK[1] ."<br>";
            }


        }

    }
}


?>