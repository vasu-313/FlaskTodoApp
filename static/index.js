 // Auto hide after 3 seconds
    setTimeout(() => {
        document.querySelectorAll('.flash').forEach(msg => {
            msg.style.display = 'none';
        });
    }, 3000);

    // Manual close
    function closeFlash(element) {
        element.parentElement.style.display = 'none';
    }