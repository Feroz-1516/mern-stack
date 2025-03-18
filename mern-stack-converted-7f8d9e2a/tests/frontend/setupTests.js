// Import necessary testing libraries
import '@testing-library/jest-dom';

// Mock fetch API
global.fetch = jest.fn(() =>
  Promise.resolve({
    json: () => Promise.resolve({}),
  })
);

// Mock CSS modules
jest.mock('*.module.css', () => ({}));

// Add any global beforeEach or afterEach hooks if needed
beforeEach(() => {
  // Clear all mocks before each test
  jest.clearAllMocks();
});

// Mock localStorage
const localStorageMock = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  clear: jest.fn()
};
global.localStorage = localStorageMock;

// Set up any necessary environment variables for testing
process.env.REACT_APP_API_URL = 'http://localhost:3000/api';

// Suppress console.error and console.warn in tests
console.error = jest.fn();
console.warn = jest.fn();