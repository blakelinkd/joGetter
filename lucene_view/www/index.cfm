<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Job Postings</title>
    <!-- Add Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-KyZXEAg3QhqLMpG8r+Knujsl7/1L_dstPt3HV5HzF6Gvk/e3s4Wz6iJgD/+ub2oU" crossorigin="anonymous">
</head>
<body>
<a href="/jobs/listJobs.cfm">Jobsasdf</a>
    <div class="container">
        <h1 class="text-center my-4">Job Postings</h1>
        <table class="table table-striped table-hover">
            <thead>
                <tr>
                    <th scope="col">IDsfart</th>
                    <th scope="col">Post Title</th>
                    <th scope="col">Link</th>
                    <th scope="col">Source</th>
                </tr>
            </thead>
            <tbody>
                <cfquery name="getJobs" datasource="job_data">
                    SELECT id, postTitle, link, source
                    FROM jobs
                    ORDER BY createdAt DESC
                    LIMIT 20
                </cfquery>
                <cfoutput query="getJobs">
                    <tr>
                        <td>#id#</td>
                        <td>#postTitle#</td>
                        <td><a href="#link#" target="_blank">#link#</a></td>
                        <td>
                            <cfif findNoCase("indeed.com", link)>
                                Indeed
                            <cfelseif findNoCase("dice.com", link)>
                                Dice
                            <cfelse>
                                Unknown
                            </cfif>
                        </td>
                    </tr>
                </cfoutput>
            </tbody>
        </table>
    </div>
</body>
</html>
