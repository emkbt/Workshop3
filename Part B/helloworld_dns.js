const express = require('express');

const app = express();

app.get('/getServer', (req, res) => {
    const serverUrl = `http://${req.hostname}:${3001}`;
    res.json({ code: 200, server: serverUrl });
});

const PORT = 3000;
app.listen(PORT, () => {
    console.log(`DNS Registry Server running at http://localhost:${PORT}/`);
});