const form = document.querySelector('#mainForm');
const spinnerWrapper = document.querySelector('#loading-wrapper')

form.addEventListener('submit', () => {
    spinnerWrapper.style.display = 'block';
    document.body.style.overflow = 'hidden';
});

form.addEventListener('load', () => {
    spinnerWrapper.style.display = 'none';
    document.body.style.overflow = 'auto';
});