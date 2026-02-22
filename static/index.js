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

// setTimeout(function () {
//     let alerts = document.querySelectorAll(".auto-hide");
//     alerts.forEach(function (alert) {
//         alert.classList.remove("show");
//         alert.classList.add("fade");
//         setTimeout(() => alert.remove(), 500);
//     });
// }, 3000); // 3000ms = 3 seconds




document.getElementById("project").addEventListener("change", function(){

    let projectId = this.value;

    if (projectId == "0") {
        document.getElementById("task").innerHTML = "<option value='0'>Select Task</option>";
        document.getElementById("activity").innerHTML = "<option value='0'>Select Activity</option>";
        return;
    }

    fetch("/get_tasks/" + projectId)
    .then(response => response.json())
    .then(data => {

        let taskDropdown = document.getElementById("task");
        taskDropdown.innerHTML = "<option value='0'>Select Task</option>";

        data.forEach(function(task){
            let option = document.createElement("option");
            option.value = task.id;
            option.text = task.name;
            taskDropdown.appendChild(option);
        });

        document.getElementById("activity").innerHTML = "<option value='0'>Select Activity</option>";
    });
});



document.getElementById("task").addEventListener("change", function(){

    let taskId = this.value;

    if (taskId == "0") {
        document.getElementById("activity").innerHTML = "<option value='0'>Select Activity</option>";
        return;
    }

    fetch("/get_activities/" + taskId)
    .then(response => response.json())
    .then(data => {

        let activityDropdown = document.getElementById("activity");
        activityDropdown.innerHTML = "<option value='0'>Select Activity</option>";

        data.forEach(function(activity){
            let option = document.createElement("option");
            option.value = activity.id;
            option.text = activity.name;
            activityDropdown.appendChild(option);
        });
    });
});

