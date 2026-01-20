#!/usr/bin/env python3
"""
Specific Design System Tests as requested in the review
Testing the exact scenarios mentioned in the review request
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

class DesignSystemSpecificTester:
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
    
    def login_admin(self):
        """Login as admin"""
        login_data = {
            "email": "admin@wedding.com",
            "password": "admin123"
        }
        
        try:
            response = self.session.post(f"{API_BASE}/auth/login", json=login_data)
            
            if response.status_code == 200:
                data = response.json()
                self.admin_token = data["access_token"]
                self.session.headers.update({"Authorization": f"Bearer {self.admin_token}"})
                print("✅ Admin authentication successful")
                return True
            else:
                print(f"❌ Admin login failed: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Admin login exception: {str(e)}")
            return False
    
    def test_1_create_profile_without_design_id(self):
        """Test 1: Create profile without specifying design_id (should default to "temple_divine")"""
        print("\n📝 Test 1: Create profile without specifying design_id")
        
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
                        "test_name": "Default Design"
                    })
                    self.log_test("Test 1 - Default Design", True, 
                                f"✅ Profile created with default design_id: {data['design_id']}")
                    return True
                else:
                    self.log_test("Test 1 - Default Design", False, 
                                f"Expected 'temple_divine', got: {data.get('design_id')}")
                    return False
            else:
                self.log_test("Test 1 - Default Design", False, 
                            f"Profile creation failed: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Test 1 - Default Design", False, f"Exception: {str(e)}")
            return False
    
    def test_2_create_profile_with_royal_classic(self):
        """Test 2: Create profile with design_id="royal_classic" """
        print("\n📝 Test 2: Create profile with design_id='royal_classic'")
        
        profile_data = {
            "groom_name": "Vikram Singh",
            "bride_name": "Priya Sharma",
            "event_type": "marriage",
            "event_date": (datetime.now() + timedelta(days=45)).isoformat(),
            "venue": "ITC Grand Chola, Chennai",
            "language": ["english", "hindi"],
            "design_id": "royal_classic",  # Specific design
            "sections_enabled": {
                "opening": True,
                "welcome": True,
                "couple": True,
                "photos": True,
                "video": True,
                "events": True,
                "greetings": True,
                "footer": True
            }
        }
        
        try:
            response = self.session.post(f"{API_BASE}/admin/profiles", json=profile_data)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("design_id") == "royal_classic":
                    self.test_profiles.append({
                        "id": data["id"],
                        "slug": data["slug"],
                        "design_id": data["design_id"],
                        "test_name": "Royal Classic Design"
                    })
                    self.log_test("Test 2 - Royal Classic Design", True, 
                                f"✅ Profile created with design_id: {data['design_id']}")
                    return True
                else:
                    self.log_test("Test 2 - Royal Classic Design", False, 
                                f"Expected 'royal_classic', got: {data.get('design_id')}")
                    return False
            else:
                self.log_test("Test 2 - Royal Classic Design", False, 
                            f"Profile creation failed: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Test 2 - Royal Classic Design", False, f"Exception: {str(e)}")
            return False
    
    def test_3_create_profile_with_floral_soft(self):
        """Test 3: Create profile with design_id="floral_soft" """
        print("\n📝 Test 3: Create profile with design_id='floral_soft'")
        
        profile_data = {
            "groom_name": "Rohit Kumar",
            "bride_name": "Ananya Iyer",
            "event_type": "engagement",
            "event_date": (datetime.now() + timedelta(days=60)).isoformat(),
            "venue": "Leela Palace, Bangalore",
            "language": ["english", "tamil"],
            "design_id": "floral_soft",  # Specific design
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
                
                if data.get("design_id") == "floral_soft":
                    self.test_profiles.append({
                        "id": data["id"],
                        "slug": data["slug"],
                        "design_id": data["design_id"],
                        "test_name": "Floral Soft Design"
                    })
                    self.log_test("Test 3 - Floral Soft Design", True, 
                                f"✅ Profile created with design_id: {data['design_id']}")
                    return True
                else:
                    self.log_test("Test 3 - Floral Soft Design", False, 
                                f"Expected 'floral_soft', got: {data.get('design_id')}")
                    return False
            else:
                self.log_test("Test 3 - Floral Soft Design", False, 
                            f"Profile creation failed: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Test 3 - Floral Soft Design", False, f"Exception: {str(e)}")
            return False
    
    def test_4_update_profile_design(self):
        """Test 4: Update existing profile to change design_id from temple_divine to cinematic_luxury"""
        print("\n📝 Test 4: Update profile design from temple_divine to cinematic_luxury")
        
        if not self.test_profiles:
            self.log_test("Test 4 - Update Design", False, "No test profiles available")
            return False
        
        # Use the first profile (temple_divine)
        profile = self.test_profiles[0]
        
        update_data = {
            "design_id": "cinematic_luxury"
        }
        
        try:
            response = self.session.put(f"{API_BASE}/admin/profiles/{profile['id']}", json=update_data)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get("design_id") == "cinematic_luxury":
                    # Update our test profile record
                    profile["design_id"] = "cinematic_luxury"
                    self.log_test("Test 4 - Update Design", True, 
                                f"✅ Design updated from temple_divine to: {data['design_id']}")
                    return True
                else:
                    self.log_test("Test 4 - Update Design", False, 
                                f"Expected 'cinematic_luxury', got: {data.get('design_id')}")
                    return False
            else:
                self.log_test("Test 4 - Update Design", False, 
                            f"Profile update failed: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Test 4 - Update Design", False, f"Exception: {str(e)}")
            return False
    
    def test_5_get_profile_by_id(self):
        """Test 5: GET profile by ID and verify design_id is in response"""
        print("\n📝 Test 5: GET profile by ID and verify design_id in response")
        
        if not self.test_profiles:
            self.log_test("Test 5 - Get Profile by ID", False, "No test profiles available")
            return False
        
        # Test the updated profile
        profile = self.test_profiles[0]
        
        try:
            response = self.session.get(f"{API_BASE}/admin/profiles/{profile['id']}")
            
            if response.status_code == 200:
                data = response.json()
                
                if "design_id" in data and data["design_id"] == profile["design_id"]:
                    self.log_test("Test 5 - Get Profile by ID", True, 
                                f"✅ design_id present in response: {data['design_id']}")
                    return True
                else:
                    self.log_test("Test 5 - Get Profile by ID", False, 
                                f"design_id missing or incorrect: {data.get('design_id')}")
                    return False
            else:
                self.log_test("Test 5 - Get Profile by ID", False, 
                            f"Get profile failed: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Test 5 - Get Profile by ID", False, f"Exception: {str(e)}")
            return False
    
    def test_6_get_public_invitation(self):
        """Test 6: GET public invitation and verify design_id is in response"""
        print("\n📝 Test 6: GET public invitation and verify design_id in response")
        
        if not self.test_profiles:
            self.log_test("Test 6 - Public Invitation", False, "No test profiles available")
            return False
        
        # Test multiple profiles
        success_count = 0
        
        for profile in self.test_profiles:
            try:
                # Use new session without auth for public access
                public_session = requests.Session()
                response = public_session.get(f"{API_BASE}/invite/{profile['slug']}")
                
                if response.status_code == 200:
                    data = response.json()
                    
                    if "design_id" in data and data["design_id"] == profile["design_id"]:
                        self.log_test(f"Test 6 - Public Invitation ({profile['test_name']})", True, 
                                    f"✅ design_id present: {data['design_id']}")
                        success_count += 1
                    else:
                        self.log_test(f"Test 6 - Public Invitation ({profile['test_name']})", False, 
                                    f"design_id missing or incorrect: {data.get('design_id')}")
                else:
                    self.log_test(f"Test 6 - Public Invitation ({profile['test_name']})", False, 
                                f"Public invitation failed: {response.status_code}")
                    
            except Exception as e:
                self.log_test(f"Test 6 - Public Invitation ({profile['test_name']})", False, f"Exception: {str(e)}")
        
        return success_count == len(self.test_profiles)
    
    def test_7_create_all_8_designs(self):
        """Test 7: Create profiles with all 8 design IDs and verify each is stored correctly"""
        print("\n📝 Test 7: Create profiles with all 8 design IDs")
        
        all_designs = [
            "temple_divine", "royal_classic", "floral_soft", "cinematic_luxury",
            "heritage_scroll", "minimal_elegant", "modern_premium", "artistic_handcrafted"
        ]
        
        success_count = 0
        
        for i, design_id in enumerate(all_designs):
            profile_data = {
                "groom_name": f"Test Groom {design_id.title()}",
                "bride_name": f"Test Bride {design_id.title()}",
                "event_type": "marriage",
                "event_date": (datetime.now() + timedelta(days=70 + i)).isoformat(),
                "venue": f"Test Venue for {design_id}",
                "language": ["english"],
                "design_id": design_id,
                "sections_enabled": {
                    "opening": True,
                    "welcome": True,
                    "couple": True,
                    "photos": False,
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
                        self.log_test(f"Test 7 - Design {design_id}", True, 
                                    f"✅ Profile created with design: {design_id}")
                        success_count += 1
                    else:
                        self.log_test(f"Test 7 - Design {design_id}", False, 
                                    f"Expected {design_id}, got: {data.get('design_id')}")
                else:
                    self.log_test(f"Test 7 - Design {design_id}", False, 
                                f"Profile creation failed: {response.status_code}")
                    
            except Exception as e:
                self.log_test(f"Test 7 - Design {design_id}", False, f"Exception: {str(e)}")
        
        return success_count == len(all_designs)
    
    def run_all_tests(self):
        """Run all specific tests as mentioned in review request"""
        print("🚀 Starting SPECIFIC Design System Tests as per Review Request")
        print("=" * 80)
        
        # Login first
        if not self.login_admin():
            print("❌ Cannot proceed without authentication")
            return False
        
        test_results = []
        
        # Run all specific tests
        test_results.append(self.test_1_create_profile_without_design_id())
        test_results.append(self.test_2_create_profile_with_royal_classic())
        test_results.append(self.test_3_create_profile_with_floral_soft())
        test_results.append(self.test_4_update_profile_design())
        test_results.append(self.test_5_get_profile_by_id())
        test_results.append(self.test_6_get_public_invitation())
        test_results.append(self.test_7_create_all_8_designs())
        
        # Summary
        passed = sum(test_results)
        total = len(test_results)
        
        print("\n" + "=" * 80)
        print(f"🏁 SPECIFIC DESIGN SYSTEM TEST SUMMARY: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 ALL SPECIFIC DESIGN SYSTEM TESTS PASSED!")
            print("✅ Design system backend integration working correctly")
            return True
        else:
            failed = total - passed
            print(f"⚠️  {failed} specific tests failed")
            return False

def main():
    """Main test execution"""
    tester = DesignSystemSpecificTester()
    
    success = tester.run_all_tests()
    
    if success:
        print("\n✅ All specific design system tests completed successfully!")
        exit(0)
    else:
        print("\n❌ Some specific design system tests failed!")
        exit(1)

if __name__ == "__main__":
    main()