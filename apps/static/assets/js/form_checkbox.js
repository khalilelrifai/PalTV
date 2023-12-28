document.getElementById('departmentSelect').addEventListener('change', updateAssignedTo);
document.getElementById('locationSelect').addEventListener('change', updateAssignedTo);

function updateAssignedTo() {
    const department = document.getElementById('departmentSelect').value;
    const location = document.getElementById('locationSelect').value; // Add this line

    if (department  && location) { // Modify this condition to include location
        fetch(`get_employees/?department=${department}&location=${location}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log('Received data:', data); // Log the received data

                const assignedToCheckbox = document.getElementById('assignedToCheckbox');
                assignedToCheckbox.innerHTML = ''; // Clear existing checkboxes

                if (data && data.length > 0) {
                        data.forEach(employee => {
                            const checkboxDiv = document.createElement('div'); // Create a div for each checkbox

                            const checkbox = document.createElement('input');
                            checkbox.type = 'checkbox';
                            checkbox.name = 'assigned_to';
                            checkbox.value = employee.id;
                            checkbox.classList.add('form-check-input');
                            checkboxDiv.required = true;
                             // Add class to the checkbox
                            
                            const label = document.createElement('label');
                            label.appendChild(checkbox);
                            label.appendChild(document.createTextNode(' '+ employee.user__first_name + ' ' + employee.user__last_name));
                            
                            checkboxDiv.appendChild(label); // Append label to the div
                            assignedToCheckbox.appendChild(checkboxDiv); // Append div to the main container
                        });
                        document.getElementById('assignedToSection').style.display = 'block';
                    }
else {
                    console.log('No data received or empty data.'); // Log if no or empty data received
                    document.getElementById('assignedToSection').style.display = 'none';
                }
            })
            .catch(error => {
                console.error('There was a problem with the fetch operation:', error);
            });
    } else {
        document.getElementById('assignedToSection').style.display = 'none';
    }
}