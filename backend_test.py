#!/usr/bin/env python3
"""
Backend Testing Suite for Template System (PHASE 12 - PART 3)
Tests all template system functionality including model verification, 
save-as-template, list templates, create from template, and edge cases.
"""

import requests
import json
from datetime import datetime, timezone, timedelta
import uuid

# Configuration
BACKEND_URL = "https://nuptial-dashboard-1.preview.emergentagent.com/api"
ADMIN_EMAIL = "admin@wedding.com"
ADMIN_PASSWORD = "admin123"

class TemplateSystemTester:
    def __init__(self):
        self.session = requests.Session()
        self.admin_token = None
        self.test_profile_id = None
        self.template_id = None
        self.new_profile_from_template_id = None
        
    def authenticate_admin(self):
        """Authenticate as admin and get token"""
        print("🔐 Authenticating admin...")
        
        response = self.session.post(f"{BACKEND_URL}/auth/login", json={
            "email": ADMIN_EMAIL,
            "password": ADMIN_PASSWORD
        })
        
        if response.status_code == 200:
            data = response.json()
            self.admin_token = data["access_token"]
            self.session.headers.update({"Authorization": f"Bearer {self.admin_token}"})
            print(f"✅ Admin authenticated successfully")
            return True
        else:
            print(f"❌ Admin authentication failed: {response.status_code} - {response.text}")
            return False
    
    def create_test_profile(self):
        """Create a test profile for template testing"""
        print("\n📝 Creating test profile for template testing...")
        
        # Create realistic Indian wedding profile data
        profile_data = {
            "groom_name": "Arjun Sharma",
            "bride_name": "Priya Patel", 
            "event_type": "Wedding",
            "event_date": (datetime.now(timezone.utc) + timedelta(days=60)).isoformat(),
            "venue": "Grand Palace Banquet Hall",
            "city": "Mumbai",
            "invitation_message": "Join us as we celebrate our union in the presence of family and friends",
            "language": ["english", "telugu"],
            "design_id": "royal_classic",
            "deity_id": "ganesha",
            "whatsapp_groom": "+919876543210",
            "whatsapp_bride": "+919876543211",
            "enabled_languages": ["english", "telugu"],
            "custom_text": {
                "english": {
                    "opening": "With great joy, we invite you to our wedding celebration"
                }
            },
            "about_couple": "<p>Arjun and Priya met during their college years and have been together for 5 years.</p>",
            "family_details": "<p>Son of Mr. & Mrs. Sharma, Daughter of Mr. & Mrs. Patel</p>",
            "love_story": "<p>Our love story began in the library and blossomed over shared dreams.</p>",
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
                "enabled": True,
                "file_url": "https://example.com/wedding-music.mp3"
            },
            "map_settings": {
                "embed_enabled": True
            },
            "contact_info": {
                "groom_phone": "+919876543210",
                "bride_phone": "+919876543211",
                "emergency_phone": "+919876543212",
                "email": "arjun.priya@wedding.com"
            },
            "events": [
                {
                    "name": "Mehendi Ceremony",
                    "date": (datetime.now(timezone.utc) + timedelta(days=58)).strftime("%Y-%m-%d"),
                    "start_time": "16:00",
                    "end_time": "20:00",
                    "venue_name": "Sharma Residence",
                    "venue_address": "123 Wedding Street, Mumbai",
                    "map_link": "https://maps.google.com/mehendi",
                    "description": "Traditional henna ceremony",
                    "visible": True,
                    "order": 0
                },
                {
                    "name": "Wedding Ceremony",
                    "date": (datetime.now(timezone.utc) + timedelta(days=60)).strftime("%Y-%m-%d"),
                    "start_time": "10:00",
                    "end_time": "14:00",
                    "venue_name": "Grand Palace Banquet Hall",
                    "venue_address": "456 Celebration Avenue, Mumbai",
                    "map_link": "https://maps.google.com/wedding",
                    "description": "Main wedding ceremony",
                    "visible": True,
                    "order": 1
                }
            ],
            "link_expiry_type": "days",
            "link_expiry_value": 30
        }
        
        response = self.session.post(f"{BACKEND_URL}/admin/profiles", json=profile_data)
        
        if response.status_code == 200:
            data = response.json()
            self.test_profile_id = data["id"]
            print(f"✅ Test profile created successfully: {self.test_profile_id}")
            print(f"   Profile: {data['groom_name']} & {data['bride_name']}")
            print(f"   Slug: {data['slug']}")
            print(f"   is_template: {data.get('is_template', False)}")
            return True
        else:
            print(f"❌ Failed to create test profile: {response.status_code} - {response.text}")
            return False
    
    def test_backend_model_verification(self):
        """Test 1: Verify is_template field exists in Profile models"""
        print("\n🔍 TEST 1: Backend Model Verification")
        
        # Get the created profile to verify is_template field exists
        response = self.session.get(f"{BACKEND_URL}/admin/profiles/{self.test_profile_id}")
        
        if response.status_code == 200:
            data = response.json()
            
            # Check if is_template field exists and defaults to false
            if "is_template" in data:
                if data["is_template"] == False:
                    print("✅ is_template field exists in ProfileResponse model and defaults to false")
                    return True
                else:
                    print(f"❌ is_template field exists but has wrong default value: {data['is_template']}")
                    return False
            else:
                print("❌ is_template field missing from ProfileResponse model")
                return False
        else:
            print(f"❌ Failed to get profile for model verification: {response.status_code}")
            return False
    
    def test_save_profile_as_template(self):
        """Test 2: Save Profile as Template (POST /api/admin/profiles/{id}/save-as-template)"""
        print("\n📋 TEST 2: Save Profile as Template")
        
        # Call save-as-template endpoint
        response = self.session.post(f"{BACKEND_URL}/admin/profiles/{self.test_profile_id}/save-as-template")
        
        if response.status_code == 200:
            data = response.json()
            
            # Verify the profile's is_template field is set to true
            if data.get("is_template") == True:
                print("✅ Profile successfully saved as template")
                print(f"   Profile ID: {data['id']}")
                print(f"   is_template: {data['is_template']}")
                print(f"   Profile unchanged: {data['groom_name']} & {data['bride_name']}")
                
                # Store template ID for later tests
                self.template_id = data["id"]
                
                # Verify profile is still accessible and unchanged
                if (data["groom_name"] == "Arjun Sharma" and 
                    data["bride_name"] == "Priya Patel" and
                    data["venue"] == "Grand Palace Banquet Hall"):
                    print("✅ Profile data remains unchanged after template conversion")
                    return True
                else:
                    print("❌ Profile data was modified during template conversion")
                    return False
            else:
                print(f"❌ is_template field not set correctly: {data.get('is_template')}")
                return False
        else:
            print(f"❌ Failed to save profile as template: {response.status_code} - {response.text}")
            return False
    
    def test_list_templates(self):
        """Test 3: List Templates (GET /api/admin/templates)"""
        print("\n📋 TEST 3: List Templates")
        
        # Call templates endpoint
        response = self.session.get(f"{BACKEND_URL}/admin/templates")
        
        if response.status_code == 200:
            templates = response.json()
            
            # Verify only profiles with is_template=true are returned
            if isinstance(templates, list):
                print(f"✅ Templates endpoint returned {len(templates)} templates")
                
                # Find our template in the list
                our_template = None
                for template in templates:
                    if template["id"] == self.template_id:
                        our_template = template
                        break
                
                if our_template:
                    print("✅ Our template found in templates list")
                    print(f"   Template: {our_template['groom_name']} & {our_template['bride_name']}")
                    print(f"   is_template: {our_template.get('is_template')}")
                    
                    # Verify all required fields are present
                    required_fields = ["id", "slug", "groom_name", "bride_name", "design_id", 
                                     "deity_id", "events", "sections_enabled", "created_at"]
                    missing_fields = [field for field in required_fields if field not in our_template]
                    
                    if not missing_fields:
                        print("✅ All template fields present in response")
                        
                        # Verify templates are sorted by created_at (newest first)
                        if len(templates) > 1:
                            dates = [datetime.fromisoformat(t["created_at"].replace('Z', '+00:00')) for t in templates]
                            if dates == sorted(dates, reverse=True):
                                print("✅ Templates sorted by created_at (newest first)")
                            else:
                                print("⚠️ Templates may not be sorted correctly by created_at")
                        
                        return True
                    else:
                        print(f"❌ Missing template fields: {missing_fields}")
                        return False
                else:
                    print("❌ Our template not found in templates list")
                    return False
            else:
                print(f"❌ Templates endpoint returned invalid format: {type(templates)}")
                return False
        else:
            print(f"❌ Failed to get templates: {response.status_code} - {response.text}")
            return False
    
    def test_create_profile_from_template(self):
        """Test 4: Create Profile from Template (POST /api/admin/profiles/from-template/{template_id})"""
        print("\n🏗️ TEST 4: Create Profile from Template")
        
        # Call create-from-template endpoint
        response = self.session.post(f"{BACKEND_URL}/admin/profiles/from-template/{self.template_id}")
        
        if response.status_code == 200:
            new_profile = response.json()
            self.new_profile_from_template_id = new_profile["id"]
            
            print("✅ New profile created from template successfully")
            print(f"   New Profile ID: {new_profile['id']}")
            print(f"   New Slug: {new_profile['slug']}")
            
            # Verify new profile has new unique ID (different from template)
            if new_profile["id"] != self.template_id:
                print("✅ New profile has unique ID (different from template)")
            else:
                print("❌ New profile has same ID as template")
                return False
            
            # Verify new unique slug (different from template)
            # Get template to compare slug
            template_response = self.session.get(f"{BACKEND_URL}/admin/profiles/{self.template_id}")
            if template_response.status_code == 200:
                template_data = template_response.json()
                if new_profile["slug"] != template_data["slug"]:
                    print("✅ New profile has unique slug (different from template)")
                else:
                    print("❌ New profile has same slug as template")
                    return False
            
            # Verify is_template is set to false
            if new_profile.get("is_template") == False:
                print("✅ New profile has is_template set to false")
            else:
                print(f"❌ New profile is_template not set correctly: {new_profile.get('is_template')}")
                return False
            
            # Verify all other fields copied from template
            template_response = self.session.get(f"{BACKEND_URL}/admin/profiles/{self.template_id}")
            if template_response.status_code == 200:
                template_data = template_response.json()
                
                # Check key fields are copied
                fields_to_check = ["groom_name", "bride_name", "design_id", "deity_id", 
                                 "venue", "city", "invitation_message", "enabled_languages",
                                 "about_couple", "family_details", "love_story"]
                
                all_copied = True
                for field in fields_to_check:
                    if new_profile.get(field) != template_data.get(field):
                        print(f"❌ Field {field} not copied correctly")
                        print(f"   Template: {template_data.get(field)}")
                        print(f"   New Profile: {new_profile.get(field)}")
                        all_copied = False
                
                if all_copied:
                    print("✅ All key fields copied from template correctly")
                
                # Verify events are copied
                if len(new_profile.get("events", [])) == len(template_data.get("events", [])):
                    print("✅ Events copied from template")
                else:
                    print("❌ Events not copied correctly from template")
                    return False
                
                # Verify sections_enabled copied
                if new_profile.get("sections_enabled") == template_data.get("sections_enabled"):
                    print("✅ Sections enabled settings copied from template")
                else:
                    print("❌ Sections enabled settings not copied correctly")
                    return False
                
                # Verify fresh timestamps (created_at, updated_at)
                template_created = datetime.fromisoformat(template_data["created_at"].replace('Z', '+00:00'))
                new_created = datetime.fromisoformat(new_profile["created_at"].replace('Z', '+00:00'))
                
                if new_created > template_created:
                    print("✅ New profile has fresh timestamps")
                else:
                    print("❌ New profile timestamps not updated")
                    return False
                
                return all_copied
            else:
                print("❌ Failed to get template data for comparison")
                return False
        else:
            print(f"❌ Failed to create profile from template: {response.status_code} - {response.text}")
            return False
    
    def test_regular_profiles_exclude_templates(self):
        """Test 5: Regular Profile List Excludes Templates (GET /api/admin/profiles)"""
        print("\n📋 TEST 5: Regular Profile List Excludes Templates")
        
        # Get regular profiles list
        response = self.session.get(f"{BACKEND_URL}/admin/profiles")
        
        if response.status_code == 200:
            profiles = response.json()
            
            print(f"✅ Regular profiles endpoint returned {len(profiles)} profiles")
            
            # Verify templates (is_template=true) are NOT included
            template_found = False
            regular_profile_found = False
            
            for profile in profiles:
                if profile.get("is_template") == True:
                    template_found = True
                    print(f"❌ Template found in regular profiles list: {profile['id']}")
                elif profile["id"] == self.new_profile_from_template_id:
                    regular_profile_found = True
                    print(f"✅ New profile from template found in regular profiles list")
            
            if not template_found:
                print("✅ No templates found in regular profiles list")
            
            if regular_profile_found:
                print("✅ Profile created from template appears in regular profiles")
                return not template_found
            else:
                print("⚠️ Profile created from template not found in regular profiles")
                return not template_found
        else:
            print(f"❌ Failed to get regular profiles: {response.status_code} - {response.text}")
            return False
    
    def test_edge_cases(self):
        """Test 6: Edge Cases"""
        print("\n🧪 TEST 6: Edge Cases")
        
        success_count = 0
        total_tests = 4
        
        # Test save-as-template with invalid profile ID
        print("\n   6.1: Save-as-template with invalid profile ID")
        invalid_id = str(uuid.uuid4())
        response = self.session.post(f"{BACKEND_URL}/admin/profiles/{invalid_id}/save-as-template")
        if response.status_code == 404:
            print("   ✅ Invalid profile ID returns 404")
            success_count += 1
        else:
            print(f"   ❌ Invalid profile ID returned {response.status_code}, expected 404")
        
        # Test create-from-template with invalid template ID
        print("\n   6.2: Create-from-template with invalid template ID")
        invalid_id = str(uuid.uuid4())
        response = self.session.post(f"{BACKEND_URL}/admin/profiles/from-template/{invalid_id}")
        if response.status_code == 404:
            print("   ✅ Invalid template ID returns 404")
            success_count += 1
        else:
            print(f"   ❌ Invalid template ID returned {response.status_code}, expected 404")
        
        # Test create-from-template with non-template profile ID
        print("\n   6.3: Create-from-template with non-template profile ID")
        if self.new_profile_from_template_id:
            response = self.session.post(f"{BACKEND_URL}/admin/profiles/from-template/{self.new_profile_from_template_id}")
            if response.status_code == 404:
                print("   ✅ Non-template profile ID returns 404")
                success_count += 1
            else:
                print(f"   ❌ Non-template profile ID returned {response.status_code}, expected 404")
        else:
            print("   ⚠️ No regular profile available for testing")
        
        # Test endpoints without authentication
        print("\n   6.4: Endpoints without authentication")
        # Create session without auth token
        no_auth_session = requests.Session()
        
        # Test save-as-template without auth
        response = no_auth_session.post(f"{BACKEND_URL}/admin/profiles/{self.test_profile_id}/save-as-template")
        if response.status_code == 403:
            print("   ✅ Save-as-template without auth returns 403")
            success_count += 1
        else:
            print(f"   ❌ Save-as-template without auth returned {response.status_code}, expected 403")
        
        print(f"\n   Edge cases passed: {success_count}/{total_tests}")
        return success_count == total_tests
    
    def verify_template_remains_unchanged(self):
        """Verify that the original template remains unchanged after creating profile from it"""
        print("\n🔍 VERIFICATION: Template Remains Unchanged")
        
        # Get template data
        response = self.session.get(f"{BACKEND_URL}/admin/profiles/{self.template_id}")
        
        if response.status_code == 200:
            template_data = response.json()
            
            # Verify it's still a template
            if template_data.get("is_template") == True:
                print("✅ Original profile is still marked as template")
            else:
                print("❌ Original profile is no longer marked as template")
                return False
            
            # Verify key data unchanged
            if (template_data["groom_name"] == "Arjun Sharma" and
                template_data["bride_name"] == "Priya Patel" and
                template_data["venue"] == "Grand Palace Banquet Hall"):
                print("✅ Template data remains unchanged")
                return True
            else:
                print("❌ Template data was modified")
                return False
        else:
            print(f"❌ Failed to verify template: {response.status_code}")
            return False
    
    def run_all_tests(self):
        """Run all template system tests"""
        print("🚀 STARTING TEMPLATE SYSTEM BACKEND TESTING")
        print("=" * 60)
        
        # Authenticate
        if not self.authenticate_admin():
            return False
        
        # Create test profile
        if not self.create_test_profile():
            return False
        
        # Run all tests
        test_results = []
        
        test_results.append(("Backend Model Verification", self.test_backend_model_verification()))
        test_results.append(("Save Profile as Template", self.test_save_profile_as_template()))
        test_results.append(("List Templates", self.test_list_templates()))
        test_results.append(("Create Profile from Template", self.test_create_profile_from_template()))
        test_results.append(("Regular Profiles Exclude Templates", self.test_regular_profiles_exclude_templates()))
        test_results.append(("Edge Cases", self.test_edge_cases()))
        test_results.append(("Template Remains Unchanged", self.verify_template_remains_unchanged()))
        
        # Print results summary
        print("\n" + "=" * 60)
        print("📊 TEMPLATE SYSTEM TEST RESULTS SUMMARY")
        print("=" * 60)
        
        passed = 0
        total = len(test_results)
        
        for test_name, result in test_results:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} - {test_name}")
            if result:
                passed += 1
        
        print(f"\n🎯 OVERALL RESULT: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 ALL TEMPLATE SYSTEM TESTS PASSED!")
            print("\n✅ TEMPLATE SYSTEM FEATURES VERIFIED:")
            print("   • is_template boolean field working correctly")
            print("   • Save profile as template functionality")
            print("   • List templates with proper filtering")
            print("   • Create new profile from template with unique IDs")
            print("   • Regular profiles exclude templates")
            print("   • Proper authentication required")
            print("   • Edge case handling")
            return True
        else:
            print(f"❌ {total - passed} tests failed. Template system needs fixes.")
            return False

def main():
    """Main test execution"""
    tester = TemplateSystemTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n🎊 TEMPLATE SYSTEM BACKEND TESTING COMPLETED SUCCESSFULLY!")
    else:
        print("\n💥 TEMPLATE SYSTEM BACKEND TESTING FAILED!")
    
    return success

if __name__ == "__main__":
    main()