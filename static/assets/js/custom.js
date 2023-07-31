$('.add-to-cart').click(function(e){
    e.preventDefault();

    var product_id = $(this).closest('.product_data').find('prod_id').val();
    var product_qty = $(this).closest('.product_data').find('prod_qty').val();
    var token = $('input[name="csrfmiddlewaretoken"]').val();
    $.ajax({
        method:'POST',
        url:'/add-to-cart',
        data:{product_id:product_id, product_qty:product_qty, csrfmiddlewaretoken:token},
        
        success:function(response){
            console.log(response);
            alertify.success('Item added to cart');
        }
    });
});