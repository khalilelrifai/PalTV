
    // Add JavaScript code to track the uploading progress
    const form = document.getElementById('upload-form');
    const uploadStatus = document.getElementById('upload-status');

    let uploadInProgress = false; // Keep track of whether an upload is in progress

    form.addEventListener('submit', (event) => {
        event.preventDefault();

        if (uploadInProgress) {
            // If an upload is already in progress, prevent the form submission
            return;
        }

        const formData = new FormData(form);

        const request = new XMLHttpRequest();
        request.open('POST', '/ftp/upload/'); // Replace with your actual upload endpoint

        request.upload.addEventListener('progress', (event) => {
            if (event.lengthComputable) {
                const progress = Math.round((event.loaded / event.total) * 100);
                uploadStatus.textContent = `Uploading: ${progress}%`;
            }
        });

        request.onreadystatechange = function() {
            if (request.readyState === XMLHttpRequest.DONE) {
                if (request.status === 200) {
                    uploadStatus.textContent = 'Upload complete';
                    window.removeEventListener('beforeunload', preventExitDuringUpload);
                    form.reset();
                    // Redirect to the list page
                    window.location.href = '{% url 'ftp:my_list' %}'; // Replace with the URL of your list page
                } else {
                    uploadStatus.textContent = 'Upload failed';
                }

                uploadInProgress = false; // Reset the flag when the upload is complete
                window.removeEventListener('beforeunload', preventExitDuringUpload); // Remove the event listener
            }
        };

        // Set the flag to indicate that an upload is in progress
        uploadInProgress = true;
        // Add event listener to prevent the user from leaving the page during upload
        window.addEventListener('beforeunload', preventExitDuringUpload);

        request.send(formData);
    });

    function preventExitDuringUpload(event) {
        event.preventDefault();
        event.returnValue = ''; // This is necessary for older browsers
    }
