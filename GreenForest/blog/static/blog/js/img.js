function openImageModal(imageUrl, productName) {
    var modal = document.getElementById('imageModal');
    var modalImage = document.getElementById('modalImage');
    var modalCaption = document.getElementById('modalCaption');

    modal.style.display = 'block';
    modalImage.src = imageUrl;
    modalCaption.textContent = productName;
}

function closeImageModal() {
    var modal = document.getElementById('imageModal');
    modal.style.display = 'none';
}

// Закрытие модального окна при клике вне изображения
window.onclick = function(event) {
    var modal = document.getElementById('imageModal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
};