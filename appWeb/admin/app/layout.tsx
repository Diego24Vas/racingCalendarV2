import type { ReactNode } from 'react';
import './globals.css';

export const metadata = {
  title: 'Admin - Racing Calendar',
  description: 'Panel de administración',
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="es">
      <body>{children}</body>
    </html>
  );
}
