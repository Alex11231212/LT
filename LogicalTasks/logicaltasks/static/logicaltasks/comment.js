$('#form-floating form').submit(function(e) {
    e.preventDefault();

    $.ajax({
        type: 'post',
        url: $(this).parent().attr('action'),
        data: $(this).parent().serialize(),
    }).done(function(data) {
        alert('The AJAX is done, and the server said ' + data);
    });
});