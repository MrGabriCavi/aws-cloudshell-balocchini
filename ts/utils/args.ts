import { parseArgs } from 'util';
import Bun from 'bun';

export function getArgs() {
  const { values } = parseArgs({
    args: Bun.argv,
    options: {
      profile: {
        type: 'string',
        short: 'p',
      },
      roleARN: {
        type: 'string',
      },
      roleSessionName: {
        type: 'string',
      },
      region: {
        type: 'string',
        short: 'r',
      },
      service: {
        type: 'string',
        short: 's',
      },
      help: {
        type: 'boolean',
        short: 'h',
      },
    },
    allowPositionals: true,
    strict: true,
  });

  return values;
}
