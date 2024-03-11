<cfquery name="getJobs" datasource="lucee">
    SELECT 
        id, 
        logo, 
        postTitle, 
        locality || ', ' || country AS location, 
        hasApplied, 
        compatibility_score, 
        companyName, 
        link,
        skills,
        salaryMax AS salary,
        TO_CHAR(datePosted, 'MM/DD/') || SUBSTRING(TO_CHAR(datePosted, 'YY') FROM 1 FOR 2) AS datePosted
    FROM 
        jobs
    WHERE 
        companyName <> '' AND
        link <> '' AND
        salaryMin IS NOT NULL
    ORDER BY 
        datePosted DESC
    LIMIT 100;
</cfquery>


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Job Postings - Explore Latest Job Opportunities</title>
    <meta name="description" content="Discover and apply to the latest job opportunities across various sectors. Find jobs that match your skills and preferences.">
    <meta name="keywords" content="job postings, career opportunities, apply now, technology jobs, hiring, employment">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://www.yourwebsite.com/job-postings">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <link rel="stylesheet" href="/css/styles.css">
    <style>
        .logo {
            width: 32px;
        }
    </style>
</head>
<body>
<div class="container">
    <header>
        <h1 class="text-center my-4">Explore Latest Job Opportunities</h1>
        <p class="text-center">Search for tech jobs by company name or post title.</p>
    </header>
    <div class="row justify-content-center">
        <div class="col-lg-8">
            <!-- Search jobs form -->
            <form class="mb-3" id="searchForm" role="search">
                <div class="form-row align-items-center">
                    <div class="col-sm-8 my-1">
                        <input type="search" class="form-control" placeholder="Search by company name or post title" aria-label="Search jobs by company name or post title" id="searchInput">
                    </div>
                    <div class="col-sm-4 my-1">
                        <button class="btn btn-outline-success w-100" type="submit">Search</button>
                    </div>
                </div>
            </form>

            <!-- Upload resume form -->
            <form action="uploadResume.cfm" method="post" enctype="multipart/form-data" class="needs-validation" novalidate>
                <div class="form-group">
                    <label for="resume">Select resume to upload:</label>
                    <div class="custom-file mb-3">
                        <input type="file" class="custom-file-input" id="resume" name="resume" required aria-describedby="resumeHelp">
                        <label class="custom-file-label" for="resume">Choose file...</label>
                        <small id="resumeHelp" class="form-text text-muted">Your resume will be uploaded securely and kept private.</small>
                        <div class="invalid-feedback">Please select your resume file.</div>
                    </div>
                </div>
                <button type="submit" class="btn btn-primary" name="submit">Upload Resume</button>
            </form>
        </div>
    </div>

    <section>
        <h2 class="visually-hidden text-center my-5">Job Listings</h2>
        <table class="table table-striped table-hover">
            <thead class="thead-dark">
                <tr>
                    <th scope="col" data-is-numeric="false">Logo</th>
                    <th scope="col" data-is-numeric="false">Company</th>
                    <th scope="col" data-is-numeric="false">Location</th>
                    <th scope="col" data-is-numeric="false">Post Title</th>
                    <th scope="col" data-is-numeric="false">Date</th>
                    <th scope="col" data-is-numeric="true">Salary</th>
                    <th scope="col" data-is-numeric="false">Job Board</th>
                    <th scope="col" data-is-numeric="false">Application Status</th>
                </tr>
            </thead>
            <tbody>
                <cfoutput query="getJobs">
                    <tr>
                        <td><img class="logo" src="#getJobs.logo#" alt="#getJobs.companyName# Logo" onerror="this.style.display='none';"></td>
                        <td>#getJobs.companyName#</td>
                        <td>#getJobs.location#</td>
                        <td>#getJobs.postTitle#</td>
                        <td>#getJobs.datePosted#</td>
                        <td>#getJobs.salary#</td>
                        <td>
                            <cfif FindNoCase("indeed.com", getJobs.link)>
                                <a href="#getJobs.link#" class="btn btn-link" rel="noopener noreferrer">Indeed.com</a>
                            <cfelseif FindNoCase("dice.com", getJobs.link)>
                                <a href="#getJobs.link#" class="btn btn-link" rel="noopener noreferrer">Dice.com</a>
                            <cfelse>
                                <a href="#getJobs.link#" class="btn btn-link" rel="noopener noreferrer">Link</a>
                            </cfif>
                        </td>
                        <td>
                            <button class="btn toggle-applied btn-sm #getJobs.hasApplied eq 1 ? 'btn-success' : 'btn-secondary'#"
                                    data-applied="#getJobs.hasApplied#"
                                    data-id="#getJobs.id#"
                                    aria-pressed="#getJobs.hasApplied eq 1 ? 'true' : 'false'#">
                                #getJobs.hasApplied eq 0 ? 'Not Applied' : 'Applied'#
                            </button>
                        </td>
                    </tr>
                </cfoutput>
            </tbody>
        </table>
    </section>
</div>

<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/popper.js@1.12.9/dist/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
<script>
    function applyToJob(button) {
    var jobId = button.getAttribute('data-id');
    var hasApplied = button.getAttribute('data-applied');

    var link = button.parentElement.previousElementSibling.firstElementChild.href;
    window.open(link, '_blank');

    // Update button appearance based on hasApplied status
    if (hasApplied == 0) {
        // Update button appearance immediately
        button.innerText = 'Applied';
        button.classList.remove('btn-secondary');
        button.classList.add('btn-success');
        button.setAttribute('data-applied', 1);
    }
    
    // Perform AJAX request to update hasApplied to 1
    var xhr = new XMLHttpRequest();
    xhr.open('GET', 'updateJob.cfm?jobId=' + jobId, true);
    xhr.onload = function () {
        if (xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            if (!response.success) {
                alert(response.message);
            }
        } else {
            alert('Failed to update row');
        }
    };
    xhr.send();
}

document.addEventListener('DOMContentLoaded', function() {
    // Define a function to sort rows
    function sortTable(columnIndex, isNumeric, sortOrder) {
        var rows = Array.from(document.querySelector('table tbody').rows);

        rows.sort(function(a, b) {
            var aValue = a.cells[columnIndex].innerText;
            var bValue = b.cells[columnIndex].innerText;

            if (isNumeric) {
                aValue = parseFloat(aValue) || 0;
                bValue = parseFloat(bValue) || 0;
                return sortOrder === 'asc' ? aValue - bValue : bValue - aValue;
            } else {
                return sortOrder === 'asc' ? aValue.localeCompare(bValue) : bValue.localeCompare(aValue);
            }
        });

        rows.forEach(function(row) {
            document.querySelector('table tbody').appendChild(row);
        });
    }

    // Attach click event listeners to table headers
    var headers = document.querySelectorAll('th');
    headers.forEach(function(header, index) {
        header.addEventListener('click', function() {
            var sortOrder = header.getAttribute('data-sort') || 'asc';
            var isNumeric = header.getAttribute('data-is-numeric') === 'true';
            // Toggle sort order for the next click
            sortOrder = sortOrder === 'asc' ? 'desc' : 'asc';
            header.setAttribute('data-sort', sortOrder);
            // Perform the sort
            sortTable(index, isNumeric, sortOrder);
        });
    });
});

    
    <!-- Search functionality -->
    document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('searchForm').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent form submission

        var searchQuery = document.getElementById('searchInput').value.trim().toLowerCase();
        var rows = document.querySelectorAll('tbody tr');

        rows.forEach(function(row) {
            var company = row.querySelector('td:nth-child(2)').textContent.trim().toLowerCase();
            var location = row.querySelector('td:nth-child(3)').textContent.trim().toLowerCase();
            var postTitle = row.querySelector('td:nth-child(4)').textContent.trim().toLowerCase();

            if (company.includes(searchQuery) || location.includes(searchQuery) || postTitle.includes(searchQuery)) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    });
});

<!-- upload control code -->
document.addEventListener("DOMContentLoaded", function(event) {
    // Listen for changes to the file input
    document.getElementById('resume').addEventListener('change', function(e) {
        var fileName = e.target.files[0].name; // Get the selected file name
        // Update the label to show the file name
        document.querySelector('label[for="resume"]').textContent = fileName;
    });

    // Attach a submit event listener to the upload form
    document.querySelector('form[action="uploadResume.cfm"]').addEventListener('submit', function(e) {
        // Prevent the default form submission
        e.preventDefault();

        // Create FormData and append the file
        var formData = new FormData();
        var fileInput = document.getElementById('resume');
        if (fileInput.files.length > 0) {
            var file = fileInput.files[0];
            formData.append('resume', file, file.name);
        }

        // Send the FormData to your ColdFusion page
        fetch('uploadResume.cfm', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.text()) // Assuming the response is text/html
        .then(data => {
            // Handle success
            console.log('Success:', data);
            // Display success message or process returned data
            alert('File uploaded successfully!');
            // Optionally display the response in your page
            document.body.innerHTML += `<div>${data}</div>`; // Customize as needed
        })
        .catch((error) => {
            // Handle errors
            console.error('Error:', error);
            alert('File upload failed.');
        });
    });
});



</script>

</body>
</html>
