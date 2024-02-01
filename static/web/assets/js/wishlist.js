$(document).ready(function () {
   
    $(".add-to-cart-btn").click(function () {
        var product_Id = $(this).data("product_id");
        var Id = $(this).data("id");
        var url = "/shop/cart/add/?product_id="+product_Id;
        var remove_url= '/shop/wishlist/remove/'+Id+'/';
        $.ajax({
            type: "GET",
            url: url,
            success: function (data) {
                $('#header_wishlist_count').html(data.wishlist_count)
                $('#header_cart_count').html(data.cart_count)
                showAlert(data.message, "alert-success");
                
            },
            error: function (data) {
                // Display error message
                showAlert(data.responseJSON.message, "alert-danger");
            }
        });
        // Send AJAX request to remove from wishlist
        $.ajax({
            url: remove_url,  // Replace with the actual URL for removing from wishlist
            success: function (data) {
                window.location.reload();
            },
            error: function (error) {
                showAlert(data.responseJSON.message, "alert-danger");
            }
        });
    });
    $(".remove-btn").click(function () {
        var product_Id = $(this).data("product_id");
        var remove_url= '/shop/wishlist/remove/'+product_Id+'/';
        $.ajax({
            type: "GET",
            url: remove_url,
            
            success: function (data) {
                showAlert(data.message, "alert-success");
                window.location.reload();
                
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