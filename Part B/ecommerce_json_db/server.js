const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(bodyParser.json());
app.use(express.static('public1'));

// Function to read data from JSON file
const readDataFromFile = (filename) => {
    try {
        return JSON.parse(fs.readFileSync(`./data/${filename}.json`));
    } catch (error) {
        console.error(`Error reading ${filename}:`, error);
        return [];
    }
};

// Function to write data to JSON file
const writeDataToFile = (filename, data) => {
    try {
        fs.writeFileSync(`./data/${filename}.json`, JSON.stringify(data, null, 2));
    } catch (error) {
        console.error(`Error writing ${filename}:`, error);
    }
};

// Products Routes
app.get('/products', (req, res) => {
    const products = readDataFromFile('products');
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
    writeDataToFile('products', products);
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
    writeDataToFile('products', products);
    res.json(products[index]);
});

app.delete('/products/:id', (req, res) => {
    let products = readDataFromFile('products');
    const index = products.findIndex(product => product.id === req.params.id);

    if (index === -1) {
        return res.status(404).json({ error: 'Product not found' });
    }

    products.splice(index, 1);
    writeDataToFile('products', products);
    res.json({ message: 'Product deleted successfully' });
});

// Orders Routes
app.post('/orders', (req, res) => {
    const newOrder = req.body;
    newOrder.orderId = Date.now().toString(); // Generate a unique order ID
    let orders = readDataFromFile('orders');
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

    // Read cart data
    let carts = readDataFromFile('carts');

    // Find user's cart or create a new one
    let cart = carts.find(cart => cart.userId === userId);
    if (!cart) {
        cart = { userId, items: [] };
        carts.push(cart);
    }

    // Add item to cart or update quantity if already exists
    const existingItemIndex = cart.items.findIndex(item => item.productId === productId);
    if (existingItemIndex !== -1) {
        cart.items[existingItemIndex].quantity += quantity;
    } else {
        cart.items.push({ productId, quantity });
    }

    // Write cart data
    writeDataToFile('carts', carts);

    // Return updated cart
    res.json(cart);
});

app.get('/cart/:userId', (req, res) => {
    const { userId } = req.params;

    // Read cart data
    const carts = readDataFromFile('carts');

    // Find user's cart
    const cart = carts.find(cart => cart.userId === userId);

    // Return user's cart
    if (cart) {
        res.json(cart);
    } else {
        res.status(404).json({ error: 'Cart not found' });
    }
});

app.delete('/cart/:userId/item/:productId', (req, res) => {
    const { userId, productId } = req.params;

    // Read cart data
    let carts = readDataFromFile('carts');

    // Find user's cart
    const cartIndex = carts.findIndex(cart => cart.userId === userId);
    if (cartIndex === -1) {
        return res.status(404).json({ error: 'Cart not found' });
    }

    // Remove item from cart
    const cart = carts[cartIndex];
    const itemIndex = cart.items.findIndex(item => item.productId === productId);
    if (itemIndex !== -1) {
        cart.items.splice(itemIndex, 1);
    }

    // Write cart data
    writeDataToFile('carts', carts);

    // Return updated cart
    res.json(cart);
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
