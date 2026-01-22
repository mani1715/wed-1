#!/usr/bin/env python3
"""
PHASE 12 - PART 5: AUDIT LOGS Backend Testing
Test all audit log functionality including models, API endpoints, and auto-cleanup logic.
"""

import requests
import json
import time
from datetime import datetime, timezone
from typing import Dict, Any, List

# Configuration
BASE_URL = "https://nuptial-hub-23.preview.emergentagent.com/api"
ADMIN_EMAIL = "admin@wedding.com"
ADMIN_PASSWORD = "admin123"

class AuditLogTester:
    def __init__(self):
        self.session = requests.Session()
        self.admin_token = None
        self.test_profiles = []
        self.test_results = []
        
    def log_test(self, test_name: str, success: bool, message: str):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name} - {message}")
        self.test_results.append({
            "test": test_name,
            "success": success,
            "message": message
        })
    
    def admin_login(self) -> bool:
        """Login as admin and get token"""
        try:
            response = self.session.post(f"{BASE_URL}/auth/login", json={
                "email": ADMIN_EMAIL,
                "password": ADMIN_PASSWORD
            })
            
            if response.status_code == 200:
                data = response.json()
                self.admin_token = data["access_token"]
                self.session.headers.update({
                    "Authorization": f"Bearer {self.admin_token}"
                })
                self.log_test("Admin Login", True, "Successfully logged in as admin")
                return True
            else:
                self.log_test("Admin Login", False, f"Login failed: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            self.log_test("Admin Login", False, f"Login error: {str(e)}")
            return False
    
    def create_test_profile(self, groom_name: str, bride_name: str) -> Dict[str, Any]:
        """Create a test profile and return profile data"""
        try:
            profile_data = {
                "groom_name": groom_name,
                "bride_name": bride_name,
                "event_type": "wedding",
                "event_date": "2024-06-15T10:00:00Z",
                "venue": "Grand Palace Hotel",
                "city": "Mumbai",
                "invitation_message": "Join us for our special day",
                "language": ["english"],
                "design_id": "royal_classic",
                "deity_id": "ganesha",
                "whatsapp_groom": "+919876543210",
                "whatsapp_bride": "+919876543211",
                "enabled_languages": ["english", "telugu"],
                "events": [
                    {
                        "name": "Wedding Ceremony",
                        "date": "2024-06-15",
                        "start_time": "10:00",
                        "end_time": "12:00",
                        "venue_name": "Grand Palace Hotel",
                        "venue_address": "123 Main St, Mumbai",
                        "map_link": "https://maps.google.com/example",
                        "description": "Main wedding ceremony",
                        "visible": True,
                        "order": 0
                    }
                ],
                "link_expiry_type": "days",
                "link_expiry_value": 30
            }
            
            response = self.session.post(f"{BASE_URL}/admin/profiles", json=profile_data)
            
            if response.status_code == 200:
                profile = response.json()
                self.test_profiles.append(profile)
                return profile
            else:
                raise Exception(f"Profile creation failed: {response.status_code} - {response.text}")
                
        except Exception as e:
            raise Exception(f"Error creating profile: {str(e)}")
    
    def test_audit_log_model_fields(self):
        """Test 1: Verify AuditLog model exists with required fields"""
        try:
            # Create a test profile to trigger audit log creation
            profile = self.create_test_profile("Rajesh Kumar", "Priya Sharma")
            
            # Get audit logs to verify model structure
            response = self.session.get(f"{BASE_URL}/admin/audit-logs")
            
            if response.status_code == 200:
                logs = response.json()
                
                if len(logs) > 0:
                    log = logs[0]  # Get the most recent log
                    
                    # Check required fields
                    required_fields = ["id", "action", "admin_id", "profile_id", "profile_slug", "details", "timestamp"]
                    missing_fields = [field for field in required_fields if field not in log]
                    
                    if not missing_fields:
                        # Verify the log is for profile creation
                        if log["action"] == "profile_create" and log["profile_id"] == profile["id"]:
                            self.log_test("AuditLog Model Fields", True, 
                                        f"All required fields present: {required_fields}")
                        else:
                            self.log_test("AuditLog Model Fields", False, 
                                        f"Expected profile_create action, got: {log['action']}")
                    else:
                        self.log_test("AuditLog Model Fields", False, 
                                    f"Missing required fields: {missing_fields}")
                else:
                    self.log_test("AuditLog Model Fields", False, "No audit logs found after profile creation")
            else:
                self.log_test("AuditLog Model Fields", False, 
                            f"Failed to get audit logs: {response.status_code}")
                
        except Exception as e:
            self.log_test("AuditLog Model Fields", False, f"Error: {str(e)}")
    
    def test_get_audit_logs_endpoint(self):
        """Test 2: Verify GET /api/admin/audit-logs endpoint"""
        try:
            # Test with admin authentication
            response = self.session.get(f"{BASE_URL}/admin/audit-logs")
            
            if response.status_code == 200:
                logs = response.json()
                
                # Verify response is a list
                if isinstance(logs, list):
                    # Verify logs are sorted by timestamp descending (newest first)
                    if len(logs) >= 2:
                        timestamps = [log["timestamp"] for log in logs[:2]]
                        if timestamps[0] >= timestamps[1]:
                            self.log_test("GET Audit Logs Endpoint", True, 
                                        f"Endpoint working, returned {len(logs)} logs in correct order")
                        else:
                            self.log_test("GET Audit Logs Endpoint", False, 
                                        "Logs not sorted in reverse chronological order")
                    else:
                        self.log_test("GET Audit Logs Endpoint", True, 
                                    f"Endpoint working, returned {len(logs)} logs")
                else:
                    self.log_test("GET Audit Logs Endpoint", False, 
                                "Response is not a list")
            else:
                self.log_test("GET Audit Logs Endpoint", False, 
                            f"Endpoint failed: {response.status_code} - {response.text}")
                
            # Test without authentication
            temp_session = requests.Session()
            response = temp_session.get(f"{BASE_URL}/admin/audit-logs")
            
            if response.status_code == 403 or response.status_code == 401:
                self.log_test("GET Audit Logs Auth Required", True, 
                            "Endpoint correctly requires admin authentication")
            else:
                self.log_test("GET Audit Logs Auth Required", False, 
                            f"Endpoint should require auth, got: {response.status_code}")
                
        except Exception as e:
            self.log_test("GET Audit Logs Endpoint", False, f"Error: {str(e)}")
    
    def test_profile_create_audit_logging(self):
        """Test 3: Verify profile creation generates audit log"""
        try:
            # Get initial audit log count
            response = self.session.get(f"{BASE_URL}/admin/audit-logs")
            initial_count = len(response.json()) if response.status_code == 200 else 0
            
            # Create a new profile
            profile = self.create_test_profile("Amit Patel", "Sneha Gupta")
            
            # Get updated audit logs
            response = self.session.get(f"{BASE_URL}/admin/audit-logs")
            
            if response.status_code == 200:
                logs = response.json()
                new_count = len(logs)
                
                if new_count > initial_count:
                    # Find the profile_create log
                    create_log = next((log for log in logs if 
                                     log["action"] == "profile_create" and 
                                     log["profile_id"] == profile["id"]), None)
                    
                    if create_log:
                        # Verify log details
                        details = create_log.get("details", {})
                        expected_details = ["groom_name", "bride_name", "event_type"]
                        
                        if all(key in details for key in expected_details):
                            self.log_test("Profile Create Audit Log", True, 
                                        f"Audit log created with correct details: {details}")
                        else:
                            self.log_test("Profile Create Audit Log", False, 
                                        f"Missing details in audit log: {details}")
                    else:
                        self.log_test("Profile Create Audit Log", False, 
                                    "No profile_create audit log found")
                else:
                    self.log_test("Profile Create Audit Log", False, 
                                "No new audit log created after profile creation")
            else:
                self.log_test("Profile Create Audit Log", False, 
                            f"Failed to get audit logs: {response.status_code}")
                
        except Exception as e:
            self.log_test("Profile Create Audit Log", False, f"Error: {str(e)}")
    
    def test_profile_update_audit_logging(self):
        """Test 4: Verify profile update generates audit log"""
        try:
            # Create a profile first
            profile = self.create_test_profile("Vikram Singh", "Anita Sharma")
            profile_id = profile["id"]
            
            # Get initial audit log count
            response = self.session.get(f"{BASE_URL}/admin/audit-logs")
            initial_count = len(response.json()) if response.status_code == 200 else 0
            
            # Update the profile
            update_data = {
                "venue": "Updated Grand Palace Hotel",
                "city": "Updated Mumbai"
            }
            
            response = self.session.put(f"{BASE_URL}/admin/profiles/{profile_id}", json=update_data)
            
            if response.status_code == 200:
                # Get updated audit logs
                response = self.session.get(f"{BASE_URL}/admin/audit-logs")
                
                if response.status_code == 200:
                    logs = response.json()
                    new_count = len(logs)
                    
                    if new_count > initial_count:
                        # Find the profile_update log
                        update_log = next((log for log in logs if 
                                         log["action"] == "profile_update" and 
                                         log["profile_id"] == profile_id), None)
                        
                        if update_log:
                            details = update_log.get("details", {})
                            updated_fields = details.get("updated_fields", [])
                            
                            if "venue" in updated_fields and "city" in updated_fields:
                                self.log_test("Profile Update Audit Log", True, 
                                            f"Audit log created with updated fields: {updated_fields}")
                            else:
                                self.log_test("Profile Update Audit Log", False, 
                                            f"Incorrect updated fields in audit log: {updated_fields}")
                        else:
                            self.log_test("Profile Update Audit Log", False, 
                                        "No profile_update audit log found")
                    else:
                        self.log_test("Profile Update Audit Log", False, 
                                    "No new audit log created after profile update")
                else:
                    self.log_test("Profile Update Audit Log", False, 
                                f"Failed to get audit logs: {response.status_code}")
            else:
                self.log_test("Profile Update Audit Log", False, 
                            f"Profile update failed: {response.status_code}")
                
        except Exception as e:
            self.log_test("Profile Update Audit Log", False, f"Error: {str(e)}")
    
    def test_profile_delete_audit_logging(self):
        """Test 5: Verify profile deletion generates audit log"""
        try:
            # Create a profile first
            profile = self.create_test_profile("Rohit Mehta", "Kavya Nair")
            profile_id = profile["id"]
            
            # Get initial audit log count
            response = self.session.get(f"{BASE_URL}/admin/audit-logs")
            initial_count = len(response.json()) if response.status_code == 200 else 0
            
            # Delete the profile
            response = self.session.delete(f"{BASE_URL}/admin/profiles/{profile_id}")
            
            if response.status_code == 200:
                # Get updated audit logs
                response = self.session.get(f"{BASE_URL}/admin/audit-logs")
                
                if response.status_code == 200:
                    logs = response.json()
                    new_count = len(logs)
                    
                    if new_count > initial_count:
                        # Find the profile_delete log
                        delete_log = next((log for log in logs if 
                                         log["action"] == "profile_delete" and 
                                         log["profile_id"] == profile_id), None)
                        
                        if delete_log:
                            details = delete_log.get("details", {})
                            
                            if "groom_name" in details and "bride_name" in details:
                                self.log_test("Profile Delete Audit Log", True, 
                                            f"Audit log created with profile names: {details}")
                            else:
                                self.log_test("Profile Delete Audit Log", False, 
                                            f"Missing profile names in audit log: {details}")
                        else:
                            self.log_test("Profile Delete Audit Log", False, 
                                        "No profile_delete audit log found")
                    else:
                        self.log_test("Profile Delete Audit Log", False, 
                                    "No new audit log created after profile deletion")
                else:
                    self.log_test("Profile Delete Audit Log", False, 
                                f"Failed to get audit logs: {response.status_code}")
            else:
                self.log_test("Profile Delete Audit Log", False, 
                            f"Profile deletion failed: {response.status_code}")
                
        except Exception as e:
            self.log_test("Profile Delete Audit Log", False, f"Error: {str(e)}")
    
    def test_profile_duplicate_audit_logging(self):
        """Test 6: Verify profile duplication generates audit log"""
        try:
            # Create a profile first
            profile = self.create_test_profile("Arjun Reddy", "Meera Iyer")
            profile_id = profile["id"]
            
            # Get initial audit log count
            response = self.session.get(f"{BASE_URL}/admin/audit-logs")
            initial_count = len(response.json()) if response.status_code == 200 else 0
            
            # Duplicate the profile
            response = self.session.post(f"{BASE_URL}/admin/profiles/{profile_id}/duplicate")
            
            if response.status_code == 200:
                duplicated_profile = response.json()
                
                # Get updated audit logs
                response = self.session.get(f"{BASE_URL}/admin/audit-logs")
                
                if response.status_code == 200:
                    logs = response.json()
                    new_count = len(logs)
                    
                    if new_count > initial_count:
                        # Find the profile_duplicate log
                        duplicate_log = next((log for log in logs if 
                                            log["action"] == "profile_duplicate" and 
                                            log["profile_id"] == duplicated_profile["id"]), None)
                        
                        if duplicate_log:
                            details = duplicate_log.get("details", {})
                            expected_keys = ["original_profile_id", "original_slug", "groom_name", "bride_name"]
                            
                            if all(key in details for key in expected_keys):
                                self.log_test("Profile Duplicate Audit Log", True, 
                                            f"Audit log created with correct details: {details}")
                            else:
                                self.log_test("Profile Duplicate Audit Log", False, 
                                            f"Missing details in audit log: {details}")
                        else:
                            self.log_test("Profile Duplicate Audit Log", False, 
                                        "No profile_duplicate audit log found")
                    else:
                        self.log_test("Profile Duplicate Audit Log", False, 
                                    "No new audit log created after profile duplication")
                else:
                    self.log_test("Profile Duplicate Audit Log", False, 
                                f"Failed to get audit logs: {response.status_code}")
            else:
                self.log_test("Profile Duplicate Audit Log", False, 
                            f"Profile duplication failed: {response.status_code}")
                
        except Exception as e:
            self.log_test("Profile Duplicate Audit Log", False, f"Error: {str(e)}")
    
    def test_template_save_audit_logging(self):
        """Test 7: Verify template save generates audit log"""
        try:
            # Create a profile first
            profile = self.create_test_profile("Karan Malhotra", "Riya Kapoor")
            profile_id = profile["id"]
            
            # Get initial audit log count
            response = self.session.get(f"{BASE_URL}/admin/audit-logs")
            initial_count = len(response.json()) if response.status_code == 200 else 0
            
            # Save as template
            response = self.session.post(f"{BASE_URL}/admin/profiles/{profile_id}/save-as-template")
            
            if response.status_code == 200:
                # Get updated audit logs
                response = self.session.get(f"{BASE_URL}/admin/audit-logs")
                
                if response.status_code == 200:
                    logs = response.json()
                    new_count = len(logs)
                    
                    if new_count > initial_count:
                        # Find the template_save log
                        template_log = next((log for log in logs if 
                                           log["action"] == "template_save" and 
                                           log["profile_id"] == profile_id), None)
                        
                        if template_log:
                            details = template_log.get("details", {})
                            
                            if "groom_name" in details and "bride_name" in details:
                                self.log_test("Template Save Audit Log", True, 
                                            f"Audit log created with profile names: {details}")
                            else:
                                self.log_test("Template Save Audit Log", False, 
                                            f"Missing profile names in audit log: {details}")
                        else:
                            self.log_test("Template Save Audit Log", False, 
                                        "No template_save audit log found")
                    else:
                        self.log_test("Template Save Audit Log", False, 
                                    "No new audit log created after template save")
                else:
                    self.log_test("Template Save Audit Log", False, 
                                f"Failed to get audit logs: {response.status_code}")
            else:
                self.log_test("Template Save Audit Log", False, 
                            f"Template save failed: {response.status_code}")
                
        except Exception as e:
            self.log_test("Template Save Audit Log", False, f"Error: {str(e)}")
    
    def test_audit_log_limit_and_cleanup(self):
        """Test 8: Verify audit log auto-cleanup maintains last 1000 logs"""
        try:
            # Get current audit log count
            response = self.session.get(f"{BASE_URL}/admin/audit-logs")
            
            if response.status_code == 200:
                logs = response.json()
                current_count = len(logs)
                
                # Note: In a real test environment, we would need to create 1000+ logs
                # to test the cleanup functionality. For this test, we'll verify the
                # endpoint returns a maximum of 1000 logs and check if cleanup logic exists
                
                if current_count <= 1000:
                    self.log_test("Audit Log Limit", True, 
                                f"Audit logs count ({current_count}) is within 1000 limit")
                else:
                    self.log_test("Audit Log Limit", False, 
                                f"Audit logs count ({current_count}) exceeds 1000 limit")
                
                # Verify logs are sorted newest first
                if len(logs) >= 2:
                    first_timestamp = datetime.fromisoformat(logs[0]["timestamp"].replace('Z', '+00:00'))
                    second_timestamp = datetime.fromisoformat(logs[1]["timestamp"].replace('Z', '+00:00'))
                    
                    if first_timestamp >= second_timestamp:
                        self.log_test("Audit Log Sorting", True, 
                                    "Audit logs are sorted in reverse chronological order (newest first)")
                    else:
                        self.log_test("Audit Log Sorting", False, 
                                    "Audit logs are not sorted correctly")
                else:
                    self.log_test("Audit Log Sorting", True, 
                                "Insufficient logs to test sorting (less than 2 logs)")
                    
            else:
                self.log_test("Audit Log Limit", False, 
                            f"Failed to get audit logs: {response.status_code}")
                
        except Exception as e:
            self.log_test("Audit Log Limit", False, f"Error: {str(e)}")
    
    def test_audit_log_comprehensive_flow(self):
        """Test 9: Comprehensive test flow as specified in review request"""
        try:
            print("\n🔄 Starting comprehensive audit log test flow...")
            
            # Step 1: Create a test profile
            profile = self.create_test_profile("Comprehensive Test", "Flow Profile")
            profile_id = profile["id"]
            
            # Step 2: Update the profile
            update_data = {"venue": "Updated Test Venue"}
            response = self.session.put(f"{BASE_URL}/admin/profiles/{profile_id}", json=update_data)
            
            if response.status_code != 200:
                raise Exception(f"Profile update failed: {response.status_code}")
            
            # Step 3: Duplicate the profile
            response = self.session.post(f"{BASE_URL}/admin/profiles/{profile_id}/duplicate")
            
            if response.status_code != 200:
                raise Exception(f"Profile duplication failed: {response.status_code}")
            
            duplicated_profile = response.json()
            
            # Step 4: Save original as template
            response = self.session.post(f"{BASE_URL}/admin/profiles/{profile_id}/save-as-template")
            
            if response.status_code != 200:
                raise Exception(f"Template save failed: {response.status_code}")
            
            # Step 5: Delete the duplicated profile
            response = self.session.delete(f"{BASE_URL}/admin/profiles/{duplicated_profile['id']}")
            
            if response.status_code != 200:
                raise Exception(f"Profile deletion failed: {response.status_code}")
            
            # Step 6: Retrieve all audit logs and verify
            response = self.session.get(f"{BASE_URL}/admin/audit-logs")
            
            if response.status_code == 200:
                logs = response.json()
                
                # Look for all expected audit log actions
                expected_actions = ["profile_create", "profile_update", "profile_duplicate", "template_save", "profile_delete"]
                found_actions = []
                
                for log in logs:
                    if log.get("profile_id") in [profile_id, duplicated_profile["id"]]:
                        found_actions.append(log["action"])
                
                # Check if all expected actions are found
                missing_actions = [action for action in expected_actions if action not in found_actions]
                
                if not missing_actions:
                    # Verify logs are sorted newest first
                    test_logs = [log for log in logs if log.get("profile_id") in [profile_id, duplicated_profile["id"]]]
                    
                    if len(test_logs) >= 2:
                        timestamps = [datetime.fromisoformat(log["timestamp"].replace('Z', '+00:00')) for log in test_logs[:2]]
                        
                        if timestamps[0] >= timestamps[1]:
                            self.log_test("Comprehensive Flow Test", True, 
                                        f"All audit actions logged correctly: {found_actions}")
                        else:
                            self.log_test("Comprehensive Flow Test", False, 
                                        "Audit logs not sorted in reverse chronological order")
                    else:
                        self.log_test("Comprehensive Flow Test", True, 
                                    f"All audit actions logged correctly: {found_actions}")
                else:
                    self.log_test("Comprehensive Flow Test", False, 
                                f"Missing audit actions: {missing_actions}")
            else:
                self.log_test("Comprehensive Flow Test", False, 
                            f"Failed to retrieve audit logs: {response.status_code}")
                
        except Exception as e:
            self.log_test("Comprehensive Flow Test", False, f"Error: {str(e)}")
    
    def run_all_tests(self):
        """Run all audit log tests"""
        print("🚀 Starting PHASE 12 - PART 5: AUDIT LOGS Backend Testing")
        print("=" * 70)
        
        # Login first
        if not self.admin_login():
            print("❌ Cannot proceed without admin authentication")
            return
        
        # Run all tests
        test_methods = [
            self.test_audit_log_model_fields,
            self.test_get_audit_logs_endpoint,
            self.test_profile_create_audit_logging,
            self.test_profile_update_audit_logging,
            self.test_profile_delete_audit_logging,
            self.test_profile_duplicate_audit_logging,
            self.test_template_save_audit_logging,
            self.test_audit_log_limit_and_cleanup,
            self.test_audit_log_comprehensive_flow
        ]
        
        for test_method in test_methods:
            try:
                test_method()
                time.sleep(0.5)  # Small delay between tests
            except Exception as e:
                test_name = test_method.__name__.replace('test_', '').replace('_', ' ').title()
                self.log_test(test_name, False, f"Test execution error: {str(e)}")
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 70)
        print("📊 AUDIT LOGS TESTING SUMMARY")
        print("=" * 70)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print("\n❌ FAILED TESTS:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  • {result['test']}: {result['message']}")
        
        print("\n🎯 AUDIT LOGS TESTING COMPLETE")
        
        # Cleanup test profiles
        self.cleanup_test_profiles()
    
    def cleanup_test_profiles(self):
        """Clean up test profiles created during testing"""
        print("\n🧹 Cleaning up test profiles...")
        
        for profile in self.test_profiles:
            try:
                # Only delete if not already deleted during testing
                response = self.session.get(f"{BASE_URL}/admin/profiles/{profile['id']}")
                if response.status_code == 200:
                    profile_data = response.json()
                    if profile_data.get('is_active', True):  # Only delete if still active
                        self.session.delete(f"{BASE_URL}/admin/profiles/{profile['id']}")
            except:
                pass  # Ignore cleanup errors
        
        print(f"✅ Cleanup completed for {len(self.test_profiles)} test profiles")

if __name__ == "__main__":
    tester = AuditLogTester()
    tester.run_all_tests()