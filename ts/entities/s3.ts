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

  public async listInstances() {
    const output = await this.client.send(new ListBucketsCommand({}));
    this.buckets.push(
      ...(output.Buckets?.map((bucket) => bucket.Name) as string[])
    );
    return this.buckets;
  }

  private async getBucketsAction<T>(
    _bucket: string,
    action: (bucket: string) => Promise<T | undefined>
  ): Promise<T | undefined> {
    if (!this.buckets.length) return undefined;

    for (const bucket of this.buckets) {
      try {
        if (bucket === _bucket) {
          return action(bucket);
        }
      } catch (e: any) {
        console.error(e.message);
      }
    }
    return undefined;
  }

  public async getBucketLocation(bucket: string) {
    return this.getBucketsAction<GetBucketLocationCommandOutput>(
      bucket,
      (Bucket) => this.client.send(new GetBucketLocationCommand({ Bucket }))
    );
  }

  public async getBucketAcl(bucket: string) {
    return this.getBucketsAction<GetBucketAclCommandOutput>(bucket, (Bucket) =>
      this.client.send(new GetBucketAclCommand({ Bucket }))
    );
  }
}
