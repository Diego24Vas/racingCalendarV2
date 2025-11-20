export interface User {
    id: number;
    nombre: string;
    apellido?: string;
    correo: string;
    id_pais?: number;
    rol: 'usuario' | 'admin';
    activo: boolean;
    created_at: string;
    updated_at?: string;
}
