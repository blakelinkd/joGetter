<table class="table table-striped table-hover">
    <thead>
        <tr>
            <th scope="col">Company</th>
            <th scope="col">Job Title</th>
            <th scope="col">Apply Link</th>
            <th scope="col">Applied?</th>
        </tr>
    </thead>
    <tbody>
        <cfoutput query="attributes.data">
            <tr>
                <th scope="row">#attributes.data.companyName#</th>
                <td style="width: auto">#attributes.data.postTitle#</td>
                <td>
                    <cfif FindNoCase("indeed.com", attributes.data.link)>
                        <a href="#attributes.data.link#" class="btn btn-link">Indeed.com</a>
                    <cfelseif FindNoCase("dice.com", attributes.data.link)>
                        <a href="#attributes.data.link#" class="btn btn-link">Dice.com</a>
                    <cfelse>
                        <a href="#attributes.data.link#" class="btn btn-link">Link</a>
                    </cfif>
                </td>
                <td>
                    <button class="btn toggle-applied #attributes.data.hasApplied eq 0 ? 'btn-secondary' : 'btn-success'# btn-sm" 
                        data-applied="#attributes.data.hasApplied#" 
                        data-id="#attributes.data.id#" 
                        onclick="toggleApplicationStatus(this);" 
                        style="width: 100px;">
                        #attributes.data.hasApplied eq 0 ? 'Not Applied' : 'Applied'#
                    </button>
                </td>
            </tr>
        </cfoutput>
    </tbody>
</table>
