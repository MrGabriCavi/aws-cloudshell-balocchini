import { DescribeDBInstancesCommand, RDSClient } from '@aws-sdk/client-rds';
import type { AssumeRoleCommandOutput } from '@aws-sdk/client-sts';
import settings from '../utils/settings';

export default class RDS {
  private readonly client: RDSClient;
  private readonly accountId: string;
  private dbInstances: Record<string, string>[];
  constructor(
    credentials: AssumeRoleCommandOutput['Credentials'],
    accountId: string
  ) {
    this.client = new RDSClient({
      region: settings.REGION,
      credentials: {
        accessKeyId: credentials?.AccessKeyId as string,
        secretAccessKey: credentials?.SecretAccessKey as string,
        sessionToken: credentials?.SessionToken as string,
      },
    });
    this.dbInstances = [];
    this.accountId = accountId;
  }

  public async listDBInstances() {
    const list = await this.client.send(new DescribeDBInstancesCommand({}));
    if (!list.DBInstances || !list.DBInstances?.length) {
      return [];
    }
    for (const dbInstance of list.DBInstances) {
      this.dbInstances.push({
        id: dbInstance.DBInstanceIdentifier as string,
        name: dbInstance.DBName as string,
        endpoint: dbInstance.Endpoint?.Address as string,
        port: dbInstance.Endpoint?.Port?.toString() as string,
        status: dbInstance.DBInstanceStatus as string,
        arn: dbInstance.DBInstanceArn as string,
        accountId: this.accountId,
      });
    }
    return this.dbInstances;
  }
}
