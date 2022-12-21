var element = document.getElementsByClassName('dropdown');
console.log('OK');

element[0].addEventListener('click', function(){
    element[0].classList.toggle('open');
});