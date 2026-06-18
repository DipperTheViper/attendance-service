Feature: Admin Panel

  Scenario: Admin views all attendance records
    When admin gets attendance list
    Then the response status should be 200
    And the response should contain "records"

  Scenario: Admin filters attendance by user
    When admin gets attendance list filtered by user
    Then the response status should be 200

  Scenario: Admin filters attendance by date
    When admin gets attendance list with date_from "2024-01-01T00:00:00" and date_to "2030-01-01T00:00:00"
    Then the response status should be 200

  Scenario: Admin soft deletes attendance record
    Given there is an attendance record
    When admin deletes the attendance record
    Then the response status should be 200

  Scenario: Deleted record does not appear in list
    Given admin has deleted an attendance record
    When admin gets attendance list
    Then the deleted record should not be in the list

  Scenario: Non-admin cannot access admin endpoints
    When I access admin attendance list without admin token
    Then the response status should be 403
