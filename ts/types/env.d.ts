declare module 'bun' {
  interface Env {
    ROLE_ARN: string;
    ROLE_SESSION_NAME: string;
    REGION: string;
    DEFAULT_PROFILE: string;
  }
}
