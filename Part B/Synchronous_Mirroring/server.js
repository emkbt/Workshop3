const express = require('express');
const fs = require('fs');
const bodyParser = require('body-parser');
const app = express();
const PORT = 3000;

const { startFailoverMonitoring } = require('./failover');
startFailoverMonitoring();

app.use(bodyParser.json());

const readDataFromFile = (filename) => {
    try {
        return JSON.parse(fs.readFileSync(`./data/${filename}.json`));
    } catch (error) {
        console.error(`Error reading ${filename}:`, error);
        return [];
    }
};

const writeToPrimaryStorage = (filename, data) => {
    try {
        fs.writeFileSync(`./data/${filename}.json`, JSON.stringify(data, null, 2));
    } catch (error) {
        console.error(`Error writing ${filename}:`, error);
    }
};

const writeToMirroredStorage  = (filename, data) => {
    try {
        fs.writeFileSync(`./data_2/${filename}.json`, JSON.stringify(data, null, 2));
    } catch (error) {
        console.error(`Error writing ${filename}:`, error);
    }
};

// Products Routes
app.get('/products', (req, res) => {
    let products = readDataFromFile('products');
    // Filter by category if provided in query params
    if (req.query.category) {
        products = products.filter(product => product.category === req.query.category);
    }
    // Filter by inStock if provided in query params
    if (req.query.inStock) {
        const inStock = req.query.inStock.toLowerCase() === 'true';
        products = products.filter(product => product.inStock === inStock);
    }
    res.json(products);
});

app.get('/products/:id', (req, res) => {
    const products = readDataFromFile('products');
    const product = products.find(product => product.id === req.params.id);
    if (!product) {
        return res.status(404).json({ error: 'Product not found' });
    }
    res.json(product);
});

app.post('/products', (req, res) => {
    const newProduct = req.body;
    newProduct.id = Date.now().toString(); // Generate a unique ID
    let products = readDataFromFile('products');
    products.push(newProduct);
    writeToPrimaryStorage('products', products);
    writeToMirroredStorage('products', products);
    res.json(newProduct);
});

app.put('/products/:id', (req, res) => {
    const updatedProduct = req.body;
    let products = readDataFromFile('products');
    const index = products.findIndex(product => product.id === req.params.id);
    if (index === -1) {
        return res.status(404).json({ error: 'Product not found' });
    }
    products[index] = { ...products[index], ...updatedProduct };
    writeToPrimaryStorage('products', products);
    writeToMirroredStorage('products', products);
    res.json(products[index]);
});

app.delete('/products/:id', (req, res) => {
    let products = readDataFromFile('products');
    const index = products.findIndex(product => product.id === req.params.id);
    if (index === -1) {
        return res.status(404).json({ error: 'Product not found' });
    }
    products.splice(index, 1);
    writeToPrimaryStorage('products', products);
    writeToMirroredStorage('products', products);
    res.json({ message: 'Product deleted successfully' });
});


// Orders Routes
app.post('/orders', (req, res) => {
    const newOrder = req.body;
    newOrder.id = Date.now().toString(); // Generate a unique order ID
    const orders = readDataFromFile('orders');
    orders.push(newOrder);
    writeToPrimaryStorage('orders', orders);
    writeToMirroredStorage('orders', orders);
    res.json(newOrder);
});

app.get('/orders/:userId', (req, res) => {
    const userId = req.params.userId;
    const orders = readDataFromFile('orders');
    const userOrders = orders.filter(order => order.userId === userId);
    res.json(userOrders);
});


// Cart Routes
app.post('/cart/:userId', (req, res) => {
    const { userId } = req.params;
    const { productId, quantity } = req.body;
    let carts = readDataFromFile('cart');
    let cart = carts.find(cart => cart.userId === userId);
    if (!cart) {
        cart = { userId, items: [] };
        carts.push(cart);
    }
    const existingItemIndex = cart.items.findIndex(item => item.productId === productId);
    if (existingItemIndex !== -1) {
        cart.items[existingItemIndex].quantity += quantity;
    } else {
        cart.items.push({ productId, quantity });
    }
    writeToPrimaryStorage('cart', carts);
    writeToMirroredStorage('cart', carts);
    res.json(cart);
});

app.get('/cart/:userId', (req, res) => {
    const { userId } = req.params;
    const carts = readDataFromFile('cart');
    const cart = carts.find(cart => cart.userId === userId);
    if (cart) {
        res.json(cart);
    } else {
        res.status(404).json({ error: 'Cart not found' });
    }
});

app.delete('/cart/:userId/item/:productId', (req, res) => {
    const { userId, productId } = req.params;
    let carts = readDataFromFile('cart');
    const cartIndex = carts.findIndex(cart => cart.userId === userId);
    if (cartIndex === -1) {
        return res.status(404).json({ error: 'Cart not found' });
    }
    const cart = carts[cartIndex];
    const itemIndex = cart.items.findIndex(item => item.productId === productId);
    if (itemIndex !== -1) {
        cart.items.splice(itemIndex, 1);
    }
    writeToPrimaryStorage('cart', carts);
    writeToMirroredStorage('cart', carts);
    res.json(cart);
});


app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html');
});

app.get('/products.html', (req, res) => {
    res.sendFile(__dirname + '/products.html');
});

app.get('/product-detail.html', (req, res) => {
    res.sendFile(__dirname + '/product-detail.html');
});

app.get('/orders.html', (req, res) => {
    res.sendFile(__dirname + '/orders.html');
});

app.get('/cart.html', (req, res) => {
    res.sendFile(__dirname + '/cart.html');
});

app.listen(PORT, () => {
    console.log(`E-commerce running at http://localhost:${PORT}/`);
});