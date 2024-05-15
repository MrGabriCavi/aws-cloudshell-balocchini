import fs from 'fs/promises';
import { fromIni } from '@aws-sdk/credential-providers';

export async function writeFile<T>(
  data: T,
  filename: string,
  options: { ext: string } = {
    ext: 'json',
  }
): Promise<void> {
  try {
    const fname = `${new Date().toISOString()}-${filename}.${options.ext}`;
    let file: Buffer | undefined;
    try {
      file = await fs.readFile(`./output/${fname}`);
    } catch (e) {
      console.error('File not found');
    }

    if (file) {
      await fs.unlink(`./output/${fname}`);
    }
    if (options.ext === 'csv') {
      await fs.writeFile(`./output/${fname}`, data as string, {
        flag: 'a',
      });
    } else {
      await fs.writeFile(`./output/${fname}`, JSON.stringify(data, null, 2), {
        flag: 'a',
      });
    }
  } catch (e: any) {
    console.error(e.message);
  }
}

export async function createDir(): Promise<void> {
  try {
    await fs.mkdir('output');
  } catch (e) {
    console.error('Directory already exists, ignoring...');
  }
}

export function getAWSProfile(profile: string) {
  return fromIni({
    profile,
  });
}

export function getARN(
  service: string,
  location: string,
  accountId: string,
  bucket?: string,
  instanceId?: string
) {
  switch (service) {
    case 's3':
      return `arn:aws:s3:::${bucket}`;
    case 'ec2':
      const resourceType = 'instance';
      return `arn:aws:ec2:${location}:${accountId}:${resourceType}/${instanceId}`;
    default:
      throw new Error('Service not supported');
  }
}

export function getURL(bucket: string, location: string) {
  return `https://s3.${location}.amazonaws.com/${bucket}`;
}

export function checkArgs(args: Record<string, string | boolean | undefined>) {
  const required = [
    'profile',
    'roleARN',
    'roleSessionName',
    'region',
    // 'service',
  ];

  const missing = [];

  for (const arg of required) {
    if (!args) continue;
    if (!args[arg] || args['help']) {
      missing.push(arg);
    }
  }

  return missing;
}

export function getHelp(): void {
  console.log(`---------------------------
  Usage: bun run index.ts [options]
  --profile, -p: AWS profile to use
  --roleARN: ARN of the role to assume
  --roleSessionName: Name of the role session
  --region, -r: AWS region
  --service, -s: AWS service to list resources from
  --help, -h: Display this message
  ---------------------------`);
  process.exit(0);
}

export function convertToCSV(data: Record<string, string>) {
  const csvRows: string[] = [];
  for (const [_, value] of Object.entries(data)) {
    csvRows.push(value);
  }

  return csvRows.join('\n');
}
