/**
 * Block variables
 */
let current_pos = 0;
let ajax_lock = false;
let call_lock = false;
let current_xhr;
let search_type = "st-cont";


/**
 * Templates
 */
const EntryRowTemplate = ({keb, entry_id}) => {
    return `
    <button type="button" class="list-group-item list-group-item-action entry" data-toggle="modal" data-target=".def-modal" id="${entry_id}">${keb}</button>
    `;
};

const LoadingRowTemplate = `
<button type="button" class="list-group-time list-group-item-action d-flex justify-content-center" id="loading-row">
    <div class="spinner-grow text-primary " role="status">
        <span class="sr-only">Loading...</span>
    </div>
</button>
`;


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
    $('#branding').text(search);

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
        $('#loading').show();
        $('#results').append(LoadingRowTemplate);
    }
    else
    {
        $('#loading').hide();
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
