$(document).on('click', '#rec_movies', function() {
    var myModal = new bootstrap.Modal(document.getElementById('start_movies_modal'));
    myModal.show();
});

$(document).on('click', '#start_movies_game', function() {
    $.get('/movies', function(data) {
        response = JSON.parse(data);
        var div = $('#movies_body');
        $.each(response.movies, function(movie) {
            div.append($('<div></div>').text(this));
        });
    });
});