import STS from './entities/sts';
import {
  createDir,
  checkArgs,
  getHelp,
  getMenu,
  handleEC2Menu,
  handleRDSMenu,
  handleS3Menu,
  startVariables,
} from './utils';
import { Menu } from './types';
import { getArgs } from './utils/args';

try {
  const args = getArgs();
  let { bdata, bcsv, idata, icsv, rdsdata, rdscsv } = startVariables();

  const missing = checkArgs(args);
  if (missing.length > 0) {
    if (missing.includes('help')) {
      getHelp();
    }
    console.error(`Missing required arguments: ${missing.join(', ')}`);
    process.exit(1);
  }
  let profile = args.profile;

  console.info(`${profile} profile selected`);
  const stsClient = new STS(profile!, args.region as string);
  const assumedRole = await stsClient.assumeRole(
    args.roleARN!,
    args.roleSessionName!
  );
  await createDir();
  let selectMenu = getMenu();

  while (selectMenu !== 0) {
    switch (selectMenu) {
      case Menu.S3:
        await handleS3Menu(assumedRole, args.region as string, { bdata, bcsv });
        break;
      case Menu.EC2:
        await handleEC2Menu(assumedRole, args.region as string, {
          idata,
          icsv,
        });
        break;
      case Menu.RDS:
        await handleRDSMenu(assumedRole, args.region as string, {
          rdsdata,
          rdscsv,
        });
        break;
      default:
        console.warn('Invalid selection');
        break;
    }

    selectMenu = getMenu();
  }

  if (selectMenu === 0) {
    console.log('Bye');
    process.exit(0);
  }
} catch (e: any) {
  console.error(e.message);
  process.exit(1);
}
