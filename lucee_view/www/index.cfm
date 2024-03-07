<cfquery name="getJobs" datasource="job_data">
    SELECT * FROM jobs
WHERE companyName <> ''
AND link <> ''
ORDER BY id DESC
LIMIT 100;

</cfquery>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Job Postings</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
</head>
<body>

<div class="container mx-auto my-auto">
    <h1 class="text-center my-4">Job Postings</h1>
    <table class="table table-striped table-hover">
        <thead class="thead-dark">
            <tr>
                <th scope="col" data-column="0">Company</th>
                <th scope="col" data-column="1">Post Title</th>
                <th scope="col" data-column="2">Compatibility</th>
                <th scope="col" data-column="3">Salary</th>
                <th scope="col" data-column="4">Job Board</th>
                <th scope="col" data-column="5">hasApplied</th>
            </tr>
        </thead>
        <tbody>
            <cfoutput query="getJobs">
                <tr>
                    <td>#getJobs.companyName#</td>
                    <td>#getJobs.postTitle#</td>
                    <td>#NumberFormat(getJobs.compatibility_score, '9.99')#</td>
                    <td>#getJobs.salary#</td>

                    <td>
                        <cfif FindNoCase("indeed.com", getJobs.link)>
                            <a href="#getJobs.link#" class="btn btn-link">Indeed.com</a>
                        <cfelseif FindNoCase("dice.com", getJobs.link)>
                            <a href="#getJobs.link#" class="btn btn-link">Dice.com</a>
                        <cfelse>
                            <a href="#getJobs.link#" class="btn btn-link">Link</a>
                        </cfif>
                    </td>
                    <td>
                     <button class="btn toggle-applied btn-sm #getJobs.hasApplied eq 1 ? 'btn-success' : 'btn-secondary'#" 
                        data-applied="#getJobs.hasApplied#" 
                        data-id="#getJobs.id#" 
                        onclick="applyToJob(this);" 
                        style="width: 100px;">
                        #getJobs.hasApplied eq 0 ? 'Not Applied' : 'Applied'#
                    </button>

                </td>
                    
                </tr>
            </cfoutput>
        </tbody>
    </table>
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
        var table = document.querySelector('.table');
        var headers = table.querySelectorAll('th');

        // Add click event listeners to the table headers
        headers.forEach(function(header) {
            header.addEventListener('click', function() {
                var column = header.dataset.column;
                var sortOrder = header.dataset.sort || 'asc'; // Default sort order is ascending

                // Toggle sort order
                sortOrder = sortOrder === 'asc' ? 'desc' : 'asc';
                header.dataset.sort = sortOrder;

                // Get all rows
                var rows = table.querySelectorAll('tbody tr');

                // Convert NodeList to array for sorting
                rows = Array.prototype.slice.call(rows);

                // Sort rows based on column value
                rows.sort(function(a, b) {
                    var aValue = a.querySelector('td:nth-child(' + (parseInt(column) + 1) + ')').innerText;
                    var bValue = b.querySelector('td:nth-child(' + (parseInt(column) + 1) + ')').innerText;

                    // Convert values to numeric for numerical sorting
                    if (!isNaN(aValue) && !isNaN(bValue)) {
                        return sortOrder === 'asc' ? aValue - bValue : bValue - aValue;
                    } else {
                        return sortOrder === 'asc' ? aValue.localeCompare(bValue) : bValue.localeCompare(aValue);
                    }
                });

                // Re-append sorted rows to the table body
                var tbody = table.querySelector('tbody');
                rows.forEach(function(row) {
                    tbody.appendChild(row);
                });
            });
        });
    });

</script>


</body>
</html>
