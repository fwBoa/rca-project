import { render, screen, fireEvent } from '@testing-library/react';
import TaskForm from './TaskForm';

describe('TaskForm', () => {
    it('renders correctly', () => {
        render(<TaskForm onSubmit={jest.fn()} />);
        expect(screen.getByPlaceholderText(/Nouveau ticket.../i)).toBeInTheDocument();
        expect(screen.getByRole('button', { name: /Ajouter/i })).toBeInTheDocument();
    });

    it('calls onSubmit when form is submitted with a title', () => {
        const mockOnSubmit = jest.fn();
        render(<TaskForm onSubmit={mockOnSubmit} />);

        fireEvent.change(screen.getByPlaceholderText(/Nouveau ticket.../i), { target: { value: 'New Test Task' } });
        fireEvent.click(screen.getByRole('button', { name: /Ajouter/i }));

        expect(mockOnSubmit).toHaveBeenCalledWith({ title: 'New Test Task', description: '' });
    });
});
