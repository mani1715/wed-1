#!/usr/bin/env python3
"""
Admin Profile Save Functionality Testing
Tests the specific 422 error scenario reported by user when saving profiles in admin panel.

FOCUS AREAS:
1. Admin authentication
2. Profile creation with minimal required fields
3. Validation error testing (422 responses)
4. English language requirement validation
5. Response format verification
"""

import requests
import json
from datetime import datetime, timedelta
import sys
import traceback

# Configuration
BASE_URL = "https://errorfix-wedding.preview.emergentagent.com/api"
ADMIN_EMAIL = "admin@wedding.com"
ADMIN_PASSWORD = "admin123"

class AdminProfileSaveTester:
    def __init__(self):
        self.token = None
        self.test_profiles = []
        self.passed_tests = 0
        self.total_tests = 0
        
    def authenticate(self):
        """Authenticate as admin"""
        print("🔐 Authenticating as admin...")
        
        response = requests.post(f"{BASE_URL}/auth/login", json={
            "email": ADMIN_EMAIL,
            "password": ADMIN_PASSWORD
        })
        
        if response.status_code == 200:
            data = response.json()
            self.token = data["access_token"]
            print(f"✅ Authentication successful")
            print(f"   Admin ID: {data.get('admin', {}).get('id', 'N/A')}")
            print(f"   Admin Email: {data.get('admin', {}).get('email', 'N/A')}")
            return True
        else:
            print(f"❌ Authentication failed: {response.status_code} - {response.text}")
            return False
    
    def get_headers(self):
        """Get authorization headers"""
        return {"Authorization": f"Bearer {self.token}"}
    
    def run_test(self, test_name, test_func):
        """Run a single test with error handling"""
        self.total_tests += 1
        print(f"\n🧪 TEST {self.total_tests}: {test_name}")
        
        try:
            result = test_func()
            if result:
                self.passed_tests += 1
                print(f"✅ PASSED: {test_name}")
            else:
                print(f"❌ FAILED: {test_name}")
            return result
        except Exception as e:
            print(f"❌ ERROR in {test_name}: {str(e)}")
            traceback.print_exc()
            return False
    
    def test_minimal_profile_creation_success(self):
        """Test 1: Profile Creation with Minimal Required Fields (Should Succeed)"""
        
        # Calculate future date for event_date
        future_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        
        profile_data = {
            "groom_name": "Rajesh",
            "bride_name": "Priya", 
            "event_type": "marriage",
            "event_date": f"{future_date}T10:00:00",
            "venue": "Grand Palace",
            "enabled_languages": ["english"],
            "events": []
        }
        
        print(f"   📝 Creating profile with minimal required fields:")
        print(f"      Groom: {profile_data['groom_name']}")
        print(f"      Bride: {profile_data['bride_name']}")
        print(f"      Event Date: {profile_data['event_date']}")
        print(f"      Venue: {profile_data['venue']}")
        print(f"      Languages: {profile_data['enabled_languages']}")
        
        response = requests.post(
            f"{BASE_URL}/admin/profiles",
            json=profile_data,
            headers=self.get_headers()
        )
        
        print(f"   📡 Response Status: {response.status_code}")
        
        if response.status_code in [200, 201]:
            profile = response.json()
            self.test_profiles.append(profile["id"])
            
            print(f"   ✅ Profile created successfully!")
            print(f"      Profile ID: {profile['id']}")
            print(f"      Slug: {profile['slug']}")
            print(f"      Invitation Link: {profile.get('invitation_link', 'N/A')}")
            
            # Verify required fields are present in response
            required_fields = ['id', 'slug', 'groom_name', 'bride_name', 'event_type', 'event_date', 'venue', 'enabled_languages']
            missing_fields = []
            
            for field in required_fields:
                if field not in profile:
                    missing_fields.append(field)
            
            if missing_fields:
                print(f"   ⚠️ Missing fields in response: {missing_fields}")
                return False
            
            # Verify English is in enabled_languages
            if "english" not in profile.get('enabled_languages', []):
                print(f"   ❌ English not found in enabled_languages: {profile.get('enabled_languages')}")
                return False
            
            print(f"   ✅ All required fields present in response")
            print(f"   ✅ English language requirement satisfied")
            return True
            
        else:
            print(f"   ❌ Profile creation failed: {response.status_code}")
            try:
                error_detail = response.json()
                print(f"   📋 Error Details: {json.dumps(error_detail, indent=2)}")
            except:
                print(f"   📋 Raw Response: {response.text}")
            return False
    
    def test_missing_required_fields_validation(self):
        """Test 2: Missing Required Fields Should Return 422 Validation Error"""
        
        # Test cases with missing required fields
        test_cases = [
            {
                "name": "Missing groom_name",
                "data": {
                    "bride_name": "Priya",
                    "event_type": "marriage", 
                    "event_date": "2026-02-15T10:00:00",
                    "venue": "Grand Palace",
                    "enabled_languages": ["english"]
                }
            },
            {
                "name": "Missing bride_name", 
                "data": {
                    "groom_name": "Rajesh",
                    "event_type": "marriage",
                    "event_date": "2026-02-15T10:00:00", 
                    "venue": "Grand Palace",
                    "enabled_languages": ["english"]
                }
            },
            {
                "name": "Missing event_type",
                "data": {
                    "groom_name": "Rajesh",
                    "bride_name": "Priya",
                    "event_date": "2026-02-15T10:00:00",
                    "venue": "Grand Palace", 
                    "enabled_languages": ["english"]
                }
            },
            {
                "name": "Missing event_date",
                "data": {
                    "groom_name": "Rajesh",
                    "bride_name": "Priya",
                    "event_type": "marriage",
                    "venue": "Grand Palace",
                    "enabled_languages": ["english"]
                }
            },
            {
                "name": "Missing venue",
                "data": {
                    "groom_name": "Rajesh", 
                    "bride_name": "Priya",
                    "event_type": "marriage",
                    "event_date": "2026-02-15T10:00:00",
                    "enabled_languages": ["english"]
                }
            }
        ]
        
        # NOTE: enabled_languages is NOT required - it has default value ["english"]
        
        all_passed = True
        
        for i, test_case in enumerate(test_cases):
            print(f"   🔍 Sub-test {i+1}: {test_case['name']}")
            
            response = requests.post(
                f"{BASE_URL}/admin/profiles",
                json=test_case['data'],
                headers=self.get_headers()
            )
            
            print(f"      Status: {response.status_code}")
            
            if response.status_code == 422:
                try:
                    error_detail = response.json()
                    print(f"      ✅ Correctly returned 422 validation error")
                    print(f"      📋 Error: {error_detail.get('detail', 'No detail')}")
                except:
                    print(f"      ✅ Correctly returned 422 (could not parse JSON)")
            else:
                print(f"      ❌ Expected 422, got {response.status_code}")
                try:
                    print(f"      📋 Response: {response.json()}")
                except:
                    print(f"      📋 Raw Response: {response.text}")
                all_passed = False
        
        return all_passed
    
    def test_english_language_requirement(self):
        """Test 3: English Must Be in enabled_languages (Backend Requirement)"""
        
        # Test cases without English in enabled_languages
        test_cases = [
            {
                "name": "Only Telugu (no English)",
                "enabled_languages": ["telugu"]
            },
            {
                "name": "Only Hindi (no English)", 
                "enabled_languages": ["hindi"]
            },
            {
                "name": "Multiple languages without English",
                "enabled_languages": ["telugu", "tamil", "kannada"]
            },
            {
                "name": "Empty languages array",
                "enabled_languages": []
            }
        ]
        
        all_passed = True
        
        for i, test_case in enumerate(test_cases):
            print(f"   🔍 Sub-test {i+1}: {test_case['name']}")
            
            profile_data = {
                "groom_name": "Rajesh",
                "bride_name": "Priya",
                "event_type": "marriage", 
                "event_date": "2026-02-15T10:00:00",
                "venue": "Grand Palace",
                "enabled_languages": test_case["enabled_languages"],
                "events": []
            }
            
            response = requests.post(
                f"{BASE_URL}/admin/profiles",
                json=profile_data,
                headers=self.get_headers()
            )
            
            print(f"      Status: {response.status_code}")
            print(f"      Languages: {test_case['enabled_languages']}")
            
            if response.status_code == 422:
                try:
                    error_detail = response.json()
                    print(f"      ✅ Correctly rejected (English required)")
                    print(f"      📋 Error: {error_detail.get('detail', 'No detail')}")
                except:
                    print(f"      ✅ Correctly rejected (422 response)")
            else:
                print(f"      ❌ Expected 422 validation error, got {response.status_code}")
                if response.status_code == 200:
                    # If it succeeded, clean up the profile
                    try:
                        profile = response.json()
                        self.test_profiles.append(profile["id"])
                    except:
                        pass
                all_passed = False
        
        return all_passed
    
    def test_valid_language_combinations_with_english(self):
        """Test 4: Valid Language Combinations (All Must Include English)"""
        
        test_cases = [
            {
                "name": "English only",
                "enabled_languages": ["english"]
            },
            {
                "name": "English + Telugu",
                "enabled_languages": ["english", "telugu"]
            },
            {
                "name": "English + Tamil + Kannada",
                "enabled_languages": ["english", "tamil", "kannada"]
            },
            {
                "name": "All supported languages",
                "enabled_languages": ["english", "telugu", "tamil", "kannada", "malayalam"]
            }
        ]
        
        all_passed = True
        
        for i, test_case in enumerate(test_cases):
            print(f"   🔍 Sub-test {i+1}: {test_case['name']}")
            
            profile_data = {
                "groom_name": f"Test Groom {i+1}",
                "bride_name": f"Test Bride {i+1}",
                "event_type": "marriage",
                "event_date": "2026-02-15T10:00:00", 
                "venue": "Grand Palace",
                "enabled_languages": test_case["enabled_languages"],
                "events": []
            }
            
            response = requests.post(
                f"{BASE_URL}/admin/profiles",
                json=profile_data,
                headers=self.get_headers()
            )
            
            print(f"      Status: {response.status_code}")
            print(f"      Languages: {test_case['enabled_languages']}")
            
            if response.status_code in [200, 201]:
                profile = response.json()
                self.test_profiles.append(profile["id"])
                print(f"      ✅ Profile created successfully")
                print(f"      📋 Profile ID: {profile['id']}")
                
                # Verify enabled_languages in response
                response_languages = profile.get('enabled_languages', [])
                if set(response_languages) == set(test_case['enabled_languages']):
                    print(f"      ✅ Languages correctly stored: {response_languages}")
                else:
                    print(f"      ❌ Language mismatch - Expected: {test_case['enabled_languages']}, Got: {response_languages}")
                    all_passed = False
            else:
                print(f"      ❌ Profile creation failed: {response.status_code}")
                try:
                    error_detail = response.json()
                    print(f"      📋 Error: {error_detail}")
                except:
                    print(f"      📋 Raw Response: {response.text}")
                all_passed = False
        
        return all_passed
    
    def test_response_format_verification(self):
        """Test 5: Response Format Verification - All Necessary Fields Present"""
        
        profile_data = {
            "groom_name": "Response Test Groom",
            "bride_name": "Response Test Bride",
            "event_type": "marriage",
            "event_date": "2026-02-15T10:00:00",
            "venue": "Grand Palace",
            "enabled_languages": ["english"],
            "events": []
        }
        
        response = requests.post(
            f"{BASE_URL}/admin/profiles",
            json=profile_data,
            headers=self.get_headers()
        )
        
        if response.status_code not in [200, 201]:
            print(f"   ❌ Profile creation failed: {response.status_code}")
            return False
        
        profile = response.json()
        self.test_profiles.append(profile["id"])
        
        # Expected fields in response
        expected_fields = {
            'id': str,
            'slug': str,
            'groom_name': str,
            'bride_name': str,
            'event_type': str,
            'event_date': str,
            'venue': str,
            'enabled_languages': list,
            'events': list,
            'created_at': str,
            'updated_at': str,
            'is_active': bool,
            'invitation_link': str,
            'sections_enabled': dict,
            'design_id': str
        }
        
        print(f"   📋 Verifying response format...")
        
        all_fields_present = True
        for field, expected_type in expected_fields.items():
            if field not in profile:
                print(f"      ❌ Missing field: {field}")
                all_fields_present = False
            else:
                actual_value = profile[field]
                if not isinstance(actual_value, expected_type):
                    print(f"      ❌ Wrong type for {field}: expected {expected_type.__name__}, got {type(actual_value).__name__}")
                    all_fields_present = False
                else:
                    print(f"      ✅ {field}: {expected_type.__name__} ✓")
        
        # Verify specific field values
        if profile.get('groom_name') != profile_data['groom_name']:
            print(f"   ❌ Groom name mismatch")
            all_fields_present = False
        
        if profile.get('bride_name') != profile_data['bride_name']:
            print(f"   ❌ Bride name mismatch") 
            all_fields_present = False
        
        if profile.get('is_active') != True:
            print(f"   ❌ Profile should be active by default")
            all_fields_present = False
        
        if not profile.get('invitation_link', '').startswith('/invite/'):
            print(f"   ❌ Invalid invitation_link format: {profile.get('invitation_link')}")
            all_fields_present = False
        
        if all_fields_present:
            print(f"   ✅ All expected fields present with correct types")
            print(f"   ✅ Field values match input data")
            
        return all_fields_present
    
    def cleanup_test_profiles(self):
        """Clean up test profiles"""
        if not self.test_profiles:
            return
            
        print(f"\n🧹 Cleaning up {len(self.test_profiles)} test profiles...")
        
        for profile_id in self.test_profiles:
            try:
                response = requests.delete(
                    f"{BASE_URL}/admin/profiles/{profile_id}",
                    headers=self.get_headers()
                )
                if response.status_code == 200:
                    print(f"   ✓ Deleted profile {profile_id}")
                else:
                    print(f"   ⚠️ Failed to delete profile {profile_id}: {response.status_code}")
            except Exception as e:
                print(f"   ⚠️ Error deleting profile {profile_id}: {str(e)}")
    
    def run_all_tests(self):
        """Run all admin profile save tests"""
        print("🚀 Starting Admin Profile Save Functionality Testing")
        print("=" * 70)
        print("🎯 FOCUS: Testing 422 error scenarios and validation")
        print("=" * 70)
        
        if not self.authenticate():
            return False
        
        # Run all tests
        tests = [
            ("Profile Creation with Minimal Required Fields (Success Case)", self.test_minimal_profile_creation_success),
            ("Missing Required Fields Validation (422 Errors)", self.test_missing_required_fields_validation),
            ("English Language Requirement Validation", self.test_english_language_requirement),
            ("Valid Language Combinations with English", self.test_valid_language_combinations_with_english),
            ("Response Format Verification", self.test_response_format_verification)
        ]
        
        for test_name, test_func in tests:
            self.run_test(test_name, test_func)
        
        # Cleanup
        self.cleanup_test_profiles()
        
        # Summary
        print("\n" + "=" * 70)
        print("📊 ADMIN PROFILE SAVE TESTING SUMMARY")
        print("=" * 70)
        print(f"✅ Passed: {self.passed_tests}/{self.total_tests} tests")
        print(f"❌ Failed: {self.total_tests - self.passed_tests}/{self.total_tests} tests")
        
        if self.passed_tests == self.total_tests:
            print("🎉 ALL ADMIN PROFILE SAVE TESTS PASSED!")
            print("✅ Admin profile save functionality is working correctly")
            print("✅ 422 validation errors are working as expected")
            return True
        else:
            print("⚠️ Some tests failed - Admin profile save needs attention")
            return False

def main():
    """Main function"""
    tester = AdminProfileSaveTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎯 ADMIN PROFILE SAVE TESTING COMPLETE - ALL TESTS PASSED!")
        sys.exit(0)
    else:
        print("\n❌ ADMIN PROFILE SAVE TESTING FAILED")
        sys.exit(1)

if __name__ == "__main__":
    main()