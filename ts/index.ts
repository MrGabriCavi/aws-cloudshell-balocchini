import STS from './entities/sts';
import S3 from './entities/s3';
import EC2 from './entities/ec2';
import S3BucketBuilder from './entities/builders/S3BucketBuilder';
import EC2Builder from './entities/builders/EC2Builder';
import RDS from './entities/rds';
import RDSBuilder from './entities/builders/RDSBuilder';
import { checkArgs, createDir, getHelp, writeFile } from './utils';
import type { IExportData } from './types';
import { getArgs } from './utils/args';

try {
  const args = getArgs();

  const missing = checkArgs(args);
  if (missing.length > 0) {
    if (missing.includes('help')) {
      getHelp();
    }
    console.error(`Missing required arguments: ${missing.join(', ')}`);
    process.exit(1);
  }
  let profile = args.profile;

  console.log('Profile selected:', profile);
  const stsClient = new STS(profile!, args.region!);

  let bdata: IExportData = {};
  let bcsv = 'name,location,accountId,arn\n';
  let idata: IExportData = {};
  let icsv = 'instanceId,ip,name,accountId,arn\n';
  let rdsdata: IExportData = {};
  let rdscsv = 'id,name,accountId,endpoint,port,arn,status\n';

  const assumedRole = await stsClient.assumeRole(
    args.roleARN!,
    args.roleSessionName!
  );

  console.log(args.region);

  const s3Client = new S3(assumedRole.Credentials, args.region!);
  const ec2Client = new EC2(assumedRole.Credentials, args.region!);
  const RDSClient = new RDS(assumedRole.Credentials, args.region!);
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
  const ext = prompt('Enter the file extension (csv, json):');
  if (!ext) {
    console.error('No file extension provided');
    process.exit(1);
  }
  for (const bucket of buckets) {
    const bucketLocation = await s3Client.getBucketLocation();

    bdata = new S3BucketBuilder(bdata).build({
      bucket,
      location: bucketLocation?.LocationConstraint as string,
      accountId: assumedRole.SourceIdentity as string,
    });
    bcsv += new S3BucketBuilder(bdata).buildCSV({
      bucket,
      location: bucketLocation?.LocationConstraint as string,
      accountId: assumedRole.SourceIdentity as string,
    });
  }

  for (const instance of instances) {
    idata = new EC2Builder(idata).build({
      instanceId: instance.id,
      location: instance.location,
      ip: instance.ip,
      name: instance.name,
      accountId: instance.accountId,
    });
    icsv += new EC2Builder(idata).buildCSV({
      instanceId: instance.id,
      location: instance.location,
      ip: instance.ip,
      name: instance.name,
      accountId: instance.accountId,
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
    rdscsv += new RDSBuilder(rdsdata).buildCSV({
      name: rdsInstance.name,
      port: rdsInstance.port,
      status: rdsInstance.status,
      endpoint: rdsInstance.endpoint,
      id: rdsInstance.id,
      arn: rdsInstance.arn,
    });
  }

  console.log('Writing data...');
  if (ext === 'csv') {
    await Promise.all([
      createDir(),
      writeFile(bcsv, `s3-buckets`, { ext }),
      writeFile(icsv, `ec2-instances`, { ext }),
      writeFile(rdscsv, `rds-dbs`, { ext }),
    ]);
  } else {
    await Promise.all([
      createDir(),
      writeFile(bdata, `s3-buckets`, { ext }),
      writeFile(idata, `ec2-instances`, { ext }),
      writeFile(rdsdata, `rds-dbs`, { ext }),
    ]);
  }
  console.log('Data written successfully');
} catch (e: any) {
  console.error(e.message);
  process.exit(1);
}
