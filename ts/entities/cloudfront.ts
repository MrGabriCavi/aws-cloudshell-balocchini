import type { AssumeRoleCommandOutput } from '@aws-sdk/client-sts';
import {
  CloudFrontClient,
  ListDistributionsCommand,
  CreateInvalidationCommand,
} from '@aws-sdk/client-cloudfront';

class Cloudfront {
  private readonly client: CloudFrontClient;
  constructor(
    credentials: AssumeRoleCommandOutput['Credentials'],
    region: string
  ) {
    this.client = new CloudFrontClient({
      region,
      credentials: {
        accessKeyId: credentials?.AccessKeyId as string,
        secretAccessKey: credentials?.SecretAccessKey as string,
      },
    });
  }

  public async listDistributions() {
    // List all CloudFront distributions
    return await this.client.send(new ListDistributionsCommand({}));
  }

  public async invalidateDistribution(
    distributionId: string,
    paths: string[] = []
  ) {
    // Invalidate the CloudFront distribution
    if (!paths.length) {
      paths.push('/*');
    }
    return await this.client.send(
      new CreateInvalidationCommand({
        DistributionId: distributionId,
        InvalidationBatch: {
          CallerReference: `API-${Date.now().toString()}`,
          Paths: {
            Quantity: paths.length,
            Items: paths,
          },
        },
      })
    );
  }
}

export default Cloudfront;
