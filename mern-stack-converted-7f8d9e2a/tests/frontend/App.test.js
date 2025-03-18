import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';
import App from '../source/App';
import { BrowserRouter as Router } from 'react-router-dom';

jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  BrowserRouter: ({ children }) => <div>{children}</div>,
}));

test('renders App component without crashing', () => {
  render(<App />);
  expect(screen.getByRole('navigation')).toBeInTheDocument();
});

describe('App routing', () => {
  const routes = [
    { path: '/login', testId: 'login-page' },
    { path: '/blogs', testId: 'blogs-page' },
    { path: '/myBlogs', testId: 'user-blogs-page' },
    { path: '/myBlogs/1', testId: 'blog-detail-page' },
    { path: '/blogs/add', testId: 'add-blog-page' },
  ];

  test.each(routes)('renders correct component for $path', ({ path, testId }) => {
    window.history.pushState({}, '', path);
    render(<App />);
    expect(screen.getByTestId(testId)).toBeInTheDocument();
  });
});