const express = require('express');
const fs = require('fs');
const bodyParser = require('body-parser');

const app = express();
const PORT = 3000;

app.use(bodyParser.json());

const readDataFromFile = (filename) => {
    try {
        return JSON.parse(fs.readFileSync(`./data/${filename}.json`));
    } catch (error) {
        console.error(`Error reading ${filename}:`, error);
        return [];
    }
};

const writeDataToFile = (filename, data) => {
    try {
        fs.writeFileSync(`./data/${filename}.json`, JSON.stringify(data, null, 2));
    } catch (error) {
        console.error(`Error writing ${filename}:`, error);
    }
};

// Products Routes
app.get('/products', (req, res) => {
    let products = readDataFromFile();

    if (req.query.category) {
        products = products.filter(product => product.category === req.query.category);
    }

    if (req.query.inStock) {
        const inStock = req.query.inStock.toLowerCase() === 'true';
        products = products.filter(product => product.inStock === inStock);
    }

    res.json(products);
});

app.get('/products/:id', (req, res) => {
    const products = readDataFromFile();
    const product = products.find(product => product.id === req.params.id);

    if (!product) {
        return res.status(404).json({ error: 'Product not found' });
    }

    res.json(product);
});

app.post('/products', (req, res) => {
    const newProduct = req.body;
    newProduct.id = Date.now().toString();
    let products = readDataFromFile();
    products.push(newProduct);
    writeDataToFile(products);
    res.json(newProduct);
});

app.put('/products/:id', (req, res) => {
    const updatedProduct = req.body;
    let products = readDataFromFile();
    const index = products.findIndex(product => product.id === req.params.id);

    if (index === -1) {
        return res.status(404).json({ error: 'Product not found' });
    }

    products[index] = { ...products[index], ...updatedProduct };
    writeDataToFile(products);
    res.json(products[index]);
});

app.delete('/products/:id', (req, res) => {
    let products = readDataFromFile();
    const index = products.findIndex(product => product.id === req.params.id);

    if (index === -1) {
        return res.status(404).json({ error: 'Product not found' });
    }

    products.splice(index, 1);
    writeDataToFile(products);
    res.json({ message: 'Product deleted successfully' });
});

// Orders Routes
app.post('/orders', (req, res) => {
    const newOrder = req.body;
    newOrder.id = Date.now().toString();
    const orders = readDataFromFile('orders');
    orders.push(newOrder);
    writeDataToFile('orders', orders);
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
    let carts = readDataFromFile('carts');
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

    writeDataToFile('carts', carts);
    res.json(cart);
});

app.get('/cart/:userId', (req, res) => {
    const { userId } = req.params;
    const carts = readDataFromFile('carts');
    const cart = carts.find(cart => cart.userId === userId);

    if (cart) {
        res.json(cart);
    } else {
        res.status(404).json({ error: 'Cart not found' });
    }
});

app.delete('/cart/:userId/item/:productId', (req, res) => {
    const { userId, productId } = req.params;
    let carts = readDataFromFile('carts');
    const cartIndex = carts.findIndex(cart => cart.userId === userId);

    if (cartIndex === -1) {
        return res.status(404).json({ error: 'Cart not found' });
    }

    const cart = carts[cartIndex];
    const itemIndex = cart.items.findIndex(item => item.productId === productId);

    if (itemIndex !== -1) {
        cart.items.splice(itemIndex, 1);
    }
    
    writeDataToFile('carts', carts);
    res.json(cart);
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});