import argparse
from balocchini.session.session import create_session
from balocchini.s3.common import S3Common

def main():
    parser = argparse.ArgumentParser(description='Elenca tutti i bucket S3.')
    parser.add_argument('--profile', type=str, help='Profilo AWS da utilizzare')
    args = parser.parse_args()

    session = create_session(args.profile)
    s3_common = S3Common(session)
    buckets = s3_common.list_buckets()

    for bucket in buckets:
        print(bucket)

if __name__ == "__main__":
    main()