// TODO: Convert the following into a odoo widget if possible.
(async () => {
    if (window.location.pathname.startsWith("/home")) {
        // Await new Promise((resolve) => setTimeout(resolve, 3000));
        try {
            const res = await $.get("/api/v1/ssp/program/memberships", {limit: 10});
            var progMemTemplate = `<div id="program_applications">
                <table class="table-sm table-hover table-striped">
                    <thead>
                        <tr>
                            <th>Program Name</th>
                            <th>Application ID</th>
                            <th>Status</th>
                            <th>Submitted On</th>
                            <th>Enrollment Date</th>
                            <th>Entitlement</th>
                            <th>Ammount Received</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>`;
            res.forEach((each) => {
                progMemTemplate += `<td>${each.program_name}</td>
                    <td></td>
                    <td>${each.state}</td>
                    <td></td>
                    <td>${each.enrollment_date}</td>
                    <td></td>
                    <td></td>`;
            });
            progMemTemplate += `</tr>
                    </tbody>
                </table>
            </div>`;
            $("div#program_applications").replaceWith(progMemTemplate);
        } catch (err) {
            console.error(err);
            $("div#program_applications").replaceWith("<span>Error Loading programs</span>");
        }
    }
})();
