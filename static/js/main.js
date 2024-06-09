function sendData() {
	const navigatorData = {
		language: navigator.language,
		userAgent: navigator.userAgent,
		osCpu: navigator.oscpu
	};
	fetch('/collect-data', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({ event: 'page_view', navigator: navigatorData })
	});
}
sendData();
