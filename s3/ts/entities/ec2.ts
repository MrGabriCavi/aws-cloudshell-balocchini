import { DescribeInstancesCommand, EC2Client } from '@aws-sdk/client-ec2';
import { type AssumeRoleCommandOutput } from '@aws-sdk/client-sts';
import settings from '../utils/settings';

export default class EC2 {
  private readonly client: EC2Client;
  private readonly accountId: string;
  private ec2Instances: Record<string, string>[];
  constructor(
    credentials: AssumeRoleCommandOutput['Credentials'],
    accountId: string
  ) {
    this.client = new EC2Client({
      region: settings.REGION,
      credentials: {
        accessKeyId: credentials?.AccessKeyId as string,
        secretAccessKey: credentials?.SecretAccessKey as string,
        sessionToken: credentials?.SessionToken as string,
      },
    });
    this.ec2Instances = [];
    this.accountId = accountId;
  }

  public async listInstances() {
    const list = await this.client.send(new DescribeInstancesCommand({}));
    if (!list.Reservations || !list.Reservations?.length) {
      return [];
    }
    for (const reservation of list.Reservations) {
      if (!reservation.Instances || !reservation.Instances?.length) {
        continue;
      }
      for (const instance of reservation.Instances) {
        this.ec2Instances.push({
          id: instance.InstanceId as string,
          ip: instance.PublicIpAddress as string,
          name: instance.KeyName as string,
          accountId: this.accountId,
        });
      }
    }
    return this.ec2Instances;
  }
}
