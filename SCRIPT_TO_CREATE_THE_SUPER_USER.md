# Super Admin Creation

## Command

Run the following command from your backend project folder:

```bash
python script/create_superadmin.py --name "Admin" --email admin@test.com --password admin123
```

## Example

```bash
python script/create_superadmin.py --name "Mouli Admin" --email mouli@test.com --password Admin@123
```

## What Happens?

* Checks if the user already exists.
* Creates a Super Admin user.
* Generates an access token.
* Displays the user details and token.

## Sample Output

```text
Created super admin:

id: 1
name: Admin
email: admin@test.com
role: SUPER_ADMIN

Authorization: Bearer <ACCESS_TOKEN>
```

## If User Already Exists

```text
User already exists: id=1, email=admin@test.com, role=SUPER_ADMIN
```
