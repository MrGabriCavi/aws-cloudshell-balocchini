import type { BuildInput, BuildURLInput } from '../../types';

export default abstract class DataBuilder<T> {
  constructor(protected data: T) {}
  abstract build(data: BuildInput): T;
  abstract buildURL(data: BuildURLInput): string;
  abstract buildArn(data: BuildInput): string;
}
