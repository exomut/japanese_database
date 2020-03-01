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
    if(!get_cookie('welcomed')) {
        $('#welcome').modal('show');
		make_cookie('welcomed', 'true', 180);
    }
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
//$(document).on('input', '#search-form', function () {
//    search();
//});


/**
 * Search Submit using Ajax
 */
function search()
{
    let search = $('#search').val();

    if (current_xhr) current_xhr.abort();

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
    if (ajax_lock) {
        $('#results').append(LoadingRowTemplate);
    }
    else {
        $('#loading-row').remove();
    }
}

function get_entries()
{
    let search = $('#search').val();
    ajaxCall('/search', search , current_pos, function (json) {
        current_pos = json.pos;

        if (json.entries.length === 0) {
            $('#count').text(current_pos);
            call_lock = true;
            ajax_lock = false;
        }
        else{
            let plus = '+';
            if (json.entries.length < json.limit) {
                plus = '';
                call_lock = true;
            }

            $('#count').text(current_pos + plus);
            make_entries(json.entries);
        }
        toggle_loading()
    });
}


function make_entries(entries) {
    // Set a ajax click handler for each entry
    entries.forEach(element => {

        if (element.keb == ''){
            // Apply the template
            $('#results').append(EntryRowTemplateNoKanji({reb: element.reb, reb_count: element.reb_count,
                trans: element.trans, trans_count: element.trans_count, entry_id: element.entry_id}));
        }else{
            // Apply the template
            $('#results').append(EntryRowTemplate({keb: element.keb, keb_count: element.keb_count,
                reb: element.reb, reb_count: element.reb_count,
                trans: element.trans, trans_count: element.trans_count, entry_id: element.entry_id}));
        }

        document.getElementById(element.entry_id).onclick = function () {
            $('#defModalKanji').html('')
            $('#defModalReading').html('')
            $('#defModalTranslation').html('');
            $('#defModalExamples').html('');

            $('#kanjiCardLoading').show();
            $('#readingCardLoading').show();
            $('#transCardLoading').show();
            $('#examCardLoading').show();

            let search = $('#search').val();
            let regex = new RegExp(search, 'ig');

            ajaxCall('/definition', element.entry_id, 0, function (json) {
                let search_term = '';
                if (json.keb.length > 0) {
                    search_term = json.keb[0];
                    $('#kanjiCard').show();
                    json.keb.forEach(function (element, i)
                    {
                        text = element.replace(regex, Highlighter);
                        $('#defModalKanji').append(KanjiRowTemplate({ kanji: text, id: i+1}))
                    });
                }else{
                    search_term = json.reb[0];
                    $('#kanjiCard').hide();
                }
                json.reb.forEach(function (element, i)
                {
                    text = element.replace(regex, Highlighter);
                    $('#defModalReading').append(ReadingRowTemplate({ reading: text, id: i+1}))
                });
                json.trans.forEach(function (element, i)
                {
                	let modal_trans = $('#defModalTranslation')
                    if (json.pos[i]) {
                    	info = json.pos[i].replace(/\|/g, "<br />");
                        modal_trans.append(TranslationRowInformation({info: info}));
                    }

                    text = element.replace(regex, Highlighter);
                    modal_trans.append(TranslationRowTemplate({ trans: text, id: i+1}))
                });

                $('#kanjiCardLoading').hide();
                $('#readingCardLoading').hide();
                $('#transCardLoading').hide();


                $('#examplesCard').show();
                ajaxCall('/examples', search_term, 0, function (json) {
                    if(json.examples.length > 0){
                        json.examples.forEach(function (element, i)
                        {
                            let modal_exam = $('#defModalExamples')

                            modal_exam.append(ExampleRowTemplate(
                                { japanese: element.japanese, english: element.english, id: i+1}
                            ))
                        });
                    }else{
                        $('#examplesCard').hide();
                    }

                    $('#examCardLoading').hide();
                })
            })
        };
    });
    ajax_lock = false;
}


/**
 * Ajax call template for Django
 */
const ajaxCall = function(url, query, pos, successCallback) {
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
