var element = document.getElementsByClassName('dropdown');
console.log('OK');

$(document).on("click", ".dropdown", function () {
    $('.dropdown').get(0).classList.toggle('open');
})

$(document).on("click", ".cart-update", function () {
    var id = this.dataset.id;
    var action = this.dataset.action;
    var user = this.dataset.user;

    console.log(id);
    console.log(action);

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
            'template': 'homepage',
        }),
        dataType: 'json',
        success: function (result) {
            $('#navbar').html(result);
        },
        error: function (error) {
            console.log('error');
            console.log(error);
        },

    });
}