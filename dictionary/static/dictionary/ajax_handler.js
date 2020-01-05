/**
 * global variables
 */
let current_pos = 0;
let ajax_lock = false;

/**
 * Handlers
 */
$("#main").scroll(function(){
    let ele = $('#main');
    if ( !ajax_lock && ele.get(0).scrollHeight - ele.height() - 50 <= ele.scrollTop() ) {
        ajax_lock = true;
        get_entries();
    }
});

$(document).on('submit', '#search-form', function (e) {
    e.preventDefault();
    search();
});

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
    $('#branding').text(search);

    // Clear old results
    $('#results').html("");

    current_pos = 0;

    get_entries()
}

function get_entries()
{
    let search = $('#search').val();
    ajaxCall('/search', search , current_pos, function (json) {
        current_pos = json.pos;
        make_entries(json.entries);
    });
}

const EntryRowTemplate = ({keb, entry_id}) => `
<div class="col-12 list-group-item list-group-item-action entry" data-toggle="modal" data-target=".def-modal" id="${entry_id}">${keb}</div>
`;

function make_entries(entries) {
    // Set a ajax click handler for each entry
    entries.forEach(element => {

        // Apply the template
        $('#results').append(EntryRowTemplate({keb: element.keb, entry_id: element.entry_id}));

        document.getElementById(element.entry_id).onclick = function () {
            ajaxCall('/definition', element.entry_id, 0, function (json) {

                $('#defModalLabel').text(json.keb);
                $('#defModalReading').text(json.reb);
                $('#defModalTranslation').text(json.trans);

            })
        };

    });
    ajax_lock = false;
}

/**
 * Ajax call template for Django
 */
const ajaxCall = function(url, query, pos, successCallback) {
    $.ajax({
        url: url,
        type: 'POST',
        dataType: 'json',
        data: {
            query: query,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            pos: pos,
            action: 'post'
        },
        success: [ successCallback ]
    })
};
