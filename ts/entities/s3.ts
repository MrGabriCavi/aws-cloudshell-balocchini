import settings from '../utils/settings';
import {
  GetBucketAclCommand,
  GetBucketLocationCommand,
  ListBucketsCommand,
  S3Client,
  type GetBucketAclCommandOutput,
  type GetBucketLocationCommandOutput,
} from '@aws-sdk/client-s3';
import type { AssumeRoleCommandOutput } from '@aws-sdk/client-sts';

export default class S3 {
  private readonly client: S3Client;
  private buckets: string[];
  constructor(
    credentials: AssumeRoleCommandOutput['Credentials'],
    region: string
  ) {
    this.client = new S3Client({
      region,
      credentials: {
        accessKeyId: credentials?.AccessKeyId as string,
        secretAccessKey: credentials?.SecretAccessKey as string,
        sessionToken: credentials?.SessionToken as string,
      },
    });
    this.buckets = [];
  }

  public async listBuckets() {
    const output = await this.client.send(new ListBucketsCommand({}));
    console.log(output);

    this.buckets.push(
      ...(output.Buckets?.map((bucket) => bucket.Name) as string[])
    );

    return this.buckets;
  }

  private async getBucketsAction<T>(
    buckets: string[],
    action: (bucket: string) => Promise<T | null>
  ) {
    if (!buckets.length) return null;

    if (buckets.length === 1) {
      return action(buckets[0]);
    }

    for (const bucket of buckets) {
      try {
        return action(bucket);
      } catch (e: any) {
        console.error(e.message);
      }
    }

    return null;
  }

  public async getBucketLocation() {
    return this.getBucketsAction<GetBucketLocationCommandOutput>(
      this.buckets,
      (Bucket) => this.client.send(new GetBucketLocationCommand({ Bucket }))
    );
  }

  public async getBucketAcl() {
    return this.getBucketsAction<GetBucketAclCommandOutput>(
      this.buckets,
      (Bucket) => this.client.send(new GetBucketAclCommand({ Bucket }))
    );
  }
}
