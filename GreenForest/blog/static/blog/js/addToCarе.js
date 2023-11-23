function addToCart(productId) {
    fetch(`/add_to_cart/${productId}/`, { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            updateCart(data);
        })
        .catch(error => console.error('Error:', error));
}

function updateCart(cartData) {
    const cartContainer = document.getElementById('cart-container');
    cartContainer.innerHTML = cartData.cart_html;
}
