export enum Menu {
  EXIT,
  S3,
  EC2,
  RDS,
}

export enum S3Menu {
  EXIT,
  LIST_BUCKETS,
}

export enum EC2Menu {
  EXIT,
  LIST_INSTANCES,
}

export enum RDSMenu {
  EXIT,
  LIST_INSTANCES,
}

export enum Services {
  S3 = 's3',
  EC2 = 'ec2',
  RDS = 'rds',
}

export enum FileTypes {
  JSON = 'json',
  CSV = 'csv',
}
