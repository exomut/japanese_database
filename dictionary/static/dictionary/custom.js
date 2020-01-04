const EntryRowTemplate = ({keb}) => `
    <li class="list-group-item">${keb}</li>
`;


$(document).on('submit', '#search-form', function (e) {
    e.preventDefault();
    $.ajax({
        url: '/search',
        type: 'POST',
        dataType: 'json',
        data: {
            query: $('#search').val(),
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            action: 'post'
        },
        success: [function (json) {
            $('#branding').text($('#search').val());
            $('#results').html("");
            json.entries.forEach(element => $('#results').append(EntryRowTemplate({keb: element})));
        }]
    })
});
