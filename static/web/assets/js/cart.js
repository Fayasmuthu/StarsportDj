
$(document).ready(function () {
    var cart_total = $("#cart_total").text();
    var cart_total = cart_total.replace('₹', '');
    var service_fee = $("#service_fee").text();
    var service_fee = service_fee.replace('₹', '');
    var sub_total = parseFloat(cart_total) + parseFloat(service_fee);
    $("#sub_total").text("₹"+sub_total.toFixed(2));
    // minus to cart`
    $(".cart-minus-btn").click(function () {
        var product_Id = $(this).data("product_id");
        var url = "/shop/cart-minus/?item_id=" + product_Id;
        var qty_value = $("#quantity-" + product_Id);
        var total_amt = $("#total-" + product_Id);
        $.ajax({
            type: "GET",
            url: url,
            success: function (data) {
              if (data.quantity == '1') {window.location.reload()}
              qty_value.val(data.quantity);
              total_amt.text("₹"+data.total_price);
              $('#cart_total').html("₹"+data.cart_total);
              sub_total = parseFloat(data.cart_total) + parseFloat(service_fee);
              $("#sub_total").text("₹"+sub_total.toFixed(2));
              
                
            },
            error: function (data) {
                // Display error message
                showAlert(data.responseJSON.message, "alert-danger");
            }
        });
    });
    // Add to cart
    $(".cart-add-btn").click(function () {
        var product_Id = $(this).data("product_id");
        var url = "/shop/cart/add/?product_id="+product_Id; 
        var qty_value = $("#quantity-" + product_Id);
        var total_amt = $("#total-" + product_Id);
        $.ajax({
            type: "GET",
            url: url,
            
            success: function (data) {
              qty_value.val(data.quantity);
              total_amt.text("₹"+data.total_price);
              $('#cart_total').html("₹"+data.cart_total);
              sub_total = parseFloat(data.cart_total) + parseFloat(service_fee);
              $("#sub_total").text("₹"+sub_total.toFixed(2));
              
                
            },
            error: function (data) {
                // Display error message
                showAlert(data.responseJSON.message, "alert-danger");
            }
        });
    });
    function showAlert(message, alertClass) {
          var alertContainer = $("#alert-container");
          var alertDiv = $("<div>").addClass("alert " + alertClass).text(message);
          alertContainer.append(alertDiv);
  
          // Automatically hide the alert after 5 seconds
          setTimeout(function () {
              alertDiv.remove();
          }, 800);
      }
    
  });