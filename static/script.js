async function loadLogs(badgeNumber) {
    try {
        const response = await fetch(`/logs/${badgeNumber}`);
        const data = await response.json();
        
        const logsDiv = document.getElementById('logs');
        if (data.error) {
            logsDiv.innerHTML = `<p class="text-red-500">${data.error}</p>`;
        } else {
            logsDiv.innerHTML = `
                <h2 class="text-xl font-semibold mb-2">Employee: ${data.employee}</h2>
                <ul class="list-disc pl-5">
                    ${data.history.map(log => `<li>${log.status} at ${log.timestamp}</li>`).join('')}
                </ul>
            `;
        }
    } catch (err) {
        console.error("Error fetching logs:", err);
    }
}

// Initial load for demo purposes (using the badge number from your seed data)
loadLogs('12345');