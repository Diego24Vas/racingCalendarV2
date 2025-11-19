import { ExampleEntity } from '@domain/ExampleEntity';

export function exampleUseCase(entity: ExampleEntity): string {
  return `Hola, ${entity.name}!`;
}
