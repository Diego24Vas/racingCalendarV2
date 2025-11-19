import type { ReactNode } from 'react';
import './globals.css';

export const metadata = {
  title: 'User - Racing Calendar',
  description: 'Portal de usuario',
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="es">
      <body>{children}</body>
    </html>
  );
}
