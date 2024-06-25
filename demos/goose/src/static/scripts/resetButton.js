document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('resetButton').addEventListener("click", function () {
        window.location.href = `/reset/${GUID}`;
    });
})