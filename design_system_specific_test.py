#!/usr/bin/env python3
"""
Specific Design System Testing for Wedding Invitation Platform
Testing the exact requirements from the review request
"""

import requests
import json
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/frontend/.env')

# Get backend URL from environment
BACKEND_URL = os.getenv('REACT_APP_BACKEND_URL', 'http://localhost:8001')
API_BASE = f"{BACKEND_URL}/api"

print(f"🔗 Testing backend at: {API_BASE}")

class DesignSystemTester:
    def __init__(self):
        self.session = requests.Session()
        self.admin_token = None
        self.test_profiles = []  # Store test profile data
        
    def log_test(self, test_name, success, details=""):
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   {details}")
        if not success:
            print()
    
    def admin_login(self):
        """Login with admin credentials from review request"""
        print("\n🔐 Admin Authentication...")
        
        login_data = {
            "email": "admin@wedding.com",
            "password": "admin123"
        }
        
        try:
            response = self.session.post(f"{API_BASE}/auth/login", json=login_data)
            
            if response.status_code == 200:
                data = response.json()
                if "access_token" in data:
                    self.admin_token = data["access_token"]
                    self.session.headers.update({"Authorization": f"Bearer {self.admin_token}"})
                    self.log_test("Admin Login", True, f"Authenticated as: {data['admin']['email']}")
                    return True
                else:
                    self.log_test("Admin Login", False, "Missing access token")
                    return False
            else:
                self.log_test("Admin Login", False, f"Status: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Admin Login", False, f"Exception: {str(e)}")
            return False
    
    def test_1_profile_creation_default_design(self):
        """Test 1: Create a profile without specifying design_id - should default to 'temple_divine'"""
        print("\n📝 TEST 1: Profile Creation with Default Design...")
        
        if not self.admin_token:
            self.log_test("Test 1 - Default Design", False, "No admin token")
            return False
        
        profile_data = {
            "groom_name": "Arjun Mehta",
            "bride_name": "Kavya Reddy",
            "event_type": "marriage",
            "event_date": (datetime.now() + timedelta(days=30)).isoformat(),
            "venue": "Taj Falaknuma Palace, Hyderabad",
            "language": ["english", "telugu"],
            "sections_enabled": {
                "opening": True,
                "welcome": True,
                "couple": True,
                "photos": True,
                "video": False,
                "events": True,
                "greetings": True,
                "footer": True
            }
            # NOT specifying design_id - should default to temple_divine
        }
        
        try:
            response = self.session.post(f"{API_BASE}/admin/profiles", json=profile_data)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("design_id") == "temple_divine":
                    self.test_profiles.append({
                        "id": data["id"],
                        "slug": data["slug"],
                        "design_id": data["design_id"],
                        "names": f"{data['groom_name']} & {data['bride_name']}"
                    })
                    self.log_test("Test 1 - Default Design", True, 
                                f"✅ Profile defaults to 'temple_divine' as expected")
                    return True
                else:
                    self.log_test("Test 1 - Default Design", False, 
                                f"Expected 'temple_divine', got '{data.get('design_id')}'")
                    return False
            else:
                self.log_test("Test 1 - Default Design", False, 
                            f"Profile creation failed: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Test 1 - Default Design", False, f"Exception: {str(e)}")
            return False
    
    def test_2_profile_creation_specific_designs(self):
        """Test 2: Create profiles with each of the 8 design IDs"""
        print("\n🎨 TEST 2: Profile Creation with Specific Designs...")
        
        if not self.admin_token:
            self.log_test("Test 2 - Specific Designs", False, "No admin token")
            return False
        
        # All 8 design IDs from the review request
        design_ids = [
            "temple_divine",
            "royal_classic", 
            "floral_soft",
            "cinematic_luxury",
            "heritage_scroll",
            "minimal_elegant",
            "modern_premium",
            "artistic_handcrafted"
        ]
        
        all_passed = True
        
        for i, design_id in enumerate(design_ids):
            profile_data = {
                "groom_name": f"Test Groom {i+1}",
                "bride_name": f"Test Bride {i+1}",
                "event_type": "marriage",
                "event_date": (datetime.now() + timedelta(days=35 + i)).isoformat(),
                "venue": f"Test Venue {i+1}",
                "language": ["english"],
                "design_id": design_id,  # Specific design
                "sections_enabled": {
                    "opening": True,
                    "welcome": True,
                    "couple": True,
                    "photos": True,
                    "video": False,
                    "events": True,
                    "greetings": True,
                    "footer": True
                }
            }
            
            try:
                response = self.session.post(f"{API_BASE}/admin/profiles", json=profile_data)
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if data.get("design_id") == design_id:
                        self.test_profiles.append({
                            "id": data["id"],
                            "slug": data["slug"],
                            "design_id": data["design_id"],
                            "names": f"{data['groom_name']} & {data['bride_name']}"
                        })
                        self.log_test(f"Design: {design_id}", True, 
                                    f"✅ Profile created with design '{design_id}'")
                    else:
                        self.log_test(f"Design: {design_id}", False, 
                                    f"Expected '{design_id}', got '{data.get('design_id')}'")
                        all_passed = False
                else:
                    self.log_test(f"Design: {design_id}", False, 
                                f"Creation failed: {response.status_code}")
                    all_passed = False
                    
            except Exception as e:
                self.log_test(f"Design: {design_id}", False, f"Exception: {str(e)}")
                all_passed = False
        
        return all_passed
    
    def test_3_profile_update_design(self):
        """Test 3: Update a profile's design_id to a different theme"""
        print("\n🔄 TEST 3: Profile Update Design...")
        
        if not self.admin_token or not self.test_profiles:
            self.log_test("Test 3 - Update Design", False, "No admin token or test profiles")
            return False
        
        # Use first test profile and update its design
        profile = self.test_profiles[0]
        original_design = profile["design_id"]
        new_design = "cinematic_luxury"  # Change to different design
        
        update_data = {
            "design_id": new_design
        }
        
        try:
            response = self.session.put(f"{API_BASE}/admin/profiles/{profile['id']}", json=update_data)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("design_id") == new_design:
                    # Update our test profile record
                    profile["design_id"] = new_design
                    self.log_test("Test 3 - Update Design", True, 
                                f"✅ Design updated from '{original_design}' to '{new_design}'")
                    return True
                else:
                    self.log_test("Test 3 - Update Design", False, 
                                f"Expected '{new_design}', got '{data.get('design_id')}'")
                    return False
            else:
                self.log_test("Test 3 - Update Design", False, 
                            f"Update failed: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Test 3 - Update Design", False, f"Exception: {str(e)}")
            return False
    
    def test_4_profile_retrieval(self):
        """Test 4: GET profile by ID and GET all profiles - verify design_id is included"""
        print("\n📋 TEST 4: Profile Retrieval...")
        
        if not self.admin_token or not self.test_profiles:
            self.log_test("Test 4 - Profile Retrieval", False, "No admin token or test profiles")
            return False
        
        profile = self.test_profiles[0]
        
        try:
            # Test 4a: GET single profile by ID
            response = self.session.get(f"{API_BASE}/admin/profiles/{profile['id']}")
            
            if response.status_code == 200:
                data = response.json()
                
                if "design_id" in data and data["design_id"] == profile["design_id"]:
                    self.log_test("Test 4a - GET Profile by ID", True, 
                                f"✅ design_id '{data['design_id']}' included in response")
                else:
                    self.log_test("Test 4a - GET Profile by ID", False, 
                                f"design_id missing or incorrect: {data.get('design_id')}")
                    return False
            else:
                self.log_test("Test 4a - GET Profile by ID", False, 
                            f"Request failed: {response.status_code}")
                return False
            
            # Test 4b: GET all profiles
            response = self.session.get(f"{API_BASE}/admin/profiles")
            
            if response.status_code == 200:
                profiles = response.json()
                
                # Find our test profile in the list
                our_profile = next((p for p in profiles if p["id"] == profile["id"]), None)
                
                if our_profile and "design_id" in our_profile:
                    self.log_test("Test 4b - GET All Profiles", True, 
                                f"✅ design_id '{our_profile['design_id']}' included in profiles list")
                    return True
                else:
                    self.log_test("Test 4b - GET All Profiles", False, 
                                "design_id missing in profiles list")
                    return False
            else:
                self.log_test("Test 4b - GET All Profiles", False, 
                            f"Request failed: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Test 4 - Profile Retrieval", False, f"Exception: {str(e)}")
            return False
    
    def test_5_public_invitation_api(self):
        """Test 5: GET /api/invite/:slug and verify design_id is returned"""
        print("\n🌐 TEST 5: Public Invitation API...")
        
        if not self.test_profiles:
            self.log_test("Test 5 - Public Invitation", False, "No test profiles")
            return False
        
        profile = self.test_profiles[0]
        
        try:
            # Use a new session without auth headers for public access
            public_session = requests.Session()
            response = public_session.get(f"{API_BASE}/invite/{profile['slug']}")
            
            if response.status_code == 200:
                data = response.json()
                
                if "design_id" in data and data["design_id"] == profile["design_id"]:
                    self.log_test("Test 5 - Public Invitation", True, 
                                f"✅ design_id '{data['design_id']}' returned in public invitation")
                    return True
                else:
                    self.log_test("Test 5 - Public Invitation", False, 
                                f"design_id missing or incorrect: {data.get('design_id')}")
                    return False
            else:
                self.log_test("Test 5 - Public Invitation", False, 
                            f"Public invitation failed: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Test 5 - Public Invitation", False, f"Exception: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all design system tests as specified in review request"""
        print("🚀 DESIGN SYSTEM TESTING - REVIEW REQUEST REQUIREMENTS")
        print("=" * 70)
        print("Admin Credentials: admin@wedding.com / admin123")
        print("=" * 70)
        
        test_results = []
        
        # Authentication
        if not self.admin_login():
            print("❌ Cannot proceed without authentication")
            return False
        
        # Run all 5 tests from review request
        test_results.append(self.test_1_profile_creation_default_design())
        test_results.append(self.test_2_profile_creation_specific_designs())
        test_results.append(self.test_3_profile_update_design())
        test_results.append(self.test_4_profile_retrieval())
        test_results.append(self.test_5_public_invitation_api())
        
        # Summary
        passed = sum(test_results)
        total = len(test_results)
        
        print("\n" + "=" * 70)
        print(f"🏁 DESIGN SYSTEM TEST SUMMARY: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 ALL DESIGN SYSTEM REQUIREMENTS VERIFIED!")
            print("✅ Profile creation with default design works")
            print("✅ Profile creation with all 8 specific designs works")
            print("✅ Profile design update works")
            print("✅ Profile retrieval includes design_id")
            print("✅ Public invitation API returns design_id")
            print("\n🎯 Backend design system is production-ready!")
            return True
        else:
            failed = total - passed
            print(f"⚠️  {failed} tests failed. Issues need attention!")
            return False

def main():
    """Main test execution"""
    tester = DesignSystemTester()
    success = tester.run_all_tests()
    
    if success:
        exit(0)
    else:
        exit(1)

if __name__ == "__main__":
    main()