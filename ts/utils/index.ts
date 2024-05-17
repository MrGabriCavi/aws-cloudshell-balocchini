import fs from 'fs/promises';
import S3 from '../entities/s3';
import S3BucketBuilder from '../entities/builders/S3BucketBuilder';
import EC2 from '../entities/ec2';
import EC2Builder from '../entities/builders/EC2Builder';
import RDS from '../entities/rds';
import { fromIni } from '@aws-sdk/credential-providers';
import {
  S3Menu,
  type IExportData,
  type BuilderType,
  type Element,
  RDSMenu,
  EC2Menu,
  type BuildInputEC2,
  type BuildInputRDS,
  type BuilderHandler,
  type BuildersType,
  Services,
  FileTypes,
} from '../types';
import type { AssumeRoleCommandOutput } from '@aws-sdk/client-sts';
import { getEC2Menu, getExtension, getRDSMenu, getS3Menu } from './menu';
import type { GetBucketLocationCommandOutput } from '@aws-sdk/client-s3';
import RDSBuilder from '../entities/builders/RDSBuilder';
import { isEC2Builder, isRDSBuilder, isS3BucketBuilder } from './guards';

export async function writeFile(
  data: string,
  filename: string,
  ext: string
): Promise<void> {
  try {
    const fname = `${new Date().toISOString()}-${filename}.${ext}`;
    await fs.writeFile(`output/${fname}`, data, { flag: 'a' });
  } catch (e: any) {
    console.error(e.message);
  }
}

export async function createDir(): Promise<void> {
  try {
    await fs.mkdir('output');
  } catch (e) {
    console.warn('Directory already exists, ignoring...');
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
  const required = ['profile', 'roleARN', 'roleSessionName', 'region'];

  const missing = [];

  for (const arg of required) {
    if (!args) continue;
    if (!args[arg] || args['help']) {
      missing.push(arg);
    }
  }

  return missing;
}

export async function handleBuilder(
  builder: BuildersType,
  data: any,
  format: string,
  action?: (element: string) => Promise<any>
) {
  let handled = false;
  for (const key in builderHandlers) {
    const { typeGuard, handler } = builderHandlers[key];

    if (typeGuard(builder)) {
      handled = true;
      if (action) {
        const location = (
          await action(data.bucket)
        ).LocationConstraint.toString();
        data = {
          ...data,
          location,
        };
      }

      handler(builder, data, format);
      return;
    }
  }
  if (!handled) {
    console.error('Unknown builder type');
  }
}

const handler: BuilderHandler<any, any> = (
  builder: any,
  data: any,
  format: string
) => {
  if (format === FileTypes.JSON) {
    return builder.build(data);
  }
  return builder.buildCSV(data);
};

const builderHandlers: {
  [key: string]: {
    typeGuard: (builder: BuildersType) => boolean;
    handler: BuilderHandler<any, any>;
  };
} = {
  S3BucketBuilder: {
    typeGuard: isS3BucketBuilder,
    handler,
  },
  EC2Builder: {
    typeGuard: isEC2Builder,
    handler,
  },
  RDSBuilder: {
    typeGuard: isRDSBuilder,
    handler,
  },
};

export function startVariables() {
  let bdata: IExportData = {};
  let bcsv = 'name,location,accountId,arn\n';
  let idata: IExportData = {};
  let icsv = 'instanceId,ip,name,accountId,arn\n';
  let rdsdata: IExportData = {};
  let rdscsv = 'id,name,accountId,endpoint,port,arn,status\n';
  return { bdata, bcsv, idata, icsv, rdsdata, rdscsv };
}

function getEC2Object(data: Record<string, string>, accountId: string) {
  return {
    instanceId: data.instanceId,
    ip: data.ip,
    name: data.name,
    accountId,
  };
}

function getS3Object(data: string, accountId: string) {
  return {
    bucket: data,
    accountId,
  };
}

function getRDSObject(data: Record<string, string>) {
  return {
    id: data.id,
    name: data.name,
    endpoint: data.endpoint,
    port: data.port,
    status: data.status,
    arn: data.arn,
  };
}

function getPayload(
  data: string | Record<string, string>,
  accountId: string,
  type: string
) {
  if (typeof data === 'object' && type === Services.EC2) {
    return getEC2Object(data, accountId);
  }
  if (typeof data === 'object' && type === Services.RDS) {
    return getRDSObject(data);
  }
  return getS3Object(data as string, accountId);
}

export async function buildData<
  T,
  Z extends GetBucketLocationCommandOutput | undefined
>(
  elements: Element<T>,
  builder: BuilderType<T>,
  format: string,
  args: {
    jsonData: IExportData;
    csvData: string;
    service: string;
    accountId?: string;
  },
  action?: (element: string) => Promise<Z>
): Promise<void> {
  const { accountId, service } = args;

  for (const element of elements) {
    await handleBuilder(
      builder,
      getPayload(element, accountId as string, service),
      format,
      action
    );
  }
}

export async function handleS3Menu(
  assumedRole: AssumeRoleCommandOutput,
  region: string,
  params: { bdata: IExportData; bcsv: string }
) {
  let { bcsv, bdata } = params;
  const s3Client = new S3(assumedRole.Credentials, region);
  let selectMenuS3 = getS3Menu();
  while (selectMenuS3 !== 0) {
    switch (selectMenuS3) {
      case S3Menu.LIST_BUCKETS:
        const buckets = await s3Client.listBuckets();
        if (!buckets.length) {
          console.error('No buckets found');
          break;
        }

        const builder = new S3BucketBuilder(bdata, bcsv);
        const params = {
          jsonData: bdata,
          csvData: bcsv,
          accountId: assumedRole.AssumedRoleUser?.AssumedRoleId as string,
          service: Services.S3,
        };

        const ext = getExtension();
        await buildData<string[], GetBucketLocationCommandOutput | undefined>(
          buckets,
          builder,
          ext,
          params,
          (element) => {
            return s3Client.getBucketLocation(element);
          }
        );

        if (!ext || (!ext.includes('json') && !ext.includes('csv'))) {
          console.error('No file extension provided');
          break;
        }

        bdata = builder.getJSON();
        bcsv = builder.getCSV();

        const data = ext === FileTypes.CSV ? bcsv : JSON.stringify(bdata);
        await writeFile(data, 's3-buckets', ext);

        break;
      default:
        console.warn('Invalid selection');
        break;
    }
    selectMenuS3 = getS3Menu();
  }
}

export async function handleEC2Menu(
  assumedRole: AssumeRoleCommandOutput,
  region: string,
  params: { idata: IExportData; icsv: string }
) {
  let { idata, icsv } = params;
  const ec2Client = new EC2(assumedRole.Credentials, region!);
  let selectMenuEC2 = getEC2Menu();

  while (selectMenuEC2 !== 0) {
    switch (selectMenuEC2) {
      case EC2Menu.LIST_INSTANCES:
        const instances = await ec2Client.listInstances();
        if (!instances.length) {
          console.error('No instances found');
          break;
        }
        const builder = new EC2Builder(idata, icsv);
        const params = {
          jsonData: idata,
          csvData: icsv,
          service: Services.EC2,
        };
        const ext = getExtension();
        if (!ext || (!ext.includes('json') && !ext.includes('csv'))) {
          console.error('No file extension provided');
          process.exit(1);
        }
        await buildData<BuildInputEC2, undefined>(
          instances,
          builder,
          ext,
          params
        );

        idata = builder.getJSON();
        icsv = builder.getCSV();

        const data = ext === FileTypes.CSV ? icsv : JSON.stringify(idata);
        await writeFile(data, 'ec2-instances', ext);

        break;
      default:
        console.warn('Invalid selection');
        break;
    }
    selectMenuEC2 = getEC2Menu();
  }
}

export async function handleRDSMenu(
  assumedRole: AssumeRoleCommandOutput,
  region: string,
  params: { rdsdata: IExportData; rdscsv: string }
) {
  let { rdsdata, rdscsv } = params;
  const RDSClient = new RDS(assumedRole.Credentials, region!);
  const selectMenuRDS = getRDSMenu();

  while (selectMenuRDS !== 0) {
    switch (selectMenuRDS) {
      case RDSMenu.LIST_INSTANCES:
        const rdsInstances = await RDSClient.listDBInstances();
        if (!rdsInstances.length) {
          console.error('No RDS instances found');
          break;
        }
        const builder = new RDSBuilder(rdsdata, rdscsv);
        const params = {
          jsonData: rdsdata,
          csvData: rdscsv,
          service: Services.RDS,
        };
        const ext = getExtension();
        if (!ext || (!ext.includes('json') && !ext.includes('csv'))) {
          console.error('No file extension provided');
          process.exit(1);
        }
        await buildData<BuildInputRDS, undefined>(
          rdsInstances,
          builder,
          ext,
          params
        );

        rdsdata = builder.getJSON();
        rdscsv = builder.getCSV();

        const data = ext === FileTypes.CSV ? rdscsv : JSON.stringify(rdsdata);
        await writeFile(data, 'rds-instances', ext);
        break;
      default:
        console.warn('Invalid selection');
        break;
    }
  }
}

/**
 * Export the functions from the utils folder
 */

export * from './menu';
