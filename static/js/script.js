let cart = [];
let cartCount = 0;
let cartTotal = 0;

function addToCart(productName, productPrice) {
    const product = cart.find(item => item.name === productName);
    if (product) {
        product.quantity += 1;
    } else {
        cart.push({ name: productName, price: parseFloat(productPrice), quantity: 1 });
    }
    cartCount += 1;
    cartTotal += parseFloat(productPrice);
    updateCart();
}


function removeFromCart(productName) {
    const product = cart.find(item => item.name === productName);
    if (product) {
        cartCount -= product.quantity;
        cartTotal -= product.price * product.quantity;
        cart = cart.filter(item => item.name !== productName);
        updateCart();
    }
}

function updateQuantity(productName, amount) {
    const product = cart.find(item => item.name === productName);
    if (product) {
        const newQuantity = product.quantity + amount;
        if (newQuantity > 0) {
            product.quantity = newQuantity;
            cartCount += amount;
            cartTotal += product.price * amount;
            updateCart();
        }
    }
}

function updateCart() {
    document.getElementById('cart-count').textContent = cartCount;
    document.getElementById('cart-total').textContent = cartTotal.toFixed(2); 

    const cartItems = document.getElementById('cart-items');
    cartItems.innerHTML = '';
    cart.forEach(item => {
        const div = document.createElement('div');
        div.classList.add('cart-item');
        console.log(item.name.toLocaleString());
        div.innerHTML = `
            <p class="item-name">${item.name}</p>
            <p class="item-quantity">Cantidad: ${item.quantity}</p>
            <p class="item-price">$${(item.price).toFixed(2)}</p>
            <button onclick="updateQuantity('${item.name}', -1)">-</button>
            <button onclick="updateQuantity('${item.name}', 1)">+</button>
            <button onclick="removeFromCart('${item.name}')">Eliminar</button>
        `;
        cartItems.appendChild(div);
    });

}

function openCart() {
    document.getElementById('cart-modal').style.display = 'block';
}

function closeCart() {
    document.getElementById('cart-modal').style.display = 'none';


}

function handlePaymentMethodChange() {
    const paymentMethod = document.getElementById('payment-method').value;
    const installmentsMenu = document.getElementById('installments-menu');
    if (paymentMethod === 'credit-card') {
        installmentsMenu.style.display = 'block';
    } else {
        installmentsMenu.style.display = 'none';
    }


}

function processPayment() {
    console.log('Procesando el pago...');

    // Simular la lógica de procesamiento del pago

    // Simulación de un retardo en el procesamiento del pago
    setTimeout(() => {
        // Suponiendo que el pago fue exitoso
        console.log('Pago realizado correctamente');
        
        // Mostrar la ventana de confirmación
        document.getElementById('payment-confirmation-modal').style.display = 'block';

        // Opcional: Limpiar el carrito después del pago
        cart = [];
        cartCount = 0;
        cartTotal = 0;
        updateCart();
    }, 2000); // 2 segundos de retardo simulado
}

function closeConfirmation() {
    document.getElementById('payment-confirmation-modal').style.display = 'none';
}

document.querySelector('.cart-icon').addEventListener('click', openCart);
document.getElementById('payment-method').addEventListener('change', handlePaymentMethodChange);
document.getElementById('process-payment').addEventListener('click', processPayment);
