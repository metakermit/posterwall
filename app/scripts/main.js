console.log('\'Allo \'Allo!');

function main() {
    var container = document.querySelector('#container');
    var msnry = new Masonry( container, {
        // options
        columnWidth: 200,
        itemSelector: '.item'
    });
}

$(main);

