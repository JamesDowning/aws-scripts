#!/usr/bin/env python3
'''
Script in order to generate an AWS user,
AWS credentials are presumed to be stored in ~/.aws/credentials
'''

import boto3
from botocore.exceptions import ClientError
from bullet import YesNo, Bullet

prompt = '> '

iam = boto3.client('iam')


def main():
    name, password = create_user_profile()
    access_key_id, secret_access_key = programmatic_access(name)
    added_groups = add_user_to_group(name)
    print_results(name, password, added_groups, access_key_id,
                  secret_access_key)


def create_user_profile():
    print('Insert user name: ')
    user_name = input(prompt)

    user = iam.create_user(UserName=user_name)
    name = user['User']['UserName']

    print('Insert password: ')
    password = input(prompt)

    user = iam.create_login_profile(
        UserName=name, Password=password, PasswordResetRequired=True)

    return name, password


def programmatic_access(user_name):
    cli = YesNo("Would you like to allow programmatic access? ")
    result = cli.launch()
    if result:
        access = iam.create_access_key(UserName=user_name)
        access_key_id = access['AccessKey']['AccessKeyId']
        secret_access_key = access['AccessKey']['SecretAccessKey']
    else:
        access_key_id = None
        secret_access_key = None

    return access_key_id, secret_access_key


def add_user_to_group(user_name):
    groups = iam.list_groups()
    adding_groups = True
    added_groups = []
    group_list = []
    for group in groups.get('Groups'):
        group_names = group.get('GroupName')
        group_list.append(group_names)
    while adding_groups:
        group_cli = Bullet(
            prompt="\nPlease choose a group: ",
            choices=group_list,
            indent=0,
            align=5,
            margin=2,
            shift=0,
            bullet="",
            pad_right=5)
        group_result = group_cli.launch()
        added_groups.append(group_result)
        user_group = iam.add_user_to_group(
            GroupName=group_result, UserName=user_name)
        group_list.remove(group_result)
        cli = YesNo("Would you like to add the user to another group? ")
        result = cli.launch()
        if not result:
            adding_groups = False

    return added_groups


def print_results(user_name, password, added_groups, access_key_id,
                  secret_access_key):
    print(f'Created user: {user_name}')
    print(f'Created password: {password}')
    print(f'Access Key ID: {access_key_id}')
    print(f'Secret Access Key: {secret_access_key}')
    print(f'Added to groups: {added_groups}')


if __name__ == '__main__':
    main()

# Add try and catches / error catching
