$('#list').on('click', '.addtocart', function(){
    const id = $(this).data('id');
    $.ajax({
        url: `api/products/${id}/`,
        type: 'GET',
        datatype: 'json',
        success: function(p) {
              let html=` <p>${p.name} - ${p.price} x ${p.quantity}</p> `;
              $('#cart').append(html);
        },
        error: function(xhr, status, error) {
            console.error('Failed to fetch product:', error);}
    });
});