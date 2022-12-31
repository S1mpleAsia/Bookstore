var updateBtns = document.getElementsByClassName('cart-update');
var element = document.getElementsByClassName('dropdown');
var checkoutBtn = document.getElementsByClassName('btn-checkout');

$(document).on("click", ".cart-update", function () {
    var id = this.dataset.id;
    var action = this.dataset.action;
    var user = this.dataset.user;

    if (user === 'AnonymousUser') console.log('Please logged in')
    else {
        updateCart(id, action)
    }
})

function updateCart(id, action) {
    $.ajax({
        url: '/update-cart/',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            'id': id,
            'action': action,
            'template': 'cart',
        }),
        dataType: 'json',
        success: function (result) {
            $('#cart-content').html(result);
        },
        error: function (error) {
            console.log(error);
        },

    });
}

$(document).on("click", ".btn-checkout", function () {
    location.href = '/checkout/';
})

$(document).on("click", ".dropdown", function () {
    $('.dropdown').get(0).classList.toggle('open');
})