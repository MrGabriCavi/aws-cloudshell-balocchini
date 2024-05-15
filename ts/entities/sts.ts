import {
  AssumeRoleCommand,
  GetCallerIdentityCommand,
  STSClient,
  type AssumeRoleCommandOutput,
} from '@aws-sdk/client-sts';
import { type AwsCredentialIdentityProvider } from '@aws-sdk/types';
import { getAWSProfile } from '../utils';

export default class STS {
  private readonly credentials: AwsCredentialIdentityProvider;
  private readonly client: STSClient;

  constructor(profile: string, region: string) {
    this.credentials = getAWSProfile(profile);
    this.client = new STSClient({
      region,
      credentials: this.credentials,
    });
  }

  public async getAccountId(): Promise<string> {
    const identity = await this.client.send(new GetCallerIdentityCommand({}));
    if (!identity.Account) throw new Error('Account ID not found');
    return identity.Account;
  }

  public async assumeRole(
    RoleArn: string,
    RoleSessionName: string
  ): Promise<AssumeRoleCommandOutput> {
    const assumeRolecommand = new AssumeRoleCommand({
      RoleArn,
      RoleSessionName,
    });
    return this.client.send(assumeRolecommand);
  }
}
