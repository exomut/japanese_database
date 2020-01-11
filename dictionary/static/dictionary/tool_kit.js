function get_cookie( name ) {
	let cookies = document.cookie.split( ';' )

	for (let i = 0; i < cookies.length; i++) {
		entry = cookies[i].trim()

		if (entry.startsWith( name + '=' )) {
			return entry.replace( name + '=', '' )
		}
	}
	return null
}

function make_cookie(name, value, expires) {
	let date = new Date();
	date.setTime(date.getTime() + (expires*24*60*60*1000));
	document.cookie = `${name}=${value}; expires=${date};`;
}
