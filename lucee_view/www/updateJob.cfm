<cfparam name="URL.jobId" default="">
<cfset jobId = URL.jobId>

<!--- Perform the update operation --->
<cfquery name="updateJob" datasource="job_data">
    UPDATE jobs
    SET hasApplied = 1
    WHERE id = <cfqueryparam value="#jobId#" cfsqltype="CF_SQL_INTEGER">
</cfquery>

