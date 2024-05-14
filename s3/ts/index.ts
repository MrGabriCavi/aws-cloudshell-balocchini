import Bun from 'bun';
import STS from './entities/sts';
import S3 from './entities/s3';
import EC2 from './entities/ec2';
import S3BucketBuilder from './entities/S3BucketBuilder';
import EC2Builder from './entities/EC2Builder';
import { writeFile } from './utils';
import type { IExportData } from './types';
import RDS from './entities/rds';
import RDSBuilder from './entities/RDSBuilder';

try {
  let profile = prompt('Enter your profile name:');
  if (!profile) {
    profile = Bun.env.DEFAULT_PROFILE;
  }
  console.log('Profile selected:', profile);
  const stsClient = new STS(profile);
  let bdata: IExportData = {};
  let idata: IExportData = {};
  let rdsdata: IExportData = {};
  const assumedRole = await stsClient.assumeRole();
  const accountId = assumedRole.AssumedRoleUser?.AssumedRoleId as string;
  const s3Client = new S3(assumedRole.Credentials);
  const ec2Client = new EC2(assumedRole.Credentials, accountId);
  const RDSClient = new RDS(assumedRole.Credentials, accountId);
  const buckets = await s3Client.listBuckets();
  const instances = await ec2Client.listInstances();
  const rdsInstances = await RDSClient.listDBInstances();
  if (!buckets.length) {
    console.error('No buckets found');
  }
  if (!instances.length) {
    console.error('No instances found');
  }
  if (!rdsInstances.length) {
    console.error('No RDS instances found');
  }
  for (const bucket of buckets) {
    const bucketLocation = await s3Client.getBucketLocation();
    const acl = await s3Client.getBucketAcl();

    bdata = new S3BucketBuilder(bdata).build({
      bucket,
      location: bucketLocation?.LocationConstraint as string,
      accountId: acl?.Owner?.ID as string,
    });
  }

  for (const instance of instances) {
    idata = new EC2Builder(idata).build({
      instanceId: instance.id,
      location: instance.location,
      accountId: instance.accountId,
      ip: instance.ip,
      name: instance.name,
    });
  }

  for (const rdsInstance of rdsInstances) {
    rdsdata = new RDSBuilder(rdsdata).build({
      name: rdsInstance.name,
      port: rdsInstance.port,
      status: rdsInstance.status,
      endpoint: rdsInstance.endpoint,
      id: rdsInstance.id,
      arn: rdsInstance.arn,
    });
  }

  console.log('Writing data...');
  await Promise.all([
    writeFile(bdata, 'buckets'),
    writeFile(idata, 'instances'),
    writeFile(rdsdata, 'rds'),
  ]);
  console.log('Data written successfully');
} catch (e: any) {
  console.log(e.message);
}
