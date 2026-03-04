// ==========================================
// SEND NOTIFICATION TO OFFICERS
// ==========================================

function openSendNotificationModal() {
    document.getElementById('send-notification-modal').classList.remove('hidden');
    // Close user menu
    document.getElementById('user-menu').classList.add('hidden');
}

function closeSendNotificationModal() {
    document.getElementById('send-notification-modal').classList.add('hidden');
    // Clear form
    document.getElementById('notif-title').value = '';
    document.getElementById('notif-message').value = '';
}

async function sendNotificationToOfficers() {
    const title = document.getElementById('notif-title').value.trim();
    const message = document.getElementById('notif-message').value.trim();

    if (!title || !message) {
        alert('Please enter both title and message');
        return;
    }

    try {
        const response = await fetch(`${API_CONFIG.baseUrl}/api/notifications/send`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                notification_type: 'normal',
                title: title,
                message: message,
                target_officer_ids: null, // null = broadcast to all
            }),
        });

        if (response.ok) {
            showNotification('Notification sent to all officers!', 'success');
            closeSendNotificationModal();
        } else {
            throw new Error('Failed to send notification');
        }
    } catch (error) {
        console.error('Error sending notification:', error);
        showNotification('Failed to send notification', 'error');
    }
}
