# Project Structure

This document defines the organization and folder structure conventions for the project.

## Root Directory

```
/
├── .kiro/              # Kiro AI assistant configuration
│   └── steering/       # AI guidance documents
├── src/                # Source code (create when needed)
├── tests/              # Test files (create when needed)
├── docs/               # Documentation (create when needed)
├── config/             # Configuration files (create when needed)
└── README.md           # Project overview (create when needed)
```

## Folder Conventions

- **src/**: Main application source code
- **tests/**: Unit tests, integration tests, and test utilities
- **docs/**: Project documentation, API docs, and guides
- **config/**: Environment configs, build configs, and settings
- **.kiro/**: AI assistant configuration and steering rules

## File Naming

- Use lowercase with hyphens for multi-word files: `user-service.js`
- Use descriptive names that indicate purpose
- Group related files in appropriate subdirectories
- Keep configuration files at appropriate levels (root vs config/)

## Code Organization

- Separate concerns into logical modules/packages
- Keep related functionality together
- Use clear directory hierarchies
- Maintain consistent import/export patterns
- Place shared utilities in common locations

## Documentation Structure

- README.md at root for project overview
- API documentation in docs/api/
- User guides in docs/guides/
- Technical specs in docs/specs/
- Inline code documentation for complex logic
