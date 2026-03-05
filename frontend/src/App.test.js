import { render, screen } from '@testing-library/react';
import App from './App';

// Mock axios since App makes API calls
jest.mock('axios', () => ({
    get: jest.fn(() => Promise.resolve({ data: [] })),
    post: jest.fn(),
    put: jest.fn(),
    delete: jest.fn()
}));

describe('App', () => {
    it('renders the header correctly', async () => {
        render(<App />);
        expect(screen.getByText(/Task Manager/i)).toBeInTheDocument();
    });
});
