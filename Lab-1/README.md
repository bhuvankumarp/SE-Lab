# Lab 1: Requirements Engineering & UML Use-Case Modelling

**Student:** BHUVAN KUMAR P (PES1UG24AM069)  
**Problem Statement #14:** Healthcare & Telemedicine, Corporate Mental Wellness & Counseling Platform

## Objective

Turn the given scenario into testable requirements and a UML use-case model:
- functional and non-functional requirements, each with measurable pass/fail criteria;
- at least three actors;
- a use-case diagram with at least one «include» and one «extend» relationship;
- detailed use-case flows.

## Scenario

An anonymous counselling portal for a company. Employees can check their stress levels, book confidential sessions with a licensed therapist and follow their own wellness indicators, and at no point does the employer learn who used it.

## What the report contains

1. **Scenario and approach**
2. **Stated assumptions:**
   - a 10-item stress questionnaire scored out of 40, in four bands;
   - a random, non-reversible pseudo-ID such as `WEL-7F42A91C`;
   - the employee-to-pseudo-ID mapping held in a separate identity store.
3. **Requirements:**
   - FR-001 anonymous accounts with a pseudo-ID
   - FR-002 stress self-assessment
   - FR-003 session booking without double booking
   - FR-004 wellness trend dashboard
   - FR-005 crisis escalation
   - NFR-001 timezone-correct scheduling under 2 s at peak load
   - NFR-002 identity separation, AES-256/TLS 1.3, ten-employee minimum for reports
4. **Actors:**
   - Primary: Corporate Employee, Licensed Therapist, Wellness Program Administrator.
   - Supporting: Corporate Identity Provider, Crisis Support Service, Notification Service.
5. **Use cases and traceability:** UC-01 to UC-13, each traced to its requirements.
6. **Include and extend relationships:** 5 «include» and 2 «extend».
7. **Use-case diagram** (embedded in the report)
8. **Use-case flow for UC-04, View Wellness Trend Dashboard:** preconditions, postconditions, main success scenario, alternate flows and notes.

## Files

| File | Description |
|---|---|
| [SE_Lab1_Report_PES1UG24AM069.docx](SE_Lab1_Report_PES1UG24AM069.docx) | Lab 1 report (Word) |

> **Provenance:** the report was built on the Team 14 (Helping Hands Software) shared report, so its heading still carries the template's original author line ("Prepared by Dhanush"). The document is included unchanged, exactly as submitted.

## Tools

UML use-case modelling, Microsoft Word.
