/**
 * Templates
 */
const EntryRowTemplate = ({keb, keb_count, reb, reb_count, trans, trans_count, entry_id}) => {


	return `
    	<button type="button" class="list-group-item list-group-item-action entry" data-toggle="modal" data-target="#defModal" id="${entry_id}">
    		<div class="row">
				<div class="col-4">
					<div class="row">
						<div class="col-lg"><span class="badge badge-secondary">${keb_count}</span> ${keb}</div>
						<div class="col-lg"><small><span class="badge badge-secondary">${reb_count}</span> ${reb}</small></div>
					</div>
				</div>
				<div class="col-8"><span class="badge badge-primary">${trans_count}</span> ${trans}</div>
			</div>
		</button>
    `;
};
const EntryRowTemplateNoKanji = ({reb, reb_count, trans, trans_count, entry_id}) => {
	return `
    	<button type="button" class="list-group-item list-group-item-action entry" data-toggle="modal" data-target="#defModal" id="${entry_id}">
    		<div class="row">
				<div class="col-4">
					<div class="row">
						<div class="col-12"><span class="badge badge-secondary">${reb_count}</span> ${reb}</div>
					</div>
				</div>
				<div class="col-8"><span class="badge badge-primary">${trans_count}</span> ${trans}</div>
			</div>
		</button>
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
		<div class="mb-3"><small><span class="text-primary">${english}</span></small></div>
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
