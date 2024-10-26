document.addEventListener("DOMContentLoaded", function () {
    const milestonesContainer = document.getElementById("milestones-container");
    const addMilestoneButton = document.getElementById("addMilestoneButton");

    if (addMilestoneButton) {
        addMilestoneButton.addEventListener("click", function () {
            const milestoneDiv = document.createElement("div");
            milestoneDiv.className = "milestone-item";
            milestoneDiv.innerHTML = `
                <input type="text" name="milestone" placeholder="Enter milestone">
                <button type="button" onclick="removeMilestone(this)">Delete</button>
            `;
            milestonesContainer.appendChild(milestoneDiv);
        });
    }

    window.removeMilestone = function (button) {
        button.parentElement.remove();
    };

    const taskForm = document.getElementById("editTaskForm");
    if (taskForm) {
        taskForm.addEventListener("submit", function (event) {
            const milestones = Array.from(milestonesContainer.querySelectorAll("input[name='milestone']"))
                .map(input => input.value.trim())
                .filter(value => value);

            const milestonesField = document.createElement("input");
            milestonesField.type = "hidden";
            milestonesField.name = "milestones";
            milestonesField.value = JSON.stringify(milestones);
            this.appendChild(milestonesField);
        });
    }
});
