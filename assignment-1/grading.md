# Grading Rubric

**Total Points: 100**

---

## 1. Correctness (50 points)

### 1.1 Domain Model Implementation (20 points)

- All required attributes implemented correctly
- Immutability rules enforced per specification
- Required calculations and status tracking work correctly
- Measurements collected and validated per specification
- Appropriate types used for all domain concepts

### 1.2 State Machine Implementation (15 points)

- All state transitions work correctly
- Early termination transition works correctly when triggered
- Invalid transitions throw appropriate exceptions
- State-dependent operations properly restricted per specification
- Terminal states properly locked and read-only

### 1.3 Business Rules Enforcement (10 points)

- Eligibility criteria correctly enforced
- Duplicate prevention rules properly implemented
- Automatic state transitions triggered when specified conditions met
- Required preconditions verified before operations
- Data collection rules follow state-based constraints
- All business rules from requirements enforced correctly

### 1.4 Outcome Strategies (5 points)

- Outcome strategies calculate correctly
- Each strategy returns results for BOTH treatment and control groups
- Strategies handle edge cases and use correct mathematical formulas

---

## 2. Design Quality (25 points)

### 2.1 Object-Oriented Design (10 points)

- Private fields with appropriate public/internal access
- Business logic encapsulated within domain objects
- No exposed internal state that violates invariants
- Clear, justified decision on data ownership structure
- Appropriate collection types chosen for different use cases
- Strategy pattern properly implemented for outcome calculations

### 2.2 State Machine Design (5 points)

- State transitions cleanly implemented (no deeply nested if/else chains)
- State-dependent behavior well organized
- State guards/preconditions clearly expressed

### 2.3 Code Organization (5 points)

- Logical file and folder structure
- Appropriate use of namespaces
- Clear separation between domain, strategies, and tests
- No circular dependencies or tight coupling

### 2.4 Code Quality (5 points)

- Clear, descriptive names for classes, methods, variables
- Consistent naming conventions followed (C# conventions)
- Clear code structure and formatting
- Appropriate exception types thrown with clear messages
- Proper use of access modifiers (public/private/internal)
- No code duplication (DRY principle)
- No obvious code smells (long methods, god classes, feature envy)

---

## 3. Testing (25 points)

### 3.1 Phase 1: Self-Written Tests (10 points)

- Tests verify correct behavior (not just code execution)
- Tests check both positive and negative cases
- Edge cases tested (empty data, boundary conditions)

### 3.2 Phase 2: Assigned Tests (15 points)

- Number of assigned tests that pass (1.5 pts each, 10 tests total)
- After Phase 1 submission, domain implementation is locked
- Only test project modifications allowed in Phase 2