import type EC2Builder from '../entities/builders/EC2Builder';
import type RDSBuilder from '../entities/builders/RDSBuilder';
import type S3BucketBuilder from '../entities/builders/S3BucketBuilder';

export type IExportData = Record<string, Record<string, string | undefined>>;

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
export type BuildersType = S3BucketBuilder | EC2Builder | RDSBuilder;

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
};

export type Element<T> = T extends string[]
  ? string[]
  : Record<string, string>[];
export type BuilderType<T> = T extends string[]
  ? S3BucketBuilder
  : T extends BuildInputEC2
  ? EC2Builder
  : RDSBuilder;

export type BuilderHandler<T, U> = (
  builder: T,
  data: U,
  format: string
) => void;

export * from './enum';
