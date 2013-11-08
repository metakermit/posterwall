$( document ).ready(function() {
    var container = document.querySelector('#container');
    var msnry = new Masonry( container, {
      // options
      //columnWidth: 200,
      "gutter": 20,
      itemSelector: '.item'
    });
});
