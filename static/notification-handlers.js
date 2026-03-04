// ==========================================
// NOTIFICATION SYSTEM
// ==========================================
let notifications = [];
let emergencyAlerts = [];

// Handle SOS Alert
function handleSOSAlert(data) {
    console.log('🚨 SOS ALERT RECEIVED:', data);

    const { officer_id, officer_name, lat, lng, emergency_type, message_text, triggered_at } = data;

    // Update officer marker to RED emergency state
    updateOfficerEmergencyState(officer_id, true);

    // Add to emergency alerts
    const alert = {
        id: data.notification_id || `alert_${Date.now()}`,
        officer_id,
        officer_name,
        lat,
        lng,
        emergency_type,
        message: message_text || `${emergency_type.toUpperCase()} triggered`,
        time: triggered_at,
        ...data
    };

    emergencyAlerts.unshift(alert);

    // Update emergency alerts display
    updateAlertsDisplay();

    // Play audio alert
    playEmergencySound();

    // Show browser notification if permitted
    showBrowserNotification(`🚨 EMERGENCY - ${officer_name}`, alert.message);

    // Fly to officer location
    if (lat && lng && officerMarkers[officer_id]) {
        map.flyTo([lat, lng], 16, { duration: 1.5 });
    }
}

// Handle SOS Cancelled
function handleSOSCancelled(data) {
    console.log('✅ SOS CANCELLED:', data);

    const { officer_id } = data;

    // Remove emergency state from officer marker
    updateOfficerEmergencyState(officer_id, false);

    // Remove from emergency alerts
    emergencyAlerts = emergencyAlerts.filter(alert => alert.officer_id !== officer_id);
    updateAlertsDisplay();
}

// Handle Normal Notification
function handleNotification(data) {
    console.log('📬 NOTIFICATION RECEIVED:', data);

    const { notification_id, notification_type, title, message, created_at } = data;

    if (notification_type === 'emergency') {
        // Already handled by handleSOSAlert
        return;
    }

    // Add to notifications
    const notif = {
        id: notification_id,
        type: notification_type,
        title,
        message,
        time: created_at,
        ...data
    };

    notifications.unshift(notif);

    // Update notifications display
    updateNotificationsDisplay();
}

// Update Officer Emergency State (RED highlighting)
function updateOfficerEmergencyState(officerId, isEmergency) {
    if (!officerMarkers[officerId]) return;

    const marker = officerMarkers[officerId];
    const element = marker.getElement();

    if (!element) return;

    if (isEmergency) {
        element.classList.add('officer-marker-emergency');

        // Update officer state
        if (officers[officerId]) {
            officers[officerId].sos_active = true;
        }
    } else {
        element.classList.remove('officer-marker-emergency');

        // Update officer state
        if (officers[officerId]) {
            officers[officerId].sos_active = false;
        }
    }
}

// Play Emergency Sound
function playEmergencySound() {
    const audio = document.getElementById('emergency-alert-sound');
    if (audio) {
        audio.play().catch(e => console.log('Audio play failed:', e));
    }
}

// Show Browser Notification
function showBrowserNotification(title, message) {
    if ('Notification' in window && Notification.permission === 'granted') {
        new Notification(title, {
            body: message,
            icon: '/favicon.ico',
            badge: '/favicon.ico'
        });
    } else if ('Notification' in window && Notification.permission !== 'denied') {
        Notification.requestPermission().then(permission => {
            if (permission === 'granted') {
                new Notification(title, { body: message });
            }
        });
    }
}

// Toggle Notification Panel
function toggleNotificationPanel() {
    const panel = document.getElementById('notification-panel');
    const alertsPanel = document.getElementById('alerts-panel');

    // Close alerts panel if open
    if (!alertsPanel.classList.contains('hidden')) {
        alertsPanel.classList.add('hidden');
    }

    panel.classList.toggle('hidden');

    if (!panel.classList.contains('hidden')) {
        updateNotificationsDisplay();
    }
}

// Toggle Alerts Panel
function toggleAlertsPanel() {
    const panel = document.getElementById('alerts-panel');
    const notifPanel = document.getElementById('notification-panel');

    // Close notification panel if open
    if (!notifPanel.classList.contains('hidden')) {
        notifPanel.classList.add('hidden');
    }

    panel.classList.toggle('hidden');

    if (!panel.classList.contains('hidden')) {
        updateAlertsDisplay();
    }
}

// Update Notifications Display
function updateNotificationsDisplay() {
    const list = document.getElementById('notification-list');
    const badge = document.getElementById('notif-badge');

    // Update badge
    if (notifications.length > 0) {
        badge.textContent = notifications.length;
        badge.classList.remove('hidden');
    } else {
        badge.classList.add('hidden');
    }

    // Update list
    if (notifications.length === 0) {
        list.innerHTML = `
            <div class="empty-state">
                <span class="material-icons-round">notifications_none</span>
                <p>No notifications</p>
            </div>
        `;
        return;
    }

    list.innerHTML = notifications.map(notif => `
        <div class="notification-item ${notif.type === 'emergency' ? 'emergency' : ''}">
            <div class="notification-header">
                <div class="notification-icon ${notif.type === 'emergency' ? 'emergency' : 'normal'}">
                    <span class="material-icons-round">
                        ${notif.type === 'emergency' ? 'crisis_alert' : 'info'}
                    </span>
                </div>
                <div class="notification-content">
                    <h4 class="notification-title">${notif.title}</h4>
                    <p class="notification-message">${notif.message}</p>
                    <div class="notification-meta">
                        <span class="notification-time">
                            <span class="material-icons-round">schedule</span>
                            ${formatTime(notif.time)}
                        </span>
                    </div>
                </div>
            </div>
        </div>
    `).join('');
}

// Update Alerts Display
function updateAlertsDisplay() {
    const list = document.getElementById('alerts-list');
    const badge = document.getElementById('alerts-badge');

    // Update badge
    if (emergencyAlerts.length > 0) {
        badge.textContent = emergencyAlerts.length;
        badge.classList.remove('hidden');
    } else {
        badge.classList.add('hidden');
    }

    // Update list
    if (emergencyAlerts.length === 0) {
        list.innerHTML = `
            <div class="empty-state">
                <span class="material-icons-round">shield</span>
                <p>No active emergencies</p>
            </div>
        `;
        return;
    }

    list.innerHTML = emergencyAlerts.map(alert => `
        <div class="notification-item emergency" onclick="flyToOfficer('${alert.officer_id}', ${alert.lat}, ${alert.lng})">
            <div class="notification-header">
                <div class="notification-icon emergency">
                    <span class="material-icons-round">crisis_alert</span>
                </div>
                <div class="notification-content">
                    <h4 class="notification-title">🚨 ${alert.officer_name}</h4>
                    <p class="notification-message">${alert.message}</p>
                    <div class="notification-meta">
                        <span class="notification-time">
                            <span class="material-icons-round">schedule</span>
                            ${formatTime(alert.time)}
                        </span>
                        <span>•</span>
                        <span>${alert.emergency_type.replace('_', ' ').toUpperCase()}</span>
                    </div>
                </div>
            </div>
        </div>
    `).join('');
}

// Fly to Officer
function flyToOfficer(officerId, lat, lng) {
    if (lat && lng) {
        map.flyTo([lat, lng], 18, { duration: 1.5 });

        // Select officer if marker exists
        if (officerMarkers[officerId]) {
            setTimeout(() => selectOfficer(officerId), 1500);
        }
    }
}

// Format Time
function formatTime(timestamp) {
    if (!timestamp) return 'Unknown';

    const date = new Date(timestamp);
    const now = new Date();
    const diff = Math.floor((now - date) / 1000); // seconds

    if (diff < 60) return 'Just now';
    if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
    if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;

    return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
}

// Request notification permission on load
if ('Notification' in window && Notification.permission === 'default') {
    Notification.requestPermission();
}
