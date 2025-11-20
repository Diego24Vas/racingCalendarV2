import { AuthRepository } from "../repositories/AuthRepository";
import { User } from "../models/User";

export class LoginUseCase {
    private repository: AuthRepository;

    constructor(repository: AuthRepository) {
        this.repository = repository;
    }

    async execute(email: string, password: string): Promise<User> {
        const token = await this.repository.login(email, password);
        const user = await this.repository.getProfile(token);

        if (user.rol !== 'admin') {
            throw new Error('Access denied: User is not an admin');
        }
        return user;
    }
}
