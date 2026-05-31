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

// Function to load employees into the table
async function loadEmployees() {
    const response = await fetch('/employees');
    const employees = await response.json();
    
    const tableBody = document.getElementById('employeeTable');
    tableBody.innerHTML = ''; // Clear current table

    employees.forEach(emp => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td class="p-2 border">${emp.id}</td>
            <td class="p-2 border">${emp.name}</td>
            <td class="p-2 border">${emp.badge_number}</td>
            <td class="p-2 border">
                <button onclick="deleteEmployee(${emp.id})" class="text-red-500 font-bold">Delete</button>
            </td>
        `;
        tableBody.appendChild(row);
    });
}

// Function to delete an employee
async function deleteEmployee(id) {
    if (confirm("Are you sure you want to delete this employee?")) {
        await fetch(`/employees/${id}`, { method: 'DELETE' });
        loadEmployees(); // Reload table after deletion
    }
}

// Initial load
loadEmployees();

async function addEmployee() {
    const name = document.getElementById('newName').value;
    const badge_number = document.getElementById('newBadge').value;
    const nameInput = document.getElementById('newName');
    const badgeInput = document.getElementById('newBadge');

    // 1. Basic validation
    if (!/^[A-Za-z\s]+$/.test(nameInput.value)) {
        return alert("Error: Name must only contain letters.");
    }
    if (isNaN(badgeInput.value) || badgeInput.value.trim() === "") {
        return alert("Error: Badge Number must be a valid number.");
    }

    const payload = { 
        name: nameInput.value, 
        badge_number: badgeInput.value 
    };

    const response = await fetch('/employees', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
    });
    await fetch('/employees', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, badge_number })
    });

    // Clear inputs and refresh table
    document.getElementById('newName').value = '';
    document.getElementById('newBadge').value = '';
    loadEmployees();
}

async function sendPunch(status) {
    const badge_number = document.getElementById('scanBadge').value;
    
    if (!badge_number) {
        alert("Please enter a badge number first!");
        return;
    }

    const response = await fetch('/punch', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            badge_number: badge_number, // Ensure this matches your schemas.py key
            status: status 
        })
    });

    const result = await response.json();
    if (response.ok) {
        alert(`Success: ${status}`);
        showHistory(document.getElementById('scanBadge').value);
    } else {
        // This will now show "Already checked in!" or "You must check-in first!"
        alert("Error: " + (result.detail || "Invalid operation"));
    }

    
}

async function showHistory(badgeNumber) {
    if (!badgeNumber) return alert("Enter a badge number!");

    const response = await fetch(`/history/${badgeNumber}`);
    if (!response.ok) return alert("No history found for this badge.");
    
    const history = await response.json();
    const reportTable = document.getElementById('reportTable');
    
    // Clear and fill
    reportTable.innerHTML = history.map(log => `
        <tr>
            <td class="p-2 border">${new Date(log.timestamp).toLocaleString()}</td>
            <td class="p-2 border font-bold">${log.status.toUpperCase()}</td>
        </tr>
    `).join('');
}