import { User } from "../../domain/models/User";
import { API_URL } from "../../config/env";

export class UserDataSource {
    async getUsers(): Promise<User[]> {
        try {
            const token = localStorage.getItem('token');
            const headers: HeadersInit = {};
            if (token) {
                headers['Authorization'] = `Bearer ${token}`;
            }

            const response = await fetch(`${API_URL}/usuarios/`, {
                headers: headers
            });
            if (!response.ok) {
                throw new Error('Error fetching users');
            }
            return await response.json();
        } catch (error) {
            console.error("Error in UserDataSource:", error);
            throw error;
        }
    }
}
