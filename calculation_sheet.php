<?php
/**
 * Created by PhpStorm.
 * User: naikorasu
 * Date: 25/04/19
 * Time: 11.40
 */
?>

<?php
//1. LABA KOTOR MENURUT NASABAH
$sales_by_customer = 0;
$purchase_by_customer = 0;
$gross_profit = 0;

//2. LABA KOTOR MENURUT CALCULATION SHEET
$total_sell_price_trade = 0;
$total_sell_price_prods = 0;

$total_buys_price_trade = 0;
$total_buys_price_prods = 0;

$gross_profit_trade = 0;
$gross_profit_prods = 0;

$profit_margin_trade = 0;
$profit_margin_prods = 0;

$profit_margin_avg = ($profit_margin_trade + $profit_margin_prods) / 2;


//CROSS CHECK PENJUALAN
$sales_after_profit_margin = 0;
$percent_diff_by_customer_vs_sales_after_profit_margin = 0;
$sales_amount_recommend = 0;

?>
<style>
    td {
        padding: 5px;
        font-family: Helvetica, Arial;
        font-size: smaller;
    }
    input {
        width: 99%;
    }
</style>

<table width="100%" border="1" cellpadding="5" cellspacing="0" style="width:100%;margin-top:15px;">
    <tr>
        <td colspan="2">1. LABA KOTOR MENURUT NASABAH</td>
    </tr>
    <tr>
        <td width="50%">Penjualan menurut Nasabah (rata-rata sebulan)</td>
        <td width="50%" style="text-align: right">
           <input type="text" id="sales_by_customer" name="sales_by_customer" style="text-align: right" class="calc_sheet" currency value="<?=number_format($sales_by_customer);?>">
        </td>
    </tr>
    <tr>
        <td>Pembelian menurut Nasabah (rata-rata sebulan)</td>
        <td style="text-align: right">
            <input type="text" id="purchase_by_customer" name="purchase_by_customer" style="text-align: right" class="calc_sheet" currency value="<?=number_format($purchase_by_customer);?>">
        </td>
    </tr>
    <tr>
        <td>Laba Kotor (rata-rata sebulan)</td>
        <td style="text-align: right"><span id="gross_profit"><?=number_format($gross_profit);?></span></td>
    </tr>
</table>
<hr>

<table width="100%" border="1" cellpadding="5" cellspacing="0">
    <tr>
        <td colspan="3">2. LABA KOTOR MENURUT CALCULATION SHEET</td>
    </tr>
    <tr>
        <td width="30%"></td>
        <td width="35%">Dagang</td>
        <td width="35%">Produksi</td>
    </tr>
    <tr>
        <td>Jumlah Harga Jual</td>
        <td style="text-align: right"><input type="text" id="total_sell_price_trade" name="total_sell_price_trade" style="text-align: right" class="calc_sheet" currency value="<?=number_format($total_sell_price_trade);?>"></td>
        <td style="text-align: right"><input type="text" id="total_sell_price_prods" name="total_sell_price_prods" style="text-align: right" class="calc_sheet" currency value="<?=number_format($total_sell_price_prods);?>"></td>
    </tr>
    <tr>
        <td>Jumlah Harga Beli</td>
        <td style="text-align: right"><input type="text" id="total_buys_price_trade" name="total_buys_price_trade" style="text-align: right" class="calc_sheet" currency value="<?=number_format($total_buys_price_trade);?>"></td>
        <td style="text-align: right"><input type="text" id="total_buys_price_prods" name="total_buys_price_prods" style="text-align: right" class="calc_sheet" currency value="<?=number_format($total_buys_price_prods);?>"></td>
    </tr>
    <tr>
        <td><span style="font-weight: bold;">Laba Kotor</span></td>
        <td style="text-align: right"><span id="gross_profit_trade"><?=number_format($gross_profit_trade);?></span></td>
        <td style="text-align: right"><span id="gross_profit_prods"><?=number_format($gross_profit_prods);?></span></td>
    </tr>
    <tr>
        <td><span style="font-weight: bold;">PROFIT MARGIN</span></td>
        <td style="text-align: right"><span id="profit_margin_trade"><?=number_format($profit_margin_trade);?></span>&nbsp;%</td>
        <td style="text-align: right"><span id="profit_margin_prods"><?=number_format($profit_margin_prods);?></span>&nbsp;%</td>
    </tr>
    <tr>
        <td colspan="2"><span style="font-weight: bold;">PROFIT MARGIN RATA - RATA</span></td>
        <td style="text-align: right"><span id="profit_margin_avg"><?=number_format($profit_margin_avg);?></span>&nbsp;%</td>
    </tr>
</table>
<hr>

<table width="100%" border="1" cellpadding="5" cellspacing="0">
    <tr>
        <td colspan="2">CROSS CHECK PENJUALAN</td>
    </tr>
    <tr>
        <td width="60%">Pembelian Menurut Nasabah</td>
        <td width="40%" style="text-align: right"><span id="cross_check_purchase_by_customer"><?=number_format($purchase_by_customer);?></span></td>
    </tr>
    <tr>
        <td>Profit Margin menurut Calculation Sheet</td>
        <td style="text-align: right"><span id="cross_check_profit_margin_avg"><?=number_format($profit_margin_avg);?>&nbsp;%</span></td>
    </tr>
    <tr>
        <td><span style="font-weight: bold;">Penjualan setelah Profit Margin</span></td>
        <td style="text-align: right"><span id="sales_after_profit_margin"><?=number_format($sales_after_profit_margin);?></span></td>
    </tr>
    <tr>
        <td><span style="font-weight: bold;">% Perbedaan Penjualan menurut Nasabah Vs Penjualan setelah Profit Margin</span></td>
        <td style="text-align: right"><span id="percent_diff_by_customer_vs_sales_after_profit_margin"><?=number_format($percent_diff_by_customer_vs_sales_after_profit_margin);?></span>&nbsp;%</td>
    </tr>
</table>
<hr>

<table width="100%" border="1" cellpadding="5" cellspacing="0">
    <tr>
        <td align="center"><span id="process_calculation"> . . . </span></td>
    </tr>
</table>
<hr>

<table width="100%" border="1" cellpadding="5" cellspacing="0">
    <tr>
        <td width="300px">ANGKA PENJUALAN YANG HARUS DIPAKAI</td>
        <td width="200px" style="text-align: right"><span id="sales_amount_recommend"><?=number_format($sales_amount_recommend);?></span></td>
    </tr>
</table>
<hr>


<script type="application/javascript">
    $(document).ready(function () {


        $( ".calc_sheet" ).change(function() {
            var sales_by_cust = parseFloat($("#sales_by_customer").val().replace(/,/g, ''));
            var purchase_by_cust = parseFloat($("#purchase_by_customer").val().replace(/,/g, ''));
            var gross_profit = sales_by_cust - purchase_by_cust;

            //console.log("GROSS_PROFIT:" + gross_profit);
            $("#gross_profit").html(accounting.formatMoney(gross_profit, "", 0));

            var cross_check_purchase_by_customer =  purchase_by_cust;
            $("#cross_check_purchase_by_customer").html(accounting.formatMoney(cross_check_purchase_by_customer, "", 0));

            var total_sell_price_trade = parseFloat($("#total_sell_price_trade").val().replace(/,/g, ''));
            var total_buys_price_trade = parseFloat($("#total_buys_price_trade").val().replace(/,/g, ''));
            var gross_profit_trade = total_sell_price_trade - total_buys_price_trade;

            var total_sell_price_prods = parseFloat($("#total_sell_price_prods").val().replace(/,/g, ''));
            var total_buys_price_prods = parseFloat($("#total_buys_price_prods").val().replace(/,/g, ''));
            var gross_profit_prods = total_sell_price_prods - total_buys_price_prods;

            console.log("GROSS_PROFIT_TRADE:" + gross_profit_trade);
            console.log("GROSS_PROFIT_PRODS:" + gross_profit_prods);

            $("#gross_profit_trade").html(accounting.formatMoney(gross_profit_trade, "", 0));
            $("#gross_profit_prods").html(accounting.formatMoney(gross_profit_prods, "", 0));

            var profit_margin_trade = (gross_profit_trade / total_sell_price_trade) * 100;
            var profit_margin_prods = (gross_profit_prods / total_sell_price_prods) * 100;

            console.log("PROFIT_MARGIN_TRADE:" + profit_margin_trade);
            console.log("PROFIT_MARGIN_PRODS:" + profit_margin_prods);

            if(isFinite(profit_margin_trade) == false) {
                console.log("MARGIN_TRADE_INFINITY");
                profit_margin_trade = 0;
            }

            if(isFinite(profit_margin_prods) == false) {
                console.log("MARGIN_PRODS_INFINITY");
                profit_margin_prods = 0;
            }

            $("#profit_margin_trade").html(accounting.formatMoney(profit_margin_trade, "", 2));
            $("#profit_margin_prods").html(accounting.formatMoney(profit_margin_prods, "", 2));

            var profit_margin_avg = 0;

            if(isNaN(profit_margin_trade)) {
                console.log("MARGIN_TRADE_NAN");
                profit_margin_trade = 0;
            }

            if(isNaN(profit_margin_prods)) {
                console.log("MARGIN_PRODS_NAN");
                profit_margin_prods = 0;
            }

            if(profit_margin_prods == 0) {
                profit_margin_avg = profit_margin_trade;
            }
            else if(profit_margin_trade == 0) {
                profit_margin_avg = profit_margin_prods;
            }
            else if(profit_margin_trade != 0 && profit_margin_prods != 0) {
                console.log("BOTH");
                profit_margin_avg = (profit_margin_trade + profit_margin_prods) / 2
            }

            console.log("PROFIT_MARGIN_TRADE:" + profit_margin_trade);
            console.log("PROFIT_MARGIN_PRODS:" + profit_margin_prods);
            console.log("PROFIT_MARGIN_AVERAGE:" + profit_margin_avg);

            $("#profit_margin_avg").html(accounting.formatMoney(profit_margin_avg, "", 2));

            var cross_check_profit_margin_avg = profit_margin_avg;
            $("#cross_check_profit_margin_avg").html(accounting.formatMoney(cross_check_profit_margin_avg, "", 2));

            var magic_formula = (100 - profit_margin_avg) / 100;
            console.log("MAGIC FORMULA:" + magic_formula);

            var sales_after_profit_margin = purchase_by_cust / magic_formula;
            $("#sales_after_profit_margin").html(accounting.formatMoney(sales_after_profit_margin, "", 0));

            var percent_diff_by_customer_vs_sales_after_profit_margin = (sales_by_cust / (sales_after_profit_margin) - 1) * 100;
            $("#percent_diff_by_customer_vs_sales_after_profit_margin").html(accounting.formatMoney(percent_diff_by_customer_vs_sales_after_profit_margin, "", 2));

            //IF(OR(G82>10%;G82<−10%);"TIDAK OK - Perbedaan > 10% ";"OK - Proses dapat dilanjutkan")
            var process_message = ". . .";

            if(percent_diff_by_customer_vs_sales_after_profit_margin > 10 || percent_diff_by_customer_vs_sales_after_profit_margin < (-10)) {
                process_message = "Lakukan pengecekan ulang.";
            }
            else {
                process_message = "Proses dapat dilanjutkan.";
            }

            $("#process_calculation").html(process_message);

            //IF(OR(G82>10%;G82<−10%);G81;E61)

            var sales_amount_recommend = 0;

            if(percent_diff_by_customer_vs_sales_after_profit_margin > 10 || percent_diff_by_customer_vs_sales_after_profit_margin < (-10)) {
                sales_amount_recommend = sales_after_profit_margin ;
            }
            else {
                sales_amount_recommend = sales_by_cust;
            }

            $("#sales_amount_recommend").html(accounting.formatMoney(sales_amount_recommend, "", 0));

        });
    });
</script>
