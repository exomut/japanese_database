/**
 * Search Submit using Ajax
 */
const EntryRowTemplate = ({keb, entry_id}) => `<li class="list-group-item list-group-item-action entry" id="${entry_id}">${keb}</li>`;

$(document).on('submit', '#search-form', function (e) {
    e.preventDefault();
    let search = $('#search').val();
    ajaxCall('/search', search , function (json) {
        // Set the current search term in the search bar
        $('#branding').text(search);

        let results_elem = $('#results');
        results_elem.html("");
        json.entries.forEach(element => {
            results_elem.append(EntryRowTemplate({keb: element.keb, entry_id: element.entry_id}));
            document.getElementById(element.entry_id).onclick = function () {
                alert(element.keb)
            };
        });
    })
});

/**
 * Ajax call template for Django
 */
const ajaxCall = function(url, query, successCallback) {
    $.ajax({
        url: url,
        type: 'POST',
        dataType: 'json',
        data: {
            query: query,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            action: 'post'
        },
        success: [ successCallback ]
    })
};
