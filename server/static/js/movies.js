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
var askAndGiveRec = function(movies, movie_ids) {
    var ol = $('#random_movies_container');
    $('#random_movies_container').empty();
    $.each(movies, function(movie) {
        ol.append($('<li></li>').text(this));
    });
    $('#given_movies').data('startMovie', Date.now());

    // Get result.
    timeoutFunction = setTimeout(function() {
        if ($('#given_movies').data('startMovie')) {
            $('#given_movies').prop("hidden", true);
            $.post({
                url:'/rec_movies',
                data: {
                    'startTime': $('#given_movies').data('startMovie'),
                    'endTime': Date.now(),
                    'movie_ids': movie_ids
                }
            }).done(function(data) {
                var selected_movie = JSON.parse(data).selected_movie;
                var rec_movies = JSON.parse(data).movies;
                console.log(rec_movies);
                changeCameraToDefault();
                // Append the resulted recommendation.
                container = $('#result_movies_container');
                container.empty();

                if (rec_movies.length > 0) {
                    $('#try_again').prop("hidden", true);
                    $('#selected_movie').html(selected_movie);
                    $.each(rec_movies, function(idx) {
                        var el = $('<li></li>').text(this).addClass('list-group-item');

                        container.append(el);
                    });
                } else {
                    $('#try_again').prop("hidden", false);
                    $('#selected_movie').html('');

                    var el = $('<li></li>')
                        .text("You didn't selected any movie. Do you want to try again?")
                        .addClass('list-group-item');
                    container.append(el);
                }
                // Display modal.
                var myModal = new bootstrap.Modal(document.getElementById('result_movies'));
                myModal.show();
            });
        }
    // TODO: move it to 10000.
    }, 10000);
};

var getMovies = function() {
    $.get('/random_movies', function(data) {
        var data = JSON.parse(data)
        var movies = data.movies;
        var movie_ids = data.movie_ids;
        $('#try_again').data('movies', data.movies);
        $('#try_again').data('movie_ids', data.movie_ids);

        askAndGiveRec(movies, movie_ids);
    });
};

$(document).on('click', '#work_with_movies', function() {
    var myModal = new bootstrap.Modal(document.getElementById('info_movies'));
    myModal.show();
});

$(document).on('click', '#try_again', function() {
    $('#random_movies_container').empty();
    $('#given_movies').removeData();
    $('#given_movies').removeAttr('hidden');
    var movies = $('#try_again').data('movies');
    var movie_ids = $('#try_again').data('movie_ids');

    askAndGiveRec(movies, movie_ids);
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