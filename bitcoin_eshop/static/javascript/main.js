$(document).ready(function() {
    // index.html
    $("form#choose-product p input[name=count]").addClass("span2");

    // order.html
    $("form#customer-data label").addClass("control-label");
    $("form#customer-data input").addClass("span2");
    $("form#customer-data div.form-actions button[name=cancel]").click(function(){
        window.location = "";
    });
});