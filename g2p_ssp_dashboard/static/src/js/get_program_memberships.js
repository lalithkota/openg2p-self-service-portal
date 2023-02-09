/** @odoo-module **/
import Widget from "web.Widget";

// TODO: Modify the following into an OWL Component if possible
// TODO: Modify the following to use the widget directly in dashboard view
export const ProgramApplicationsWidget = Widget.extend({
    retrieveProgramApplications: async function () {
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
            return progMemTemplate;
        } catch (err) {
            console.error(err);
            return `<span>Error Loading programs</span>`;
        }
    },
});

(async () => {
    if ($("#program_applications").length) {
        var res = await new ProgramApplicationsWidget().retrieveProgramApplications();
        $("#program_applications").replaceWith(res);
    }
})();
