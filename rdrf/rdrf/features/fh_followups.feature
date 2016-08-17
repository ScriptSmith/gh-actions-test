Feature: Follow Up forms.
  As a user of FH I want to be able to add
  multiple follow up forms.
  
  Background:
    Given site has loaded export "fh.zip"
    Given a registry named "FH Registry"
    
  Scenario: Navigate to Follow Up Form
    When I am logged in as curator
    When I click "SMITH, John" on patientlisting
    And I press "Add" button in "Follow Ups" group in sidebar 
    Then location is "Follow Up"

  Scenario: Save Follow Up
    When I am logged in as curator
    When I click "SMITH, John" on  patientlisting
    And I press "Add" button in "Follow Ups" group in sidebar 
    When I enter value "02-08-2016" for form "Follow Up" section "At follow-up" cde "Date of assessment"
    And I click Save
    Then location is "Follow Up/02-08-2016"

  Scenario: Cancel Follow Up
    When I am logged in as curator
    When I click "SMITH, John" on  patientlisting
    And I press "Add" button in "Follow Ups" group in sidebar 
    When I enter value "02-08-2016" for form "Follow Up" section "At follow-up" cde "Date of assessment"
    And I click Cancel
    And I click Leave
    Then location is "Follow Up"
    
  Scenario: Add Two Follow Ups
    When I am logged in as curator
    When I click "SMITH, John" on  patientlisting
    And I press "Add" button in "Follow Ups" group in sidebar 
    When I enter value "01-08-2016" for form "Follow Up" section "At follow-up" cde "Date of assessment"
    And I click Save
    Then location is "Follow Up/01-08-2016"
    And I press "Add" button in "Follow Ups" group in sidebar 
    When I enter value "02-08-2016" for form "Follow Up" section "At follow-up" cde "Date of assessment"
    And I click Save
    Then location is "Follow Up/02-08-2016"
 




