import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { describe, expect, it } from 'vitest';

import App from './App.jsx';

describe('App shell', () => {
  it('renders the scheduling workspace navigation and default booking view', async () => {
    render(
      <MemoryRouter initialEntries={['/']}>
        <App />
      </MemoryRouter>
    );

    expect(screen.getByRole('heading', { name: /scheduling workspace/i })).toBeTruthy();
    expect(screen.getByRole('complementary', { name: /primary navigation/i })).toBeTruthy();
    expect(await screen.findByRole('heading', { name: /book appointment/i })).toBeTruthy();
    expect(screen.getByText(/no patient login required/i)).toBeTruthy();
  });
});
