# Flow Diagram

```mermaid
flowchart TD
    A([Start]) --> B{Choose booking type}

    B -->|Restaurant| C[Ask dining date]
    C --> D[Validate date]
    D -->|Invalid / past| C
    D -->|Valid| E[Ask time]
    E --> F[Validate time]
    F -->|Invalid| E
    F -->|Valid| G[Ask party size]
    G --> H[Validate 1-20 guests]
    H -->|Invalid| G
    H -->|Valid| I[Check mock availability]

    B -->|Hotel| J[Ask check-in date]
    J --> K[Validate check-in]
    K -->|Invalid / past| J
    K -->|Valid| L[Ask check-out date]
    L --> M[Validate check-out > check-in]
    M -->|Invalid| L
    M -->|Valid| N[Ask room type]
    N --> O[Ask number of guests]
    O --> P[Validate 1-20 guests]
    P -->|Invalid| O
    P -->|Valid| I

    I --> Q{Available?}
    Q -->|No| R[Show unavailable message]
    R --> S([End])

    Q -->|Yes| T[Show booking summary]
    T --> U{Confirm?}
    U -->|No| S
    U -->|Yes| V[Create mock confirmation ID]
    V --> W[Show confirmed booking]
    W --> S
```

## Conversation Summary

### Restaurant
1. Select Restaurant.
2. Enter date.
3. Enter time.
4. Enter party size.
5. Validate inputs.
6. Check mock availability.
7. Show booking summary.
8. Confirm or cancel.

### Hotel
1. Select Hotel.
2. Enter check-in date.
3. Enter check-out date.
4. Select room type.
5. Enter number of guests.
6. Validate inputs.
7. Check mock availability.
8. Show booking summary.
9. Confirm or cancel.
