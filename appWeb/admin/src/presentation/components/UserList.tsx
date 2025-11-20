'use client';

import React, { useEffect, useState } from 'react';
import { User } from '../../domain/models/User';
import { GetUsers } from '../../domain/usecases/GetUsers';
import { UserRepositoryImpl } from '../../data/repositories/UserRepositoryImpl';
import { UserDataSource } from '../../data/datasources/UserDataSource';

export default function UserList() {
    const [users, setUsers] = useState<User[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchUsers = async () => {
            try {
                const dataSource = new UserDataSource();
                const repository = new UserRepositoryImpl(dataSource);
                const getUsersUseCase = new GetUsers(repository);
                const usersData = await getUsersUseCase.execute();
                setUsers(usersData);
            } catch (err) {
                setError('Error loading users');
                console.error(err);
            } finally {
                setLoading(false);
            }
        };

        fetchUsers();
    }, []);

    if (loading) return <div>Loading...</div>;
    if (error) return <div>{error}</div>;

    return (
        <div className="p-4">
            <h2 className="text-2xl font-bold mb-4">Users List</h2>
            <div className="overflow-x-auto">
                <table className="min-w-full bg-white border border-gray-300">
                    <thead>
                        <tr>
                            <th className="py-2 px-4 border-b">ID</th>
                            <th className="py-2 px-4 border-b">Name</th>
                            <th className="py-2 px-4 border-b">Email</th>
                            <th className="py-2 px-4 border-b">Role</th>
                            <th className="py-2 px-4 border-b">Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {users.map((user) => (
                            <tr key={user.id} className="hover:bg-gray-50">
                                <td className="py-2 px-4 border-b">{user.id}</td>
                                <td className="py-2 px-4 border-b">{user.nombre} {user.apellido}</td>
                                <td className="py-2 px-4 border-b">{user.correo}</td>
                                <td className="py-2 px-4 border-b">{user.rol}</td>
                                <td className="py-2 px-4 border-b">
                                    <span className={`px-2 py-1 rounded text-sm ${user.activo ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                                        {user.activo ? 'Active' : 'Inactive'}
                                    </span>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}
