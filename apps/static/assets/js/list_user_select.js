document.getElementById('departmentSelect').addEventListener('change', updateAssignedTo);
document.getElementById('locationSelect').addEventListener('change', updateAssignedTo);

function updateAssignedTo() {
    const department = document.getElementById('departmentSelect').value;
    const location = document.getElementById('locationSelect').value;

    if (department && location) {
        fetch(`get_employees/?department=${department}&location=${location}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log('Received data:', data);

                const assignedToSelect = document.getElementById('UserSelect');
                assignedToSelect.innerHTML = ''; // Clear existing options

                if (data && data.length > 0) {
                    data.forEach(employee => {
                        const option = document.createElement('option');
                        option.value = employee.id;
                        option.text = `${employee.user__first_name} ${employee.user__last_name}`;
                        assignedToSelect.add(option);
                    });
                    document.getElementById('UserSection').style.display = 'block';
                } else {
                    console.log('No data received or empty data.');
                    document.getElementById('UserSection').style.display = 'none';
                }
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            });
    } else {
        document.getElementById('UserSection').style.display = 'none';
    }
}