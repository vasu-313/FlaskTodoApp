// Auto hide after 3 seconds
// setTimeout(() => {
//     document.querySelectorAll('.flash').forEach(msg => {
//         msg.style.display = 'none';
//     });
// }, 3000);

// // Manual close
// function closeFlash(element) {
//     element.parentElement.style.display = 'none';
// }

setTimeout(function () {
    let alerts = document.querySelectorAll(".auto-hide");
    alerts.forEach(function (alert) {
        alert.classList.remove("show");
        alert.classList.add("fade");
        setTimeout(() => alert.remove(), 500);
    });
}, 3000); // 3000ms = 3 seconds