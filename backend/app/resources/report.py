import json

from ..db import models
from ..flask_restful_extensions import Resource


class ReportResource(Resource):
    endpoint_name = 'report'

    def post(self):
        photo_id = self.request_json['photo_id']
        user_id = self.request_json['user_id']
        reason = self.request_json.get('reason')
        verdict = self.request_json.get('verdict')

        if user_id == 'system':
            # TODO: give penalty, dont pass our cheating system
            pass

        report = models.Report.query.filter_by(
            photo_id=models.Photo.query.filter_by(app_id=photo_id).first().app_id,
        ).first()
        if report is None:
            report = models.Report(
                photo_id=models.Photo.query.filter_by(app_id=photo_id).first().app_id,
                reason=reason,
                verdicts=json.dumps({user_id: True}),
            )
        else:
            d = json.loads(report.verdicts)
            d[user_id] = verdict
            report.verdicts = json.dumps(d)
        report.save(commit=True)
        # TODO: trigger actions if all verdicts present
        # if more than 50% is positive give suspect penalty according to rules
        # cheating. Manage penalty points.
        return report.to_dict()
