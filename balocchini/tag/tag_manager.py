import argparse
import sys
import os
from prettytable import PrettyTable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Helpers.awstools import AWSTools

def add_tag(client, arn, key, value):
    try:
        client.tag_resources(ResourceARNList=[arn], Tags={key: value})
        print("Tag added successfully.")
    except Exception as e:
        print(f"Error adding tag: {e}")

def remove_tag(client, arn, key):
    try:
        client.untag_resources(ResourceARNList=[arn], TagKeys=[key])
        print("Tag removed successfully.")
    except Exception as e:
        print(f"Error removing tag: {e}")

def list_resource_tags(client, arn):
    try:
        response = client.get_resources(ResourceARNList=[arn])
        resource_tag_mappings = response.get('ResourceTagMappingList', [])
        if not resource_tag_mappings:
            print(f"Resource {arn} not found.")
            return False
        tags = resource_tag_mappings[0].get('Tags', [])
        if tags:
            table = PrettyTable()
            table.field_names = ["Key", "Value"]
            for tag in tags:
                table.add_row([tag['Key'], tag['Value']])
            print(f"Tags for {arn}:")
            print(table)
        else:
            print(f"Resource {arn} exists but has no tags.")
        return True
    except Exception as e:
        print(f"Error retrieving tags for resource {arn}: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="List and manage AWS resource tags given an ARN.")
    parser.add_argument("arn", help="The ARN of the AWS resource to list and manage tags for")
    parser.add_argument("--profile", help="AWS profile to use", default=None)
    parser.add_argument("--role-arn", help="ARN of the role to assume", default=None)
    parser.add_argument("--region", help="AWS region to use", default="us-west-1")
    args = parser.parse_args()

    client = AWSTools.initialize_client('resourcegroupstaggingapi', profile=args.profile, region=args.region, role_arn=args.role_arn)

    resource_found = list_resource_tags(client, args.arn)
    if resource_found:
        while True:
            action = input("Do you want to add, remove tags, or exit? (a/r/q): ").lower()
            if action == "a":
                key = input("Enter the tag key: ")
                value = input("Enter the tag value: ")
                add_tag(client, args.arn, key, value)
                list_resource_tags(client, args.arn)  # Show updated tags
            elif action == "r":
                key = input("Enter the tag key to remove: ")
                remove_tag(client, args.arn, key)
                list_resource_tags(client, args.arn)  # Show updated tags
            elif action == "q":
                print(f"Bye.")
                break
            else:
                print("Invalid action. Please choose 'add'(a), 'remove'(r), or 'exit'(q).")

if __name__ == "__main__":
    main()