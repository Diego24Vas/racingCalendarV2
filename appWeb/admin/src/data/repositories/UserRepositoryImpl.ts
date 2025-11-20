import { User } from "../../domain/models/User";
import { UserRepository } from "../../domain/repositories/UserRepository";
import { UserDataSource } from "../datasources/UserDataSource";

export class UserRepositoryImpl implements UserRepository {
    private dataSource: UserDataSource;

    constructor(dataSource: UserDataSource) {
        this.dataSource = dataSource;
    }

    async getUsers(): Promise<User[]> {
        return this.dataSource.getUsers();
    }
}
