Feature: Attendance

  Scenario: User manual check-in
    When I manual check-in
    Then the response status should be 200

  Scenario: User cannot check-in twice
    Given I have checked in manually
    When I manual check-in
    Then the response status should be 409

  Scenario: User manual check-out
    Given I have checked in manually
    When I manual check-out
    Then the response status should be 200

  Scenario: User cannot check-out without active check-in
    When I manual check-out
    Then the response status should be 404

  Scenario: Geo check-in within geofence
    When I send geo attendance with latitude 35.123444 and longitude 51.123444
    Then the response status should be 200

  Scenario: Geo check-out outside geofence
    Given I have geo checked in
    When I send geo attendance with latitude 0.0 and longitude 0.0
    Then the response status should be 200

  Scenario: Geo check-in outside geofence is rejected
    When I send geo attendance with latitude 0.0 and longitude 0.0
    Then the response status should be 404

  Scenario: User views attendance list
    When I get my attendance list
    Then the response status should be 200
    And the response should contain "records"

  Scenario: User filters attendance by date
    When I get my attendance list with date_from "2024-01-01T00:00:00" and date_to "2030-01-01T00:00:00"
    Then the response status should be 200
