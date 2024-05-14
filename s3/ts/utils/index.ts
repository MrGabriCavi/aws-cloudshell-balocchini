import fs from 'fs/promises';
import settings from './settings';
import { fromIni } from '@aws-sdk/credential-providers';

export async function writeFile<T>(data: T, filename: string): Promise<void> {
  try {
    let file: Buffer | undefined;
    try {
      file = await fs.readFile(`${filename}.json`);
    } catch (e) {
      console.error('File not found');
    }

    if (file) {
      await fs.unlink(`${filename}.json`);
    }
    await fs.writeFile(`${filename}.json`, JSON.stringify(data, null, 2), {
      flag: 'a',
    });
  } catch (e: any) {
    console.error(e.message);
  }
}

export function getAWSProfile(profile: string | null) {
  return fromIni({
    profile: profile ?? settings.DEFAULT_PROFILE,
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
      return `arn:aws:s3:${location}:${accountId}:${bucket}`;
    case 'ec2':
      const resourceType = 'instance';
      return `arn:aws:ec2:${location}:${accountId}:${resourceType}/${instanceId}`;
    default:
      throw new Error('Service not supported');
  }
}

export function getURL(bucket: string, location: string) {
  return `https://s3-${location}.amazonaws.com/${bucket}`;
}
