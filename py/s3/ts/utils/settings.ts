import Bun, { type Env } from 'bun';

const entries = Object.entries(Bun.env);

type nonUndefinedKeys = Exclude<keyof Env, undefined>;

export default entries.reduce((acc: Env, [key, values]) => {
  if (!values) return acc;
  acc[key as nonUndefinedKeys] = values;
  return acc;
}, {} as Env);
