$('#list').on('click', '.addtocart', function(){
    const id = $(this).data('id');
    $.ajax({
        url: `api/cart/add/${id}/`,
        type: 'POST',
        headers: {'X-CSRFToken': $('meta[name="csrf-token"]').attr('content')},
        success: function(p) {
            $('#cart').show();
            $(`#cart-item-${p.id}`).remove();
            let html=` <div class="description" id="cart-item-${p.id}">
                <p>Name: ${p.name}</p><p>Price: ${p.price}</p><p>Qty: ${p.cart_quantity}</p>
                <button class="removefromcart" data-id = "${p.id}">Remove</button>
                </div>`;
            $('#cart-items').append(html);
            $('#cart-total').text(`Total: $ ${p.total}`);
        },
        error: function (xhr) {
            console.error(xhr.responseText);}
    });
});

$('#cart').on('click', '.removefromcart', function(){
    const id = $(this).data('id');
    $.ajax({
        url: `api/cart/delete/${id}/`,
        type: 'POST',
        headers: {'X-CSRFToken': $('meta[name="csrf-token"]').attr('content')},
        success: function(p){
            $(`#cart-item-${p.removed_id}`).remove();
            $('#cart-total').text(`Total: $ ${p.total}`);
            if ($('#cart-items').children().length === 0){
                $('#cart').hide();
            }
        },
        error: function(xhr){
            console.error(xhr.responseText);
        }
    });
});