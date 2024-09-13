document.addEventListener('DOMContentLoaded', function() {
    // Add event listeners for form submissions
    document.getElementById('goalForm')?.addEventListener('submit', function(event) {
        event.preventDefault();
        fetch('/add_goal', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                email: document.getElementById('goalEmail').value,
                goals: document.getElementById('goals').value
            })
        }).then(response => response.json()).then(data => alert(data.message));
    });

    document.getElementById('appointmentForm')?.addEventListener('submit', function(event) {
        event.preventDefault();
        fetch('/schedule_appointment', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                email: document.getElementById('appointmentEmail').value,
                date: document.getElementById('appointmentDate').value,
                description: document.getElementById('description').value
            })
        }).then(response => response.json()).then(data => alert(data.message));
    });

    document.getElementById('alertForm')?.addEventListener('submit', function(event) {
        event.preventDefault();
        fetch('/emergency_alert', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                email: document.getElementById('alertEmail').value,
                alert_message: document.getElementById('alertMessage').value
            })
        }).then(response => response.json()).then(data => alert(data.message));
    });

    document.getElementById('activityForm')?.addEventListener('submit', function(event) {
        event.preventDefault();
        fetch('/add_activity', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                email: document.getElementById('activityEmail').value,
                date: document.getElementById('activityDate').value,
                type: document.getElementById('activityType').value,
                value: document.getElementById('activityValue').value
            })
        }).then(response => response.json()).then(data => alert(data.message));
    });

    document.getElementById('scoreForm')?.addEventListener('submit', function(event) {
        event.preventDefault();
        fetch('/calculate_health_score', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                email: document.getElementById('scoreEmail').value
            })
        }).then(response => response.json()).then(data => alert('Health Score: ' + data.health_score));
    });

    document.getElementById('tipsForm')?.addEventListener('submit', function(event) {
        event.preventDefault();
        fetch('/predict_health_tips', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                features: document.getElementById('features').value.split(',').map(Number)
            })
        }).then(response => response.json()).then(data => alert('Predicted Tip: ' + data.predicted_tip));
    });

    document.getElementById('locationForm')?.addEventListener('submit', function(event) {
        event.preventDefault();
        fetch('/share_location', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                email: document.getElementById('locationEmail').value,
                latitude: parseFloat(document.getElementById('latitude').value),
                longitude: parseFloat(document.getElementById('longitude').value)
            })
        }).then(response => response.json()).then(data => alert(data.message));
    });

    document.getElementById('panicForm')?.addEventListener('submit', function(event) {
        event.preventDefault();
        fetch('/panic_button', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                email: document.getElementById('panicEmail').value
            })
        }).then(response => response.json()).then(data => alert(data.message));
    });
});