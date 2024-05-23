const upstream = 'www.south-plus.net'

const upstream_path = '/'

const https = true

const disable_cache = false

let data={}
addEventListener('fetch', event => {
    event.respondWith(fetchAndApply(event.request));
})

async function fetchAndApply(request) {
    let response = null;
    let url = new URL(request.url);
    let url_hostname = url.hostname;

    if (https == true) {
        url.protocol = 'https:';
    } else {
        url.protocol = 'http:';
    }

    var upstream_domain = upstream;

    url.host = upstream_domain;
    if (url.pathname == '/') {
        url.pathname = upstream_path;
    } else {
        url.pathname = upstream_path + url.pathname;
    }

  
	let method = request.method;
	let request_headers = request.headers;
	let new_request_headers = new Headers(request_headers);
	
	new_request_headers.set('Host', upstream_domain);
	new_request_headers.set('Referer', url.protocol + '//' + upstream_domain);
	

	if(method == 'POST'){
		let origin_formData = await request.text()
		data = {
			method: method,
			headers: new_request_headers,
			body : origin_formData
		}
		console.log(data)
	}else if(method == 'GET'){
		data = {
			method: method,
			headers: new_request_headers
		}
	}
	console.log("========================")
	console.log(Object.fromEntries(data.headers))
	let original_response = await fetch(url.href, data)

	let connection_upgrade = new_request_headers.get("Upgrade");
	if (connection_upgrade && connection_upgrade.toLowerCase() == "websocket") {
		return original_response;
	}

	let resp_content = null;
	let response_headers = original_response.headers;
	let new_response_headers = new Headers(response_headers);
	let status = original_response.status;
	
	if (disable_cache) {
		new_response_headers.set('Cache-Control', 'no-store');
	}

	new_response_headers.set('access-control-allow-origin', '*');
	new_response_headers.set('access-control-allow-credentials', "true");
	new_response_headers.delete('content-security-policy');
	new_response_headers.delete('content-security-policy-report-only');
	new_response_headers.delete('clear-site-data');
	
	const content_type = new_response_headers.get('content-type');
	if ( url.pathname.startsWith("/ck.php")) {
		resp_content = original_response.body
	}else if (content_type != null && content_type.includes('text/html')) {
		resp_content = await replace_response_text(original_response, upstream_domain, url_hostname);
	} else {
		resp_content = original_response.body
	}
	
	
	response = new Response(resp_content, {
		status,
		headers: new_response_headers
	})
    
    
    return response;
}


async function replace_response_text(response, upstream_domain, host_name) {
    let text = await response.text()
	let re = new RegExp(upstream_domain, 'g')
	text = text.replace(re, host_name);
    return text;
}
