$(document).ready(function()
{
    function updatePrice()
    {
        var price = parseInt(document.getElementById("jumlahMeja").value);
        var total = (price) * 10000;
        var total = total;
        $("#hargaMeja").val("Rp "+total);
    }
    $(document).on("change, keyup input", "#jumlahMeja", updatePrice);
});

$(document).ready(function()
{
    function updatePrice()
    {
        var price = parseInt(document.getElementById("jumlahNet").value);
        var total = (price) * 5000;
        var total = total;
        $("#hargaNet").val("Rp "+total);
    }
    $(document).on("change, keyup input", "#jumlahNet", updatePrice);
});

$(document).ready(function()
{
    function updatePrice()
    {
        var price = parseInt(document.getElementById("jumlahBet").value);
        var total = (price) * 3000;
        var total = total;
        $("#hargaBet").val("Rp "+total);
    }
    $(document).on("change, keyup input", "#jumlahBet", updatePrice);
});

$(document).ready(function()
{
    function updatePrice()
    {
        var price = parseInt(document.getElementById("jumlahBola1").value);
        var total = (price) * 1000;
        var total = total;
        $("#hargaBola1").val("Rp "+total);
    }
    $(document).on("change, keyup input", "#jumlahBola1", updatePrice);
});

$(document).ready(function()
{
    function updatePrice()
    {
        var price = parseInt(document.getElementById("jumlahBola3").value);
        var total = (price) * 3000;
        var total = total;
        $("#hargaBola3").val("Rp "+total);
    }
    $(document).on("change, keyup input", "#jumlahBola3", updatePrice);
});

$(document).ready(function()
{
    function updatePrice()
    {
        var price = parseInt(document.getElementById("hargaMeja").value.slice(3)) + 
        parseInt(document.getElementById("hargaNet").value.slice(3)) + 
        parseInt(document.getElementById("hargaBet").value.slice(3)) +
        parseInt(document.getElementById("hargaBola1").value.slice(3)) +
        parseInt(document.getElementById("hargaBola3").value.slice(3));
        var total = price * parseInt(document.getElementById("lama").value);
        var total = total;
        $("#hargaTotal").val("Rp "+total);
    }
    $(document).on("change, keyup input", "#jumlahNet", updatePrice);
    $(document).on("change, keyup input", "#jumlahMeja", updatePrice);
    $(document).on("change, keyup input", "#jumlahBet", updatePrice);
    $(document).on("change, keyup input", "#jumlahBola1", updatePrice);
    $(document).on("change, keyup input", "#jumlahBola3", updatePrice);
    $(document).on("change, keyup input", "#lama", updatePrice);
});