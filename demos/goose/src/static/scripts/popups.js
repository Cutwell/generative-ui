const popupWrappers = document.querySelectorAll('.popup-wrapper');
const popups = document.querySelectorAll('.popup');
const closeButtons = document.querySelectorAll('.close-button');

function openPopup(popupWrapper) {
    popupWrapper.style.display = 'block';
    document.body.style.overflow = 'hidden';
}

function closePopup(popupWrapper) {
    popupWrapper.style.display = 'none';
    document.body.style.overflow = 'auto';
}

popups.forEach(function (popup) {
    popup.addEventListener('click', function (event) {
        event.stopPropagation();
    });
});

popupWrappers.forEach(function (popupWrapper, index) {
    popupWrapper.addEventListener('click', function () {
        closePopup(popupWrapper);
    });

    closeButtons[index].addEventListener('click', function () {
        closePopup(popupWrapper);
    });
});
