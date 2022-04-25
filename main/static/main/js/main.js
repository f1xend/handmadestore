$('.minus-btn').on('click', function(e) {
    e.preventDefault();
    var $this = $(this);
    var $input = $this.closest('div').find('input');
    var value = parseInt($input.val());

    if (value > 1) {
        value = value - 1;
    } else {
        value = 1;
    }

  $input.val(value);

});

$('.plus-btn').on('click', function(e) {
    e.preventDefault();
    var $this = $(this);
    var $input = $this.closest('div').find('input');
    var value = parseInt($input.val());

    if (value < 20) {
        value = value + 1;
    } else {
        value = 20;
    }

    $input.val(value);
});




function del(par){
    cls = '.some_class' + par
    $(document).on('click', cls, function(){
        $('#deleteModal').modal('show');
        url = $(cls).data('urlAddr');
        $(document).on('click', '.del-class', function(){
            location.replace(url);
          })
      })
}



function redirect(url){
    location.replace(url);
}
