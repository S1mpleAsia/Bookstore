var element = document.getElementsByClassName('dropdown');
var submitBtn = document.getElementsByClassName('order-submit');
var provinceSelection = document.getElementById('province')
var citySelection = document.getElementById('city')

window.onload = function () {
    $.ajax({
        url: 'https://provinces.open-api.vn/api/?depth=2',
        type: 'GET',
        dataType: 'json',
        success: function (result) {
            result.sort(getSortOrder("name"));

            console.log(result)

            for (let i = 0; i < result.length; i++) {
                provinceSelection.options[provinceSelection.options.length] = new Option(result[i]["name"], result[i]["name"])
            }

            provinceSelection.onchange = (e) => {
                citySelection.length = 1;

                for (let i = 0; i < result.length; i++) {
                    if (provinceSelection.value === result[i]["name"]) {
                        result[i]["districts"].sort(getSortOrder("name"))
                        const district = result[i]["districts"];

                        for (let j = 0; j < district.length; j++) {
                            citySelection.options[citySelection.options.length] = new Option(district[j]["name"], district[j]["name"])
                        }
                        break;
                    }

                }
            };
        },
        error: function (error) {
            console.log(error);
        },

    });
}

submitBtn[0].addEventListener('click', warningBeforeDelete);

function warningBeforeDelete(e) {
    if (!$('#customer-details')[0].checkValidity()) $('#customer-details')[0].reportValidity()

    else {
        Swal.fire({
            title: 'Are you sure?',
            text: "You won't be able to revert this!",
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Confirm',
        }).then((result) => {
            if (result.isConfirmed) {
                Swal.fire(
                    'Deleted!',
                    'Your file has been deleted.',
                    'success',
                ).then(function (){
                    saveOrder();
                    location.reload();
                })
            }

        })
    }
}

function saveOrder(e) {
    var data = {};
    var formData = $('#customer-details').serializeArray();

    $.each(formData, function (index, value) {
        data["" + value.name + ""] = value.value;
    })


    $.ajax({
        url: '/save-order/',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(data),
        dataType: 'json',
        success: function (result) {
            console.log('Ok');
        },
        error: function (error) {
            console.log(error);
        },

    });
}

element[0].addEventListener('click', function () {
    element[0].classList.toggle('open');
});

function getSortOrder(prop) {
    return function (a, b) {
        if (a[prop] > b[prop]) {
            return 1;
        } else if (a[prop] < b[prop]) {
            return -1;
        }
        return 0;
    }
}

