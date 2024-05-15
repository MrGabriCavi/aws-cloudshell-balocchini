import { type IExportData } from '../../types';
import { getARN, getURL } from '../../utils';
import DataBuilder from './dataBuilder';
import { type BuildInputS3, type BuildURLInputS3 } from '../../types';

export default class S3BucketBuilder extends DataBuilder<IExportData> {
  private readonly service = 's3';
  constructor(data: IExportData) {
    super(data);
  }
  build({ bucket, location, accountId }: BuildInputS3): IExportData {
    return (this.data = {
      ...this.data,
      [bucket]: {
        location,
        accountId,
        url: this.buildURL({ bucket, location }),
        arn: this.buildArn({ location, accountId, bucket }),
      },
    });
  }

  buildCSV({ bucket, location, accountId }: BuildInputS3) {
    return `${bucket},${location},${accountId},${this.buildURL({
      bucket,
      location,
    })},${this.buildArn({ location, accountId, bucket })}\n`;
  }

  buildArn({ location, accountId, bucket }: BuildInputS3): string {
    return getARN(this.service, location, accountId, bucket);
  }

  buildURL({ bucket, location }: BuildURLInputS3): string {
    return getURL(bucket, location);
  }
}
