# Clinical Trial Management System

You will implement a clinical trial management system that models the complete lifecycle of a clinical trial from planning through completion. This assignment focuses on **domain modeling**, **state machines**, **business rule enforcement**, and **strategy pattern implementation**.

## Learning Objectives
- Model complex domain entities with proper encapsulation
- Implement state machine patterns with strict state transition rules
- Enforce business rules and invariants within domain objects
- Apply the Strategy pattern for polymorphic behavior
- Write comprehensive unit tests for domain logic

## Your Task
Create a working implementation of the clinical trial domain as specified in `requirements.md`. The requirements document contains all business rules, state machine behavior, workflows, and outcome calculation specifications. Your job is to translate these requirements into clean, well-tested C# code.

## What to Implement

1. **Domain Model Classes**: ClinicalTrial, other entity classes, and supporting enums
2. **State Machine**: Full lifecycle management with state transitions and validation
3. **Business Workflows**: Screening, enrollment, randomization, visit recording, and outcome analysis
4. **Outcome Strategies**: Four strategy classes for calculating trial results (Binary, Continuous, Time-to-Event, Weighted)

## Design Freedom
The requirements specify **what** the system must do, not **how** to implement it. You decide:
- Object relationships (e.g. where to store visits, how to structure participants)
- Collection types (List, Dictionary, HashSet, etc.)
- How to model measurements and results
- State machine implementation approach
- Exception handling strategy

## Testing Requirements

Sample test scenarios are provided to demonstrate the testing approach. You must expand on these samples to thoroughly test your implementation.

**Phase 1 (Weeks 1-2):** Implement the domain and write comprehensive tests to verify your code works correctly.

**Phase 2 (After Week 2):** Each student will be randomly assigned 10 specific tests to implement. You will **only** be able to modify the test project—no changes to domain code are permitted. Your domain implementation must pass these assigned tests.

## Deliverables
1. Complete source code in provided project structure
2. All tests passing

## Academic Integrity
Individual assignment. All design decisions and code must be your own work and cannot be discussed with other class members.

---

- ### [Requirements](./requirements.md)
- ### [Grading Rubric](./grading.md)
