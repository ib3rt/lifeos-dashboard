---
title: "TypeScript Best Practices"
date: "2026-02-01"
tags: ["reference", "typescript", "coding"]
category: "reference"
description: "TypeScript patterns and best practices"
---

# TypeScript Best Practices

A collection of TypeScript patterns and best practices for building robust applications.

## Type Definitions

### Use Interfaces for Object Shapes
```typescript
// ✅ Good
interface User {
  id: string;
  name: string;
  email: string;
}

// ❌ Avoid for objects
 type User = {
  id: string;
  name: string;
};
```

### Use Type for Unions/Primitives
```typescript
// ✅ Good
type Status = 'loading' | 'success' | 'error';
type ID = string | number;
```

## Functions

### Explicit Return Types
```typescript
// ✅ Good - clear contract
function calculateTotal(items: Item[]): number {
  return items.reduce((sum, item) => sum + item.price, 0);
}

// ❌ Avoid - implicit return type
function calculateTotal(items: Item[]) {
  return items.reduce((sum, item) => sum + item.price, 0);
}
```

### Use Function Overloads for Complex Signatures
```typescript
function process(input: string): string;
function process(input: number): number;
function process(input: string | number): string | number {
  // Implementation
}
```

## Error Handling

### Custom Error Classes
```typescript
class ValidationError extends Error {
  constructor(message: string, public field: string) {
    super(message);
    this.name = 'ValidationError';
  }
}

// Usage
throw new ValidationError('Invalid email', 'email');
```

## Utility Types

### Common Patterns
```typescript
// Partial - all properties optional
 type PartialUser = Partial<User>;

// Pick - select specific properties
 type UserSummary = Pick<User, 'id' | 'name'>;

// Omit - exclude specific properties
 type UserWithoutEmail = Omit<User, 'email'>;

// Record - object with specific keys
 type UserMap = Record<string, User>;
```

## Strict Mode

Always enable strict mode in `tsconfig.json`:

```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true
  }
}
```

## Resources

- [[Second Brain App]] - Built with TypeScript
- Official TypeScript Handbook
