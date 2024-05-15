import type { BuildInput, BuildInputRDS, IExportData } from '../types';
import DataBuilder from './dataBuilder';

class RDSBuilder extends DataBuilder<IExportData> {
  private readonly service = 'rds';
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

  buildArn(_: BuildInputRDS): string {
    throw new Error('Method not implemented.');
  }

  buildURL(): string {
    throw new Error('Method not implemented.');
  }
}

export default RDSBuilder;
