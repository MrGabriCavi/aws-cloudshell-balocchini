import { type IExportData } from '../../types';
import { getARN } from '../../utils';
import DataBuilder from './dataBuilder';
import { type BuildInputEC2, type BuildURLInputEC2 } from '../../types';

export default class EC2Builder extends DataBuilder<IExportData> {
  private readonly service = 'ec2';
  constructor(data: IExportData) {
    super(data);
  }

  build(data: BuildInputEC2): IExportData {
    return (this.data = {
      ...this.data,
      [data.instanceId]: {
        ip: data.ip,
        name: data.name,
        accountId: data.accountId,
        arn: this.buildArn(data),
      },
    });
  }

  buildCSV(data: BuildInputEC2) {
    return `${data.instanceId},${data.ip},${data.name},${
      data.accountId
    },${this.buildArn(data)}\n`;
  }

  buildArn(data: BuildInputEC2): string {
    return getARN(
      this.service,
      data.location as string,
      data.accountId,
      undefined,
      data.instanceId
    );
  }

  buildURL(_: BuildURLInputEC2): string {
    throw new Error('Method not implemented.');
  }
}
