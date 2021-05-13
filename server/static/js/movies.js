var fixCamera = function() {
    $('.output_canvas').addClass('fix_canvas_movies');
    $('.output_canvas').attr('width', '780px');
    $('.output_canvas').attr('height', '450px');
};

var changeCameraToDefault = function() {
    $('.output_canvas').removeClass('fix_canvas_movies');
    $('.output_canvas').attr('width', '1080px');
    $('.output_canvas').attr('height', '650px');
}

var timeoutFunction;
var getMovies = function() {
    $.get('/random_movies', function(data) {
        response = JSON.parse(data);
        var ol = $('#random_movies_container');
        $('#random_movies_container').empty();
        $.each(response.movies, function(movie) {
            ol.append($('<li></li>').text(this));
        });
        $('#given_movies').data('startMovie', Date.now());

        // Get result.
        timeoutFunction = setTimeout(function() {
            if ($('#given_movies').data('startMovie')) {
                $('#given_movies').prop("hidden", true);
                $.get('/rec_movies', {
                    'startMovie': $('#given_movies').data('startMovie'),
                    'endMovie': Date.now()
                }).done(function(data) {
                    var rec_movies = JSON.parse(data).movies;
                    console.log(rec_movies);
                    changeCameraToDefault();
                    // Append the resulted recommendation.
                    container = $('#result_movies_container');
                    $.each(rec_movies, function(idx) {
                        var el = $('<li></li>').text(this);
//                        if (idx == 0) {
//                            el = $('<li></li>').text(this).addClass('badge').addClass('badge-secondary');
//                        }

                        container.append(el);
                        // TODO: remove after server side is fixed.
                        if (idx == 2) { return false; }
                    });
                    // Display modal.
                    var myModal = new bootstrap.Modal(document.getElementById('result_movies'));
                    myModal.show();
                });
            }
        // TODO: move it to 10000.
        }, 3000);
    });
};

$(document).on('click', '#work_with_movies', function() {
    var myModal = new bootstrap.Modal(document.getElementById('info_movies'));
    myModal.show();
});

$(document).on('click', '#get_movies', function() {
    $('#random_movies_container').empty();
    $('#given_movies').removeData();
    $('#given_movies').removeAttr('hidden');
    fixCamera();

    getMovies();
});

$(document).on('click', '#other_movies', function() {
    $('#given_movies').removeData();
    clearTimeout(timeoutFunction);

    getMovies();
});

$(document).on('click', '#get_rec', function() {
    $.get('/rec_movies', {
        'startMovie': $('#movies_modal').data('startMovie'),
        'endMovie': Date.now()
    }).done(function(data) {
        var rec_movies = JSON.parse(data).movies;
        console.log(rec_movies);
    });
});