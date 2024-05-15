import type { BuildInputRDS, IExportData } from '../../types';
import DataBuilder from './dataBuilder';

class RDSBuilder extends DataBuilder<IExportData> {
  constructor(data: IExportData) {
    super(data);
  }

  build(data: BuildInputRDS): IExportData {
    return (this.data = {
      ...this.data,
      [data.id]: {
        ...data,
        id: undefined,
      },
    });
  }

  buildCSV(data: BuildInputRDS) {
    return `${data.id},${data.name},${data.endpoint},${data.port},${data.arn},${data.status}\n`;
  }

  buildArn(_: BuildInputRDS): string {
    throw new Error('Method not implemented.');
  }

  buildURL(): string {
    throw new Error('Method not implemented.');
  }
}

export default RDSBuilder;
