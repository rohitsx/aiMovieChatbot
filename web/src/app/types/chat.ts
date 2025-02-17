export interface Message {
  role: 'user' | 'assistant' | 'system';
  content: string | Record<string, any>;
}

export interface Route {
  path: string;
  name: string;
}

export interface L1Request {
  character: string;
  user_message: string;
}

export interface L2Request {
  script: string;
}
