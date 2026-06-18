Feature: Authentication

  Scenario: User logs in with valid credentials
    When I login with username "testuser" and password "Test@1234"
    Then the response status should be 200
    And the response should contain "access_token"

  Scenario: User cannot login with wrong password
    When I login with username "testuser" and password "wrongpass"
    Then the response status should be 403

  Scenario: Unauthenticated request is rejected
    When I get my profile without token
    Then the response status should be 401

  Scenario: User logs out successfully
    When I logout
    Then the response status should be 200

  Scenario: Token is invalid after logout
    Given I have logged out
    When I get my profile
    Then the response status should be 401
