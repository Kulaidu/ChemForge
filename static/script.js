document.addEventListener("DOMContentLoaded", function() {
    const loader = document.getElementById('loading');

    // Show the loader when navigating away from the page
    window.addEventListener('beforeunload', () => {
        loader.classList.remove('d-none');
    });

    // Show the loader when submitting forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', () => {
            loader.classList.remove('d-none');
        });
    });

    // Hide the loader once the page fully loads
    window.addEventListener('load', () => {
        loader.classList.add('d-none');
    });
});