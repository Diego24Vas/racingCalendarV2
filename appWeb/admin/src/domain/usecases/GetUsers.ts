import { User } from "../models/User";
import { UserRepository } from "../repositories/UserRepository";

export class GetUsers {
    private repository: UserRepository;

    constructor(repository: UserRepository) {
        this.repository = repository;
    }

    async execute(): Promise<User[]> {
        return this.repository.getUsers();
    }
}
