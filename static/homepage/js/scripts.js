// var updateBtns = document.getElementsByClassName('cart-update');
// var element = document.getElementsByClassName('dropdown');
console.log($('#startPage').val());
var query = $('#query').val()

$(document).on("click", ".dropdown", function () {
    $('.dropdown').get(0).classList.toggle('open');
})

$(document).on("click", ".cart-update", function () {
    var id = this.dataset.id;
    var action = this.dataset.action;
    var user = this.dataset.user;

    if (user === 'AnonymousUser') console.log('Please logged in')
    else {
        updateCart(id, action)
    }
})

// for (let i = 0; i < updateBtns.length; i++) {
//     updateBtns[i].addEventListener('click', function () {
//         var id = this.dataset.id;
//         var action = this.dataset.action;
//         var user = this.dataset.user;
//
//         if (user === 'AnonymousUser') console.log('Please logged in')
//         else {
//             updateCart(id, action)
//         }
//     })
// }

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

$(function () {
    window.pagObj = $('#pagination').twbsPagination({
        totalPages: $('#startPage').val(),
        visiblePages: 3,
        onPageClick: function (event, page) {
            $.ajax({
                url: "/get/pagination",
                data: {
                    "page": page,
                    "q": query,
                },
                contentType: 'application/json',
                dataType: 'json',
                success: function (result) {
                    $('#content').html(result);
                },
                error: function (error) {
                    console.log('error');
                    console.log(error);
                },
            });
        }
    });
});
