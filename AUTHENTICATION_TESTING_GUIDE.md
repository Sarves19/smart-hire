# Smart Hire Authentication System - Testing & Deployment Guide

## ✅ COMPLETION STATUS

**Backend Implementation:**

- ✅ POST /auth/register - Create account with email verification OTP
- ✅ POST /auth/verify-otp - Verify registration email with OTP
- ✅ POST /auth/login - Simple email + password login (NO OTP required)
- ✅ POST /auth/forgot-password - Initiate password reset
- ✅ POST /auth/reset-password - Reset password with OTP

**Frontend Implementation:**

- ✅ register.html - Registration form with validation & password strength meter
- ✅ login.html - Login form with email + password
- ✅ verify-otp.html - Email verification OTP entry
- ✅ forgot-password.html - Password reset initiation
- ✅ reset-password.html - Password reset with new password

**Email Service:**

- ✅ EmailClient with SMTP_SSL (Port 465) & STARTTLS (Port 587) support
- ✅ EmailService with 4 email templates (OTP, Welcome, Login Notification, Security Alert)
- ✅ Gmail SMTP configured: sarbes19suresh@gmail.com with App Password

**Database & Migrations:**

- ✅ User, TrustedDevice, LoginHistory, EmailVerification models
- ✅ All migrations applied
- ✅ Alembic configured for version control

---

## 🚀 TESTING GUIDE

### ENVIRONMENT SETUP

**1. Ensure .env is configured:**

```bash
# Backend directory
cd backend

# Check .env has:
cat .env
```

Required variables in `.env`:

```
DATABASE_URL=postgresql+psycopg://postgres:admin@localhost:5432/smarthire_db
SECRET_KEY=your-32-character-minimum-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
SMTP_HOST=smtp.gmail.com
SMTP_PORT=465
SMTP_USE_SSL=True
SMTP_USERNAME=sarbes19suresh@gmail.com
SMTP_PASSWORD=oeqg jfcp xupc dzan
SMTP_FROM_EMAIL=sarbes19suresh@gmail.com
SMTP_FROM_NAME=Smart Hire
OTP_LENGTH=6
OTP_EXPIRY_MINUTES=10
OTP_MAX_ATTEMPTS=5
```

**2. Start PostgreSQL Database:**

```bash
# Windows (if using local installation)
pg_ctl -D "C:\Program Files\PostgreSQL\16\data" start

# Or using Docker
docker run --name smarthire-db -e POSTGRES_PASSWORD=admin -e POSTGRES_DB=smarthire_db -p 5432:5432 -d postgres:16
```

**3. Start Backend Server:**

```bash
cd backend

# Activate virtual environment
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python -m alembic upgrade head

# Start server
uvicorn app.main:app --reload --port 8000
```

Expected output:

```
Starting Smart Hire v1.0.0
Email (SMTP) configured: sarbes19suresh@gmail.com (host=smtp.gmail.com:465, ssl=True).
OTP emails, login notifications, and password reset emails are ENABLED.
```

**4. Start Frontend:**

```bash
cd frontend

# Start a simple HTTP server (Python 3.13+)
python -m http.server 8080

# Or use VS Code Live Server extension
```

---

### TEST SCENARIOS

#### TEST 1: User Registration → Email Verification → Login

**Steps:**

1. **Register new account:**
   - Navigate to: `http://localhost:8080/pages/auth/register.html`
   - Enter:
     - First Name: John
     - Last Name: Doe
     - Email: test_user_001@gmail.com
     - Phone: 0771234567
     - Role: CUSTOMER
     - Password: SecurePass123!@#
     - Confirm: SecurePass123!@#
   - Click "Create Account"

   **Expected:**
   - ✅ Success message: "Registration successful. Redirecting to verify OTP..."
   - ✅ Redirect to: `verify-otp.html?email=test_user_001@gmail.com`
   - ✅ Email received in inbox with 6-digit OTP code
   - ✅ User record created in database with `is_verified=False`

2. **Verify Email OTP:**
   - Enter the 6-digit OTP from email
   - Click "Verify OTP"

   **Expected:**
   - ✅ Success message
   - ✅ Auto-login: Access & Refresh tokens stored in localStorage
   - ✅ Redirect to: `/dashboard.html` (or show dashboard if exists)
   - ✅ User record now has `is_verified=True`
   - ✅ Welcome email sent to inbox

3. **Login with same email/password:**
   - Navigate to: `http://localhost:8080/pages/auth/login.html`
   - Enter:
     - Email: test_user_001@gmail.com
     - Password: SecurePass123!@#
   - Click "Sign In"

   **Expected:**
   - ✅ Success: Tokens stored in localStorage
   - ✅ Redirect to `/dashboard.html`
   - ✅ Login notification email sent to inbox
   - ✅ LoginHistory record created with `status=SUCCESS`

---

#### TEST 2: Password Reset Flow

**Steps:**

1. **Request Password Reset:**
   - Navigate to: `http://localhost:8080/pages/auth/forgot-password.html`
   - Enter email: test_user_001@gmail.com
   - Click "Send OTP"

   **Expected:**
   - ✅ Success message: "If that email is registered, a reset code has been sent."
   - ✅ Redirect to: `reset-password.html?email=test_user_001@gmail.com`
   - ✅ Password reset OTP email sent to inbox

2. **Reset Password:**
   - Enter 6-digit OTP from email
   - Enter new password: NewSecurePass456!@#
   - Confirm password
   - Click "Reset Password"

   **Expected:**
   - ✅ Success message: "Password reset successfully."
   - ✅ Redirect to: `login.html`
   - ✅ Login with new password works: NewSecurePass456!@#
   - ✅ Old password no longer works

---

#### TEST 3: Email Validation & Error Cases

**Test 3.1: Invalid Email**

- Try registering with: `notanemail`
- Expected: ❌ "Please enter a valid email."

**Test 3.2: Duplicate Email**

- Register first account with: test_duplicate@gmail.com
- Try registering second account with same email
- Expected: ❌ "Email already exists"

**Test 3.3: Weak Password**

- Try password: `123456` (no letters or symbols)
- Expected: ❌ Password validation fails

**Test 3.4: Passwords Don't Match**

- Enter password: SecurePass123!@#
- Enter confirm: DifferentPass456!@#
- Expected: ❌ "Passwords do not match"

**Test 3.5: Invalid Phone**

- Try phone: `1234567890` (not Sri Lankan format)
- Expected: ❌ "Valid Sri Lankan number required"

**Test 3.6: Invalid OTP**

- Enter wrong OTP: `000000`
- Expected: ❌ "Invalid OTP" after attempts exceeded

**Test 3.7: Expired OTP**

- Wait 11 minutes (OTP_EXPIRY_MINUTES=10)
- Try to verify
- Expected: ❌ "OTP has expired"

**Test 3.8: Login with Wrong Password**

- Email: test_user_001@gmail.com
- Password: WrongPassword123!@#
- Expected: ❌ "Invalid email or password"
- ✅ No timing difference between valid/invalid passwords (constant-time check)

**Test 3.9: Login Before Email Verified**

- Register new account but don't verify email
- Try to login
- Expected: ❌ "Please verify your email first"

---

#### TEST 4: Rate Limiting

**Test 4.1: OTP Rate Limit**

- Send OTP requests rapidly (5 requests in 10 seconds)
- Expected: ✅ First 5 succeed, 6th = ❌ 429 Too Many Requests

**Test 4.2: Login Rate Limit**

- Send login requests rapidly (10 requests in 30 seconds)
- Expected: ✅ First 10 succeed, 11th = ❌ 429 Too Many Requests

---

#### TEST 5: Token Validation

**Test 5.1: Access Token in localStorage**

- After successful login, open Browser DevTools → Application → localStorage
- Expected: ✅ `access_token`, `refresh_token`, `user` all present

**Test 5.2: Token Structure**

- Copy access_token value
- Go to: https://jwt.io
- Paste token
- Expected: ✅ Token decodes with `sub`, `type: "access"`, `exp`, `iat`, `jti`

**Test 5.3: Refresh Token Expiry**

- Refresh token has `exp` set to current_time + 7 days
- Access token has `exp` set to current_time + 30 minutes

---

#### TEST 6: Email Delivery

**Test 6.1: Registration OTP Email**

- Subject: Smart Hire - Email Verification
- Contains: 6-digit OTP code
- Professional HTML template
- Contains: First name, purpose, expiry time

**Test 6.2: Welcome Email**

- Subject: Welcome to Smart Hire
- Sent after successful email verification
- Contains: User's first name, welcome message

**Test 6.3: Login Notification Email**

- Subject: New login to your Smart Hire account
- Sent ONLY after successful login (not on failed attempts)
- Contains: Login time, IP address, browser, OS, device name
- Warning: "If this wasn't you, change your password immediately"

**Test 6.4: Password Reset Email**

- Subject: Reset your Smart Hire password
- Contains: 6-digit OTP code
- Contains: Expiry time (10 minutes)

---

## 📊 DATABASE VERIFICATION

**Check user was created:**

```sql
SELECT id, first_name, email, is_verified, is_active, created_at FROM "user" WHERE email = 'test_user_001@gmail.com';
```

**Check login history:**

```sql
SELECT id, email, status, ip_address, is_trusted_device, created_at FROM login_history WHERE email = 'test_user_001@gmail.com' ORDER BY created_at DESC;
```

**Check email verifications:**

```sql
SELECT id, user_id, otp_purpose, created_at, expires_at FROM email_verification WHERE user_id = 1 ORDER BY created_at DESC;
```

---

## 🔍 API ENDPOINT VERIFICATION

Test each endpoint with curl or Postman:

### 1. Register

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "phone_number": "0771234567",
    "password": "SecurePass123!@#",
    "role": "CUSTOMER"
  }'
```

Expected: `201 Created` with message

### 2. Verify OTP

```bash
curl -X POST http://localhost:8000/api/v1/auth/verify-otp \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "otp_code": "123456"
  }'
```

Expected: `200 OK` with message

### 3. Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePass123!@#"
  }'
```

Expected: `200 OK` with `access_token`, `refresh_token`, `token_type`, `user`

### 4. Forgot Password

```bash
curl -X POST http://localhost:8000/api/v1/auth/forgot-password \
  -H "Content-Type: application/json" \
  -d '{"email": "john@example.com"}'
```

Expected: `200 OK` with generic message (for security)

### 5. Reset Password

```bash
curl -X POST http://localhost:8000/api/v1/auth/reset-password \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "otp_code": "123456",
    "new_password": "NewSecurePass456!@#"
  }'
```

Expected: `200 OK` with message

---

## 🚨 COMMON ISSUES & FIXES

### Issue 1: "Email (SMTP) not configured"

**Solution:**

- Check .env has SMTP_USERNAME and SMTP_PASSWORD
- Verify Gmail App Password is 16 characters
- App Password must be generated from https://myaccount.google.com/apppasswords

### Issue 2: "SMTPAuthenticationError: (535, b'5.7.8 Username and password not accepted')"

**Solution:**

- Verify Gmail account is correct
- Generate NEW App Password from Google Account settings
- Gmail password ≠ App Password (App Password is only way for programmatic access)

### Issue 3: "Connection timed out" on SMTP

**Solution:**

- Check firewall allows outbound port 465 (SSL) or 587 (STARTTLS)
- If behind corporate firewall, may need to use port 587 instead of 465
- Verify SMTP_USE_SSL matches port (465=True, 587=False)

### Issue 4: "OTP not being sent"

**Solution:**

- Check backend logs for EmailClient errors
- Verify SMTP configuration via startup log
- Test SMTP manually: `python -c "from app.core.email import EmailClient; EmailClient().send_email('test@gmail.com', 'Test', '<p>Test</p>', 'Test')"`

### Issue 5: "CORS error when calling API from frontend"

**Solution:**

- Backend needs CORS middleware configured
- Check `app.main.py` has:

  ```python
  from fastapi.middleware.cors import CORSMiddleware

  app.add_middleware(
      CORSMiddleware,
      allow_origins=["*"],  # Or specific origins
      allow_credentials=True,
      allow_methods=["*"],
      allow_headers=["*"],
  )
  ```

### Issue 6: "localStorage not storing tokens"

**Solution:**

- Check browser console for JavaScript errors
- Verify API response includes access_token field
- localStorage must be enabled (not in private/incognito mode)
- Test in console: `localStorage.getItem('access_token')`

---

## 📋 PRE-PRODUCTION CHECKLIST

- [ ] Database is PostgreSQL (not SQLite)
- [ ] Environment variables all set in .env
- [ ] Gmail account configured with App Password
- [ ] SMTP_PORT matches SMTP_USE_SSL (465/SSL or 587/STARTTLS)
- [ ] SECRET_KEY is at least 32 random characters
- [ ] ACCESS_TOKEN_EXPIRE_MINUTES is 30 (or as required)
- [ ] REFRESH_TOKEN_EXPIRE_DAYS is 7 (or as required)
- [ ] All 5 test scenarios pass end-to-end
- [ ] Email delivery working for all 4 email types
- [ ] Rate limiting tested and working
- [ ] Password validation enforces all requirements
- [ ] OTP validation enforces 6-digit format
- [ ] Phone validation works for Sri Lankan numbers
- [ ] Timing attack prevention implemented (constant-time checks)
- [ ] CORS configured if frontend is on different origin
- [ ] HTTPS configured for production
- [ ] Secrets (SECRET_KEY, passwords) not committed to git
- [ ] Database backups configured
- [ ] Monitoring/logging configured for production
- [ ] Rate limits appropriate for expected load
- [ ] Error messages don't leak security information

---

## 🎯 SUCCESS CRITERIA

✅ **All tests pass:**

- User can register → verify email → login
- User can reset password
- Emails arrive within 1-2 seconds
- All validation works correctly
- Rate limiting prevents abuse
- Tokens stored and retrieved from localStorage
- No CORS errors
- No 500 errors in backend logs
- No timing differences for user enumeration

✅ **Production ready when:**

- All items in pre-production checklist completed
- All test scenarios pass 3 times in a row
- No errors in backend logs
- Email delivery confirmed for real Gmail account
- HTTPS configured
- Database backups configured
- Monitoring alerts set up

---

## 📞 NEXT STEPS

1. **Start backend server** with: `uvicorn app.main:app --reload --port 8000`
2. **Start frontend** with HTTP server
3. **Run TEST 1** (Registration → Verification → Login)
4. **Check email inbox** for OTP code
5. **Verify database** records created
6. **Run remaining tests** (2-6)
7. **Complete pre-production checklist**
8. **Deploy to production**

---

**System Status:** ✅ **READY FOR TESTING**
All backend endpoints implemented, all frontend pages created, email service configured.
