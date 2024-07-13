
document.addEventListener('DOMContentLoaded', () => {
    const burger = document.getElementById('burger-menu');
    const dropdown = document.getElementById('dropdown');

    burger.addEventListener('click', () => {
        burger.classList.toggle('is-active');
        dropdown.classList.toggle('is-active');
    });
});