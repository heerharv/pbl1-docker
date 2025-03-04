const API_URL = "http://localhost:5000/employees";

function addEmployee() {
    let name = document.getElementById("name").value;
    let email = document.getElementById("email").value;
    let department = document.getElementById("department").value;

    fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, department })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        fetchEmployees();
    })
    .catch(error => console.error("Error:", error));
}

function fetchEmployees() {
    fetch(API_URL)
        .then(res => res.json())
        .then(data => {
            let table = document.getElementById("employeeTable");
            table.innerHTML = `<tr><th>Name</th><th>Email</th><th>Department</th><th>Actions</th></tr>`;
            data.forEach(emp => {
                let row = table.insertRow();
                row.innerHTML = `
                    <td>${emp.name}</td>
                    <td>${emp.email}</td>
                    <td>${emp.department}</td>
                    <td>
                        <button onclick="deleteEmployee(${emp.id})">Delete</button>
                    </td>
                `;
            });
        });
}

function deleteEmployee(id) {
    fetch(`${API_URL}/${id}`, { method: "DELETE" })
    .then(() => fetchEmployees())
    .catch(error => console.error("Error:", error));
}

fetchEmployees();
