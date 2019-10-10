#! perl

# Copyright 2001
# Written by Budi Hartoyo

# Get Data From HTML With POST/GET Method
{
$ENV{'REQUEST_METHOD'} =~ tr/a-z/A-Z/;
if ($ENV{'REQUEST_METHOD'} eq "POST")
{
	read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
}
else
{
	$buffer = $ENV{'QUERY_STRING'};
}
	@pairs = split(/&/, $buffer);
	foreach $pair (@pairs)
	{
		($name, $value) = split(/=/, $pair);
		$value =~ tr/+/ /;
		$value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
		$contents{$name} = $value;
	     
	}
}

# Variable Declaration
$programname="analisaproses.cgi";
$formtype = "Analysis";
$ipnum  = $ENV{'REMOTE_ADDR'};
$userid=$contents{'userid'};
$userpwd=$contents{'userpwd'};
$userprgcode=$contents{'userprgcode'};
$act=$contents{'act'};
$togo=$contents{'togo'} - 1;
@groupbyfield = ("DATE_FORMAT(cust_timestamp,'%Y%m')","cust_product_id","cust_region_id","cust_timestamp","cust_printer_id","cust_courier","cust_print_company");
@groupbyname=('Bulan Print','Produk','Region','Waktu Mengerjakan','Printer ID','Kirim Ke Kurir','Mitra Print');
@groupbytable=('','TblProduct','TblRegion','','','','TblMitra');
@groupbytabletwo=('','TblProduct','TblRegion','','','','TblMitra');
$countfield = @groupbyfield;

$cekfilepasw = "tHeInterPasw.psw";
if (!open(INFO,$cekfilepasw))
{
	close(INFO);
	$msg = "Error Connection";
	&GAGAL;
}
else
{
	@lines = <INFO>;
	close(INFO);
	@datalines = split(/,/,$lines[0]);
	$namadb = $datalines[0];
	$userdb = $datalines[1];
	$passdb = $datalines[2];
	$lokasidb = $datalines[3];
}


use DBI;
@db_param = ('mysql',$lokasidb,$namadb,$userdb,$passdb);
my $dsn = "DBI:$db_param[0]:database=$db_param[2];host=$db_param[1]";
$db = DBI->connect($dsn, $db_param[3], $db_param[4], {RaiseError => 0});

   my $query = "SELECT SUBSTRING(control_flag,1,1)
   		FROM TblControl";
   my $sth = $db->prepare($query);
   $sth->execute();
   my @row = $sth->fetchrow_array;
   $controlengversion = $row[0];
   $sth->finish;

$cekhelpfile = "../../html/snm/help/" . substr($programname,0,length($programname)-4) . ".hlp";
$tambahanhelp = "<p style='margin-left: -20'>";
$programblob = "";
$programhelp = "";
$programrlink = "";
$programlinkt = "";
if (!open(INFO,$cekhelpfile))
{
	close(INFO);
}
else
{
	@helplines = <INFO>;
	close(INFO);
	$blobfinish = 1;
	for($i=0;$i<@helplines;$i++)
	{
	   if ($blobfinish eq 1)
	   {
	      if (substr($helplines[$i],0,15) ne "=== End of Desc")
	      {
	         $programblob = $programblob . $helplines[$i];
	      }
	      else
	      {
  	         $blobfinish = 0;
  	         $i = $i + 3;
	      }
	   }
	   if ($blobfinish eq 0)
	   {
	      if (substr($helplines[$i],0,15) ne "=== End of Help")
	      {
	      	if (substr($helplines[$i],1,7) eq "hr size")
	      	{
	         $programhelp = $programhelp . "$helplines[$i]";
	      	}
		else
		{
#	         $programhelp = $programhelp . "<li><p style=\"margin-top: -4\">$tambahanhelp $helplines[$i]</li>";
	         $programhelp = $programhelp . "<li>$tambahanhelp $helplines[$i]</li>";
	      	}
	      }
	      else
	      {
	      	$blobfinish = 2;
  	         $i = $i + 3;
	      }
	   }
	   if ($blobfinish eq 2)
	   {
	      if (substr($helplines[$i],0,15) ne "=== End of Rela")
	      {
	      	 $vartemp = substr($helplines[$i],0,length($helplines[$i])-1);
       		 my $query = "SELECT program_code,program_name,program_act
	   		    FROM SE_Program
	   		    WHERE program_act like '%$vartemp%'";
       		 my $sth = $db->prepare($query);
       		 $sth->execute();
       		 my @row = $sth->fetchrow_array;
       		 $sth->finish;

	      	 $tempversion = "$row[1]";
	         $programrlink = $programrlink . "<A HREF=\"javascript:GantiMenu('$row[2]','$row[0]')\">$tempversion</A> &nbsp";
#	            $programrlink = $programrlink . "<li> $tambahanhelp <A HREF=\"javascript:GantiMenu('$row[2]','$row[0]')\"><font face=Verdana>$tempversion</font></A></li>";
	      }
	      else
	      {
	      	$blobfinish = 3;
  	         $i = $i + 3;
	      }
	      if ($programrlink eq "")
	      {
	   	$programrlink = "<B>Empty</B>";
	      }
	      $programrlink = "<p style='margin-left: 10'>" . $programrlink;
	   }
	   if ($blobfinish eq 3)
	   {
	      if (substr($helplines[$i],0,15) ne "=== End of Link")
	      {
	      	 $vartemp = substr($helplines[$i],0,length($helplines[$i])-1);
       		 my $query = "SELECT program_code,program_name,program_act
	   		    FROM SE_Program
	   		    WHERE program_act like '%$vartemp%'";
       		 my $sth = $db->prepare($query);
       		 $sth->execute();
       		 my @row = $sth->fetchrow_array;
       		 $sth->finish;

	      	 $tempversion = "$row[1]";
	         $programlinkt = $programlinkt . "<A HREF=\"javascript:GantiMenu('$row[2]','$row[0]')\">$tempversion</A> &nbsp";
#	         $programlinkt = $programlinkt . "<li>$tambahanhelp <A HREF=\"javascript:GantiMenu('$row[2]','$row[0]')\">$tempversion</A></li>";
	      }
	      else
	      {
	      	$blobfinish = 1;
  	         $i = $i + 1;
	      }
	      if ($programlinkt eq "")
	      {
	   	$programlinkt = "<B>Empty</B>";
	      }
	      $programlinkt = "<p style='margin-left: 10'>" . $programlinkt;
	   }
	}
}

my $query = "SELECT *
	        FROM TblStyle";
my $sth = $db->prepare($query);
$sth->execute();
my @row;
while ($row = $sth->fetchrow_arrayref)
{
   for ($row->[0]) 
   {
      if    (/bodybgcol/)    {$stylebodybgcol = $row->[1];}
      elsif (/bodylink/)     {$stylelink = $row->[1];}
      elsif (/bodyalink/)    {$stylealink = $row->[1];}
      elsif (/bodyvlink/)    {$stylevlink = $row->[1];}
      elsif (/ie5open/)      {$styleie5menuopen = $row->[1];}
      elsif (/ie5close/)     {$styleie5menuclose = $row->[1];}
      elsif (/ie5isi/)       {$styleie5menuisi = $row->[1];}
      elsif (/obj01/)        {$styleobj01 = $row->[1];}
      else          	     {}
   }
}
$sth->finish;

my $query = "SELECT COUNT(*)
             FROM SE_UserProgram
	     WHERE user_id='$userid'
	     AND program_code='$userprgcode'";
my $sth = $db->prepare($query);
$sth->execute();
my @row = $sth->fetchrow_array;
$sth->finish; 
if ($row[0] eq 0)
{
   $msg="Anda Tidak Berhak Menjalankan Transaksi Ini";
   &MSG;
}
$sth->finish; 

my $query = "SELECT * FROM TblControl";
my $sth = $db->prepare($query);
$sth->execute();
my @row = $sth->fetchrow;
$compname = $row[0];
$compaddr = $row[1];
$compcity = $row[2];
$compphone = $row[3];
$signofftime = $row[4];
$sth->finish; 

my $query = "SELECT user_id,user_pwd,user_name,NOW(),
	     user_signin, user_key_number,
	     DATE_ADD(user_signin_time, INTERVAL '$signofftime' MINUTE),
	     user_product_id
             FROM SE_User
	     WHERE user_id='$userid'
	     AND user_pwd='$userpwd'";
my $sth = $db->prepare($query);
$sth->execute();
@row = $sth->fetchrow_array;
$sth->finish;

if ($row[0] eq "" or $row[1] eq "")
{
   $msg="<font face=Arial size=2>User ID / Password Salah</font>";
   &MSG;
}
else
{
   $peringatan = "&nbsp";
   $userid=$row[0];
   $userpwd=$row[1];
   $username=$row[2];
   $signintime=$row[3];
   $usersignin=$row[4];
   $userhwid=$row[5];
   $batassignin=$row[6];
   $userproduct =$row[7];
   if ($usersignin ne "Y")
   {
      $msg="Anda Belum Login";
      &MSG;
   }

   if ($signofftime > 0)
   {
      my $query = "SELECT '$signintime' < '$batassignin'";
      my $sth = $db->prepare($query);
      $sth->execute();
      my @row = $sth->fetchrow_array;
      $sth->finish; 
      if ($row[0] eq 0)
      {
         $sth->finish; 
         $msg="Komputer anda sudah tidak aktif selama $signofftime menit";
         &MSG;
      }
   }

   my $query = "SELECT program_name, program_desc,
   		program_helpdoc
	        FROM SE_Program
	        WHERE program_code='$userprgcode'";
   my $sth = $db->prepare($query);
   $sth->execute();
   my @row = $sth->fetchrow_array;
   $programdesc = $row[0];
   $programprofile = $row[1];
   $sth->finish; 
}

if ($act eq "")
{
   my $statement = "INSERT INTO SE_UserLog values('$userid','A',
		 '-','$signintime','$ipnum',
	         '$userprgcode','$programname','','bbbbbbbbbb')";
   my $sth = $db->prepare($statement);
   $sth->execute();
   $sth->finish;

   my $statement = "Update SE_User
		 set user_signin='Y',
		 user_signin_time='$signintime'
		 WHERE user_id='$userid'";
   my $sth = $db->prepare($statement);
   $sth->execute();
   $sth->finish;

   &MAIN;
}

if ($act eq "viewproduct")
{
  $analisaperiode1=$contents{'analisaperiode1'};
  $analisaproductid=$contents{'analisaproductid'};
  $analisaregionid=$contents{'analisaregionid'};
  $analisagroupby=$contents{'analisagroupby'};
  $analisastatus=$contents{'analisastatus'};
  $analisacourier=$contents{'analisacourier'};
  $analisasegmen=$contents{'analisasegmen'};
  $jumlahdata=$contents{'jumlahdata'};
  $startlimit=$contents{'startlimit'};
  $thetarget=$contents{'thetarget'};
  $varfield=$contents{'varfield'};
  $maxlimit = 100;

     if ($analisaregionid eq "all" or $analisaregionid eq "")
     {
        $kondisiregionid = "";
        $kondisiebsregionid = "";
     }
     else
     {
        $kondisiregionid = "AND CUST_MasterPrint$analisaperiode1.cust_region_id='$analisaregionid'";
        $kondisiebsregionid = "AND CUST_EBS$analisaperiode1.cust_region_id='$analisaregionid'";
     }
  
  
  if ($startlimit eq "")
  {
  	$startlimit = 0;
  }
  
  if($thetarget eq "prev")
  {
     $startlimit = $startlimit - ($maxlimit * 2);
  }
  $endlimit = $startlimit + $maxlimit;


# Create the html page
print "Content-type: text/html\n\n";
print <<"HTML";
<HTML>
   <HEAD>
      <META http-equiv=Content-Type content='text/html; charset=iso-8859-1'>
      <META http-equiv='Pragma' content='no-cache'>
      <META content='MSHTML 5.50.4134.100' name=GENERATOR>
      <TITLE>$compname</TITLE>
      <LINK media=screen href="/snm/icons/menu.css" rel=stylesheet>
      <Script Language="JavaScript">
         function viewAgain(thetarget)
         {
         	  document.formsubmit.thetarget.value = thetarget;
         	  document.formsubmit.submit();
         }
      </Script>
   </HEAD>
   <BODY aLink=$stylealink link=$stylelink vLink=$stylevlink bgcolor=$stylebodybgcol onload=self.focus()>
<script language="JavaScript"><!--
name = 'lainnya';
//--></script>
     <div align=center>
      <form name=formsubmit method=post>
       <font face=Verdana size=3>SUMMARY PROSES <b>$analisacourier</b> PRODUK : $analisaproductid REGION : $analisaregionid </font>
       <BR>
       <TABLE WIDTH=700 cellpadding=0 cellspacing=0 border=0>
          <tr>
             <td width=70% align=left valign=top>
HTML
   if ($startlimit <= 0)
   {
      $filevendor = "VENDOR" . $analisaproductid . $analisaregionid . $analisasegmen . $analisacourier . ".txt";
      $filevendorout = "c:/xampp/htdocs/temp/" . $filevendor;
      open(FILEVENDOR,">$filevendorout");

      $filetxt = $analisaproductid . $analisaregionid . $analisasegmen . $analisacourier . ".txt";
      $fileout = "c:/xampp/htdocs/temp/" . $filetxt;
      open(FILEOUT,">$fileout");
#         my $query = "SELECT cust_sequence,cust_nama, cust_alamat,
#                      cust_kelurahan,cust_city,cust_zipcode,cust_vendor,
#                      cust_prod_no,cust_sheet,
#                      CONCAT(cust_prod_master,',',cust_region_id,',',cust_product_id)
#	                       FROM CUST_MasterPrint$analisaperiode1
#	                       WHERE CUST_MasterPrint$analisaperiode1.cust_product_id='$analisaproductid'
#	                       $kondisiregionid
#	                       AND CUST_MasterPrint$analisaperiode1.$varfield='$analisasegmen'
#	                       AND CUST_MasterPrint$analisaperiode1.cust_courier='$analisacourier'
#	                       ORDER BY cust_prod_no";
         my $query = "SELECT cust_sequence,cust_nama, cust_alamat,
                      cust_kelurahan,cust_city,cust_zipcode,cust_vendor,
                      cust_prod_no,cust_sheet,
                      CONCAT(cust_prod_master,',',cust_region_id,',',cust_product_id)
	                       FROM CUST_MasterPrint$analisaperiode1
	                       WHERE CUST_MasterPrint$analisaperiode1.cust_product_id='$analisaproductid'
	                       $kondisiregionid
	                       AND CUST_MasterPrint$analisaperiode1.$varfield='$analisasegmen'
	                       AND CUST_MasterPrint$analisaperiode1.$analisagroupby='$analisacourier'
	                       ORDER BY cust_prod_no";
         my $sth = $db->prepare($query);
         $sth->execute();
         my @row;
         while ($row = $sth->fetchrow_arrayref)
         {
         	   $prodnoSequence = $row->[0];

         	   $prodnoNama = $row->[1];
             $dot = " " x (30 - length($prodnoNama));
             $prodnoNama .= $dot;

         	   $prodnoAlamat = $row->[2];
             $dot = " " x (90 - length($prodnoAlamat));
             $prodnoAlamat .= $dot;

         	   $prodnoCity = $row->[4];
             $dot = " " x (58 - length($prodnoCity));
             $prodnoCity .= $dot;

         	   $prodnoZipcode = $row->[5];
             $dot = " " x (5 - length($prodnoZipcode));
             $prodnoZipcode .= $dot;

         	   $prodnoVendor = $row->[6];
             $dot = " " x (5 - length($prodnoVendor));
             $prodnoVendor .= $dot;
         	   
             $prodnoDec = funcDec($row->[7]);

             $dot = " " x 16;

             print FILEOUT $prodnoSequence . $prodnoNama . $prodnoAlamat . $prodnoCity . $prodnoZipcode . $prodnoVendor . $prodnoDec . $dot . "\n";
             print FILEVENDOR $row->[9] . "\n";
         }
         $sth->finish;
      close(FILEOUT);
      close(FILEVENDOR);

   }
print <<"HTML";
                <A HREF=/temp/$filetxt>Download CTS File</A>
                &nbsp &nbsp
                <A HREF=/temp/$filevendor>Download Vendor Cetak File</A>
             </td>
             <td width=30% align=right valign=top>
                &nbsp &nbsp
HTML
              if ($startlimit <= 0)
              {
print <<"HTML";
                <font face=Arial size=2><< PREV</font>
HTML
              }
              else
              {
print <<"HTML";
                <font face=Arial size=2><A HREF="javascript:viewAgain('prev')"><< PREV</A></font>
HTML
              }
print <<"HTML";
                &nbsp &nbsp
HTML
              if ($endlimit > $jumlahdata)
              {
print <<"HTML";
                <font face=Arial size=2>NEXT >></font>
HTML
              }
              else
              {
print <<"HTML";
                <font face=Arial size=2><A HREF="javascript:viewAgain('next')">NEXT >></A></font>
HTML
              }
print <<"HTML";
             </td>
          </tr>
       </table>
       <TABLE WIDTH=700 cellpadding=0 cellspacing=0 border=1>
          <tr>
             <td width=20% align=center valign=top>
                <font face=Arial size=2><b>NOMOR REKENING</b></font>
             </td>
             <td width=70% align=center valign=top>
                <font face=Arial size=2><b>ATAS NAMA</b></font>
             </td>             
             <td width=10% align=center valign=top>
                <font face=Arial size=2><b>HAL</b></font>
             </td>             
          </tr>
HTML
         my $query = "SELECT cust_prod_no,cust_nama, cust_sheet
	                       FROM CUST_MasterPrint$analisaperiode1
	                       WHERE CUST_MasterPrint$analisaperiode1.cust_product_id='$analisaproductid'
	                       $kondisiregionid
	                       AND CUST_MasterPrint$analisaperiode1.$varfield='$analisasegmen'
	                       AND CUST_MasterPrint$analisaperiode1.$analisagroupby='$analisacourier'
	                       ORDER BY cust_prod_no
	                       LIMIT $startlimit,$maxlimit";
         my $sth = $db->prepare($query);
         $sth->execute();
         my @row;
         while ($row = $sth->fetchrow_arrayref)
         {
             $prodnoDec = funcDec($row->[0]);
print <<"HTML";
          <tr>
             <td width=20% align=center valign=top>
                <font face=Arial size=2>$prodnoDec</font>
             </td>
             <td width=70% align=left valign=top>
                <font face=Arial size=2>$row->[1]</font>
             </td>             
             <td width=10% align=center valign=top>
                <font face=Arial size=2>$row->[2]</font>
             </td>             
          </tr>
HTML
         }
         $sth->finish;
print <<"HTML";
       </table>
      <input type=hidden name=userid value=$userid>
      <input type=hidden name=userpwd value=$userpwd>
      <input type=hidden name=userprgcode value=$userprgcode>
      <input type=hidden name=thetimestamp value='$signintime'>
      <input type=hidden name=act value='$act'>
      <input type=hidden name=analisaperiode1 value='$analisaperiode1'>
      <input type=hidden name=analisaproductid value='$analisaproductid'>
      <input type=hidden name=analisaregionid value='$analisaregionid'>
      <input type=hidden name=analisagroupby value='$analisagroupby'>
      <input type=hidden name=analisastatus value='$analisastatus'>
      <input type=hidden name=analisacourier value='$analisacourier'>
      <input type=hidden name=analisasegmen value='$analisasegmen'>
      <input type=hidden name=startlimit value='$endlimit'>
      <input type=hidden name=jumlahdata value='$jumlahdata'>
      <input type=hidden name=thetarget>
      <input type=hidden name=varfield value='$varfield'>
      </form>
     </div>
   </BODY>
</HTML>
HTML
$db->disconnect;
exit;
}

if ($act eq "report")
{
  $analisabentuk=$contents{'analisabentuk'};
  $analisaperiodebln1=$contents{'analisaperiodebln1'};
  $analisaperiodebln2=$contents{'analisaperiodebln2'};
  $analisaperiodethn1=$contents{'analisaperiodethn1'};
  $analisaperiodethn2=$contents{'analisaperiodethn2'};
  $analisaperiodetgl1=$contents{'analisaperiodetgl1'};
  $analisaperiodetgl2=$contents{'analisaperiodetgl2'};
  $analisatanggal1=$analisaperiodethn1 . "-" . $analisaperiodebln1 . "-" . $analisaperiodetgl1;
  $analisatanggal2=$analisaperiodethn1 . "-" . $analisaperiodebln1 . "-" . $analisaperiodetgl2;
  $analisaproductid=$contents{'analisaproductid'};
  $analisaregionid=$contents{'analisaregionid'};
  $analisagroupby=$contents{'analisagroupby'};
  $analisapersen=$contents{'analisapersen'};
  $thetimestamp=$contents{'thetimestamp'};
  $sort1=$contents{'sort1'};
  $sort2=$contents{'sort2'};
  $ascdesc1=$contents{'ascdesc1'};
  $ascdesc2=$contents{'ascdesc2'};
  $prgsavereport=$contents{'prgsavereport'};

  if ($analisaproductid eq "BCC")
  {
  	$varfield = "cust_segmen";
  }
  else
  {
  	$varfield = "cust_branch_id";
  }
  
  

   my $statement = "Update SE_UserProgram
		 set program_save_report='$prgsavereport'
		 WHERE user_id='$userid'
		 AND program_code='$userprgcode'";
   my $sth = $db->prepare($statement);
   $sth->execute();
   $sth->finish;


  if (length($analisaperiodebln1) == 1)
  {
     $analisaperiode1=$analisaperiodethn1 . "0" . $analisaperiodebln1;
  }
  else
  {
     $analisaperiode1=$analisaperiodethn1 . $analisaperiodebln1;
  }
  $analisaperiode2=$analisaperiode1;

  if ($analisapersen <= 0)
  {
  	$analisapersen = 100;
  }


   my $statement = "Update SE_User
		 set user_signin='Y',
		 user_signin_time='$signintime'
		 WHERE user_id='$userid'
		 AND user_pwd='$userpwd'";
   my $sth = $db->prepare($statement);
   $sth->execute();
   $sth->finish;

# Create the html page
print "Content-type: text/html\n\n";
print <<"HTML";

<HTML>
   <HEAD>
      <META http-equiv=Content-Type content='text/html; charset=iso-8859-1'>
      <META http-equiv='Pragma' content='no-cache'>
      <META content='MSHTML 5.50.4134.100' name=GENERATOR>
      <TITLE>$compname</TITLE>
      <LINK media=screen href="/snm/icons/menu.css" rel=stylesheet>
      <Script Language="JavaScript">
         function viewProduct(thestatus,thesegmen,thecourier,thejumlah)
         {
         	  document.formsubmit.target="lainnya";
         	  document.formsubmit.act.value = "viewproduct";
         	  document.formsubmit.analisastatus.value = thestatus;
         	  document.formsubmit.analisasegmen.value = thesegmen;
         	  document.formsubmit.analisacourier.value = thecourier;
         	  document.formsubmit.jumlahdata.value = thejumlah;
         	  document.formsubmit.submit();
         }
         function gotoRegion(theregion)
         {
         	  document.formsubmit.target="utama";
         	  document.formsubmit.act.value = "report";
         	  document.formsubmit.analisaregionid.value = theregion;
         	  document.formsubmit.submit();
         }
      </Script>
   </HEAD>
   <BODY aLink=$stylealink link=$stylelink vLink=$stylevlink bgcolor=$stylebodybgcol>
<script language="JavaScript"><!--
name = 'utama';
//--></script>
      <script src='/snm/icons/javabits.js' language='Javascript'></script>
      <SCRIPT language=javascript src="/snm/icons/mmenu.js"></SCRIPT>      
      <div align=center>
      <TABLE cellPadding=5 width="100%" border=0>
        <TR>
    	  <TD vAlign=top width=1>
          </TD>
          <TD align=left width="100%">
            <TABLE cellSpacing=0 cellPadding=0 width="100%" border=0>
              <TR>
                <TD class=borderB>
                  <TABLE cellSpacing=1 cellPadding=13 width="100%" border=0>
                    <TR>
                      <TD class=form1 align=middle>
                         <B>$programdesc</B>
                      </TD>
                    </TR>
                  </TABLE>
                </TD>
              </TR>
              <TR>
                <TD class=borderB>
                  <TABLE cellSpacing=1 cellPadding=13 width="100%" border=0>
                    <TR>
                      <TD class=backW>
                        $programblob
                      </TD>
                    </TR>
                  </TABLE>
                </TD>
              </TR>
              <tr>
                <TD height=15></TD>
              </TR>
              <TR>
                <TD class=borderB>
                  <TABLE cellSpacing=1 cellPadding=13 width="100%" border=0>
                    <TR>
                      <TD class=backW></TD>
                    </TR>
                  </TABLE>
                </TD>
              </TR>
              <TR>
                <TD height=15></TD>
              </TR>
              <TR>
                <TD class=borderB>
                  <TABLE cellSpacing=1 cellPadding=13 width="100%" border=0>
                    <TR>
                      <TD class=backW>
                  	<form name=formsubmit method=post action=/cgi-bin/snm/$programname>
                           <A HREF="javascript:history.go($togo);"><img src=/snm/icons/back.gif border=0 width=40 height=30></A>
		  	   <BR><BR>
HTML
# BEGIN PERSENPROSES
   if ($analisabentuk eq "persenproses")
   {
        print "<font face=Arial size=2>CYCLE : &nbsp</font>";
     if ($analisaregionid eq "all" or $analisaregionid eq "")
     {
#        my $query = "SELECT cust_region_id
#	                       FROM CUST_MasterPrint$analisaperiode1
#	                       GROUP BY cust_region_id
#	                       ORDER BY cust_region_id
#	                       LIMIT 0,1";
#        my $sth = $db->prepare($query);
#        $sth->execute();
#        my @row = $sth->fetchrow_array;
#        $sth->finish; 
        $kondisiregionid = "";
        print "<font face=Arial size=2>ALL &nbsp</font>";
     }
     else
     {
        $kondisiregionid = "AND CUST_MasterPrint$analisaperiode1.cust_region_id='$analisaregionid'";
        		print "<A HREF=\"javascript:gotoRegion('all')\">ALL</A> &nbsp";
     }
        my $query = "SELECT cust_region_id
	                       FROM CUST_MasterPrint$analisaperiode1
	                       WHERE CUST_MasterPrint$analisaperiode1.cust_product_id='$analisaproductid'
	                       GROUP BY cust_region_id
	                       ORDER BY cust_region_id";
        my $sth = $db->prepare($query);
        $sth->execute();
        my @row;
        while ($row = $sth->fetchrow_arrayref)
        {
        	if ($row->[0] eq $analisaregionid)
        	{
        		print "$row->[0] &nbsp";
        	}
        	else
        	{
        		print "<A HREF=\"javascript:gotoRegion('$row->[0]')\">$row->[0]</A> &nbsp";
        	}
        }
        $sth->finish; 

print <<"HTML";
                  	   <TABLE WIDTH=100% CELLPADDING=1 CELLSPACING=1 border=0>
      	             	      <tr>
      	                	<td width=100% valign=top align=left>
      	                	   <font face=Verdana size=3>SUMMARY PROSES PRODUK : $analisaproductid PERIOD : $analisaperiode1 REGION : $analisaregionid</font>
      	                	   <table width=100% cellpadding=0 cellspacing=0 border=1 bordercolor="#000000" bordercolorlight="#000000" bordercolordark="#FFFFFF">
      	                	      <tr>
      	                	         <td width=40% align=center valign=top rowspan=2>
      	                	            <font face=Arial size=2><b>NAMA CABANG</b></font>
      	                	         </td>
      	                	         <td width=10% align=center valign=top rowspan=2>
      	                	            <font face=Arial size=2><b>CUST</b></font>
      	                	         </td>
      	                	         <td width=10% align=center valign=top rowspan=2>
      	                	            <font face=Arial size=2><b>HAL</b></font>
      	                	         </td>
      	                	         <td width=10% align=center valign=top rowspan=2>
      	                	            <font face=Arial size=2><b>AMPLOP</b></font>
      	                	         </td>
      	                	         <td width=10% align=center valign=top rowspan=2>
      	                	            <font face=Arial size=2><b>T.T.</b></font>
      	                	         </td>
      	                	         <td width=20% align=center valign=top colspan=2>
      	                	            <font face=Arial size=2><b>NO URUT</b></font>
      	                	         </td>
      	                	      </tr>
      	                	      <tr>
      	                	         <td width=10% align=center valign=top>
      	                	            <font face=Arial size=2><b>AWAL</b></font>
      	                	         </td>
      	                	         <td width=10% align=center valign=top>
      	                	            <font face=Arial size=2><b>AKHIR</b></font>
      	                	         </td>
      	                	      </tr>
HTML
   $filetxt = $analisaproductid . $analisaregionid . $userid . ".txt";
   $fileout = "c:/xampp/htdocs/temp/" . $filetxt;
   open(FILEOUT,">$fileout");
   $line = "NAMA CABANG,CUST,HAL,AMPLOP,T.T.,NO AWAL,NO AKHIR" . "\n";
   print FILEOUT $line;
            my  $query = "SELECT CUST_MasterPrint$analisaperiode1.$varfield, CUST_MasterPrint$analisaperiode1.$analisagroupby,
                         COUNT(*), SUM(cust_sheet), ROUND(SUM(cust_total_bill),0)
	                       FROM CUST_MasterPrint$analisaperiode1
	                       WHERE CUST_MasterPrint$analisaperiode1.cust_product_id='$analisaproductid'
	                       $kondisiregionid
#	                       AND CUST_MasterPrint$analisaperiode1.cust_vendor like '%DMP%'
	                       GROUP BY CUST_MasterPrint$analisaperiode1.$varfield, CUST_MasterPrint$analisaperiode1.$analisagroupby
	                       ORDER BY CUST_MasterPrint$analisaperiode1.$varfield, CUST_MasterPrint$analisaperiode1.$analisagroupby";            	
            my $sth = $db->prepare($query);
            $sth->execute();
            my @row;
            $oldsegmen = "";
            $subcust = 0;
            $subhal = 0;
            $subamplop = 0;
            $totalcust = 0;
            $totalhal = 0;
            $totalamplop = 0;
            while ($row = $sth->fetchrow_arrayref)
            {
            	   if ($analisaproductid eq "BCC")
            	   {
		               $querytemp = "SELECT segmen_name
		                              FROM TblSegmen
		                              WHERE segmen_id='$row->[0]'";
            	   }
            	   else
            	   {
		               $querytemp = "SELECT branch_name
		                              FROM TblBranch
		                              WHERE branch_id='$row->[0]'";
            	   }            	   
   		           my $sth = $db->prepare($querytemp);
		             $sth->execute();
		             my @rowtemp = $sth->fetchrow_array;
		             $sth->finish;
		             if ($rowtemp[0] eq "")
		             {
		             	  if ($row->[0] eq "")
		             	  {
		                   $segmenname = "unknown";
		                }
		                else
		             	  {
		                   $segmenname = "$row->[0]";
		                }
		             }
		             else
		             {
		                $segmenname = $rowtemp[0];
		             }
		             if ($oldsegmen ne $segmenname)
		             {
                    if ($oldsegmen ne "")
                    {
                    	 $totalcust += $subcust;
                    	 $totalhal += $subhal;
                    	 $totalamplop += $subamplop;
print <<"HTML";
      	                	      <tr>
      	                	         <td width=40% align=right valign=top>
      	                	            <font face=Arial size=2><b>Sub Total &nbsp</b></font>
      	                	         </td>
      	                	         <td width=10% align=right valign=top>
      	                	            <font face=Arial size=2><b>$subcust</b></font>
      	                	         </td>
      	                	         <td width=10% align=right valign=top>
      	                	            <font face=Arial size=2><b>$subhal</b></font>
      	                	         </td>
      	                	         <td width=10% align=right valign=top>
      	                	            <font face=Arial size=2><b>$subamplop</b></font>
      	                	         </td>
      	                	         <td width=10% align=center valign=top>
      	                	            <font face=Arial size=2>&nbsp</font>
      	                	         </td>
      	                	         <td width=10% align=center valign=top>
      	                	            <font face=Arial size=2>&nbsp</font>
      	                	         </td>
      	                	         <td width=10% align=center valign=top>
      	                	            <font face=Arial size=2>&nbsp</font>
      	                	         </td>
      	                	      </tr>
HTML
                        $line = "Sub Total,$subcust,$subhal,$subamplop,,," . "\n";
                        print FILEOUT $line;
                    }
print <<"HTML";
      	                	      <tr>
      	                	         <td width=40% align=left valign=top>
      	                	            <font face=Arial size=2><b>$segmenname</b></font>
      	                	         </td>
      	                	         <td width=10% align=center valign=top>
      	                	            <font face=Arial size=2>&nbsp</font>
      	                	         </td>
      	                	         <td width=10% align=center valign=top>
      	                	            <font face=Arial size=2>&nbsp</font>
      	                	         </td>
      	                	         <td width=10% align=center valign=top>
      	                	            <font face=Arial size=2>&nbsp</font>
      	                	         </td>
      	                	         <td width=10% align=center valign=top>
      	                	            <font face=Arial size=2>&nbsp</font>
      	                	         </td>
      	                	         <td width=10% align=center valign=top>
      	                	            <font face=Arial size=2>&nbsp</font>
      	                	         </td>
      	                	         <td width=10% align=center valign=top>
      	                	            <font face=Arial size=2>&nbsp</font>
      	                	         </td>
      	                	      </tr>
HTML
                        $line = "$segmenname,,,,,," . "\n";
                        print FILEOUT $line;

		                my $querytemp = "SELECT COUNT(*)
	                          FROM CUST_MasterPrint$analisaperiode1
	                          WHERE CUST_MasterPrint$analisaperiode1.cust_product_id='$analisaproductid'
	                          $kondisiregionid
# 	                          AND CUST_MasterPrint$analisaperiode1.cust_vendor like '%DMP%'
	                          AND CUST_MasterPrint$analisaperiode1.$varfield='$row->[0]'";
   		              my $sth = $db->prepare($querytemp);
		                $sth->execute();
		                my @rowtemp = $sth->fetchrow_array;
		                $sth->finish;
		                $varawal = $rowtemp[0];
		                $varakhir = 0;
		             	  $oldsegmen = $segmenname;
                    $subcust = 0;
                    $subhal = 0;
                    $subamplop = 0;
		             }
		             if ($row->[1] eq "")
		             {
		             	   $row->[1] = "unknown";
		             }
		             $subcust += $row->[2];
		             $subhal += $row->[3];
		             $subamplop += $row->[4];
		             if ($varakhir <= 0)
		             {
		                $varawal = $varawal - $varakhir;
		             }
		             $varakhir = $varawal - $row->[2] + 1;
print <<"HTML";
      	                	      <tr>
      	                	         <td width=40% align=left valign=top>
      	                	            <font face=Arial size=2>&nbsp $row->[1]</font>
      	                	         </td>
      	                	         <td width=10% align=right valign=top>
      	                	            <font face=Arial size=2>&nbsp <A HREF="javascript:viewProduct('cust','$row->[0]','$row->[1]','$row->[2]')">$row->[2]</A></font>
      	                	         </td>
      	                	         <td width=10% align=right valign=top>
      	                	            <font face=Arial size=2>&nbsp $row->[3]</font>
      	                	         </td>
      	                	         <td width=10% align=right valign=top>
      	                	            <font face=Arial size=2>&nbsp $row->[4]</font>
      	                	         </td>
      	                	         <td width=10% align=center valign=top>
      	                	            <font face=Arial size=2>&nbsp</font>
      	                	         </td>
      	                	         <td width=10% align=center valign=top>
      	                	            <font face=Arial size=2>$varawal</font>
      	                	         </td>
      	                	         <td width=10% align=center valign=top>
      	                	            <font face=Arial size=2>$varakhir</font>
      	                	         </td>
      	                	      </tr>
HTML
                        $line = "$row->[1],$row->[2],$row->[3],$row->[4],,$varawal,$varakhir" . "\n";
                        print FILEOUT $line;
		             $varawal = $varakhir - 1;
            }
            $sth->finish;
                    	 $totalcust += $subcust;
                    	 $totalhal += $subhal;
                    	 $totalamplop += $subamplop;
print <<"HTML";
      	                	      <tr>
      	                	         <td width=40% align=right valign=top>
      	                	            <font face=Arial size=2><b>Sub Total &nbsp</b></font>
      	                	         </td>
      	                	         <td width=10% align=right valign=top>
      	                	            <font face=Arial size=2><b>$subcust</b></font>
      	                	         </td>
      	                	         <td width=10% align=right valign=top>
      	                	            <font face=Arial size=2><b>$subhal</b></font>
      	                	         </td>
      	                	         <td width=10% align=right valign=top>
      	                	            <font face=Arial size=2><b>$subamplop</b></font>
      	                	         </td>
      	                	         <td width=10% align=center valign=top>
      	                	            <font face=Arial size=2>&nbsp</font>
      	                	         </td>
      	                	         <td width=10% align=center valign=top>
      	                	            <font face=Arial size=2>&nbsp</font>
      	                	         </td>
      	                	         <td width=10% align=center valign=top>
      	                	            <font face=Arial size=2>&nbsp</font>
      	                	         </td>
      	                	      </tr>
      	                	      <tr>
      	                	         <td width=40% align=right valign=top>
      	                	            <font face=Arial size=2>&nbsp</font>
      	                	         </td>
      	                	         <td width=10% align=right valign=top>
      	                	            <font face=Arial size=2>&nbsp</font>
      	                	         </td>
      	                	         <td width=10% align=right valign=top>
      	                	            <font face=Arial size=2>&nbsp</font>
      	                	         </td>
      	                	         <td width=10% align=right valign=top>
      	                	            <font face=Arial size=2>&nbsp</font>
      	                	         </td>
      	                	         <td width=10% align=center valign=top>
      	                	            <font face=Arial size=2>&nbsp</font>
      	                	         </td>
      	                	         <td width=10% align=center valign=top>
      	                	            <font face=Arial size=2>&nbsp</font>
      	                	         </td>
      	                	         <td width=10% align=center valign=top>
      	                	            <font face=Arial size=2>&nbsp</font>
      	                	         </td>
      	                	      </tr>
      	                	      <tr>
      	                	         <td width=40% align=right valign=top>
      	                	            <font face=Arial size=2><b>Grand Total &nbsp</b></font>
      	                	         </td>
      	                	         <td width=10% align=right valign=top>
      	                	            <font face=Arial size=2><b>$totalcust</b></font>
      	                	         </td>
      	                	         <td width=10% align=right valign=top>
      	                	            <font face=Arial size=2><b>$totalhal</b></font>
      	                	         </td>
      	                	         <td width=10% align=right valign=top>
      	                	            <font face=Arial size=2><b>$totalamplop</b></font>
      	                	         </td>
      	                	         <td width=10% align=center valign=top>
      	                	            <font face=Arial size=2>&nbsp</font>
      	                	         </td>
      	                	         <td width=10% align=center valign=top>
      	                	            <font face=Arial size=2>&nbsp</font>
      	                	         </td>
      	                	         <td width=10% align=center valign=top>
      	                	            <font face=Arial size=2>&nbsp</font>
      	                	         </td>
      	                	      </tr>
HTML
                        $line = "Sub Total,$subcust,$subhal,$subamplop,,," . "\n";
                        print FILEOUT $line;
                        $line = ",,,,,," . "\n";
                        print FILEOUT $line;
                        $line = "Grand Total,$totalcust,$totalhal,$totalamplop,,," . "\n";
                        print FILEOUT $line;
print <<"HTML";
      	                	   </table>
      	                	</td>
      	                      </tr>
                            </TABLE>
HTML
     close(FILEOUT);
     print "<A HREF=/temp/$filetxt>Download Text File</A> (Klik Kanan Save Target As..)";
   }
# END PERSEN PROSES
# BEGIN EBSPROSES
   if ($analisabentuk eq "ebsproses")
   {
        print "<font face=Arial size=2>CYCLE : &nbsp</font>";
     if ($analisaregionid eq "all" or $analisaregionid eq "")
     {
#        my $query = "SELECT cust_region_id
#	                       FROM CUST_MasterPrint$analisaperiode1
#	                       GROUP BY cust_region_id
#	                       ORDER BY cust_region_id
#	                       LIMIT 0,1";
#        my $sth = $db->prepare($query);
#        $sth->execute();
#        my @row = $sth->fetchrow_array;
#        $sth->finish; 
        $kondisiregionid = "";
        print "<font face=Arial size=2>ALL &nbsp</font>";
     }
     else
     {
        $kondisiregionid = "AND CUST_MasterPrint$analisaperiode1.cust_region_id='$analisaregionid'";
        		print "<A HREF=\"javascript:gotoRegion('all')\">ALL</A> &nbsp";
     }
        my $query = "SELECT cust_region_id
	                       FROM CUST_MasterPrint$analisaperiode1
	                       WHERE CUST_MasterPrint$analisaperiode1.cust_product_id='$analisaproductid'
	                       GROUP BY cust_region_id
	                       ORDER BY cust_region_id";
        my $sth = $db->prepare($query);
        $sth->execute();
        my @row;
        while ($row = $sth->fetchrow_arrayref)
        {
        	if ($row->[0] eq $analisaregionid)
        	{
        		print "$row->[0] &nbsp";
        	}
        	else
        	{
        		print "<A HREF=\"javascript:gotoRegion('$row->[0]')\">$row->[0]</A> &nbsp";
        	}
        }
        $sth->finish; 

print <<"HTML";
                  	   <TABLE WIDTH=100% CELLPADDING=1 CELLSPACING=1 border=0>
      	             	      <tr>
      	                	<td width=100% valign=top align=left>
      	                	   <font face=Verdana size=3>SUMMARY DELIVERY PRODUK : $analisaproductid PERIOD : $analisaperiode1 REGION : $analisaregionid</font>
      	                	   <table width=100% cellpadding=0 cellspacing=0 border=1 bordercolor="#000000" bordercolorlight="#000000" bordercolordark="#FFFFFF">
      	                	      <tr>
      	                	         <td width=40% align=center valign=top>
      	                	            <font face=Arial size=2><b>NAMA CABANG</b></font>
      	                	         </td>
      	                	         <td width=15% align=center valign=top>
      	                	            <font face=Arial size=2><b>CUST</b></font>
      	                	         </td>
      	                	         <td width=15% align=center valign=top>
      	                	            <font face=Arial size=2><b>SUKSES</b></font>
      	                	         </td>
      	                	         <td width=15% align=center valign=top>
      	                	            <font face=Arial size=2><b>GAGAL</b></font>
      	                	         </td>
      	                	         <td width=15% align=center valign=top>
      	                	            <font face=Arial size=2><b>NOSTATUS</b></font>
      	                	         </td>
      	                	      </tr>
HTML
            my  $query = "SELECT CUST_MasterPrint$analisaperiode1.$varfield, CUST_MasterPrint$analisaperiode1.$analisagroupby,
                         COUNT(*), SUM(cust_sheet), ROUND(SUM(cust_total_bill),0)
	                       FROM CUST_MasterPrint$analisaperiode1
	                       WHERE CUST_MasterPrint$analisaperiode1.cust_product_id='$analisaproductid'
	                       $kondisiregionid
	                       AND CUST_MasterPrint$analisaperiode1.cust_vendor like '%EBS%'
	                       GROUP BY CUST_MasterPrint$analisaperiode1.$varfield, CUST_MasterPrint$analisaperiode1.$analisagroupby
	                       ORDER BY CUST_MasterPrint$analisaperiode1.$varfield, CUST_MasterPrint$analisaperiode1.$analisagroupby";            	
            my $sth = $db->prepare($query);
            $sth->execute();
            my @row;
            $oldsegmen = "";
            $subcust = 0;
            $subhal = 0;
            $subamplop = 0;
            $totalcust = 0;
            $totalhal = 0;
            $totalamplop = 0;
            while ($row = $sth->fetchrow_arrayref)
            {
            	   if ($analisaproductid eq "BCC")
            	   {
		               $querytemp = "SELECT segmen_name
		                              FROM TblSegmen
		                              WHERE segmen_id='$row->[0]'";
            	   }
            	   else
            	   {
		               $querytemp = "SELECT branch_name
		                              FROM TblBranch
		                              WHERE branch_id='$row->[0]'";
            	   }            	   
   		           my $sth = $db->prepare($querytemp);
		             $sth->execute();
		             my @rowtemp = $sth->fetchrow_array;
		             $sth->finish;
		             if ($rowtemp[0] eq "")
		             {
		             	  if ($row->[0] eq "")
		             	  {
		                   $segmenname = "unknown";
		                }
		                else
		             	  {
		                   $segmenname = "$row->[0]";
		                }
		             }
		             else
		             {
		                $segmenname = $rowtemp[0];
		             }
		             if ($oldsegmen ne $segmenname)
		             {
                    if ($oldsegmen ne "")
                    {
                    	 $totalcust += $subcust;
                    	 $totalhal += $subhal;
                    	 $totalamplop += $subamplop;
print <<"HTML";
      	                	      <tr>
      	                	         <td width=40% align=right valign=top>
      	                	            <font face=Arial size=2><b>Sub Total &nbsp</b></font>
      	                	         </td>
      	                	         <td width=15% align=right valign=top>
      	                	            <font face=Arial size=2><b>$subcust</b></font>
      	                	         </td>
      	                	         <td width=15% align=right valign=top>
      	                	            <font face=Arial size=2><b>$subhal</b></font>
      	                	         </td>
      	                	         <td width=15% align=right valign=top>
      	                	            <font face=Arial size=2><b>$subamplop</b></font>
      	                	         </td>
      	                	         <td width=15% align=center valign=top>
      	                	            <font face=Arial size=2>&nbsp</font>
      	                	         </td>
      	                	      </tr>
HTML
                    }
print <<"HTML";
      	                	      <tr>
      	                	         <td width=40% align=left valign=top>
      	                	            <font face=Arial size=2><b>$segmenname</b></font>
      	                	         </td>
      	                	         <td width=15% align=center valign=top>
      	                	            <font face=Arial size=2>&nbsp</font>
      	                	         </td>
      	                	         <td width=15% align=center valign=top>
      	                	            <font face=Arial size=2>&nbsp</font>
      	                	         </td>
      	                	         <td width=15% align=center valign=top>
      	                	            <font face=Arial size=2>&nbsp</font>
      	                	         </td>
      	                	         <td width=15% align=center valign=top>
      	                	            <font face=Arial size=2>&nbsp</font>
      	                	         </td>
      	                	      </tr>
HTML

		                my $querytemp = "SELECT cust_status,COUNT(*)
	                          FROM CUST_EBS$analisaperiode1
	                          WHERE cust_region_id<>'99'
	                          $kondisiebsregionid
	                          GROUP BY cust_status";
                    my $sth = $db->prepare($querytemp);
                    $sth->execute();
                    my @rowtemp;
                    while ($rowtemp = $sth->fetchrow_arrayref)
                    {
                    	  if ($rowtemp->[0] eq "N")
                    	  {
                    	  	$subgagal = $rowtemp->[1];
                    	  }
                    	  if ($rowtemp->[0] eq "Y")
                    	  {
                    	  	$subsukses = $rowtemp->[1];
                    	  }
                    }
                    $sth->finish;
		             }
		             if ($row->[1] eq "")
		             {
		             	   $row->[1] = "unknown";
		             }
print <<"HTML";
      	                	      <tr>
      	                	         <td width=40% align=left valign=top>
      	                	            <font face=Arial size=2>&nbsp $row->[1]</font>
      	                	         </td>
      	                	         <td width=15% align=right valign=top>
      	                	            <font face=Arial size=2>&nbsp <A HREF="javascript:viewProduct('cust','$row->[0]','$row->[1]','$row->[2]')">$row->[2]</A></font>
      	                	         </td>
      	                	         <td width=15% align=right valign=top>
      	                	            <font face=Arial size=2>&nbsp $subsukses</font>
      	                	         </td>
      	                	         <td width=15% align=right valign=top>
      	                	            <font face=Arial size=2>&nbsp $subgagal</font>
      	                	         </td>
      	                	         <td width=15% align=center valign=top>
      	                	            <font face=Arial size=2>&nbsp $subnostatus</font>
      	                	         </td>
      	                	      </tr>
HTML
            }
            $sth->finish;
print <<"HTML";
      	                	   </table>
      	                	</td>
      	                      </tr>
                            </TABLE>
HTML
   }
# END EBSPROSES
# BEGIN EXCEPTNOREK
   if ($analisabentuk eq "exceptnorek")
   {
        print "<font face=Arial size=2>CYCLE : &nbsp</font>";
     if ($analisaregionid eq "all" or $analisaregionid eq "")
     {
        $kondisiregionid = "";
        print "<font face=Arial size=2>ALL &nbsp</font>";
     }
     else
     {
        $kondisiregionid = "AND split_region_id='$analisaregionid'";
        		print "<A HREF=\"javascript:gotoRegion('all')\">ALL</A> &nbsp";
     }
        my $query = "SELECT split_region_id
	                       FROM SPLIT_NorekException
	                       WHERE split_process_period='$analisaperiode1'
	                       AND split_product_id='$analisaproductid'
	                       GROUP BY split_region_id
	                       ORDER BY split_region_id";
        my $sth = $db->prepare($query);
        $sth->execute();
        my @row;
        while ($row = $sth->fetchrow_arrayref)
        {
        	if ($row->[0] eq $analisaregionid)
        	{
        		print "$row->[0] &nbsp";
        	}
        	else
        	{
        		print "<A HREF=\"javascript:gotoRegion('$row->[0]')\">$row->[0]</A> &nbsp";
        	}
        }
        $sth->finish; 

print <<"HTML";
                  	   <TABLE WIDTH=100% CELLPADDING=1 CELLSPACING=1 border=0>
      	             	      <tr>
      	                	<td width=100% valign=top align=left>
      	                	   <font face=Verdana size=3>EXCEPTION PRODUK : $analisaproductid PERIOD : $analisaperiode1 REGION : $analisaregionid</font>
      	                	   <table width=100% cellpadding=0 cellspacing=0 border=1 bordercolor="#000000" bordercolorlight="#000000" bordercolordark="#FFFFFF">
      	                	      <tr>
      	                	         <td width=30% align=center valign=top>
      	                	            <font face=Arial size=2><b>NOMOR REKENING</b></font>
      	                	         </td>
      	                	         <td width=30% align=center valign=top>
      	                	            <font face=Arial size=2><b>NAMA CUSTOMER</b></font>
      	                	         </td>
      	                	         <td width=10% align=center valign=top>
      	                	            <font face=Arial size=2><b>PRODUK</b></font>
      	                	         </td>
      	                	         <td width=15% align=center valign=top>
      	                	            <font face=Arial size=2><b>CYCLE ORIGINAL</b></font>
      	                	         </td>
      	                	         <td width=15% align=center valign=top>
      	                	            <font face=Arial size=2><b>CYCLE SAAT INI</b></font>
      	                	         </td>
      	                	      </tr>
HTML
            my  $query = "SELECT *
	                       FROM SPLIT_NorekException
	                       WHERE split_process_period='$analisaperiode1'
	                       AND split_product_id='$analisaproductid'
	                       $kondisiregionid
	                       ORDER BY split_norek";            	
            my $sth = $db->prepare($query);
            $sth->execute();
            my @row;
            while ($row = $sth->fetchrow_arrayref)
            {
		             my $querytemp = "SELECT cust_region_id, cust_nama
		                              FROM CUST_MasterPrint$analisaperiode1
		                              WHERE cust_prod_no_real='$row->[0]'";
   		           my $sth = $db->prepare($querytemp);
		             $sth->execute();
		             my @rowtemp = $sth->fetchrow_array;
		             $sth->finish;
print <<"HTML";
      	                	      <tr>
      	                	         <td width=30% align=center valign=top>
      	                	            <font face=Arial size=2>$row->[0]</font>
      	                	         </td>
      	                	         <td width=30% align=center valign=top>
      	                	            <font face=Arial size=2>$rowtemp[1]</font>
      	                	         </td>
      	                	         <td width=10% align=center valign=top>
      	                	            <font face=Arial size=2>$row->[2]</font>
      	                	         </td>
      	                	         <td width=15% align=center valign=top>
      	                	            <font face=Arial size=2>$rowtemp[0]</font>
      	                	         </td>
      	                	         <td width=15% align=center valign=top>
      	                	            <font face=Arial size=2>$row->[3]</font>
      	                	         </td>
      	                	      </tr>
HTML
            }
            $sth->finish;
   }
# END EXCEPTNOREK
# BEGIN EXCEPTFILE
   if ($analisabentuk eq "exceptfile")
   {
        print "<font face=Arial size=2>CYCLE : &nbsp</font>";
     if ($analisaregionid eq "all" or $analisaregionid eq "")
     {
        $kondisiregionid = "";
        print "<font face=Arial size=2>ALL &nbsp</font>";
     }
     else
     {
        $kondisiregionid = "AND split_region_id='$analisaregionid'";
        		print "<A HREF=\"javascript:gotoRegion('all')\">ALL</A> &nbsp";
     }
        my $query = "SELECT split_region_id
	                       FROM SPLIT_FileException
	                       WHERE split_process_period='$analisaperiode1'
	                       AND split_product_id='$analisaproductid'
	                       GROUP BY split_region_id
	                       ORDER BY split_region_id";
        my $sth = $db->prepare($query);
        $sth->execute();
        my @row;
        while ($row = $sth->fetchrow_arrayref)
        {
        	if ($row->[0] eq $analisaregionid)
        	{
        		print "$row->[0] &nbsp";
        	}
        	else
        	{
        		print "<A HREF=\"javascript:gotoRegion('$row->[0]')\">$row->[0]</A> &nbsp";
        	}
        }
        $sth->finish; 

print <<"HTML";
                  	   <TABLE WIDTH=100% CELLPADDING=1 CELLSPACING=1 border=0>
      	             	      <tr>
      	                	<td width=100% valign=top align=left>
      	                	   <font face=Verdana size=3>EXCEPTION PRODUK : $analisaproductid PERIOD : $analisaperiode1 REGION : $analisaregionid</font>
      	                	   <table width=100% cellpadding=0 cellspacing=0 border=1 bordercolor="#000000" bordercolorlight="#000000" bordercolordark="#FFFFFF">
      	                	      <tr>
      	                	         <td width=50% align=center valign=top>
      	                	            <font face=Arial size=2><b>NAMA FILE</b></font>
      	                	         </td>
      	                	         <td width=10% align=center valign=top>
      	                	            <font face=Arial size=2><b>PRODUK</b></font>
      	                	         </td>
      	                	         <td width=10% align=center valign=top>
      	                	            <font face=Arial size=2>CYCLE</font>
      	                	         </td>
      	                	         <td width=15% align=center valign=top>
      	                	            <font face=Arial size=2><b>DATA PERIOD</b></font>
      	                	         </td>
      	                	         <td width=15% align=center valign=top>
      	                	            <font face=Arial size=2><b>PROCESS PERIOD</b></font>
      	                	         </td>
      	                	      </tr>
HTML
            my  $query = "SELECT *
	                       FROM SPLIT_FileException
	                       WHERE split_process_period='$analisaperiode1'
	                       AND split_product_id='$analisaproductid'
	                       $kondisiregionid
	                       ORDER BY split_region_id,split_filename";
            my $sth = $db->prepare($query);
            $sth->execute();
            my @row;
            while ($row = $sth->fetchrow_arrayref)
            {
print <<"HTML";
      	                	      <tr>
      	                	         <td width=50% align=left valign=top>
      	                	            <font face=Arial size=2>$row->[0]</font>
      	                	         </td>
      	                	         <td width=10% align=center valign=top>
      	                	            <font face=Arial size=2>$row->[2]</font>
      	                	         </td>
      	                	         <td width=10% align=center valign=top>
      	                	            <font face=Arial size=2>$row->[3]</font>
      	                	         </td>
      	                	         <td width=15% align=center valign=top>
      	                	            <font face=Arial size=2>$row->[4]</font>
      	                	         </td>
      	                	         <td width=15% align=center valign=top>
      	                	            <font face=Arial size=2>$row->[5]</font>
      	                	         </td>
      	                	      </tr>
HTML
            }
            $sth->finish;
   }
# END EXCEPTFILE
print <<"HTML";

      		     	   <input type=hidden name=togo value=$togo>
      		     	   <input type=hidden name=userid value=$userid>
          	     	   <input type=hidden name=userpwd value=$userpwd>
      		     	   <input type=hidden name=userprgcode value=$userprgcode>
          	     	   <input type=hidden name=thetimestamp value='$signintime'>
          	     	   <input type=hidden name=act value=''>
          	     	   <input type=hidden name=analisaperiode1 value='$analisaperiode1'>
          	     	   <input type=hidden name=analisaproductid value='$analisaproductid'>
          	     	   <input type=hidden name=analisaregionid value='$analisaregionid'>
          	     	   <input type=hidden name=analisagroupby value='$analisagroupby'>
          	     	   <input type=hidden name=varfield value='$varfield'>
          	     	   <input type=hidden name=analisastatus>
          	     	   <input type=hidden name=analisacourier>
          	     	   <input type=hidden name=analisasegmen>
          	     	   <input type=hidden name=jumlahdata>
          	     	   <input type=hidden name=analisabentuk value='$analisabentuk'>
          	     	   <input type=hidden name=analisaperiodebln1 value='$analisaperiodebln1'>
          	     	   <input type=hidden name=analisaperiodebln2 value='$analisaperiodebln2'>
          	     	   <input type=hidden name=analisaperiodethn1 value='$analisaperiodethn1'>
          	     	   <input type=hidden name=analisaperiodethn2 value='$analisaperiodethn2'>
          	     	   <input type=hidden name=analisaperiodetgl1 value='$analisaperiodetgl1'>
          	     	   <input type=hidden name=analisaperiodetgl2 value='$analisaperiodetgl2'>
          	     	   <input type=hidden name=analisapersen value='$analisapersen'>
          	     	   <input type=hidden name=sort1 value='$sort1'>
          	     	   <input type=hidden name=sort2 value='$sort2'>
          	     	   <input type=hidden name=ascdesc1 value='$ascdesc1'>
          	     	   <input type=hidden name=ascdesc2 value='$ascdesc2'>
          	     	   <input type=hidden name=prgsavereport value='$$prgsavereport'>
                  	</form>
                      </TD>
                    </TR>
                    <TR>
                      <TD class=backW></TD>
                    </TR>
                  </TABLE>
                </TD>
              </TR>
              <TR>
                <TD height=15></TD>
              </TR>
              <TR>
                <TD class=borderB>
                  <A name='F1'>
                  &nbsp <font face=Verdana size=2 color=$stylebodybgcol>HELP</font>
                  <TABLE cellSpacing=1 cellPadding=13 width="100%" border=0>
                    <TR>
                      <TD class=form2>
                        <UL>
                          $programhelp
                        </UL>
                      </TD>
                    </TR>
                  </TABLE>
                  &nbsp <font face=Verdana size=2 color=$stylebodybgcol>RELATED <m>LINK</m> (Membutuhkan Data Dari) :</font>
                  <TABLE cellSpacing=1 cellPadding=13 width="100%" border=0>
                    <TR>
                      <TD class=form2>
                        <UL>
                          $programrlink
                        </UL>
                      </TD>
                    </TR>
                  </TABLE>
                  &nbsp <font face=Verdana size=2 color=$stylebodybgcol><m>LINK</m> TO (Data Diperlukan Untuk) :</font>
                  <TABLE cellSpacing=1 cellPadding=13 width="100%" border=0>
                    <TR>
                      <TD class=form2>
                        <UL>
                          $programlinkt
                        </UL>
                      </TD>
                    </TR>
                  </TABLE>
                  </A>
      		  <form name=secsystem method=post>
         	   <input type=hidden name=userhwid value='$userhwid'>
         	   <input type=hidden name=userid value='$userid'>
         	   <input type=hidden name=userpwd value='$userpwd'>
         	   <input type=hidden name=userprgcode value=''>
      		  </form>
                </TD>
              </TR>
              <TR>
                <TD height=15></TD>
              </TR>
            </TABLE>
          </TD>
        </TR>
      </TABLE>
     </div>
   </BODY>
</HTML>
HTML
$db->disconnect;
exit;
}

sub MAIN
{
# Create the html page
print "Content-type: text/html\n\n";
print <<"HTML";

<HTML>
   <HEAD>
      <META http-equiv=Content-Type content='text/html; charset=iso-8859-1'>
      <META http-equiv='Pragma' content='no-cache'>
      <META content='MSHTML 5.50.4134.100' name=GENERATOR>
      <TITLE>$compname</TITLE>
      <LINK media=screen href="/snm/icons/menu.css" rel=stylesheet>
      <Script Language="JavaScript">
HTML
  	my $query = "SELECT program_save_report
             FROM SE_UserProgram
	     WHERE user_id='$userid'
	     AND program_code='$userprgcode'";
  	my $sth = $db->prepare($query);
  	$sth->execute();
  	my @row = $sth->fetchrow_array;
  	$sth->finish;
        print "var dataReport =  new Array(";
	@datalines = split(/;/,$row[0]);
        for ($i=0;$i<@datalines;$i++)
        {
	   @datatemp = split(/:/,$datalines[$i]);
           for ($j=0;$j<@datatemp;$j++)
           {
            print "\"$datatemp[$j]\",";
           }
        }
   	print "\"'EOD'\"";
        print ")\;\n";
print <<"HTML";
         function isiSort(thenumber)
         {
            varindex = eval("document.formsubmit.groupby" + thenumber + ".selectedIndex");
            if (eval(thenumber) > 1)
            {
            	varindex--;
            }
            varvalue = eval("document.formsubmit.groupby" + thenumber + ".options[document.formsubmit.groupby" + thenumber + ".selectedIndex].value != ''");            
            if (varvalue != "")
            {
            	eval("document.formsubmit.sort" + thenumber + ".options[" + varindex + "].selected = true");
            }
         }
      </Script>
   </HEAD>
   <BODY aLink=$stylealink link=$stylelink vLink=$stylevlink bgcolor=$stylebodybgcol onload=mulailah()>
      $styleobj01
<script language="JavaScript"><!--
name = 'utama';
//--></script>
      <script src='/snm/icons/javabits.js' language='Javascript'></script>
      $styleie5menuopen
      $styleie5menuisi
      $styleie5menuclose
      <div align=center>
      <TABLE cellPadding=5 width="100%" border=0>
        <TR>
    	  <TD vAlign=top width=1>
            <TABLE cellSpacing=0 cellPadding=0 width="95%" border=0>
              <TR>
                <TD class=backW vAlign=center>
                  <SPAN>
                    <TABLE height=10 cellSpacing=0 cellPadding=0 width=250 border=0>
	              <TR>
        	        <TD class=borderB>
	                  <TABLE cellSpacing=1 cellPadding=1 width="100%" border=0>
                	    <TR>
        	              <TD align=middle>
	                         <font face=Verdana style="font-size: 12;" color="#FFFFFF"><B><U>$programdesc</U></B></font>
                	      </TD>
        	            </TR>
	                  </TABLE>
        	        </TD>
	              </TR>
        	      <TR>
	                <TD class=borderB>
                	  <TABLE cellSpacing=1 cellPadding=10 width="100%" border=0>
        	            <TR>
	                      <TD class=backW>
                	        <font face=Arial style="font-size: 11;line-height: 1">$programblob</font>
        	              </TD>
	                    </TR>
                	  </TABLE>
        	        </TD>
	              </TR>
                      <TR>
                        <TD class=borderB vAlign=center align=middle>
	                  <A name='F1'>
	                     <TABLE cellSpacing=1 cellPadding=0 width="100%" border=0>
                    	        <TR>
                      	 	  <TD bgcolor="#d0d0d0" align=center>
        	           	      <font face=Verdana style="font-size: 11;"><b>HELP</b></font>
                      	          </TD>
                    		</TR>
                    	        <TR>
                      	 	  <TD class=form2>
                      	 	     <p style="margin-top: 0; margin-bottom: -30">&nbsp;</p>
                        	     <UL>
                	        	<font face=Arial style="font-size: 11;line-height: 1">$programhelp</font>
                        	     </UL>
                      	          </TD>
                    		</TR>
                    	        <TR>
                      	 	  <TD bgcolor="#d0d0d0" align=center>
        	           	      <font face=Verdana style="font-size: 11;"><b>RELATED <m>LINK</m></b></font>
                      	          </TD>
                    		</TR>
                    	        <TR>
                      	 	  <TD class=form2>
                      	 	     <p style="margin-top: 0; margin-bottom: -30">&nbsp;</p>
                	        	<font face=Arial style="font-size: 11">$programrlink</font>
                	        	<BR><BR>
                      	          </TD>
                    		</TR>
                    	        <TR>
                      	 	  <TD bgcolor="#d0d0d0" align=center>
        	           	      <font face=Verdana style="font-size: 11;"><b><m>LINK</m> TO</b></font>
                      	          </TD>
                    		</TR>
                    	        <TR>
                      	 	  <TD class=form2>
                      	 	     <p style="margin-top: 0; margin-bottom: -30">&nbsp;</p>
                	        	<font face=Arial style="font-size: 11">$programlinkt</font>
                	        	<BR><BR>
                      	          </TD>
                    		</TR>
                    	        <TR>
                      	 	  <TD bgcolor="#d0d0d0" align=center>
        	           	      <font face=Verdana style="font-size: 11;"><b>HOW TO</b></font>
                      	          </TD>
                    		</TR>
                    	        <TR>
                      	 	  <TD class=form2>
                      	 	    <BR>
                      	 	    <BR>
                      	          </TD>
                    		</TR>
                  	     </TABLE>
                  	  </A>
                        </TD>
                      </TR>
                    </TABLE>
                  </SPAN>
          	</TD>
              </TR>
            </TABLE>
          </TD>
          <TD align=left valign=top>
            <TABLE cellSpacing=0 cellPadding=0 width="100%" border=0>
              <TR>
                <TD class=borderForm align=right>
                      <font style="font-size: 12;" color=#FFFFFF><B>Form type : $formtype &nbsp</B></font>
                </TD>
              </TR>
              <TR>
                <TD height=15></TD>
              </TR>
              <TR>
                <TD class=borderB>
                  <TABLE cellSpacing=1 cellPadding=13 width="100%" border=0>
                    <TR>
                      <TD class=backW>
                  	<form name=formsubmit method=post action=/cgi-bin/snm/$programname>
                  	   <TABLE WIDTH=100% CELLPADDING=1 CELLSPACING=1 border=0>
      	             	      <tr>
      	                	<td width=100% valign=top align=left>
      	                	   <font face=Verdana size=2><b>FILTERISASI DATA</b></font>
      	                	   <br><br>
      	                	   <table width=100% cellpadding=0 cellspacing=0 border=0>
      	                	      <tr>
      	                	         <td width=20% align=left valign=top>
      	                	   	    <font face=Arial size=2>Bentuk Analisa</font>
      	                	         </td>
      	                	         <td width=80%align=left valign=top>
      	                	          <input type=radio name=analisabentuk value='persenproses' checked>
      	                	          <font face=Arial size=2>Summary Proses</font>
      	                	          <input type=radio name=analisabentuk value='ebsproses'>
      	                	          <font face=Arial size=2>Summary Delivery</font>
      	                	          <input type=radio name=analisabentuk value='exceptnorek'>
      	                	          <font face=Arial size=2>Exception Norek</font>
      	                	          <input type=radio name=analisabentuk value='exceptfile'>
      	                	          <font face=Arial size=2>Exception File</font>
      	                	         </td>
      	                	      </tr>
      	                      	      <tr>
      	                	 	 <td width=20% align=left valign=top>
				    	    <font style="font-size: 6;" color=white>SPINInfo </font>
      	                	 	 </td>
      	                	 	 <td width=80% align=left valign=top>
				    	    <font style="font-size: 6;" color=white>SPINInfo </font>
      	                	 	 </td>
      	                      	      </tr>
      	                	      <tr>
      	                	         <td width=20% align=left valign=top>
      	                	   	    <font face=Arial size=2>Billing Periode</font>
      	                	         </td>
      	                	         <td width=80%align=left valign=top>
      	                	   	    <select name=analisaperiodebln1>
HTML
		$varyear = substr($signintime,0,4);
		for($i=1;$i<=12;$i++)
		{
		   my $querytemp = "SELECT MONTHNAME('2000-$i-01')";
   		   my $sth = $db->prepare($querytemp);
		   $sth->execute();
		   my @rowtemp = $sth->fetchrow_array;
		   $sth->finish;
		   if (length($i) < 2)
		   {
		   	$varmonth = "0" . $i;
		   }
		   else
		   {
		   	$varmonth = $i;
		   }
		   if ($i == substr($signintime,5,2))
		   {
		   	print "<option value='$varmonth' selected>$rowtemp[0]</option>";
		   }
		   else
		   {
		   	print "<option value='$varmonth'>$rowtemp[0]</option>";
		   }
		}
print <<"HTML";
      	                	   	    </select>
      	                	   	    <select name=analisaperiodethn1>
HTML
		for($i=$varyear-5;$i<=$varyear;$i++)
		{
		   if ($i == $varyear)
		   {
		   	print "<option value='$i' selected>$i</option>";
		   }
		   else
		   {
		   	print "<option value='$i'>$i</option>";
		   }
		}
print <<"HTML";
      	                	   	    </select>
      	                	   	    <font face=Arial size=2>s/d</font>
      	                	   	    <select name=analisaperiodebln2 disabled>
HTML
		for($i=1;$i<=12;$i++)
		{
		   my $querytemp = "SELECT MONTHNAME('2000-$i-01')";
   		   my $sth = $db->prepare($querytemp);
		   $sth->execute();
		   my @rowtemp = $sth->fetchrow_array;
		   $sth->finish;
		   if (length($i) < 2)
		   {
		   	$varmonth = "0" . $i;
		   }
		   else
		   {
		   	$varmonth = $i;
		   }
		   if ($i == substr($signintime,5,2))
		   {
		   	print "<option value='$varmonth' selected>$rowtemp[0]</option>";
		   }
		   else
		   {
		   	print "<option value='$varmonth'>$rowtemp[0]</option>";
		   }
		}
print <<"HTML";
      	                	   	    </select>
      	                	   	    <select name=analisaperiodethn2 disabled>
HTML
		for($i=$varyear-5;$i<=$varyear;$i++)
		{
		   if ($i == $varyear)
		   {
		   	print "<option value='$i' selected>$i</option>";
		   }
		   else
		   {
		   	print "<option value='$i'>$i</option>";
		   }
		}
print <<"HTML";
      	                	   	    </select>
      	                	         </td>
      	                	      </tr>
      	                      	      <tr>
      	                	 	 <td width=20% align=left valign=top>
				    	    <font style="font-size: 6;" color=white>SPINInfo </font>
      	                	 	 </td>
      	                	 	 <td width=80% align=left valign=top>
				    	    <font style="font-size: 6;" color=white>SPINInfo </font>
      	                	 	 </td>
      	                      	      </tr>
      	                	      <tr>
      	                	         <td width=20% align=left valign=top>
      	                	   	    <font face=Arial size=2>Produk</font>
      	                	         </td>
      	                	         <td width=80%align=left valign=top>
      	                	   	    <select name=analisaproductid>
      	                	   	       <option value=''>-- Silahkan Pilih --</option>
HTML
            my $query = "SELECT *
	                       FROM TblProduct";
            my $sth = $db->prepare($query);
            $sth->execute();
            my @row;
            while ($row = $sth->fetchrow_arrayref)
            {
            	print "<option value='$row->[0]'>$row->[0] - $row->[1]</option>";
            }
            $sth->finish;
print <<"HTML";
      	                	   	    </select>
      	                	         </td>
      	                	      </tr>
      	                      	      <tr>
      	                	 	 <td width=20% align=left valign=top>
				    	    <font style="font-size: 6;" color=white>SPINInfo </font>
      	                	 	 </td>
      	                	 	 <td width=80% align=left valign=top>
				    	    <font style="font-size: 6;" color=white>SPINInfo </font>
      	                	 	 </td>
      	                      	      </tr>
      	                      	      <tr>
      	                	 	 <td width=20% align=left valign=top>
				    	    <font style="font-size: 6;" color=white>SPINInfo </font>
      	                	 	 </td>
      	                	 	 <td width=80% align=left valign=top>
				    	    <font style="font-size: 6;" color=white>SPINInfo </font>
      	                	 	 </td>
      	                      	      </tr>
      	                	      <tr>
      	                	         <td width=20% align=left valign=top>
      	                	   	    <font face=Arial size=2>Region</font>
      	                	         </td>
      	                	         <td width=80%align=left valign=top>
      	                	   	    <select name=analisaregionid>
      	                	   	       <option value='all'>-- All --</option>
HTML
            my $query = "SELECT *
	                       FROM TblRegion
	                       ORDER BY region_id";
            my $sth = $db->prepare($query);
            $sth->execute();
            my @row;
            while ($row = $sth->fetchrow_arrayref)
            {
            	print "<option value='$row->[0]'>$row->[0] - $row->[1]</option>";
            }
            $sth->finish;
print <<"HTML";
      	                	   	    </select>
      	                	         </td>
      	                	      </tr>
      	                      	      <tr>
      	                	 	 <td width=20% align=left valign=top>
				    	    <font style="font-size: 6;" color=white>SPINInfo </font>
      	                	 	 </td>
      	                	 	 <td width=80% align=left valign=top>
				    	    <font style="font-size: 6;" color=white>SPINInfo </font>
      	                	 	 </td>
      	                      	      </tr>
      	                	      <tr>
      	                	         <td width=20% align=left valign=top>
      	                	   	    <font face=Arial size=2>Group By</font>
      	                	         </td>
      	                	         <td width=80%align=left valign=top>
      	                	   	    <select name=analisagroupby>
      	                	   	       <option value='cust_vendor'>Vendor Cetak &nbsp &nbsp &nbsp</option>
      	                	   	       <option value='cust_courier'>Courier</option>
      	                	   	    </select>
      	                	   	    <input type=submit name=buttonsubmit value='Submit'>
      	                	         </td>
      	                	      </tr>
      	                      	      <tr>
      	                	 	 <td width=20% align=left valign=top>
				    	    <font style="font-size: 6;" color=white>SPINInfo </font>
      	                	 	 </td>
      	                	 	 <td width=80% align=left valign=top>
				    	    <font style="font-size: 6;" color=white>SPINInfo </font>
      	                	 	 </td>
      	                      	      </tr>
      	                      	      <tr>
      	                	 	 <td width=20% align=left valign=top>
				    	    <font style="font-size: 6;" color=white>SPINInfo </font>
      	                	 	 </td>
      	                	 	 <td width=80% align=left valign=top>
				    	    <font style="font-size: 6;" color=white>SPINInfo </font>
      	                	 	 </td>
      	                      	      </tr>
      	                	      <tr>
      	                	         <td width=20% align=left valign=top>
      	                	   	    <font face=Arial size=2>Sort (1st)</font>
      	                	         </td>
      	                	         <td width=80%align=left valign=top>
      	                	   	    <select name=sort1>
      	                	   	       <option value=''>Persentase</option>
      	                	   	       <option value=''>Nama Kurir</option>
      	                	   	       <option value='' selected>Region ID </option>
      	                	   	       <option value=''>Product ID</option>
      	                	   	    </select>
      	                	   	    <select name=ascdesc1>
      	                	   	       <option value=''>Ascending</option>
      	                	   	       <option value='DESC'>Descending</option>
      	                	   	    </select>
      	                	   	    <font face=Arial size=2><b>Not Active for Now</b></font>
      	                	         </td>
      	                	      </tr>
      	                	      <tr>
      	                	         <td width=20% align=left valign=top>
      	                	   	    <font face=Arial size=2>Sort (2nd)</font>
      	                	         </td>
      	                	         <td width=80%align=left valign=top>
      	                	   	    <select name=sort2>
      	                	   	       <option value=''>Persentase</option>
      	                	   	       <option value=''>Nama Kurir</option>
      	                	   	       <option value=''>Region ID </option>
      	                	   	       <option value=''>Product ID</option>
      	                	   	    </select>
      	                	   	    <select name=ascdesc2>
      	                	   	       <option value=''>Ascending</option>
      	                	   	       <option value='DESC'>Descending</option>
      	                	   	    </select>
      	                	   	    <font face=Arial size=2><b>Not Active for Now</b></font>
      	                	         </td>
      	                	      </tr>
      	                	   </table>
      	                	</td>
      	                      </tr>
                            </TABLE>
      		     	           <input type=hidden name=userid value=$userid>
          	     	         <input type=hidden name=userpwd value=$userpwd>
      		     	           <input type=hidden name=userprgcode value=$userprgcode>
          	     	         <input type=hidden name=thetimestamp value='$signintime'>
          	     	         <input type=hidden name=startfirst value='0'>
          	     	         <input type=hidden name=act value='report'>
          	     	         <input type=hidden name=prgsavereport value=''>
                  	      </form>
                      </TD>
                    </TR>
                    <TR>
                      <TD class=backW></TD>
                    </TR>
                  </TABLE>
                </TD>
              </TR>
              <TR>
                <TD height=15></TD>
              </TR>
              <TR>
                <TD class=borderB>
      		  <form name=secsystem method=post>
         	   <input type=hidden name=userhwid value='$userhwid'>
         	   <input type=hidden name=userid value='$userid'>
         	   <input type=hidden name=userpwd value='$userpwd'>
         	   <input type=hidden name=userprgcode value=''>
      		  </form>
                </TD>
              </TR>
              <TR>
                <TD height=15></TD>
              </TR>
            </TABLE>
          </TD>
        </TR>
      </TABLE>
     </div>
   </BODY>
</HTML>
HTML
$db->disconnect;
exit;
}

sub funcTableProfile
{
        my $status = shift;
        my $td1 = shift;
        my $td2 = shift;
        my $td3 = shift;
	my @datalines = split(/,/,$programprofile);
	my @datatemp = split(/,/,$userproduct);
	for ($ki=0;$ki<@datatemp;$ki++)
	{
	   my @data2temp = split(/:/,$datatemp[$ki]);
	   for ($kj=0;$kj<@datalines;$kj++)
	   {
	      if ($datalines[$kj] eq $data2temp[0])
	      {
		my $temphidden = lc(substr($data2temp[0],3)) . "id";
		my $tempid = lc(substr($data2temp[0],3)) . "_id";
		my $tempname = lc(substr($data2temp[0],3));
		$tempname =~ s/\b(\w)/\U$1/g;
		if ($status == 0)
		{
print <<"HTML";
      	                	      <tr>
      	                	         <td width=$td1% align=left valign=top>
      	                	   	    <font face=Arial size=2>$tempname</font>
      	                	         </td>
      	                	         <td width=$td2% align=left valign=top>
      	                	            <table width=100% cellpadding=0 cellspacing=0>
      	                	               <tr>
HTML
		}
		else
		{
			print "varstatus = '';\n";
			print "hitstatus = 0;\n";
		}
		my $urut = 0;
		for ($kk=1;$kk<@data2temp;$kk++)
		{
       		    my $querytemp = "SELECT *
	   		    FROM $data2temp[0]
	   		    WHERE $tempid='$data2temp[$kk]'";
       		    my $sth = $db->prepare($querytemp);
       		    $sth->execute();
       		    my @rowtemp = $sth->fetchrow_array;
       		    $sth->finish;
		    if ($status == 0)
		    {
		       $urut++;
		       if ($urut > 4)
		       {
			   $urut = 1;
			   print "</tr><tr>";
		       }
print <<"HTML";
      	                	                  <td width=$td3% align=left valign=top>
          	              	       	             <input type=checkbox name=$data2temp[0]$rowtemp[0] value='Y' checked><font face=Arial style="font-size: 11;">$rowtemp[1]</font>
      	                	                  </td>
HTML
		    }
		    else
		    {
print <<"HTML";
      	                	                  if (document.formsubmit.$data2temp[0]$rowtemp[0].checked)
      	                	                  {
      	                	                  	varstatus = varstatus + "$td2$tempid = '$rowtemp[0]' OR ";
      	                	                  	hitstatus = 1;
      	                	                  }
HTML
		    }
		}
		if ($status == 0)
		{
		   for ($kl=$urut;$kl<=4;$kl++)
		   {
print <<"HTML";
      	                	                  <td width=$td3% align=left valign=top>
          	              	       	             &nbsp
      	                	                  </td>
HTML
		   }
print <<"HTML";
      	                	               </tr>
      	                	            </table>
      	                	         </td>
      	                	      </tr>
HTML
		}
		else
		{
print <<"HTML";
			if (varstatus == 0)
			{
				alert("$tempname harus dipilih, minimal satu");
				return false;
			}
			else
			{
				document.formsubmit.$td1$temphidden.value = "AND (" + varstatus.substring(0,varstatus.length-3) + ")";
			}
HTML
		}
	      }
	   }
	}
    return $terbilang;
}

sub MSG
{
# Create the html page
print "Content-type: text/html\n\n";
print <<"HTML";

<HTML>
   <HEAD>
      <TITLE>$compname</TITLE>
   </HEAD>
   <BODY aLink=red link=#000080 vLink=#000080 bgcolor="#FFFFFF">
      <div align=center>
         <TABLE BORDER=0 CELLPADDING=0 CELLSPACING=0>        
      	    <tr>
               <TD WIDTH=100% VALIGN=TOP align=left>
                  <font size=5>Pesan Kesalahan</font>
                  <br><br>
    	 	  <font face=Arial size=3 color=red>$msg</font>
    	 	  <BR>
      	 	  <A HREF=/cgi-bin/snm/signin.cgi><font face=Arial size=2>Klik disini untuk LOGIN</font></A>
               </TD>
      	    </tr>
      	    </form>
      	 </table>
      </div>
   </BODY>
</HTML>
HTML
$sth->finish();
$db->disconnect;
exit;
}

sub GAGAL
{
# Create the html page
print "Content-type: text/html\n\n";
print <<"HTML";

<HTML>
   <HEAD>
      <TITLE>$compname</TITLE><LINK href="/snm/icons/style.html" rel=stylesheet type=text/css>
   </HEAD>
   <BODY aLink=$stylealink link=$stylelink vLink=$stylevlink bgcolor=$stylebodybgcol>
      <div align=center>
         <TABLE WIDTH="760" BORDER=0 CELLPADDING=0 CELLSPACING=0>        
      	    <tr>
               <TD WIDTH=240 VALIGN=TOP align=center>&nbsp
               </TD>
               <td width=10>&nbsp</td>
               <TD WIDTH=500 VALIGN=TOP align=left>
                  <H1><B>$programdesc</B></H1>
                  <BR><BR>
                  <font face=Arial size=2>
                     $msg.
          	     <BR><BR>
                     <A HREF="javascript:history.back();"><img src=/snm/icons/back.gif border=0 width=40 height=30></A>
                  </font>
               </TD>
      	    </tr>
      	 </table>
      </div>
   </BODY>
</HTML>
HTML
$db->disconnect;
exit;
}


sub funcEnc
{
  local $param1  = shift;
	$varenc = "";
	for ($zz=0;$zz<length($param1);$zz++)
	{
		$varonedigit = substr($param1,$zz,1);
		if ($varonedigit eq "R")
		{
		   $varord = 47;
		}
		else
		{
		   $varord = ord($varonedigit) + 10 ;
		}
  	$varenc .= chr($varord);
	}
	return $varenc;
}

sub funcDec
{
  local $param1  = shift;
	$varenc = "";
	for ($zz=0;$zz<length($param1);$zz++)
	{
		$varonedigit = substr($param1,$zz,1);
		if ($varonedigit eq "/")
		{
		   $varord = 82;
		}
		else
		{
		   $varord = ord($varonedigit) - 10 ;
		}
  	$varenc .= chr($varord);
	}
	return $varenc;
}
