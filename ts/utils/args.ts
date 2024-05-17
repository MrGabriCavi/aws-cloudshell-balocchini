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
