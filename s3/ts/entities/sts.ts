import {
  AssumeRoleCommand,
  STSClient,
  type AssumeRoleCommandInput,
  type AssumeRoleCommandOutput,
} from '@aws-sdk/client-sts';
import { type AwsCredentialIdentityProvider } from '@aws-sdk/types';
import { getAWSProfile } from '../utils';

export default class STS {
  private readonly credentials: AwsCredentialIdentityProvider;
  private readonly client: STSClient;

  constructor(profile: string | null) {
    this.credentials = getAWSProfile(profile);
    this.client = new STSClient({
      region: Bun.env.REGION,
      credentials: this.credentials,
    });
  }

  public async assumeRole(): Promise<AssumeRoleCommandOutput> {
    const params: AssumeRoleCommandInput = {
      RoleArn: Bun.env.ROLE_ARN,
      RoleSessionName: Bun.env.ROLE_SESSION_NAME,
    };

    const assumeRolecommand = new AssumeRoleCommand(params);
    return this.client.send(assumeRolecommand);
  }
}
