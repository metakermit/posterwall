// function main() {
//     var container = document.querySelector('#container');
//     var msnry = new Masonry( container, {
//         // options
//         columnWidth: 200,
//         itemSelector: '.item'
//     });
// }

// $(document).ready(main);

function main() {
    var $container = $('#container');
    // initialize
    $container.masonry({
        columnWidth: 200,
        itemSelector: '.item',
        gutter: Math.random()*10+20
    });

    var msnry = $container.data('masonry');
}

$(window).load(main);
