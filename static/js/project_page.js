document.addEventListener("DOMContentLoaded", function () {
    const csrftoken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    function fetchWithCsrf(url, options = {}) {
        options.headers = options.headers || {};
        options.headers['X-CSRFToken'] = csrftoken;
        return fetch(url, options);
    }

   // Show Task Details Modal
   window.showTaskDetails = function (teamId, projectId, taskId) {
    console.log('teamId:', teamId, 'projectId:', projectId, 'taskId:', taskId);

    fetch(`/dashboard/teams/${teamId}/projects/${projectId}/tasks/${taskId}/details/`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
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

            // Set data attributes for teamId and projectId correctly
            const taskDetailsModal = document.getElementById('taskDetailsModal');
            taskDetailsModal.setAttribute('data-task-id', taskId);
            taskDetailsModal.setAttribute('data-team-id', teamId);
            taskDetailsModal.setAttribute('data-project-id', projectId);

            document.getElementById('taskDetailsOverlay').style.display = 'flex';
        })
        .catch(error => console.error('Error fetching task details:', error));
};

    // Close Task Details Modal
    window.closeModal = function() {
        document.getElementById('taskDetailsOverlay').style.display = 'none';
    }

    // Assign Task to Current User
    window.assignTaskToMe = function() {
        const teamId = document.getElementById('taskDetailsModal').getAttribute('data-team-id');
        const projectId = document.getElementById('taskDetailsModal').getAttribute('data-project-id');
        const taskId = document.getElementById('taskDetailsModal').getAttribute('data-task-id');
        fetchWithCsrf(`/dashboard/teams/${teamId}/projects/${projectId}/tasks/${taskId}/assign_to_me/`, { method: 'POST' })
            .then(response => {
                if (response.ok) {
                    location.reload();
                } else {
                    console.error("Failed to assign task.");
                }
            })
            .catch(error => console.error('Error assigning task:', error));
    }

    window.assignTaskToMe = function () {
        const taskDetailsModal = document.getElementById('taskDetailsModal');
        const teamId = taskDetailsModal.getAttribute('data-team-id');
        const projectId = taskDetailsModal.getAttribute('data-project-id');
        const taskId = taskDetailsModal.getAttribute('data-task-id');
        fetchWithCsrf(`/dashboard/teams/${teamId}/projects/${projectId}/tasks/${taskId}/assign_to_me/`, { method: 'POST' })
            .then(response => {
                if (response.ok) {
                    location.reload();
                } else {
                    console.error("Failed to assign task.");
                }
            })
            .catch(error => console.error('Error assigning task:', error));
    };
    
    window.changeStatus = function (newStatus) {
        const taskDetailsModal = document.getElementById('taskDetailsModal');
        const teamId = taskDetailsModal.getAttribute('data-team-id');
        const projectId = taskDetailsModal.getAttribute('data-project-id');
        const taskId = taskDetailsModal.getAttribute('data-task-id');
        fetchWithCsrf(`/dashboard/teams/${teamId}/projects/${projectId}/tasks/${taskId}/change_status/`, {
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
    };
    
    window.editTask = function () {
        const taskDetailsModal = document.getElementById('taskDetailsModal');
        const teamId = taskDetailsModal.getAttribute('data-team-id');
        const projectId = taskDetailsModal.getAttribute('data-project-id');
        const taskId = taskDetailsModal.getAttribute('data-task-id');
        window.location.href = `/dashboard/teams/${teamId}/projects/${projectId}/tasks/${taskId}/edit/`;
    };
    
    window.deleteTask = function () {
        const taskDetailsModal = document.getElementById('taskDetailsModal');
        const teamId = taskDetailsModal.getAttribute('data-team-id');
        const projectId = taskDetailsModal.getAttribute('data-project-id');
        const taskId = taskDetailsModal.getAttribute('data-task-id');
        if (!confirm("Are you sure you want to delete this task?")) return;
    
        fetchWithCsrf(`/dashboard/teams/${teamId}/projects/${projectId}/tasks/${taskId}/delete/`, { method: 'POST' })
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
    };
});
