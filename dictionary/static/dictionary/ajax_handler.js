/**
 * Block variables
 */
let current_pos = 0;
let ajax_lock = false;
let call_lock = false;
let current_xhr;
let search_type = "st-staw";


/**
 * Handlers
 */
// Set focus to search field
$(document).ready(function () {
  $('#search').focus();
});

// Dropdown menu to choose search type
$('.search-type').each(function () {
    $(this).click(function () {
        search_type = $(this).attr('id');
        $('#dropdownSearchType').text($(this).text());
        search();
    })
});

// Load more entries when near the bottom of the page
$("#main").scroll(function() {
    let ele = $('#main');
    if ( !ajax_lock && !call_lock && ele.get(0).scrollHeight - ele.height() - 100 <= ele.scrollTop() ) {
        ajax_lock = true;
        toggle_loading();
        get_entries();
    }
});

// Search button action and prevent standard submit action
$(document).on('submit', '#search-form', function (e) {
    e.preventDefault();
    search();
});

// Adds instant searching to the search input field
$(document).on('input', '#search-form', function () {
    search();
});


/**
 * Search Submit using Ajax
 */
function search()
{
    let search = $('#search').val();
    ajax_lock = true;
    // Set the current search term in the search bar
    $('#search-term').text(search);

    // Clear old results
    $('#results').html('');
    $('#count').text('');
    call_lock = false;
    current_pos = 0;

    toggle_loading();
    get_entries()
}


function toggle_loading() {
    if (ajax_lock)
    {
        $('#results').append(LoadingRowTemplate);
    }
    else
    {
        $('#loading-row').remove();
    }

}

function get_entries()
{
    let search = $('#search').val();
    ajaxCall('/search', search , current_pos, function (json) {
        current_pos = json.pos;

        if (json.entries.length === 0)
        {
            $('#count').text(current_pos);
            call_lock = true;
            ajax_lock = false;
            toggle_loading();
        }
        else{
            let plus = '+';
            if (json.entries.length < json.limit)
                plus = '';

            $('#count').text(current_pos + plus);
            make_entries(json.entries);
        }
        toggle_loading()
    });
}


function make_entries(entries) {
    // Set a ajax click handler for each entry
    entries.forEach(element => {

        // Apply the template
        $('#results').append(EntryRowTemplate({keb: element.keb, entry_id: element.entry_id}));

        document.getElementById(element.entry_id).onclick = function () {
            $('#defModalKanji').html('')
            $('#defModalReading').html('')
            $('#defModalTranslation').html('');

            $('#kanjiCardLoading').show();
            $('#readingCardLoading').show();
            $('#transCardLoading').show();

            let search = $('#search').val();
            let regex = new RegExp(search, 'ig');

            ajaxCall('/definition', element.entry_id, 0, function (json) {
                if (json.keb.length > 0) {
                    $('#kanjiCard').show();
                    json.keb.forEach(function (element, i)
                    {
                        text = element.replace(regex, Highlighter);
                        $('#defModalKanji').append(KanjiRowTemplate({ kanji: text, id: i+1}))
                    });
                }else{
                    $('#kanjiCard').hide();
                }
                json.reb.forEach(function (element, i)
                {
                    text = element.replace(regex, Highlighter);
                    $('#defModalReading').append(ReadingRowTemplate({ reading: text, id: i+1}))
                });
                json.trans.forEach(function (element, i)
                {
                    text = element.replace(regex, Highlighter);
                    $('#defModalTranslation').append(TranslationRowTemplate({ trans: text, id: i+1}))
                });

                $('#kanjiCardLoading').hide();
                $('#readingCardLoading').hide();
                $('#transCardLoading').hide();
            })
        };

    });

    ajax_lock = false;
}


/**
 * Ajax call template for Django
 */
const ajaxCall = function(url, query, pos, successCallback) {
    if (current_xhr)
        current_xhr.abort();

    current_xhr = $.ajax({
        url: url,
        type: 'POST',
        dataType: 'json',
        data: {
            query: query,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            pos: pos,
            action: 'post',
            type: search_type
        },
        success: [ successCallback ]
    })
};
