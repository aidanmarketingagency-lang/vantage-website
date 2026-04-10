#!/usr/bin/env python3

import requests
import sys
import json
from datetime import datetime
import time

class VantageAPITester:
    def __init__(self, base_url="https://deal-automation-6.preview.emergentagent.com"):
        self.base_url = base_url
        self.session = requests.Session()
        self.tests_run = 0
        self.tests_passed = 0
        self.admin_token = None
        self.test_user_id = None

    def log(self, message):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")

    def run_test(self, name, method, endpoint, expected_status, data=None, headers=None, cookies=None):
        """Run a single API test"""
        url = f"{self.base_url}/api/{endpoint}"
        test_headers = {'Content-Type': 'application/json'}
        if headers:
            test_headers.update(headers)

        self.tests_run += 1
        self.log(f"🔍 Testing {name}...")
        
        try:
            if method == 'GET':
                response = self.session.get(url, headers=test_headers)
            elif method == 'POST':
                response = self.session.post(url, json=data, headers=test_headers)
            elif method == 'PUT':
                response = self.session.put(url, json=data, headers=test_headers)
            elif method == 'DELETE':
                response = self.session.delete(url, headers=test_headers)

            success = response.status_code == expected_status
            if success:
                self.tests_passed += 1
                self.log(f"✅ {name} - Status: {response.status_code}")
                try:
                    return True, response.json() if response.content else {}
                except:
                    return True, {}
            else:
                self.log(f"❌ {name} - Expected {expected_status}, got {response.status_code}")
                try:
                    error_detail = response.json()
                    self.log(f"   Error: {error_detail}")
                except:
                    self.log(f"   Error: {response.text}")
                return False, {}

        except Exception as e:
            self.log(f"❌ {name} - Exception: {str(e)}")
            return False, {}

    def test_root_endpoint(self):
        """Test root API endpoint"""
        return self.run_test("Root API", "GET", "", 200)

    def test_user_registration(self):
        """Test user registration"""
        test_email = f"test_user_{int(time.time())}@example.com"
        test_data = {
            "email": test_email,
            "password": "TestPassword123!",
            "name": "Test User"
        }
        
        success, response = self.run_test(
            "User Registration",
            "POST",
            "auth/register",
            200,
            data=test_data
        )
        
        if success and 'id' in response:
            self.test_user_id = response['id']
            self.log(f"   Created user ID: {self.test_user_id}")
            return True, test_email, "TestPassword123!"
        return False, None, None

    def test_user_login(self, email, password):
        """Test user login"""
        login_data = {
            "email": email,
            "password": password
        }
        
        success, response = self.run_test(
            "User Login",
            "POST",
            "auth/login",
            200,
            data=login_data
        )
        
        if success:
            self.log(f"   Logged in user: {response.get('email', 'Unknown')}")
            return True
        return False

    def test_admin_login(self):
        """Test admin login"""
        admin_data = {
            "email": "admin@vantage.ai",
            "password": "VantageAdmin123!"
        }
        
        success, response = self.run_test(
            "Admin Login",
            "POST",
            "auth/login",
            200,
            data=admin_data
        )
        
        if success:
            self.log(f"   Admin logged in: {response.get('email', 'Unknown')}")
            return True
        return False

    def test_get_current_user(self):
        """Test get current user endpoint"""
        return self.run_test("Get Current User", "GET", "auth/me", 200)

    def test_logout(self):
        """Test user logout"""
        return self.run_test("User Logout", "POST", "auth/logout", 200)

    def test_waitlist_signup(self):
        """Test waitlist signup"""
        test_email = f"waitlist_test_{int(time.time())}@example.com"
        waitlist_data = {
            "email": test_email,
            "role": "Brand"
        }
        
        success, response = self.run_test(
            "Waitlist Signup",
            "POST",
            "waitlist/signup",
            200,
            data=waitlist_data
        )
        
        if success:
            self.log(f"   Waitlist entry created: {response.get('email', 'Unknown')}")
        return success

    def test_waitlist_duplicate(self):
        """Test waitlist duplicate email handling"""
        test_email = f"duplicate_test_{int(time.time())}@example.com"
        waitlist_data = {
            "email": test_email,
            "role": "Creator"
        }
        
        # First signup should succeed
        success1, _ = self.run_test(
            "Waitlist Signup (First)",
            "POST",
            "waitlist/signup",
            200,
            data=waitlist_data
        )
        
        # Second signup should fail with 400
        success2, _ = self.run_test(
            "Waitlist Duplicate Check",
            "POST",
            "waitlist/signup",
            400,
            data=waitlist_data
        )
        
        return success1 and success2

    def test_audit_questions(self):
        """Test audit questions endpoint"""
        success, response = self.run_test("Get Audit Questions", "GET", "audit/questions", 200)
        
        if success and isinstance(response, list) and len(response) == 9:
            self.log(f"   Retrieved {len(response)} audit questions")
            return True, response
        elif success:
            self.log(f"   Warning: Expected 9 questions, got {len(response) if isinstance(response, list) else 'non-list'}")
        return False, []

    def test_audit_submission(self):
        """Test audit submission with AI generation"""
        # First get questions
        questions_success, questions = self.test_audit_questions()
        if not questions_success:
            return False

        # Prepare sample answers
        sample_answers = [
            {"question_id": 1, "answer": "Brand"},
            {"question_id": 2, "answer": "1-5"},
            {"question_id": 3, "answer": "Manual search"},
            {"question_id": 4, "answer": "$5K-$25K"},
            {"question_id": 5, "answer": "Finding the right creators"},
            {"question_id": 6, "answer": "Engagement metrics"},
            {"question_id": 7, "answer": "2-4 weeks"},
            {"question_id": 8, "answer": "Instagram"},
            {"question_id": 9, "answer": "Scale campaigns"}
        ]
        
        audit_data = {"answers": sample_answers}
        
        self.log("   Submitting audit (AI generation may take a few seconds)...")
        success, response = self.run_test(
            "Audit Submission",
            "POST",
            "audit/submit",
            200,
            data=audit_data
        )
        
        if success:
            required_fields = ['campaign_health_summary', 'top_problems', 'prioritized_actions', 'focus_this_week']
            has_all_fields = all(field in response for field in required_fields)
            
            if has_all_fields:
                self.log(f"   AI analysis generated successfully")
                self.log(f"   Summary: {response['campaign_health_summary'][:100]}...")
                return True
            else:
                self.log(f"   Warning: Missing required fields in response")
                return False
        return False

    def test_brute_force_protection(self):
        """Test brute force protection on login"""
        test_email = f"brute_test_{int(time.time())}@example.com"
        wrong_password = "WrongPassword123!"
        
        self.log("   Testing brute force protection (5 failed attempts)...")
        
        # Try 5 failed login attempts
        for i in range(5):
            login_data = {"email": test_email, "password": wrong_password}
            success, response = self.run_test(
                f"Brute Force Attempt {i+1}",
                "POST",
                "auth/login",
                401,
                data=login_data
            )
            if not success:
                return False
        
        # 6th attempt should be rate limited (429)
        login_data = {"email": test_email, "password": wrong_password}
        success, response = self.run_test(
            "Brute Force Lockout Check",
            "POST",
            "auth/login",
            429,
            data=login_data
        )
        
        return success

    def test_admin_waitlist_stats(self):
        """Test admin waitlist stats endpoint"""
        return self.run_test("Admin Waitlist Stats", "GET", "waitlist/stats", 200)

    def test_admin_waitlist_entries(self):
        """Test admin waitlist entries endpoint"""
        success, response = self.run_test("Admin Waitlist Entries", "GET", "waitlist/entries", 200)
        
        if success and isinstance(response, list):
            self.log(f"   Retrieved {len(response)} waitlist entries")
            return True
        return success

    def test_admin_audit_stats(self):
        """Test admin audit stats endpoint"""
        return self.run_test("Admin Audit Stats", "GET", "audit/stats", 200)

    def test_admin_audit_entries(self):
        """Test admin audit entries endpoint"""
        success, response = self.run_test("Admin Audit Entries", "GET", "audit/entries", 200)
        
        if success and isinstance(response, list):
            self.log(f"   Retrieved {len(response)} audit entries")
            return True
        return success

    def test_audit_by_id(self):
        """Test getting audit by ID endpoint"""
        # First submit an audit to get an ID
        sample_answers = [
            {"question_id": 1, "answer": "Brand"},
            {"question_id": 2, "answer": "1-5"},
            {"question_id": 3, "answer": "Manual search"},
            {"question_id": 4, "answer": "$5K-$25K"},
            {"question_id": 5, "answer": "Finding the right creators"},
            {"question_id": 6, "answer": "Engagement metrics"},
            {"question_id": 7, "answer": "2-4 weeks"},
            {"question_id": 8, "answer": "Instagram"},
            {"question_id": 9, "answer": "Scale campaigns"}
        ]
        
        audit_data = {"answers": sample_answers}
        success, response = self.run_test(
            "Audit Submission for ID Test",
            "POST",
            "audit/submit",
            200,
            data=audit_data
        )
        
        if success and 'id' in response:
            audit_id = response['id']
            # Now test getting audit by ID
            return self.run_test("Get Audit by ID", "GET", f"audit/{audit_id}", 200)
        
        return False
    # Phase 3 Test Methods
    def test_admin_users(self):
        """Test admin users endpoint"""
        success, response = self.run_test("Get All Users", "GET", "admin/users", 200)
        
        if success and isinstance(response, list):
            self.log(f"   Retrieved {len(response)} registered users")
            return True
        return success

    def test_admin_user_stats(self):
        """Test admin user stats endpoint"""
        success, response = self.run_test("Get User Stats", "GET", "admin/users/stats", 200)
        
        if success:
            required_fields = ['total', 'admins', 'by_type', 'recent_7_days']
            has_all_fields = all(field in response for field in required_fields)
            
            if has_all_fields:
                self.log(f"   Total users: {response['total']}, Admins: {response['admins']}")
                return True
            else:
                self.log(f"   Warning: Missing required fields in user stats")
                return False
        return False

    def test_csv_export(self):
        """Test CSV export functionality"""
        success, response = self.run_test("Export Waitlist CSV", "GET", "admin/export/waitlist", 200)
        return success

    def test_delete_endpoints(self):
        """Test delete endpoints with invalid IDs"""
        # Test delete user with invalid ID
        success1, _ = self.run_test("Delete Invalid User", "DELETE", "admin/users/invalid_id", 404)
        
        # Test delete waitlist entry with invalid ID  
        success2, _ = self.run_test("Delete Invalid Waitlist", "DELETE", "admin/waitlist/invalid_id", 404)
        
        # Test delete audit with invalid ID
        success3, _ = self.run_test("Delete Invalid Audit", "DELETE", "admin/audits/invalid_id", 404)
        
        return success1 and success2 and success3

    def test_password_reset_flow(self):
        """Test password reset functionality"""
        self.log("   Testing password reset flow...")
        
        # Test forgot password
        success1, _ = self.run_test(
            "Forgot Password",
            "POST",
            "auth/forgot-password",
            200,
            data={"email": "admin@vantage.ai"}
        )
        
        # Test verify invalid token
        success2, _ = self.run_test(
            "Verify Invalid Token",
            "GET", 
            "auth/verify-reset-token/invalid_token",
            400
        )
        
        # Test reset with invalid token
        success3, _ = self.run_test(
            "Reset with Invalid Token",
            "POST",
            "auth/reset-password", 
            400,
            data={"token": "invalid_token", "new_password": "NewPass123!"}
        )
        
        return success1 and success2 and success3

    def test_profile_management(self):
        """Test profile management endpoints"""
        self.log("   Testing profile management...")
        
        # Test get profile
        success1, response = self.run_test("Get My Profile", "GET", "profile/me", 200)
        
        if not success1:
            return False
            
        # Test update profile
        success2, response = self.run_test(
            "Update Profile",
            "PUT",
            "profile/me",
            200,
            data={
                "name": "Updated Admin",
                "bio": "Test bio",
                "company": "Vantage",
                "website": "https://vantage.ai",
                "location": "San Francisco",
                "platforms": ["Instagram", "TikTok"],
                "niche": ["Business", "Tech"],
                "budget_range": "$25K-$100K"
            }
        )
        
        # Test get public profile (using admin's ID if available)
        success3 = True
        if success2 and 'id' in response:
            user_id = response['id']
            success3, _ = self.run_test("Get Public Profile", "GET", f"profile/{user_id}", 200)
        
        return success1 and success2 and success3

def main():
    print("🚀 Starting Vantage API Testing...")
    print("=" * 60)
    
    tester = VantageAPITester()
    
    # Test sequence - Part 1: Basic functionality
    basic_tests = [
        ("Root API", tester.test_root_endpoint),
        ("User Registration", lambda: tester.test_user_registration()[0]),
        ("Admin Login", tester.test_admin_login),
        ("Get Current User", tester.test_get_current_user),
        ("User Logout", tester.test_logout),
        ("Waitlist Signup", tester.test_waitlist_signup),
        ("Waitlist Duplicate Check", tester.test_waitlist_duplicate),
        ("Audit Questions", lambda: tester.test_audit_questions()[0]),
        ("Audit Submission (AI)", tester.test_audit_submission),
        ("Brute Force Protection", tester.test_brute_force_protection),
        ("Get Audit by ID", tester.test_audit_by_id),
    ]
    
    # Run basic tests
    for test_name, test_func in basic_tests:
        try:
            result = test_func()
            if not result:
                print(f"\n⚠️  {test_name} failed - continuing with other tests...")
        except Exception as e:
            print(f"\n💥 {test_name} crashed: {str(e)}")
            tester.tests_run += 1
    
    # Test sequence - Part 2: Admin endpoints (need fresh admin login)
    print(f"\n🔐 Testing Admin Endpoints (logging in as admin)...")
    admin_login_success = tester.test_admin_login()
    
    if admin_login_success:
        admin_tests = [
            ("Admin Waitlist Stats", tester.test_admin_waitlist_stats),
            ("Admin Waitlist Entries", tester.test_admin_waitlist_entries),
            ("Admin Audit Stats", tester.test_admin_audit_stats),
            ("Admin Audit Entries", tester.test_admin_audit_entries),
            ("Phase 3: Admin Users", tester.test_admin_users),
            ("Phase 3: Admin User Stats", tester.test_admin_user_stats),
            ("Phase 3: CSV Export", tester.test_csv_export),
            ("Phase 3: Delete Endpoints", tester.test_delete_endpoints),
            ("Phase 3: Password Reset", tester.test_password_reset_flow),
            ("Phase 3: Profile Management", tester.test_profile_management),
        ]
        
        for test_name, test_func in admin_tests:
            try:
                result = test_func()
                if not result:
                    print(f"\n⚠️  {test_name} failed - continuing with other tests...")
            except Exception as e:
                print(f"\n💥 {test_name} crashed: {str(e)}")
                tester.tests_run += 1
    else:
        print("❌ Admin login failed - skipping admin endpoint tests")
        tester.tests_run += 4  # Count the skipped tests
    
    # Final results
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {tester.tests_passed}/{tester.tests_run} passed")
    
    if tester.tests_passed == tester.tests_run:
        print("🎉 All tests passed!")
        return 0
    else:
        print(f"❌ {tester.tests_run - tester.tests_passed} tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())