import { API_URL } from "../../config/env";
import { User } from "../../domain/models/User";

export class AuthDataSource {
    async login(email: string, password: string): Promise<string> {
        const formData = new URLSearchParams();
        formData.append('username', email);
        formData.append('password', password);

        console.log('Attempting login to:', `${API_URL}/token`);

        try {
            const response = await fetch(`${API_URL}/token`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: formData,
                mode: 'cors',
                credentials: 'omit',
            });

            console.log('Response status:', response.status);

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Login failed');
            }

            const data = await response.json();
            console.log('Login successful, token received');
            return data.access_token;
        } catch (error) {
            console.error('Login error:', error);
            if (error instanceof TypeError && error.message.includes('fetch')) {
                throw new Error('No se puede conectar con el servidor. Verifica que la API esté corriendo en ' + API_URL);
            }
            throw error;
        }
    }

    async getProfile(token: string): Promise<User> {
        const response = await fetch(`${API_URL}/usuarios/me`, {
            headers: {
                'Authorization': `Bearer ${token}`,
            },
        });

        if (!response.ok) {
            throw new Error('Failed to fetch profile');
        }

        return await response.json();
    }
}
