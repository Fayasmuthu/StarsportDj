
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
// Initial update on page load for all cards
$('.cart-div').each(function () {
    updatePricesAndOffer($(this));
});
// Event listener for radio button click within each card
$('input[name="product_size"]').on('click', function () {
    var card = $(this).closest('.cart-div');
    updatePricesAndOffer(card);
});
// Event listener for thumbnail click
$('.thumbnails-img').click(function () {
    var imageUrl = $(this).data('image-url');
    $('.zoom').css('background-image', 'url(' + imageUrl + ')');
    $('.change-img').attr('src', imageUrl);
});
$(".input-group").on("click", ".button-plus", function (event) {
    event.preventDefault();
    handleQuantityChange(1);
});

$(".input-group").on("click", ".button-minus", function (event) {
    event.preventDefault();
    handleQuantityChange(-1);
});

function handleQuantityChange(change) {
    var inputField = $(".input-group .quantity-field");
    var currentQuantity = parseInt(inputField.val(), 10);
    
    // Increment or decrement the quantity
    var newQuantity = currentQuantity + change;

    // Ensure the new quantity is positive
    newQuantity = Math.max(0, newQuantity);

    // Update the input field with the new quantity
    inputField.val(newQuantity);

    // Enable or disable the "Add to Cart" button based on the new quantity
    var addToCartButton = $(".cart-add-btn_quickview");
    addToCartButton.prop("disabled", newQuantity === 0);
}

// cart add 
$(".cart-add-btn_quickview").click(function () {
    var card = $(this).closest('.cart-div');
    default_product_id = $(this).data('default-size');
    var product = card.find('input[name="product_size"]:checked').val();
    if (!product) {
    product = default_product_id;  //  'default_product_id' with your actual default value
    }
    var qty = card.find('input[name="quantity"]').val();
    var url = "/shop/cart/add/?product_id="+product+"&quantity="+qty; 
    $.ajax({
    type: "GET",
    url: url,
    success: function (data) {
        // Display success message
        $('#header_cart_count').html(data.cart_count)
        // Redirect to the cart page
        window.location.href = "/shop/cart/";
    },
    error: function (data) {
        if (data.status == '401') {window.location.href = '/accounts/login/';
        }else{showAlert(data.responseJSON.message, "alert-danger");}
    }
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
$(".cart-add-btn-combo").click(function () {
    var product_Id = $(this).data("product-id");
    var quantity = $("input[name='quantity']").val()
    var url = "/shop/cart/add/?product_id="+product_Id+"&quantity="+quantity; 
    $.ajax({
        type: "GET",
        url: url,
        
        success: function (data) {
          $('.header_cart_count').html(data.cart_count)
      Swal.fire({
        title: "<strong>Item Added to Cart</strong>",
        icon: "success",
        html: `
            <p>Your item has been added to the cart successfully!</p>
            <p>What would you like to do next?</p>
        `,
        showCloseButton: true,
        showCancelButton: true,
        focusConfirm: false,
        confirmButtonText: `
            View Cart
            <i class="fa fa-shopping-cart"></i>
        `,
        confirmButtonAriaLabel: "View Cart",
        cancelButtonText: `
            Checkout
            <i class="fa fa-credit-card"></i>
        `,
        cancelButtonAriaLabel: "Checkout",
        timer: 5000, 
        timerProgressBar: true
      }).then((result) => {
          if (result.isConfirmed) {
              // Redirect to the view cart page
              window.location.href = '/shop/cart/';
          } else if (result.dismiss === Swal.DismissReason.cancel) {
              // Redirect to the checkout page
              window.location.href = '/checkout/';
          }
      });
      
        
    },
    error: function (data) {
      if (data.status == '401') {
        window.location.href = '/accounts/login/';
    } else {
        // Display error message with SweetAlert
        Swal.fire({
            title: "Error",
            icon: "error",
            text: data.responseJSON.message || "An error occurred while adding the item to the cart."
        });
    }
  }
    });
});
});