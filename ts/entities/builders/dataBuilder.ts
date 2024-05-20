import type { BuildInput, BuildURLInput, IExportData } from '../../types';

export default abstract class DataBuilder<T> {
  constructor(protected jsonData: T, protected csvData: string) {}
  abstract build(data: BuildInput): T;
  abstract buildURL(data: BuildURLInput): string;
  abstract buildArn(data: BuildInput): string;
  abstract getJSON(): IExportData;
  abstract getCSV(): string;
}
