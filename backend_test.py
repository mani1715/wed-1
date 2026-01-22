#!/usr/bin/env python3
"""
COMPREHENSIVE BACKEND TESTING - MULTI-EVENT INVITATION SYSTEM
Testing all EventInvitation CRUD operations and public endpoints
"""

import requests
import json
import sys
from datetime import datetime, timezone

# Configuration
BASE_URL = "https://wed-organizer-18.preview.emergentagent.com/api"
ADMIN_EMAIL = "admin@wedding.com"
ADMIN_PASSWORD = "admin123"

class BackendTester:
    def __init__(self):
        self.base_url = BASE_URL
        self.token = None
        self.profile_id = None
        self.slug = None
        self.event_invitations = {}  # Store created event invitations
        
    def log(self, message):
        """Log test messages"""
        print(f"[TEST] {message}")
        
    def error(self, message):
        """Log error messages"""
        print(f"[ERROR] {message}")
        
    def success(self, message):
        """Log success messages"""
        print(f"[SUCCESS] {message}")
        
    def login_admin(self):
        """Phase 1: Login as admin and get JWT token"""
        self.log("Phase 1: Admin Login")
        
        login_data = {
            "email": ADMIN_EMAIL,
            "password": ADMIN_PASSWORD
        }
        
        response = requests.post(f"{self.base_url}/auth/login", json=login_data)
        
        if response.status_code == 200:
            data = response.json()
            self.token = data["access_token"]
            self.success(f"Admin login successful. Token: {self.token[:20]}...")
            return True
        else:
            self.error(f"Admin login failed: {response.status_code} - {response.text}")
            return False
    
    def get_headers(self):
        """Get authorization headers"""
        return {"Authorization": f"Bearer {self.token}"}
    
    def create_test_profile(self):
        """Phase 1: Create a test profile for testing"""
        self.log("Phase 1: Creating test profile (Rajesh & Priya wedding)")
        
        profile_data = {
            "groom_name": "Rajesh Kumar",
            "bride_name": "Priya Sharma",
            "event_type": "marriage",
            "event_date": "2024-12-25T10:00:00Z",
            "venue": "Grand Palace Hotel, Mumbai",
            "city": "Mumbai",
            "invitation_message": "Join us in celebrating our special day",
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
        
        response = requests.post(
            f"{self.base_url}/admin/profiles",
            json=profile_data,
            headers=self.get_headers()
        )
        
        if response.status_code == 200:
            data = response.json()
            self.profile_id = data["id"]
            self.slug = data["slug"]
            self.success(f"Test profile created successfully. ID: {self.profile_id}, Slug: {self.slug}")
            return True
        else:
            self.error(f"Profile creation failed: {response.status_code} - {response.text}")
            return False
    
    def test_get_empty_event_invitations(self):
        """Phase 2: Test 4 - GET empty event invitations"""
        self.log("Test 4: GET /api/admin/profiles/{profile_id}/event-invitations (should return empty array)")
        
        response = requests.get(
            f"{self.base_url}/admin/profiles/{self.profile_id}/event-invitations",
            headers=self.get_headers()
        )
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) == 0:
                self.success("✅ GET event invitations returns empty array initially")
                return True
            else:
                self.error(f"Expected empty array, got: {data}")
                return False
        else:
            self.error(f"GET event invitations failed: {response.status_code} - {response.text}")
            return False
    
    def test_create_engagement_invitation(self):
        """Phase 2: Test 5 - Create engagement event invitation"""
        self.log("Test 5: POST /api/admin/profiles/{profile_id}/event-invitations (engagement)")
        
        invitation_data = {
            "event_type": "engagement",
            "design_id": "royal_classic",
            "deity_id": "ganesha"
        }
        
        response = requests.post(
            f"{self.base_url}/admin/profiles/{self.profile_id}/event-invitations",
            json=invitation_data,
            headers=self.get_headers()
        )
        
        if response.status_code == 200:
            data = response.json()
            if (data.get("event_type") == "engagement" and 
                data.get("design_id") == "royal_classic" and
                data.get("deity_id") == "ganesha" and
                "invitation_link" in data and
                data["invitation_link"] == f"/invite/{self.slug}/engagement"):
                
                self.event_invitations["engagement"] = data
                self.success("✅ Engagement event invitation created successfully")
                self.success(f"   Invitation link: {data['invitation_link']}")
                self.success(f"   Deity ID allowed for engagement: {data['deity_id']}")
                return True
            else:
                self.error(f"Engagement invitation data incorrect: {data}")
                return False
        else:
            self.error(f"Engagement invitation creation failed: {response.status_code} - {response.text}")
            return False
    
    def test_create_haldi_invitation(self):
        """Phase 2: Test 6 - Create haldi event invitation (deity should be forced to null)"""
        self.log("Test 6: POST /api/admin/profiles/{profile_id}/event-invitations (haldi - deity forced to null)")
        
        invitation_data = {
            "event_type": "haldi",
            "design_id": "floral_soft",
            "deity_id": "ganesha"  # This should be forced to null
        }
        
        response = requests.post(
            f"{self.base_url}/admin/profiles/{self.profile_id}/event-invitations",
            json=invitation_data,
            headers=self.get_headers()
        )
        
        if response.status_code == 200:
            data = response.json()
            if (data.get("event_type") == "haldi" and 
                data.get("design_id") == "floral_soft" and
                data.get("deity_id") is None and  # Should be forced to null
                "invitation_link" in data):
                
                self.event_invitations["haldi"] = data
                self.success("✅ Haldi event invitation created successfully")
                self.success(f"   Deity ID forced to null for Haldi: {data['deity_id']}")
                return True
            else:
                self.error(f"Haldi invitation data incorrect: {data}")
                return False
        else:
            self.error(f"Haldi invitation creation failed: {response.status_code} - {response.text}")
            return False
    
    def test_create_mehendi_invitation(self):
        """Phase 2: Test 7 - Create mehendi event invitation (deity should be forced to null)"""
        self.log("Test 7: POST /api/admin/profiles/{profile_id}/event-invitations (mehendi - deity forced to null)")
        
        invitation_data = {
            "event_type": "mehendi",
            "design_id": "temple_divine",
            "deity_id": "shiva_parvati"  # This should be forced to null
        }
        
        response = requests.post(
            f"{self.base_url}/admin/profiles/{self.profile_id}/event-invitations",
            json=invitation_data,
            headers=self.get_headers()
        )
        
        if response.status_code == 200:
            data = response.json()
            if (data.get("event_type") == "mehendi" and 
                data.get("design_id") == "temple_divine" and
                data.get("deity_id") is None and  # Should be forced to null
                "invitation_link" in data):
                
                self.event_invitations["mehendi"] = data
                self.success("✅ Mehendi event invitation created successfully")
                self.success(f"   Deity ID forced to null for Mehendi: {data['deity_id']}")
                return True
            else:
                self.error(f"Mehendi invitation data incorrect: {data}")
                return False
        else:
            self.error(f"Mehendi invitation creation failed: {response.status_code} - {response.text}")
            return False
    
    def test_create_duplicate_engagement(self):
        """Phase 2: Test 8 - Try to create duplicate engagement invitation (should fail)"""
        self.log("Test 8: POST duplicate engagement invitation (should return 400 error)")
        
        invitation_data = {
            "event_type": "engagement",
            "design_id": "floral_soft",
            "deity_id": "lakshmi_vishnu"
        }
        
        response = requests.post(
            f"{self.base_url}/admin/profiles/{self.profile_id}/event-invitations",
            json=invitation_data,
            headers=self.get_headers()
        )
        
        if response.status_code == 400:
            self.success("✅ Duplicate engagement invitation correctly rejected with 400 error")
            return True
        else:
            self.error(f"Expected 400 error for duplicate, got: {response.status_code} - {response.text}")
            return False
    
    def test_get_all_event_invitations(self):
        """Phase 2: Test 9 - GET all event invitations (should return 3)"""
        self.log("Test 9: GET /api/admin/profiles/{profile_id}/event-invitations (should return 3 invitations)")
        
        response = requests.get(
            f"{self.base_url}/admin/profiles/{self.profile_id}/event-invitations",
            headers=self.get_headers()
        )
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) == 3:
                event_types = [inv["event_type"] for inv in data]
                expected_types = ["engagement", "haldi", "mehendi"]
                
                if all(et in event_types for et in expected_types):
                    self.success("✅ GET event invitations returns 3 invitations (engagement, haldi, mehendi)")
                    
                    # Verify invitation links
                    for inv in data:
                        expected_link = f"/invite/{self.slug}/{inv['event_type']}"
                        if inv["invitation_link"] == expected_link:
                            self.success(f"   ✅ {inv['event_type']} link correct: {inv['invitation_link']}")
                        else:
                            self.error(f"   ❌ {inv['event_type']} link incorrect: {inv['invitation_link']}")
                    
                    return True
                else:
                    self.error(f"Expected event types {expected_types}, got: {event_types}")
                    return False
            else:
                self.error(f"Expected 3 invitations, got: {len(data) if isinstance(data, list) else 'not a list'}")
                return False
        else:
            self.error(f"GET event invitations failed: {response.status_code} - {response.text}")
            return False
    
    def test_update_haldi_invitation(self):
        """Phase 2: Test 10 - Update haldi invitation design"""
        self.log("Test 10: PUT /api/admin/event-invitations/{invitation_id} (update haldi design)")
        
        haldi_invitation = self.event_invitations.get("haldi")
        if not haldi_invitation:
            self.error("Haldi invitation not found in stored invitations")
            return False
        
        update_data = {
            "design_id": "temple_divine"
        }
        
        response = requests.put(
            f"{self.base_url}/admin/event-invitations/{haldi_invitation['id']}",
            json=update_data,
            headers=self.get_headers()
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("design_id") == "temple_divine":
                self.success("✅ Haldi invitation design updated successfully")
                self.event_invitations["haldi"] = data  # Update stored data
                return True
            else:
                self.error(f"Design update failed, got: {data}")
                return False
        else:
            self.error(f"Haldi invitation update failed: {response.status_code} - {response.text}")
            return False
    
    def test_disable_engagement_invitation(self):
        """Phase 2: Test 11 - Disable engagement invitation"""
        self.log("Test 11: PUT /api/admin/event-invitations/{invitation_id} (disable engagement)")
        
        engagement_invitation = self.event_invitations.get("engagement")
        if not engagement_invitation:
            self.error("Engagement invitation not found in stored invitations")
            return False
        
        update_data = {
            "enabled": False
        }
        
        response = requests.put(
            f"{self.base_url}/admin/event-invitations/{engagement_invitation['id']}",
            json=update_data,
            headers=self.get_headers()
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("enabled") is False:
                self.success("✅ Engagement invitation disabled successfully")
                self.event_invitations["engagement"] = data  # Update stored data
                return True
            else:
                self.error(f"Disable failed, got: {data}")
                return False
        else:
            self.error(f"Engagement invitation disable failed: {response.status_code} - {response.text}")
            return False
    
    def test_public_disabled_engagement(self):
        """Phase 3: Test 12 - GET disabled engagement invitation (should return 404)"""
        self.log("Test 12: GET /api/invite/{slug}/engagement (should return 404 - disabled)")
        
        response = requests.get(f"{self.base_url}/invite/{self.slug}/engagement")
        
        if response.status_code == 404:
            self.success("✅ Disabled engagement invitation correctly returns 404")
            return True
        else:
            self.error(f"Expected 404 for disabled invitation, got: {response.status_code} - {response.text}")
            return False
    
    def test_enable_engagement_invitation(self):
        """Phase 3: Test 13 - Re-enable engagement invitation"""
        self.log("Test 13: PUT /api/admin/event-invitations/{invitation_id} (re-enable engagement)")
        
        engagement_invitation = self.event_invitations.get("engagement")
        if not engagement_invitation:
            self.error("Engagement invitation not found in stored invitations")
            return False
        
        update_data = {
            "enabled": True
        }
        
        response = requests.put(
            f"{self.base_url}/admin/event-invitations/{engagement_invitation['id']}",
            json=update_data,
            headers=self.get_headers()
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("enabled") is True:
                self.success("✅ Engagement invitation re-enabled successfully")
                self.event_invitations["engagement"] = data  # Update stored data
                return True
            else:
                self.error(f"Re-enable failed, got: {data}")
                return False
        else:
            self.error(f"Engagement invitation re-enable failed: {response.status_code} - {response.text}")
            return False
    
    def test_public_enabled_engagement(self):
        """Phase 3: Test 14 - GET enabled engagement invitation"""
        self.log("Test 14: GET /api/invite/{slug}/engagement (should return invitation data)")
        
        response = requests.get(f"{self.base_url}/invite/{self.slug}/engagement")
        
        if response.status_code == 200:
            data = response.json()
            
            # Verify it uses EventInvitation design_id and deity_id
            engagement_invitation = self.event_invitations.get("engagement")
            if (data.get("design_id") == engagement_invitation.get("design_id") and
                data.get("deity_id") == engagement_invitation.get("deity_id") and
                data.get("slug") == self.slug):
                
                self.success("✅ Enabled engagement invitation returns correct data")
                self.success(f"   Uses EventInvitation design_id: {data['design_id']}")
                self.success(f"   Uses EventInvitation deity_id: {data['deity_id']}")
                self.success(f"   Includes profile data: {data['groom_name']} & {data['bride_name']}")
                return True
            else:
                self.error(f"Engagement invitation data incorrect: {data}")
                return False
        else:
            self.error(f"Enabled engagement invitation failed: {response.status_code} - {response.text}")
            return False
    
    def test_public_haldi_invitation(self):
        """Phase 3: Test 15 - GET haldi invitation (deity should be null)"""
        self.log("Test 15: GET /api/invite/{slug}/haldi (deity should be null)")
        
        response = requests.get(f"{self.base_url}/invite/{self.slug}/haldi")
        
        if response.status_code == 200:
            data = response.json()
            
            if (data.get("deity_id") is None and
                data.get("slug") == self.slug):
                
                self.success("✅ Haldi invitation returns correct data")
                self.success(f"   Deity ID is null (no lord background): {data['deity_id']}")
                return True
            else:
                self.error(f"Haldi invitation data incorrect: {data}")
                return False
        else:
            self.error(f"Haldi invitation failed: {response.status_code} - {response.text}")
            return False
    
    def test_public_nonexistent_reception(self):
        """Phase 3: Test 16 - GET reception invitation (should return 404 - not created)"""
        self.log("Test 16: GET /api/invite/{slug}/reception (should return 404 - not created)")
        
        response = requests.get(f"{self.base_url}/invite/{self.slug}/reception")
        
        if response.status_code == 404:
            self.success("✅ Non-existent reception invitation correctly returns 404")
            return True
        else:
            self.error(f"Expected 404 for non-existent reception, got: {response.status_code} - {response.text}")
            return False
    
    def test_delete_haldi_invitation(self):
        """Phase 3: Test 17 - Delete haldi invitation"""
        self.log("Test 17: DELETE /api/admin/event-invitations/{invitation_id} (delete haldi)")
        
        haldi_invitation = self.event_invitations.get("haldi")
        if not haldi_invitation:
            self.error("Haldi invitation not found in stored invitations")
            return False
        
        response = requests.delete(
            f"{self.base_url}/admin/event-invitations/{haldi_invitation['id']}",
            headers=self.get_headers()
        )
        
        if response.status_code == 200:
            self.success("✅ Haldi invitation deleted successfully")
            del self.event_invitations["haldi"]  # Remove from stored data
            return True
        else:
            self.error(f"Haldi invitation deletion failed: {response.status_code} - {response.text}")
            return False
    
    def test_get_remaining_invitations(self):
        """Phase 3: Test 18 - GET remaining invitations (should be 2)"""
        self.log("Test 18: GET /api/admin/profiles/{profile_id}/event-invitations (should return 2 invitations)")
        
        response = requests.get(
            f"{self.base_url}/admin/profiles/{self.profile_id}/event-invitations",
            headers=self.get_headers()
        )
        
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list) and len(data) == 2:
                event_types = [inv["event_type"] for inv in data]
                expected_types = ["engagement", "mehendi"]
                
                if all(et in event_types for et in expected_types):
                    self.success("✅ GET event invitations returns 2 remaining invitations (engagement, mehendi)")
                    return True
                else:
                    self.error(f"Expected event types {expected_types}, got: {event_types}")
                    return False
            else:
                self.error(f"Expected 2 invitations, got: {len(data) if isinstance(data, list) else 'not a list'}")
                return False
        else:
            self.error(f"GET remaining invitations failed: {response.status_code} - {response.text}")
            return False
    
    def test_invalid_event_type(self):
        """Validation Test 19 - Try invalid event_type"""
        self.log("Test 19: POST invalid event_type 'birthday' (should return validation error)")
        
        invitation_data = {
            "event_type": "birthday",
            "design_id": "royal_classic",
            "deity_id": "ganesha"
        }
        
        response = requests.post(
            f"{self.base_url}/admin/profiles/{self.profile_id}/event-invitations",
            json=invitation_data,
            headers=self.get_headers()
        )
        
        if response.status_code == 422:  # Validation error
            self.success("✅ Invalid event_type 'birthday' correctly rejected with validation error")
            return True
        else:
            self.error(f"Expected 422 validation error for invalid event_type, got: {response.status_code} - {response.text}")
            return False
    
    def test_invalid_profile_id(self):
        """Validation Test 20 - Try invalid profile_id"""
        self.log("Test 20: POST to invalid profile_id (should return 404)")
        
        invitation_data = {
            "event_type": "marriage",
            "design_id": "royal_classic",
            "deity_id": "ganesha"
        }
        
        response = requests.post(
            f"{self.base_url}/admin/profiles/invalid-profile-id/event-invitations",
            json=invitation_data,
            headers=self.get_headers()
        )
        
        if response.status_code == 404:
            self.success("✅ Invalid profile_id correctly returns 404 profile not found")
            return True
        else:
            self.error(f"Expected 404 for invalid profile_id, got: {response.status_code} - {response.text}")
            return False
    
    def run_all_tests(self):
        """Run all tests in sequence"""
        print("=" * 80)
        print("COMPREHENSIVE BACKEND TESTING - MULTI-EVENT INVITATION SYSTEM")
        print("=" * 80)
        
        tests = [
            # Phase 1: Setup & Profile Creation
            ("Admin Login", self.login_admin),
            ("Create Test Profile", self.create_test_profile),
            
            # Phase 2: EventInvitation CRUD Operations
            ("Test 4: GET Empty Event Invitations", self.test_get_empty_event_invitations),
            ("Test 5: Create Engagement Invitation", self.test_create_engagement_invitation),
            ("Test 6: Create Haldi Invitation (Deity Forced Null)", self.test_create_haldi_invitation),
            ("Test 7: Create Mehendi Invitation (Deity Forced Null)", self.test_create_mehendi_invitation),
            ("Test 8: Create Duplicate Engagement (Should Fail)", self.test_create_duplicate_engagement),
            ("Test 9: GET All Event Invitations (Should Return 3)", self.test_get_all_event_invitations),
            ("Test 10: Update Haldi Invitation Design", self.test_update_haldi_invitation),
            ("Test 11: Disable Engagement Invitation", self.test_disable_engagement_invitation),
            
            # Phase 3: Public Invitation Endpoints
            ("Test 12: GET Disabled Engagement (Should Return 404)", self.test_public_disabled_engagement),
            ("Test 13: Re-enable Engagement Invitation", self.test_enable_engagement_invitation),
            ("Test 14: GET Enabled Engagement Invitation", self.test_public_enabled_engagement),
            ("Test 15: GET Haldi Invitation (Deity Null)", self.test_public_haldi_invitation),
            ("Test 16: GET Non-existent Reception (Should Return 404)", self.test_public_nonexistent_reception),
            ("Test 17: Delete Haldi Invitation", self.test_delete_haldi_invitation),
            ("Test 18: GET Remaining Invitations (Should Return 2)", self.test_get_remaining_invitations),
            
            # Validation Tests
            ("Test 19: Invalid Event Type Validation", self.test_invalid_event_type),
            ("Test 20: Invalid Profile ID Validation", self.test_invalid_profile_id),
        ]
        
        passed = 0
        failed = 0
        
        for test_name, test_func in tests:
            print(f"\n{'='*60}")
            print(f"Running: {test_name}")
            print('='*60)
            
            try:
                if test_func():
                    passed += 1
                    print(f"✅ PASSED: {test_name}")
                else:
                    failed += 1
                    print(f"❌ FAILED: {test_name}")
            except Exception as e:
                failed += 1
                self.error(f"Exception in {test_name}: {str(e)}")
                print(f"❌ FAILED: {test_name} (Exception)")
        
        # Final Results
        print("\n" + "="*80)
        print("FINAL TEST RESULTS")
        print("="*80)
        print(f"Total Tests: {passed + failed}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Success Rate: {(passed / (passed + failed) * 100):.1f}%")
        
        if failed == 0:
            print("\n🎉 ALL TESTS PASSED! Multi-Event Invitation System is working correctly!")
        else:
            print(f"\n⚠️  {failed} test(s) failed. Please review the errors above.")
        
        return failed == 0

if __name__ == "__main__":
    tester = BackendTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)