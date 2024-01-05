
  $(document).ready(function () {
    // Function to update prices and offer percent for a specific card
    function updatePricesAndOffer(card) {
      var selectedRadio = card.find('input[name="product_size"]:checked');
      if (selectedRadio.length > 0) {
        var salePrice = selectedRadio.data('sale_price');
        var originalPrice = selectedRadio.data('original_price');
        var offerPercent = parseFloat(selectedRadio.data('offer_percent')).toFixed(2); 
        
        card.find('.sale_price').text('₹' + salePrice);
        card.find('.original_price').text('₹' + originalPrice);
        card.find('.offer_percent').text(offerPercent + '% OFF');

      }
    }

    // Event listener for radio button click within each card
    $('input[name="product_size"]').off('click').on('click', function () {
      var card = $(this).closest('.cart-div');
      updatePricesAndOffer(card);
    });
    // Event listener for add cart button click
    $("#cart-add-btn").click(function () {
        var product_Id = $('input[name="product_size"]:checked').val();
        var quantity = $("input[name='quantity']").val()
        var url = "/shop/cart/add/?product_id="+product_Id+"&quantity="+quantity; 
        $.ajax({
            type: "GET",
            url: url,
            
            success: function (data) {
              window.location.href = "/shop/cart/";
              showAlert(data.message, "alert-success");
                
            },
            error: function (data) {
              if (data.status == '401') {window.location.href = '/accounts/login/';
              }else{showAlert(data.responseJSON.message, "alert-danger");}
          }
        });
    });
    // wishlist add
$(".add-wishlist-btn").click(function () {
  var product = $('input[name="product_size"]:checked').val();
    var url = "/shop/wishlist/add/?product_id="+product;
    $.ajax({
    type: "GET",
    url: url,
    success: function (data) {
        // Display success message
        $('#header_wishlist_count').html(data.wishlist_count)
        // Redirect to the wishlist page
        window.location.href = "/shop/wishlist/";
    },
    error: function (data) {
      if (data.status == '401') {window.location.href = '/accounts/login/';
      }else{showAlert(data.responseJSON.message, "alert-danger");}
  }
    })
})
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
  