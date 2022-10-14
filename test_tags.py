#
# program to test parsing --tags in a simpler format   --tage key=value key=value
#
# Es. --tags role=admin app=siebel stage=dev user="Matteo" date="14-10-2022"
# becomes: [{'key': 'role', 'value': 'admin'}, {'key': 'app', 'value': 'siebel'}, {'key': 'stage', 'value': 'dev'}, {'key': 'user', 'value': 'Matteo'}, {'key': 'date', 'value': '14-10-2022'}]
#

import argparse


class parsetags(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, dict())
        tgs = None
        for value in values:
            key, value = value.split('=')
            getattr(namespace, self.dest)[key] = value
            tgs = [{"key": k, "value": v} for (k, v) in namespace.tags.items()]
        namespace.tags = tgs


parser = argparse.ArgumentParser()
# noinspection PyTypeChecker
parser.add_argument('-t', '--tags', nargs='*', action=parsetags)
args = parser.parse_args()
tg_list = args.tags
print(tg_list)
