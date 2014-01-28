console.log('\'Allo \'Allo!');

var container = document.querySelector('#container');
var msnry = new Masonry( container, {
    // options
    columnWidth: 200,
    itemSelector: '.item'
});
