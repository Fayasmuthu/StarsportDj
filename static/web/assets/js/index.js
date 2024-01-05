
$(document).ready(function () {
// Function to update prices  for a specific card
function updatePricesAndOffer(card) {
    var selected = card.find('select[name="product_size"] option:selected');
    if (selected.length > 0) {
        var salePrice = selected.data('sale_price');
        var originalPrice = selected.data('original_price');
        card.find('.sale_price').text('₹' + salePrice);
        card.find('.original_price').text('₹' + originalPrice);
    }
}
// Event listener for select button click within each card
$('select[name="product_size"]').change(function () {
    var card = $(this).closest('.card-product');
    updatePricesAndOffer(card);
});

// add cart ajax
$(".cart-add-btn").click(function () {
    var card = $(this).closest('.card-product');
    var selected = card.find('select[name="product_size"] option:selected');
    var product= selected.val();
    var url = "/shop/cart/add/?product_id="+product; 
    $.ajax({
        type: "GET",
        url: url,
        success: function (data) {
            
            // Display success message
            $('#header_cart_count').html(data.cart_count)
            
            showAlert(data.message, "alert-success");
        },
        error: function (data) {
            
            if (data.status == '401') {window.location.href = '/accounts/login/';
            }else{showAlert(data.responseJSON.message, "alert-danger");}
        }
    });
});

// add wishlist ajax
$(".btn-action-wishlist").click(function () {
    var card = $(this).closest('.card-product');
    var selected = card.find('select[name="product_size"] option:selected');
    var product= selected.val();
    var url = "/shop/wishlist/add/?product_id="+product; 
    $.ajax({
    type: "GET",
    url: url,
    success: function (data) {
        // Display success message
        $('#header_wishlist_count').html(data.wishlist_count)
        
        showAlert(data.message, "alert-success");
    },
    error: function (data) {
        if (data.status == '401') {window.location.href = '/accounts/login/';
        }else{showAlert(data.responseJSON.message, "alert-danger");}
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
