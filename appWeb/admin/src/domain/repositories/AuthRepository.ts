import { User } from "../models/User";

export interface AuthRepository {
    login(email: string, password: string): Promise<string>; // Returns token
    getProfile(token: string): Promise<User>;
    logout(): void;
}
