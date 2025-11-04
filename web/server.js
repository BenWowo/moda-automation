const http = require('http');
const fs = require('fs');
const path = require('path');
require('dotenv').config({ path: path.join(__dirname, '..', '.env') });

const PORT = process.env.PORT || 8080;
const PASSWORD = process.env.PASSWORD || 'video123';

const mimeTypes = {
	'.html': 'text/html',
	'.js': 'text/javascript',
	'.css': 'text/css',
	'.png': 'image/png',
	'.ico': 'image/x-icon',
	'.webmanifest': 'application/manifest+json'
};

const server = http.createServer((req, res) => {
	if (req.url === '/api/config') {
		res.writeHead(200, { 'Content-Type': 'application/json' });
		res.end(JSON.stringify({ password: PASSWORD }));
		return;
	}

	let filePath = path.join(__dirname, 'src', req.url === '/' ? 'index.html' : req.url);
	const extname = path.extname(filePath);
	const contentType = mimeTypes[extname] || 'application/octet-stream';

	fs.readFile(filePath, (err, content) => {
		if (err) {
			if (err.code === 'ENOENT') {
				res.writeHead(404);
				res.end('404 Not Found');
			} else {
				res.writeHead(500);
				res.end('500 Internal Server Error');
			}
		} else {
			res.writeHead(200, { 'Content-Type': contentType });
			res.end(content);
		}
	});
});

server.listen(PORT, () => {
	console.log(`Server running at http://localhost:${PORT}/`);
});
