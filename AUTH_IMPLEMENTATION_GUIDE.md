# Auth System Implementation Guide

## Overview
This is a **single-model, role-based authentication system** with two roles:
- **super_admin**: Can create users and manage the system
- **user**: Regular users created by super_admin

---

## Architecture

### Database Model (User)
```
- id: Integer (Primary Key)
- name: String
- email: String (Unique)
- password: String (Hashed)
- role: String ('super_admin' or 'user')
- is_active: Boolean (for soft delete)
- created_at: String (timestamp)
```

### Role Hierarchy
```
super_admin (Full Access)
    └── Can create users
    └── Can view all users
    └── Can deactivate users
    └── Can create other super_admins (if needed)

user (Limited Access)
    └── Can login
    └── Can view own profile only
```

---

## User Flow

### 1️⃣ Initial Setup: Create First Super Admin
**Endpoint:** `POST /api/v1/auth/super-admin/setup`
```json
{
  "name": "Admin User",
  "email": "admin@company.com",
  "password": "strongpassword123",
  "role": "super_admin"
}
```
- ⚠️ Should only work if NO super_admin exists
- In production, **remove this endpoint** after setup or protect it

### 2️⃣ Super Admin Login
**Endpoint:** `POST /api/v1/auth/login`
```json
{
  "email": "admin@company.com",
  "password": "strongpassword123"
}
```
Returns: User details with role = "super_admin"

### 3️⃣ Super Admin Creates Regular User
**Endpoint:** `POST /api/v1/auth/super-admin/create-user`
```json
{
  "name": "John Doe",
  "email": "john@company.com",
  "password": "usersecurepass123",
  "role": "user"
}
```
- ✅ Requires super_admin authentication
- ✅ Automatically sets role = "user"
- Returns: Created user details

### 4️⃣ User Login
**Endpoint:** `POST /api/v1/auth/login`
```json
{
  "email": "john@company.com",
  "password": "usersecurepass123"
}
```
Returns: User details with role = "user"

### 5️⃣ Super Admin Views All Users
**Endpoint:** `GET /api/v1/auth/super-admin/users`
- Requires super_admin authentication
- Returns: List of all active users

### 6️⃣ Super Admin Deactivates User
**Endpoint:** `DELETE /api/v1/auth/super-admin/users/{user_id}`
- Requires super_admin authentication
- Soft deletes (sets is_active = false)
- User cannot login after deactivation

---

## Permission System

### Permission Functions (in `permissions.py`)
```python
is_superadmin(user)        # Check if super_admin
is_user(user)              # Check if regular user
is_active(user)            # Check if account is active
can_create_users(user)     # Only super_admin can create users
can_manage_users(user)     # Only super_admin can manage users
```

### Route Protection (in `dependencies.py`)
```python
get_current_superadmin()   # Returns super_admin or 403 error
get_current_user()         # Returns current user (TODO: Implement JWT)
```

---

## Endpoints Summary

| Endpoint | Method | Auth Required | Access |
|----------|--------|---------------|--------|
| `/auth/super-admin/setup` | POST | ❌ No | Initial super_admin setup |
| `/auth/login` | POST | ❌ No | All users |
| `/auth/super-admin/create-user` | POST | ✅ super_admin | Create user |
| `/auth/super-admin/create-superadmin` | POST | ✅ super_admin | Create super_admin |
| `/auth/super-admin/users` | GET | ✅ super_admin | List all users |
| `/auth/super-admin/users/{id}` | DELETE | ✅ super_admin | Deactivate user |

---

## Security Best Practices

### ✅ Implemented
- [x] Single role model (no role bloat)
- [x] Role-based access control (RBAC)
- [x] Password hashing (SHA-256)
- [x] Only super_admin creates users
- [x] Soft delete (is_active flag)
- [x] Permission checks at service level
- [x] Clear separation of concerns

### ⚠️ TODO: Production Requirements
- [ ] Implement JWT token authentication
- [ ] Add token refresh mechanism
- [ ] Add rate limiting on login
- [ ] Add audit logging for super_admin actions
- [ ] Use bcrypt instead of SHA-256
- [ ] Add email verification
- [ ] Add password reset flow
- [ ] Disable `/auth/super-admin/setup` after first super_admin created
- [ ] Add database migration for new fields (is_active, created_at)

---

## Testing Guide

### Test 1: Setup Super Admin
```bash
curl -X POST http://localhost:8000/api/v1/auth/super-admin/setup \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Admin",
    "email": "admin@test.com",
    "password": "admin123"
  }'
```

### Test 2: Super Admin Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@test.com",
    "password": "admin123"
  }'
```

### Test 3: Create User (Super Admin)
```bash
curl -X POST http://localhost:8000/api/v1/auth/super-admin/create-user \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer {token}" \
  -d '{
    "name": "John Doe",
    "email": "john@test.com",
    "password": "user123"
  }'
```

### Test 4: User Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@test.com",
    "password": "user123"
  }'
```

---

## Migration Notes

### Database Changes
Run migration to add new columns:
```sql
ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT TRUE;
ALTER TABLE users ADD COLUMN created_at VARCHAR;
```

### Model Updates
- ✅ Updated to use `role = "user"` or `role = "super_admin"`
- ✅ Added `is_active` field
- ✅ Added `created_at` field

### Service Layer
- ✅ Only super_admin can create users
- ✅ Permission checks implemented
- ✅ Error handling with clear messages

### Route Changes
- ❌ Removed: `/register` (anyone could register)
- ❌ Removed: `/admin` (no permission checks)
- ✅ Added: `/super-admin/create-user` (protected)
- ✅ Added: `/super-admin/users` (protected)
- ✅ Added: `/super-admin/users/{id}` (protected)
- ✅ Kept: `/login` (public for all users)

---

## Key Implementation Details

### Single Model Benefits
1. **Simplicity**: One table, same fields
2. **Performance**: No joins needed
3. **Maintainability**: Less code duplication
4. **Flexibility**: Can add more roles easily

### Why No Two Models?
❌ Would require:
- Duplicate fields (name, email, password in both tables)
- Joins for queries
- More complex logic
- More maintenance burden
- Not necessary for your use case

---

## Next Steps

1. **Implement JWT Authentication**
   - Extract token from `Authorization: Bearer {token}` header
   - Validate token and extract user_id
   - Update `get_current_user()` in dependencies.py

2. **Add Database Migration**
   - Add `is_active` and `created_at` columns
   - Create migration script

3. **Test All Endpoints**
   - Use provided curl commands
   - Verify permission checks work

4. **Configure in Production**
   - Disable `/auth/super-admin/setup` after first super_admin
   - Use bcrypt for password hashing
   - Add rate limiting and audit logging

5. **Optional: Add More Features**
   - Super admin password reset for users
   - User profile update endpoint
   - Bulk user creation
   - Audit log for all operations
