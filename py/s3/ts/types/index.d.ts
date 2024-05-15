export type IExportData = Record<string, Record<string, string | undefined>>;

export enum Services {
  S3 = 's3',
  EC2 = 'ec2',
}

export type BuildURLInput = BuildURLInputS3 | BuildURLInputEC2;

export type BuildURLInputS3 = {
  bucket: string;
  location: string;
};

export type BuildURLInputEC2 = {
  region: string;
  accountId: string;
  instanceId: string;
};

export type BuildInput = BuildInputS3 | BuildInputEC2 | BuildInputRDS;

export type BuildInputS3 = {
  bucket: string;
  location: string;
  accountId: string;
};

export type BuildInputEC2 = {
  instanceId: string;
  ip: string;
  name: string;
  accountId: string;
  location?: string;
};

export type BuildInputRDS = {
  id: string;
  name: string;
  endpoint: string;
  port: string;
  status: string;
  arn: string;
  accountId: string;
};
