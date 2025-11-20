import { AuthRepository } from "../../domain/repositories/AuthRepository";
import { AuthDataSource } from "../datasources/AuthDataSource";
import { User } from "../../domain/models/User";

export class AuthRepositoryImpl implements AuthRepository {
    private dataSource: AuthDataSource;

    constructor(dataSource: AuthDataSource) {
        this.dataSource = dataSource;
    }

    async login(email: string, password: string): Promise<string> {
        const token = await this.dataSource.login(email, password);
        localStorage.setItem('token', token);
        return token;
    }

    async getProfile(token: string): Promise<User> {
        return this.dataSource.getProfile(token);
    }

    logout(): void {
        localStorage.removeItem('token');
    }
}
