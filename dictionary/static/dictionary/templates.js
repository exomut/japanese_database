/**
 * Templates
 */
const EntryRowTemplate = ({keb, entry_id}) => {
	return `
    	<button type="button" class="list-group-item list-group-item-action entry" data-toggle="modal" data-target="#defModal" id="${entry_id}">${keb}</button>
    `;
};

const KanjiRowTemplate = ({kanji, id}) => {
	return `
    	<div><span class="badge badge-secondary mr-2">${id}</span>${kanji}</div>
    `;
};

const ReadingRowTemplate = ({reading, id}) => {
	return `
	 	<div class="reading-row"><span class="badge badge-secondary mr-2">${id}</span>${reading}</div>
    `;
};

const TranslationRowTemplate = ({trans, id}) => {
	return `
		<div><span class="badge badge-primary mr-2">${id}</span>${trans}</div>
    `;
};

const ExampleRowTemplate = ({japanese, english, id}) => {
	return `
		<div><span class="badge badge-primary mr-2">${id}</span>${japanese}</div>
		<div>${english}</div>
    `;
};

const LoadingRowTemplate = `
	<button type="button" class="list-group-time list-group-item-action d-flex justify-content-center" id="loading-row">
    	<div class="spinner-grow text-primary " role="status">
        	<span class="sr-only">Loading...</span>
    	</div>
	</button>
`;

const Highlighter = (s) => { return `<span class="bg-warning">${s}</span>`;};

const TranslationRowInformation = ({info}) => {
	return `
		<p class="text-primary p-0 m-0"><small>${info}</small></p>
	`;
};
