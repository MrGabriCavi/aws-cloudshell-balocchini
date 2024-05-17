export function getHelp(): void {
  console.log(`---------------------------
    Usage: bun run index.ts [options]
    --profile, -p: AWS profile to use
    --roleARN: ARN of the role to assume
    --roleSessionName: Name of the role session
    --region, -r: AWS region
    --help, -h: Display this message
    ---------------------------`);
  process.exit(0);
}

export function getMenu() {
  return +prompt(
    `
AWS Menu:
---------------------
0. Exit
1. S3 Operations
2. EC2 Operations
3. RDS Operations
---------------------
Select an option:`
  )!;
}

export function getS3Menu() {
  return +prompt(`
S3 Menu:
---------------------
0. Exit
1. List Buckets
---------------------
Select an option:`)!;
}

export function getEC2Menu() {
  return +prompt(`
EC2 Menu:
---------------------
0. Exit
1. List Instances
---------------------
Select an option:`)!;
}

export function getRDSMenu() {
  return +prompt(`
RDS Menu:
---------------------
0. Exit
1. List Instances
---------------------
Select an option:`)!;
}

export function getExtension() {
  return prompt('Enter the file extension (csv, json):')!;
}
