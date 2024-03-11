<cfif isDefined("form.resume")>
    <cffile action="upload" filefield="form.resume" destination="/tmp" nameconflict="overwrite" result="uploadResult">
    <cfhttp method="post" url="http://flaskapp:5000/upload-resume" multipart="yes">
        <cfhttpparam type="file" file="#uploadResult.serverDirectory#\#uploadResult.serverFile#" name="resume">
    </cfhttp>
    
    <!--- Display the returned text to the user --->
    <cfoutput>#cfhttp.filecontent#</cfoutput>
</cfif>
