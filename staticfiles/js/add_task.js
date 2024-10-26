document.addEventListener("DOMContentLoaded", function () {
    const milestonesContainer = document.getElementById("milestones-container");
    const addMilestoneButton = document.getElementById("addMilestoneButton");

    // Add milestone input field
    addMilestoneButton.addEventListener("click", function () {
        const milestoneDiv = document.createElement("div");
        milestoneDiv.className = "milestone-item";
        milestoneDiv.innerHTML = `
            <input type="text" name="milestone" placeholder="Enter milestone">
            <button type="button" onclick="removeMilestone(this)">Delete</button>
        `;
        milestonesContainer.appendChild(milestoneDiv);
    });

    // Remove a specific milestone input field
    window.removeMilestone = function (button) {
        button.parentElement.remove();
    };

    // Convert milestones to JSON before form submission
    document.getElementById("addTaskForm").addEventListener("submit", function (event) {
        const milestones = Array.from(milestonesContainer.querySelectorAll("input[name='milestone']"))
            .map(input => input.value.trim())
            .filter(value => value);
    
        const milestonesField = document.createElement("input");
        milestonesField.type = "hidden";
        milestonesField.name = "milestones";
        milestonesField.value = JSON.stringify(milestones);
        this.appendChild(milestonesField);
    });
});
