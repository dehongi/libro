document.addEventListener('DOMContentLoaded', function () {
    // Handle comment form submissions
    document.querySelectorAll('.comment-form').forEach(form => {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            const formData = new FormData(this);

            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': formData.get('csrfmiddlewaretoken')
                }
            })
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'success') {
                        // Add new comment to the list
                        const commentsList = this.closest('.comments-section').querySelector('.comments-list');
                        const newComment = createCommentElement(data.comment);
                        commentsList.appendChild(newComment);
                        this.reset();
                    }
                });
        });
    });
});

function createCommentElement(comment) {
    const div = document.createElement('div');
    div.className = 'border-start border-3 ps-3 mb-2';
    div.innerHTML = `
        <p class="small mb-1">
            <strong>${comment.user}</strong>
            <span class="text-muted">• ${comment.created_at}</span>
        </p>
        <p class="mb-0">${comment.content}</p>
    `;
    return div;
} 