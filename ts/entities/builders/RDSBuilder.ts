import DataBuilder from './dataBuilder';
import type { BuildInputRDS, IExportData } from '../../types';

class RDSBuilder extends DataBuilder<IExportData> {
  constructor(data: IExportData, csvData: string) {
    super(data, csvData);
  }

  build(data: BuildInputRDS): IExportData {
    return (this.jsonData = {
      ...this.jsonData,
      [data.id]: {
        ...data,
        id: undefined,
      },
    });
  }

  buildCSV(data: BuildInputRDS) {
    return (this.csvData += `${data.id},${data.name},${data.endpoint},${data.port},${data.arn},${data.status}\n`);
  }

  buildArn(_: BuildInputRDS): string {
    throw new Error('Method not implemented.');
  }

  buildURL(): string {
    throw new Error('Method not implemented.');
  }

  getJSON(): IExportData {
    return this.jsonData;
  }

  getCSV(): string {
    return this.csvData;
  }
}

export default RDSBuilder;
