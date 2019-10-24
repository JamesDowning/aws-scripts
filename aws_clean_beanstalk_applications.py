#!/usr/bin/env python3
'''
Script to delete beanstalk application versions
older than given number of days.
AWS credentials are presumed to be stored in ~/.aws/credentials
'''
# TODO: Add success or fail for deletion.
# CHECK VERSION DEPLOYED TO == NOTHING

import boto3
import datetime
import sys
from botocore.exceptions import ClientError
from bullet import YesNo, Bullet

prompt = '> '

eb = boto3.client('elasticbeanstalk')


def main():
    apps = describe_application_versions()
    apps_to_delete = parse_application_list(*apps)
    while not apps_to_delete:
        print('No application versions found older than given days. \n')
        main()
    delete_application_versions(apps_to_delete)


def describe_application_versions():
    application_versions = eb.describe_application_versions()
    # Extract Application versions list.
    app_versions = application_versions.get('ApplicationVersions')
    return app_versions


# Returns list of app versions older than specified date
def parse_application_list(*args):
    target_apps = []
    try:
        num_days = int(
            input("Delete application versions older than:   (days) "))
    except ValueError:
        print("Please enter a valid number of days.")
        main()
    for app in args:
        date_created = app.get('DateCreated')
        if date_created.replace(tzinfo=None) < datetime.datetime.now(
        ) - datetime.timedelta(days=int(num_days)):
            target_apps.append(app)

    return target_apps


def delete_application_versions(target_apps):
    num_apps = len(target_apps)
    keys = ['ApplicationName', 'VersionLabel']
    cli = YesNo(
        f"{num_apps} application versions will be deleted, would you like to proceed? "
    )
    result = cli.launch()
    if result:
        print("deleting apps...")
        for r in target_apps:
            p = [r.get(key) for key in keys]
            delete_app = eb.delete_application_version(
                ApplicationName=p[0],
                VersionLabel=p[1],
                DeleteSourceBundle=True)
            print(delete_app)
        print("Finished request")
    else:
        quit()
    return None


if __name__ == '__main__':
    main()
