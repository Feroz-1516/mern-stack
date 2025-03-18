// config.js

const config = {
  API: {
    BASE_URL: process.env.REACT_APP_API_BASE_URL || 'http://localhost:5001/api',
    ENDPOINTS: {
      LOGIN: '/login',
      SIGNUP: '/signup',
      BLOGS: '/blogs',
      USERS: '/users',
    },
  },
  AUTH: {
    TOKEN_KEY: 'blogAppAuthToken',
  },
};

export default config;