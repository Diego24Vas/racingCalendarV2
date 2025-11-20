'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';

export default function DashboardPage() {
    const [user, setUser] = useState<any>(null);
    const router = useRouter();

    useEffect(() => {
        // Verificar si hay token en localStorage
        const token = localStorage.getItem('token');
        if (!token) {
            router.push('/login');
            return;
        }

        // Aquí podrías cargar los datos del usuario si lo necesitas
        // Por ahora solo mostramos un mensaje de bienvenida
    }, [router]);

    const handleLogout = () => {
        localStorage.removeItem('token');
        router.push('/login');
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
            <nav className="bg-white shadow-sm">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex justify-between h-16 items-center">
                        <h1 className="text-2xl font-bold text-gray-900">Racing Calendar Admin</h1>
                        <button
                            onClick={handleLogout}
                            className="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                        >
                            Cerrar Sesión
                        </button>
                    </div>
                </div>
            </nav>

            <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
                <div className="px-4 py-6 sm:px-0">
                    <div className="bg-white rounded-lg shadow-lg p-8">
                        <div className="text-center">
                            <h2 className="text-4xl font-bold text-gray-900 mb-4">
                                ¡Bienvenido al Panel de Administración!
                            </h2>
                            <p className="text-xl text-gray-600 mb-8">
                                Has iniciado sesión correctamente
                            </p>

                            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
                                <div className="bg-blue-50 p-6 rounded-lg hover:shadow-md transition-shadow">
                                    <div className="text-blue-600 text-4xl mb-3">👥</div>
                                    <h3 className="text-lg font-semibold text-gray-900 mb-2">Usuarios</h3>
                                    <p className="text-gray-600 mb-4">Gestiona los usuarios del sistema</p>
                                    <button
                                        onClick={() => router.push('/users')}
                                        className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                                    >
                                        Ver Usuarios
                                    </button>
                                </div>

                                <div className="bg-green-50 p-6 rounded-lg hover:shadow-md transition-shadow">
                                    <div className="text-green-600 text-4xl mb-3">🏁</div>
                                    <h3 className="text-lg font-semibold text-gray-900 mb-2">Carreras</h3>
                                    <p className="text-gray-600 mb-4">Administra el calendario de carreras</p>
                                    <button
                                        className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700"
                                    >
                                        Próximamente
                                    </button>
                                </div>

                                <div className="bg-purple-50 p-6 rounded-lg hover:shadow-md transition-shadow">
                                    <div className="text-purple-600 text-4xl mb-3">⚙️</div>
                                    <h3 className="text-lg font-semibold text-gray-900 mb-2">Configuración</h3>
                                    <p className="text-gray-600 mb-4">Ajustes del sistema</p>
                                    <button
                                        className="px-4 py-2 bg-purple-600 text-white rounded-md hover:bg-purple-700"
                                    >
                                        Próximamente
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </main>
        </div>
    );
}
