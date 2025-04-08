// App.test.js

import React from 'react';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import { act } from 'react-dom/test-utils';
import { ToastContainer, toast } from 'react-toastify';

// Mock external dependencies
jest.mock('react-toastify', () => ({
  ToastContainer: jest.fn(() => null),
  toast: {
    error: jest.fn(),
  },
}));

// Mock components
jest.mock('./components/Navbar', () => () => <div data-testid="navbar">Navbar</div>);
jest.mock('./components/Cards', () => ({ courses }) => (
  <div data-testid="cards">
    {courses.map(course => (
      <div key={course.id}>{course.title}</div>
    ))}
  </div>
));
jest.mock('./components/Filter', () => ({ filterData, category, setCategory }) => (
  <div data-testid="filter">
    <select value={category} onChange={(e) => setCategory(e.target.value)}>
      {filterData.map(item => (
        <option key={item} value={item}>{item}</option>
      ))}
    </select>
  </div>
));
jest.mock('./components/Spinner', () => () => <div data-testid="spinner">Loading...</div>);

// Mock utility functions
const mockCourses = [
  { id: 1, title: 'React Course', description: 'Learn React fundamentals', image: 'react.jpg', category: 'Frontend' },
  { id: 2, title: 'Node.js Course', description: 'Build backend with Node.js', image: 'nodejs.jpg', category: 'Backend' },
];

jest.mock('./utils/data', () => ({
  getCourses: jest.fn(() => Promise.resolve(mockCourses)),
  getCategories: jest.fn(() => ['Frontend', 'Backend']),
  filterCourses: jest.fn((courses, category) => 
    category === 'All' ? courses : courses.filter(course => course.category === category)
  ),
}));

// Import the component to be tested
import App from './App';

describe('App Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders Navbar, Filter, and Cards components', async () => {
    await act(async () => {
      render(<App />);
    });

    expect(screen.getByTestId('navbar')).toBeInTheDocument();
    expect(screen.getByTestId('filter')).toBeInTheDocument();
    expect(screen.getByTestId('cards')).toBeInTheDocument();
  });

  test('displays spinner while loading', async () => {
    render(<App />);
    expect(screen.getByTestId('spinner')).toBeInTheDocument();
    
    await waitFor(() => {
      expect(screen.queryByTestId('spinner')).not.toBeInTheDocument();
    });
  });

  test('fetches and displays courses', async () => {
    await act(async () => {
      render(<App />);
    });

    expect(screen.getByText('React Course')).toBeInTheDocument();
    expect(screen.getByText('Node.js Course')).toBeInTheDocument();
  });

  test('filters courses by category', async () => {
    await act(async () => {
      render(<App />);
    });

    const filterSelect = screen.getByTestId('filter').querySelector('select');
    fireEvent.change(filterSelect, { target: { value: 'Frontend' } });

    await waitFor(() => {
      expect(screen.getByText('React Course')).toBeInTheDocument();
      expect(screen.queryByText('Node.js Course')).not.toBeInTheDocument();
    });
  });

  test('handles API error', async () => {
    const errorMessage = 'Network Error: Unable to fetch courses';
    jest.spyOn(console, 'error').mockImplementation(() => {}); // Suppress console.error
    jest.mocked(getCourses).mockRejectedValueOnce(new Error('Network Error'));

    await act(async () => {
      render(<App />);
    });

    await waitFor(() => {
      expect(toast.error).toHaveBeenCalledWith(errorMessage);
    });

    console.error.mockRestore();
  });
});

// Helper function to mock fetch for integration testing
function setupFetchMock(mockData) {
  global.fetch = jest.fn().mockImplementation(() =>
    Promise.resolve({
      json: () => Promise.resolve(mockData),
    })
  );
}

// Example of how to use the helper function for integration testing
describe('App Integration', () => {
  beforeEach(() => {
    setupFetchMock(mockCourses);
  });

  afterEach(() => {
    global.fetch.mockClear();
    delete global.fetch;
  });

  test('integrates with mock API', async () => {
    await act(async () => {
      render(<App />);
    });

    await waitFor(() => {
      expect(screen.getByText('React Course')).toBeInTheDocument();
      expect(screen.getByText('Node.js Course')).toBeInTheDocument();
    });

    expect(global.fetch).toHaveBeenCalledTimes(1);
  });
});