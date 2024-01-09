import csv
import json

from django.core.management.base import BaseCommand

from permissions_auditor.core import get_views


class Command(BaseCommand):
    help = 'Dumps all detected view permissions to the specified output format.'

    def add_arguments(self, parser):
        parser.add_argument(
            "--format",
            default="json",
            help="Specifies the output serialization format for permissions. Options: csv, json",
        )
        parser.add_argument(
            "-o", "--output", help="Specifies file to which the output is written."
        )

    def handle(self, *args, **options):
        format = options["format"]
        output = options["output"]
        views = get_views()

        if format == 'csv':
            if output:
                with open(output, 'w', newline='') as file:
                    writer = csv.writer(file, dialect='excel')
                    self._write_csv(views, writer)
            else:
                writer = csv.writer(self.stdout)
                self._write_csv(views, writer)

        elif format == 'json':
            data = [v._asdict() for v in views]

            if output:
                with open(output, 'w') as file:
                    json.dump(data, file, indent=4)
            else:
                self.stdout.write(json.dumps(data))
        else:
            raise NotImplementedError('Output format `{}` is not implemented.'.format(format))

    def _write_csv(self, views, writer):
        # Header
        writer.writerow(['module', 'name', 'url', 'permissions', 'login_required', 'docstring'])

        for view in views:
            writer.writerow(view)
