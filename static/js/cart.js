// Cart functionality
function updateCart(bookId, change) {
    const cartItems = JSON.parse(localStorage.getItem('cart') || '[]');
    const itemIndex = cartItems.findIndex(item => item.id === bookId);
    
    if (itemIndex > -1) {
        cartItems[itemIndex].quantity += change;
        if (cartItems[itemIndex].quantity <= 0) {
            cartItems.splice(itemIndex, 1);
        }
    } else if (change > 0) {
        cartItems.push({ id: bookId, quantity: 1 });
    }
    
    localStorage.setItem('cart', JSON.stringify(cartItems));
    updateCartBadge();
}

function updateCartBadge() {
    const cartItems = JSON.parse(localStorage.getItem('cart') || '[]');
    const totalItems = cartItems.reduce((sum, item) => sum + item.quantity, 0);
    document.getElementById('cart-badge').textContent = totalItems;
}

// Initialize cart badge on page load
document.addEventListener('DOMContentLoaded', function() {
    updateCartBadge();
});
