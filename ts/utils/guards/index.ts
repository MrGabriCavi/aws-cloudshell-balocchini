import EC2Builder from '../../entities/builders/EC2Builder';
import RDSBuilder from '../../entities/builders/RDSBuilder';
import S3BucketBuilder from '../../entities/builders/S3BucketBuilder';
import type { BuildersType } from '../../types';

// Type guard functions
export function isS3BucketBuilder(
  builder: BuildersType
): builder is S3BucketBuilder {
  return builder instanceof S3BucketBuilder;
}

export function isEC2Builder(
  builder: S3BucketBuilder | EC2Builder | RDSBuilder
): builder is EC2Builder {
  return builder instanceof EC2Builder;
}

export function isRDSBuilder(
  builder: S3BucketBuilder | EC2Builder | RDSBuilder
): builder is RDSBuilder {
  return builder instanceof RDSBuilder;
}
