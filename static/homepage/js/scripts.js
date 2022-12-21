var updateBtns = document.getElementsByClassName('cart-update');
var element = document.getElementsByClassName('dropdown');

for(let i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function() {
        var id = this.dataset.id;
        var action = this.dataset.action;
        var user = this.dataset.user;

        if (user === 'AnonymousUser') console.log('Please logged in')
        else {
            updateCart(id, action)
        }
    })
}

function updateCart(id, action) {
    $.ajax({
        url: '/update-cart/',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            'id': id,
            'action': action,
        }),
        dataType: 'json',
        success: function (result) {
            console.log('Success');
            // location.reload();
        },
        error: function (error) {
            console.log('error');
            console.log(error);
        },

    });
}

element[0].addEventListener('click', function(){
    element[0].classList.toggle('open');
});