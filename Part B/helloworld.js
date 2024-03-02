const http = require('http');
const express = require('express');
const app = express();

const server = http.createServer((req, res) => {
    res.writeHead(200, {'Content-Type': 'text/plain'});
    res.end('Hello World\n');
});

app.get('/getServer', (req, res) => {
    const serverUrl = `http://${req.hostname}:${3001}`;
    res.json({ code: 200, server: serverUrl });
});

server.listen(3001, () => {
    console.log('Server running at http://localhost:3001/');
});

app.listen(3000, () => {
    console.log(`DNS Registry Server running at http://localhost:3000/`);
});