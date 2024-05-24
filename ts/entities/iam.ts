import {
  CreateRoleCommand,
  IAMClient,
  ListRolesCommand,
} from '@aws-sdk/client-iam';
import type { AssumeRoleCommandOutput } from '@aws-sdk/client-sts';

class IAM {
  private readonly client: IAMClient;
  private roles: Record<string, string>[];
  constructor(
    credentials: AssumeRoleCommandOutput['Credentials'],
    region: string
  ) {
    this.client = new IAMClient({
      region,
      credentials: {
        accessKeyId: credentials?.AccessKeyId as string,
        secretAccessKey: credentials?.SecretAccessKey as string,
      },
    });
    this.roles = [];
  }

  public async listRoles(): Promise<Record<string, string>[]> {
    const list = await this.client.send(new ListRolesCommand({}));
    if (!list.Roles || !list.Roles?.length) {
      return [];
    }
    for (const role of list.Roles) {
      this.roles.push({
        id: role.RoleId as string,
        name: role.RoleName as string,
        arn: role.Arn as string,
        created: role.CreateDate?.toISOString() as string,
        path: role.Path as string,
      });
    }
    return this.roles;
  }

  public async createRole(roleName: string, policyDocument: string) {
    // Create a new IAM role
    return await this.client.send(
      new CreateRoleCommand({
        RoleName: roleName,
        AssumeRolePolicyDocument: policyDocument,
      })
    );
  }
}
