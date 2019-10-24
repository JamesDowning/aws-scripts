import boto3
from botocore.exceptions import ClientError


try:
    iam = boto3.client('iam')
    user = iam.create_user(UserName='James')
    print("Created user: %s" % user)
except ClientError as e:
    if e.response['Error']['Code'] == 'EntityAlreadyExists':
        print("User already exists")
    else:
        print("Unexpected error: %s" % e)

add = iam.add_user_to_group(
    GroupName='BasicUser',
    UserName=UserName
)

