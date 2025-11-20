import UserList from '../../presentation/components/UserList';

export default function UsersPage() {
    return (
        <div className="container mx-auto">
            <h1 className="text-3xl font-bold my-6">User Management</h1>
            <UserList />
        </div>
    );
}
