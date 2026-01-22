#!/usr/bin/env python3
"""
MULTI-EVENT INVITATION SYSTEM Backend Testing
Tests all backend APIs for the event invitation system
"""

import requests
import json
import sys
from datetime import datetime, timedelta

# Configuration
BASE_URL = "https://marry-mate-13.preview.emergentagent.com/api"
ADMIN_EMAIL = "admin@wedding.com"
ADMIN_PASSWORD = "admin123"

class EventInvitationTester:
    def __init__(self):
        self.token = None
        self.profile_id = None
        self.profile_slug = None
        self.event_invitations = []
        self.test_results = []
        
    def log_test(self, test_name, success, message="", details=None):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name}")
        if message:
            print(f"    {message}")
        if details:
            print(f"    Details: {details}")
        
        self.test_results.append({
            "test": test_name,
            "success": success,
            "message": message,
            "details": details
        })
        print()
    
    def admin_login(self):
        """Test 1: Admin Authentication"""
        print("🔐 Testing Admin Authentication...")
        
        try:
            response = requests.post(f"{BASE_URL}/auth/login", json={
                "email": ADMIN_EMAIL,
                "password": ADMIN_PASSWORD
            }, verify=True, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get("access_token")
                self.log_test("Admin Login", True, f"Token received: {self.token[:20]}...")
                return True
            else:
                self.log_test("Admin Login", False, f"Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Admin Login", False, f"Exception: {str(e)}")
            return False
    
    def create_test_profile(self):
        """Test 2: Create Test Profile"""
        print("👰 Creating Test Profile...")
        
        if not self.token:
            self.log_test("Create Test Profile", False, "No authentication token")
            return False
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        # Create profile with realistic Indian wedding data
        profile_data = {
            "groom_name": "Rajesh Kumar",
            "bride_name": "Priya Sharma",
            "event_type": "marriage",
            "event_date": (datetime.now() + timedelta(days=30)).isoformat(),
            "venue": "Grand Palace Banquet Hall",
            "city": "Mumbai",
            "invitation_message": "Join us in celebrating our union",
            "language": ["english", "telugu"],
            "design_id": "royal_classic",
            "deity_id": "ganesha",
            "whatsapp_groom": "+919876543210",
            "whatsapp_bride": "+919876543211",
            "enabled_languages": ["english", "telugu"],
            "sections_enabled": {
                "opening": True,
                "welcome": True,
                "couple": True,
                "about": True,
                "family": True,
                "love_story": True,
                "photos": True,
                "video": False,
                "events": True,
                "rsvp": True,
                "greetings": True,
                "footer": True,
                "contact": True,
                "calendar": True,
                "countdown": True,
                "qr": True
            },
            "background_music": {
                "enabled": False,
                "file_url": None
            },
            "map_settings": {
                "embed_enabled": False
            },
            "contact_info": {
                "groom_phone": "+919876543210",
                "bride_phone": "+919876543211",
                "emergency_phone": "+919876543212",
                "email": "rajesh.priya@wedding.com"
            },
            "events": [],
            "link_expiry_type": "days",
            "link_expiry_value": 30
        }
        
        try:
            response = requests.post(f"{BASE_URL}/admin/profiles", 
                                   json=profile_data, headers=headers, 
                                   verify=True, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                self.profile_id = data.get("id")
                self.profile_slug = data.get("slug")
                self.log_test("Create Test Profile", True, 
                            f"Profile created - ID: {self.profile_id}, Slug: {self.profile_slug}")
                return True
            else:
                self.log_test("Create Test Profile", False, 
                            f"Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Create Test Profile", False, f"Exception: {str(e)}")
            return False
    
    def test_get_empty_event_invitations(self):
        """Test 3a: GET Event Invitations (Empty)"""
        print("📋 Testing GET Event Invitations (Empty)...")
        
        if not self.token or not self.profile_id:
            self.log_test("GET Empty Event Invitations", False, "Missing token or profile_id")
            return False
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        try:
            response = requests.get(f"{BASE_URL}/admin/profiles/{self.profile_id}/event-invitations", 
                                  headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) == 0:
                    self.log_test("GET Empty Event Invitations", True, "Returns empty array initially")
                    return True
                else:
                    self.log_test("GET Empty Event Invitations", False, 
                                f"Expected empty array, got: {data}")
                    return False
            else:
                self.log_test("GET Empty Event Invitations", False, 
                            f"Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("GET Empty Event Invitations", False, f"Exception: {str(e)}")
            return False
    
    def test_create_event_invitations(self):
        """Test 3b: POST Create Event Invitations"""
        print("➕ Testing Create Event Invitations...")
        
        if not self.token or not self.profile_id:
            self.log_test("Create Event Invitations", False, "Missing token or profile_id")
            return False
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        # Test 1: Create Engagement event invitation with lord background
        print("  Test 1: Create Engagement with deity_id: ganesha")
        try:
            engagement_data = {
                "event_type": "engagement",
                "design_id": "royal_classic",
                "deity_id": "ganesha"
            }
            
            response = requests.post(f"{BASE_URL}/admin/profiles/{self.profile_id}/event-invitations", 
                                   json=engagement_data, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                expected_link = f"/invite/{self.profile_slug}/engagement"
                if data.get("invitation_link") == expected_link:
                    self.event_invitations.append(data)
                    self.log_test("Create Engagement Event", True, 
                                f"Success - Link: {data.get('invitation_link')}")
                else:
                    self.log_test("Create Engagement Event", False, 
                                f"Wrong invitation_link: {data.get('invitation_link')}")
                    return False
            else:
                self.log_test("Create Engagement Event", False, 
                            f"Status: {response.status_code}, Response: {response.text}")
                return False
        except Exception as e:
            self.log_test("Create Engagement Event", False, f"Exception: {str(e)}")
            return False
        
        # Test 2: Create Haldi event invitation with deity_id (should fail)
        print("  Test 2: Create Haldi with deity_id: ganesha (should fail)")
        try:
            haldi_data = {
                "event_type": "haldi",
                "design_id": "floral_soft",
                "deity_id": "ganesha"
            }
            
            response = requests.post(f"{BASE_URL}/admin/profiles/{self.profile_id}/event-invitations", 
                                   json=haldi_data, headers=headers)
            
            if response.status_code == 422:
                self.log_test("Create Haldi with Deity (Validation)", True, 
                            "Correctly rejected deity for Haldi event")
            else:
                self.log_test("Create Haldi with Deity (Validation)", False, 
                            f"Should have failed with 422, got: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Create Haldi with Deity (Validation)", False, f"Exception: {str(e)}")
            return False
        
        # Test 3: Create Haldi event invitation with deity_id: null
        print("  Test 3: Create Haldi with deity_id: null")
        try:
            haldi_data = {
                "event_type": "haldi",
                "design_id": "floral_soft",
                "deity_id": None
            }
            
            response = requests.post(f"{BASE_URL}/admin/profiles/{self.profile_id}/event-invitations", 
                                   json=haldi_data, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                expected_link = f"/invite/{self.profile_slug}/haldi"
                if data.get("invitation_link") == expected_link:
                    self.event_invitations.append(data)
                    self.log_test("Create Haldi Event", True, 
                                f"Success - Link: {data.get('invitation_link')}")
                else:
                    self.log_test("Create Haldi Event", False, 
                                f"Wrong invitation_link: {data.get('invitation_link')}")
                    return False
            else:
                self.log_test("Create Haldi Event", False, 
                            f"Status: {response.status_code}, Response: {response.text}")
                return False
        except Exception as e:
            self.log_test("Create Haldi Event", False, f"Exception: {str(e)}")
            return False
        
        # Test 4: Create Marriage event invitation with deity_id: lakshmi_vishnu
        print("  Test 4: Create Marriage with deity_id: lakshmi_vishnu")
        try:
            marriage_data = {
                "event_type": "marriage",
                "design_id": "temple_divine",
                "deity_id": "lakshmi_vishnu"
            }
            
            response = requests.post(f"{BASE_URL}/admin/profiles/{self.profile_id}/event-invitations", 
                                   json=marriage_data, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                expected_link = f"/invite/{self.profile_slug}/marriage"
                if data.get("invitation_link") == expected_link:
                    self.event_invitations.append(data)
                    self.log_test("Create Marriage Event", True, 
                                f"Success - Link: {data.get('invitation_link')}")
                else:
                    self.log_test("Create Marriage Event", False, 
                                f"Wrong invitation_link: {data.get('invitation_link')}")
                    return False
            else:
                self.log_test("Create Marriage Event", False, 
                            f"Status: {response.status_code}, Response: {response.text}")
                return False
        except Exception as e:
            self.log_test("Create Marriage Event", False, f"Exception: {str(e)}")
            return False
        
        # Test 5: Create duplicate Engagement invitation (should fail)
        print("  Test 5: Create duplicate Engagement (should fail)")
        try:
            duplicate_data = {
                "event_type": "engagement",
                "design_id": "modern_premium",
                "deity_id": "shiva_parvati"
            }
            
            response = requests.post(f"{BASE_URL}/admin/profiles/{self.profile_id}/event-invitations", 
                                   json=duplicate_data, headers=headers)
            
            if response.status_code == 400:
                self.log_test("Create Duplicate Event (Validation)", True, 
                            "Correctly rejected duplicate event type")
            else:
                self.log_test("Create Duplicate Event (Validation)", False, 
                            f"Should have failed with 400, got: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Create Duplicate Event (Validation)", False, f"Exception: {str(e)}")
            return False
        
        return True
    
    def test_get_event_invitations_list(self):
        """Test 3c: GET Event Invitations (List)"""
        print("📋 Testing GET Event Invitations (List)...")
        
        if not self.token or not self.profile_id:
            self.log_test("GET Event Invitations List", False, "Missing token or profile_id")
            return False
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        try:
            response = requests.get(f"{BASE_URL}/admin/profiles/{self.profile_id}/event-invitations", 
                                  headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) == 3:
                    # Verify each event invitation
                    event_types = [ei.get("event_type") for ei in data]
                    expected_types = ["engagement", "haldi", "marriage"]
                    
                    if all(et in event_types for et in expected_types):
                        # Check invitation links
                        for ei in data:
                            expected_link = f"/invite/{self.profile_slug}/{ei['event_type']}"
                            if ei.get("invitation_link") != expected_link:
                                self.log_test("GET Event Invitations List", False, 
                                            f"Wrong link for {ei['event_type']}: {ei.get('invitation_link')}")
                                return False
                        
                        self.log_test("GET Event Invitations List", True, 
                                    f"Returns 3 event invitations: {event_types}")
                        return True
                    else:
                        self.log_test("GET Event Invitations List", False, 
                                    f"Wrong event types: {event_types}")
                        return False
                else:
                    self.log_test("GET Event Invitations List", False, 
                                f"Expected 3 invitations, got: {len(data) if isinstance(data, list) else 'not a list'}")
                    return False
            else:
                self.log_test("GET Event Invitations List", False, 
                            f"Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("GET Event Invitations List", False, f"Exception: {str(e)}")
            return False
    
    def test_update_event_invitations(self):
        """Test 3d: PUT Update Event Invitations"""
        print("✏️ Testing Update Event Invitations...")
        
        if not self.token or len(self.event_invitations) < 3:
            self.log_test("Update Event Invitations", False, "Missing token or event invitations")
            return False
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        # Find engagement invitation
        engagement_invitation = None
        haldi_invitation = None
        marriage_invitation = None
        
        for ei in self.event_invitations:
            if ei.get("event_type") == "engagement":
                engagement_invitation = ei
            elif ei.get("event_type") == "haldi":
                haldi_invitation = ei
            elif ei.get("event_type") == "marriage":
                marriage_invitation = ei
        
        # Test 1: Update Engagement invitation design
        print("  Test 1: Update Engagement design_id to 'floral_soft'")
        if engagement_invitation:
            try:
                update_data = {"design_id": "floral_soft"}
                
                response = requests.put(f"{BASE_URL}/admin/event-invitations/{engagement_invitation['id']}", 
                                      json=update_data, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("design_id") == "floral_soft":
                        self.log_test("Update Engagement Design", True, 
                                    f"Design updated to: {data.get('design_id')}")
                    else:
                        self.log_test("Update Engagement Design", False, 
                                    f"Design not updated: {data.get('design_id')}")
                        return False
                else:
                    self.log_test("Update Engagement Design", False, 
                                f"Status: {response.status_code}, Response: {response.text}")
                    return False
            except Exception as e:
                self.log_test("Update Engagement Design", False, f"Exception: {str(e)}")
                return False
        
        # Test 2: Try to add deity to Haldi (should fail)
        print("  Test 2: Try to add deity_id to Haldi (should fail)")
        if haldi_invitation:
            try:
                update_data = {"deity_id": "ganesha"}
                
                response = requests.put(f"{BASE_URL}/admin/event-invitations/{haldi_invitation['id']}", 
                                      json=update_data, headers=headers)
                
                if response.status_code == 422:
                    self.log_test("Update Haldi Deity (Validation)", True, 
                                "Correctly rejected deity for Haldi")
                else:
                    # Check if deity was forced to null (backend enforcement)
                    if response.status_code == 200:
                        data = response.json()
                        if data.get("deity_id") is None:
                            self.log_test("Update Haldi Deity (Validation)", True, 
                                        "Backend enforced deity_id=null for Haldi")
                        else:
                            self.log_test("Update Haldi Deity (Validation)", False, 
                                        f"Deity should be null, got: {data.get('deity_id')}")
                            return False
                    else:
                        self.log_test("Update Haldi Deity (Validation)", False, 
                                    f"Unexpected status: {response.status_code}")
                        return False
            except Exception as e:
                self.log_test("Update Haldi Deity (Validation)", False, f"Exception: {str(e)}")
                return False
        
        # Test 3: Disable Marriage invitation
        print("  Test 3: Set Marriage invitation enabled=false")
        if marriage_invitation:
            try:
                update_data = {"enabled": False}
                
                response = requests.put(f"{BASE_URL}/admin/event-invitations/{marriage_invitation['id']}", 
                                      json=update_data, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("enabled") == False:
                        self.log_test("Disable Marriage Event", True, 
                                    f"Marriage invitation disabled: {data.get('enabled')}")
                        # Update our local copy
                        marriage_invitation["enabled"] = False
                    else:
                        self.log_test("Disable Marriage Event", False, 
                                    f"Enabled not updated: {data.get('enabled')}")
                        return False
                else:
                    self.log_test("Disable Marriage Event", False, 
                                f"Status: {response.status_code}, Response: {response.text}")
                    return False
            except Exception as e:
                self.log_test("Disable Marriage Event", False, f"Exception: {str(e)}")
                return False
        
        return True
    
    def test_delete_event_invitation(self):
        """Test 3e: DELETE Event Invitation"""
        print("🗑️ Testing Delete Event Invitation...")
        
        if not self.token or len(self.event_invitations) < 1:
            self.log_test("Delete Event Invitation", False, "Missing token or event invitations")
            return False
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        # Delete the first event invitation (engagement)
        invitation_to_delete = self.event_invitations[0]
        
        try:
            response = requests.delete(f"{BASE_URL}/admin/event-invitations/{invitation_to_delete['id']}", 
                                     headers=headers)
            
            if response.status_code == 200:
                self.log_test("Delete Event Invitation", True, 
                            f"Deleted {invitation_to_delete['event_type']} invitation")
                
                # Verify it's removed from the list
                list_response = requests.get(f"{BASE_URL}/admin/profiles/{self.profile_id}/event-invitations", 
                                           headers=headers)
                
                if list_response.status_code == 200:
                    data = list_response.json()
                    event_types = [ei.get("event_type") for ei in data]
                    
                    if invitation_to_delete['event_type'] not in event_types:
                        self.log_test("Verify Deletion", True, 
                                    f"Event removed from list. Remaining: {event_types}")
                        return True
                    else:
                        self.log_test("Verify Deletion", False, 
                                    f"Event still in list: {event_types}")
                        return False
                else:
                    self.log_test("Verify Deletion", False, 
                                f"Failed to get updated list: {list_response.status_code}")
                    return False
            else:
                self.log_test("Delete Event Invitation", False, 
                            f"Status: {response.status_code}, Response: {response.text}")
                return False
                
        except Exception as e:
            self.log_test("Delete Event Invitation", False, f"Exception: {str(e)}")
            return False
    
    def test_public_event_invitation_apis(self):
        """Test 4: Public Event Invitation APIs"""
        print("🌐 Testing Public Event Invitation APIs...")
        
        if not self.profile_slug:
            self.log_test("Public Event APIs", False, "Missing profile slug")
            return False
        
        # Test 4a: GET event-specific public view (Haldi - should work)
        print("  Test 4a: GET /api/invite/{slug}/haldi")
        try:
            response = requests.get(f"{BASE_URL}/invite/{self.profile_slug}/haldi")
            
            if response.status_code == 200:
                data = response.json()
                # Should return invitation data with design_id from EventInvitation
                if data.get("design_id") == "floral_soft":  # Haldi was created with floral_soft
                    self.log_test("Public Haldi Event View", True, 
                                f"Returns correct design_id: {data.get('design_id')}")
                else:
                    self.log_test("Public Haldi Event View", False, 
                                f"Wrong design_id: {data.get('design_id')}")
                    return False
            else:
                self.log_test("Public Haldi Event View", False, 
                            f"Status: {response.status_code}, Response: {response.text}")
                return False
        except Exception as e:
            self.log_test("Public Haldi Event View", False, f"Exception: {str(e)}")
            return False
        
        # Test 4b: GET disabled event (Marriage - should return 404)
        print("  Test 4b: GET /api/invite/{slug}/marriage (disabled)")
        try:
            response = requests.get(f"{BASE_URL}/invite/{self.profile_slug}/marriage")
            
            if response.status_code == 404:
                self.log_test("Public Disabled Event View", True, 
                            "Correctly returns 404 for disabled event")
            else:
                self.log_test("Public Disabled Event View", False, 
                            f"Should return 404, got: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Public Disabled Event View", False, f"Exception: {str(e)}")
            return False
        
        # Test 4c: GET non-existent event invitation (Reception)
        print("  Test 4c: GET /api/invite/{slug}/reception (non-existent)")
        try:
            response = requests.get(f"{BASE_URL}/invite/{self.profile_slug}/reception")
            
            # Should either return 404 or fallback to WeddingEvent logic
            if response.status_code in [404, 200]:
                self.log_test("Public Non-existent Event View", True, 
                            f"Handles non-existent event correctly: {response.status_code}")
            else:
                self.log_test("Public Non-existent Event View", False, 
                            f"Unexpected status: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Public Non-existent Event View", False, f"Exception: {str(e)}")
            return False
        
        return True
    
    def test_validation_rules(self):
        """Test 5: Validation Rules"""
        print("🔍 Testing Validation Rules...")
        
        if not self.token or not self.profile_id:
            self.log_test("Validation Rules", False, "Missing token or profile_id")
            return False
        
        headers = {"Authorization": f"Bearer {self.token}"}
        
        # Test invalid event_type
        print("  Test: Invalid event_type")
        try:
            invalid_data = {
                "event_type": "birthday",  # Invalid
                "design_id": "royal_classic",
                "deity_id": None
            }
            
            response = requests.post(f"{BASE_URL}/admin/profiles/{self.profile_id}/event-invitations", 
                                   json=invalid_data, headers=headers)
            
            if response.status_code == 422:
                self.log_test("Invalid Event Type Validation", True, 
                            "Correctly rejected invalid event_type")
            else:
                self.log_test("Invalid Event Type Validation", False, 
                            f"Should reject invalid event_type, got: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Invalid Event Type Validation", False, f"Exception: {str(e)}")
            return False
        
        # Test invalid deity_id
        print("  Test: Invalid deity_id")
        try:
            invalid_data = {
                "event_type": "reception",
                "design_id": "royal_classic",
                "deity_id": "invalid_deity"  # Invalid
            }
            
            response = requests.post(f"{BASE_URL}/admin/profiles/{self.profile_id}/event-invitations", 
                                   json=invalid_data, headers=headers)
            
            if response.status_code == 422:
                self.log_test("Invalid Deity ID Validation", True, 
                            "Correctly rejected invalid deity_id")
            else:
                self.log_test("Invalid Deity ID Validation", False, 
                            f"Should reject invalid deity_id, got: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Invalid Deity ID Validation", False, f"Exception: {str(e)}")
            return False
        
        return True
    
    def run_all_tests(self):
        """Run all tests in sequence"""
        print("🚀 Starting MULTI-EVENT INVITATION SYSTEM Backend Tests\n")
        
        # Test sequence
        tests = [
            ("Admin Authentication", self.admin_login),
            ("Create Test Profile", self.create_test_profile),
            ("GET Empty Event Invitations", self.test_get_empty_event_invitations),
            ("Create Event Invitations", self.test_create_event_invitations),
            ("GET Event Invitations List", self.test_get_event_invitations_list),
            ("Update Event Invitations", self.test_update_event_invitations),
            ("Delete Event Invitation", self.test_delete_event_invitation),
            ("Public Event Invitation APIs", self.test_public_event_invitation_apis),
            ("Validation Rules", self.test_validation_rules)
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            print(f"{'='*60}")
            print(f"Running: {test_name}")
            print(f"{'='*60}")
            
            if test_func():
                passed += 1
            else:
                print(f"❌ Test '{test_name}' failed. Stopping execution.")
                break
        
        # Summary
        print(f"\n{'='*60}")
        print(f"🎯 TEST SUMMARY")
        print(f"{'='*60}")
        print(f"Passed: {passed}/{total}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("🎉 ALL TESTS PASSED! MULTI-EVENT INVITATION SYSTEM is working correctly.")
        else:
            print("❌ Some tests failed. Please check the implementation.")
        
        return passed == total

def main():
    """Main test execution"""
    tester = EventInvitationTester()
    success = tester.run_all_tests()
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()