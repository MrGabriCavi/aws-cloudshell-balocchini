declare module 'bun' {
  interface Env {
    ROLE_ARN: string;
    ROLE_SESSION_NAME: string;
    ACCESS_KEY_ID: string;
    SECRET_ACCESS_KEY: string;
    REGION: string;
    DEFAULT_PROFILE: string;
  }
}
