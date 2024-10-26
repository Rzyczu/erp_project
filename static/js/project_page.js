document.addEventListener("DOMContentLoaded", function () {
    const csrftoken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    function fetchWithCsrf(url, options = {}) {
        options.headers = options.headers || {};
        options.headers['X-CSRFToken'] = csrftoken;
        return fetch(url, options);
    }

    // Show Task Details Modal
    window.showTaskDetails = function(taskId) {
        fetch(`/tasks/${taskId}/details/`)
            .then(response => response.json())
            .then(data => {
                document.getElementById('modalTaskName').innerText = data.name || '-';
                document.getElementById('modalTaskDescription').innerText = data.description || '-';
                document.getElementById('modalTaskDueDate').innerText = data.due_date || '-';
                document.getElementById('modalAssignedUser').innerText = data.assigned_user || 'Unassigned';
                document.getElementById('modalTaskStatus').innerText = data.status || '-';

                const milestonesList = document.getElementById('modalMilestones');
                milestonesList.innerHTML = '';
                if (data.milestones && data.milestones.length > 0) {
                    data.milestones.forEach((milestone, index) => {
                        const li = document.createElement('li');
                        li.textContent = `${index + 1}. ${milestone}`;
                        milestonesList.appendChild(li);
                    });
                } else {
                    milestonesList.innerHTML = '<li>No milestones available.</li>';
                }

                const imagesContainer = document.getElementById('modalImages');
                imagesContainer.innerHTML = '';
                if (data.images && data.images.length > 0) {
                    data.images.forEach(imageUrl => {
                        const img = document.createElement('img');
                        img.src = imageUrl;
                        img.alt = 'Task Image';
                        img.style.width = '100px';
                        img.style.margin = '5px';
                        imagesContainer.appendChild(img);
                    });
                } else {
                    imagesContainer.textContent = 'No images available.';
                }

                document.getElementById('taskDetailsOverlay').style.display = 'flex';
                document.getElementById('taskDetailsModal').setAttribute('data-task-id', taskId);
            })
            .catch(error => console.error('Error fetching task details:', error));
    }

    // Close Task Details Modal
    window.closeModal = function() {
        document.getElementById('taskDetailsOverlay').style.display = 'none';
    }

    // Assign Task to Current User
    window.assignTaskToMe = function() {
        const taskId = document.getElementById('taskDetailsModal').getAttribute('data-task-id');
        fetchWithCsrf(`/tasks/${taskId}/assign_to_me/`, { method: 'POST' })
            .then(response => {
                if (response.ok) {
                    location.reload();
                } else {
                    console.error("Failed to assign task.");
                }
            })
            .catch(error => console.error('Error assigning task:', error));
    }

    // Change Task Status
    window.changeStatus = function(newStatus) {
        const taskId = document.getElementById('taskDetailsModal').getAttribute('data-task-id');
        fetchWithCsrf(`/tasks/${taskId}/change_status/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ status: newStatus })
        })
            .then(response => {
                if (response.ok) {
                    location.reload();
                } else {
                    console.error("Failed to update task status.");
                }
            })
            .catch(error => console.error('Error changing status:', error));
    }

    // Edit Task
    window.editTask = function() {
        const taskId = document.getElementById('taskDetailsModal').getAttribute('data-task-id');
        window.location.href = `/tasks/${taskId}/edit/`;
    }

    // Delete Task
    window.deleteTask = function() {
        const taskId = document.getElementById('taskDetailsModal').getAttribute('data-task-id');
        if (!confirm("Are you sure you want to delete this task?")) return;

        fetchWithCsrf(`/tasks/${taskId}/delete/`, { method: 'POST' })
            .then(response => {
                if (response.ok) {
                    alert("Task deleted successfully!");
                    closeModal();
                    location.reload();
                } else {
                    alert("Failed to delete the task.");
                }
            })
            .catch(error => console.error("Error deleting task:", error));
    }
});
