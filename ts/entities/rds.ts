import {
  CreateDBSnapshotCommand,
  DescribeDBInstancesCommand,
  RDSClient,
} from '@aws-sdk/client-rds';
import type { AssumeRoleCommandOutput } from '@aws-sdk/client-sts';

export default class RDS {
  private readonly client: RDSClient;
  private dbInstances: Record<string, string>[];
  constructor(
    credentials: AssumeRoleCommandOutput['Credentials'],
    region: string
  ) {
    this.client = new RDSClient({
      region,
      credentials: {
        accessKeyId: credentials?.AccessKeyId as string,
        secretAccessKey: credentials?.SecretAccessKey as string,
        sessionToken: credentials?.SessionToken as string,
      },
    });
    this.dbInstances = [];
  }

  public async listInstances() {
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
      });
    }
    return this.dbInstances;
  }

  public async createSnapshot(instanceId: string, snapshotName: string) {
    // Create a snapshot of the RDS instance
    return await this.client.send(
      new CreateDBSnapshotCommand({
        DBInstanceIdentifier: instanceId,
        DBSnapshotIdentifier: snapshotName,
      })
    );
  }
}
