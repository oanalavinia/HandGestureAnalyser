//
// Working with files.
//
$(document).on('click', '#work_with_files', function() {
    $('#files_game').removeAttr('hidden');
});

$(document).on('click', '#go_back_file', function(evt) {
    $('#files_game').prop("hidden", !this.checked);
    $('#go_back_file').prop("hidden", !this.checked);
    $('#uploaded_file_content').prop("hidden", !this.checked);
    $('.output_canvas').removeClass('fix_canvas');
    $('.output_canvas').attr('width', '1080px');
    $('.output_canvas').attr('height', '650px');
});

// When a file is submitted upload it to the server.
$(document).on('click', '#submit_file', function(event) {
    event.preventDefault();
    var input = $('#input_file').get(0).files[0];
    var fd = new FormData();
    fd.append( 'file', input);
    fd.append('context', "PDFDocument");

    $.ajax({
      url: '/uploader',
      data: fd,
      processData: false,
      contentType: false,
      type: 'POST',
      success: function(data) {
        // Set-up the display. Fix the camera on top left.
        $('.output_canvas').addClass('fix_canvas');
        $('.output_canvas').attr('width', '500');
        $('.output_canvas').attr('height', '350');
        $('#uploaded_file_content').removeAttr('hidden');
        $('#go_back_file').removeAttr('hidden');

        // Add file info.
        var fileUrl ='/static/files/' + data.fileName;
        $('#uploaded_file_content').width(data.width);
        $('#uploaded_file_content').height(data.height);
        $('#uploaded_file_iframe').attr('src', fileUrl);
        $('#uploaded_file_iframe').attr('width', data.width);
        $('#uploaded_file_iframe').attr('height', parseInt(data.height) * parseInt(data.nr_pages));
        $('#uploaded_file_content').data('pageHeight', data.height);
      }
    });
})

var lastGestures = {};
var maybeChangePage = function(gesture) {
    if (lastGestures[gesture] == undefined) {
        lastGestures[gesture] = 1;
    } else {
        lastGestures[gesture]++;
    }
    if (gesture == 'five' && lastGestures[gesture] == 25) {
        lastGestures = {};
        if (Date.now() % 3) {
            nextPage();
            $.post({
                url: '/add_file_rule',
                data: {gesture: 'five'},
                success: function(data) {
                    console.log(data);
                }
            });
        }
    } else if (gesture == 'four' && lastGestures[gesture] == 25) {
        lastGestures = {};
        if (Date.now() % 3) {
            previousPage();
            $.post({
                url: '/add_file_rule',
                data: {gesture: 'four'},
                success: function(data) {
                    console.log(data);
                }
            });
        }
    }
};

var nextPage = function() {
    var pageHeight = parseInt($('#uploaded_file_content').data('pageHeight'));
    $("#uploaded_file_content").scrollTop($('#uploaded_file_content').scrollTop() + pageHeight);
};

var previousPage = function() {
    var pageHeight = parseInt($('#uploaded_file_content').data('pageHeight'));
    $("#uploaded_file_content").scrollTop($('#uploaded_file_content').scrollTop() - pageHeight);
};

$(document).on('click', '#next_page', function() {
    var pageHeight = parseInt($('#uploaded_file_content').data('pageHeight'));
    $("#uploaded_file_content").scrollTop($('#uploaded_file_content').scrollTop() + pageHeight);
});

$(document).on('click', '#previous_page', function() {
    var pageHeight = parseInt($('#uploaded_file_content').data('pageHeight'));
    $("#uploaded_file_content").scrollTop($('#uploaded_file_content').scrollTop() - pageHeight);
});