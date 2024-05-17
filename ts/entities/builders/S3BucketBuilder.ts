import DataBuilder from './dataBuilder';
import { type IExportData } from '../../types';
import { getARN, getURL } from '../../utils';
import { type BuildInputS3, type BuildURLInputS3 } from '../../types';

export default class S3BucketBuilder extends DataBuilder<IExportData> {
  private readonly service = 's3';
  constructor(data: IExportData, csvData: string) {
    super(data, csvData);
  }
  build({ bucket, location, accountId }: BuildInputS3): IExportData {
    return (this.jsonData = {
      ...this.jsonData,
      [bucket]: {
        location,
        accountId,
        url: this.buildURL({ bucket, location }),
        arn: this.buildArn({ location, accountId, bucket }),
      },
    });
  }

  buildCSV({ bucket, location, accountId }: BuildInputS3) {
    return (this.csvData += `${bucket},${location},${accountId},${this.buildURL(
      {
        bucket,
        location,
      }
    )},${this.buildArn({ location, accountId, bucket })}\n`);
  }

  buildArn({ location, accountId, bucket }: BuildInputS3): string {
    return getARN(this.service, location, accountId, bucket);
  }

  buildURL({ bucket, location }: BuildURLInputS3): string {
    return getURL(bucket, location);
  }

  getJSON(): IExportData {
    return this.jsonData;
  }

  getCSV(): string {
    return this.csvData;
  }
}
