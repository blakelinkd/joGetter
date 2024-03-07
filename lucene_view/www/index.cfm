<cfquery name="getJobs" datasource="job_data">
    SELECT * FROM jobs
    ORDER BY id DESC
    LIMIT 500
</cfquery>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Job Postings</title>
    <!-- Add Bootstrap CSS -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
</head>
<body>

<div class="container">
    <h1 class="text-center my-4">Job Postings</h1>
    <table class="table table-striped table-hover">
        <thead class="thead-dark">
            <tr>
                <th scope="col">Company</th>
                <th scope="col">Post Title</th>
                <th scope="col">Location</th>
                <th scope="col">Salary</th>
                <th scope="col">Job Board</th>
                <th scope="col">hasApplied</th>
                <!-- Add more table headers as needed -->
            </tr>
        </thead>
        <tbody>
            <cfoutput query="getJobs">
                <tr>
                    <td>#getJobs.companyName#</td>
                    <td>#getJobs.postTitle#</td>
                    <td>#getJobs.location#</td>
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
                    <button class="btn toggle-applied #getJobs.hasApplied eq 0 ? 'btn-secondary' : 'btn-success'# btn-sm" 
                        data-applied="#getJobs.hasApplied#" 
                        data-id="#getJobs.id#" 
                        onclick="toggleApplicationStatus(this);" 
                        style="width: 100px;">
                        #getJobs.hasApplied eq 0 ? 'Not Applied' : 'Applied'#
                    </button>
                </td>
                    
                    <!-- Add more table cells as needed -->
                </tr>
            </cfoutput>
        </tbody>
    </table>
</div>
<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/popper.js@1.12.9/dist/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
</body>
</html>
