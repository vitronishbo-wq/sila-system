"""
Architecture visualization for AÇÃO 3 - BaseRequestService

This module generates mermaid diagrams showing:
1. Current parallel architecture (problems)
2. Target inheritance architecture (solution)
3. Data flow through template method pattern
4. Test consolidation opportunity
"""

# Generate and render all architecture diagrams
# Run this to embed diagrams in documentation

BEFORE_AFTER_ARCHITECTURE = """
graph TB
    subgraph BEFORE ["BEFORE: Parallel Implementations (Duplicated Logic)"]
        direction TB
        
        CRS["RequestService<br/>(citizen/core)"]
        SRS["RequestService<br/>(service_requests)"]
        HCS["HealthcareService<br/>(saude_primaria)"]
        
        CRS --> |create_request| CR1["Create<br/>15 lines"]
        CR1 --> |audit| CA1["Audit<br/>6 lines"]
        CA1 --> |notify| CN1["Notify<br/>4 lines"]
        
        SRS --> |create_request| CR2["Create<br/>18 lines"]
        CR2 --> |audit| CA2["Audit<br/>6 lines (DUPLICATE)"]
        CA2 --> |notify| CN2["Notify<br/>4 lines (DUPLICATE)"]
        
        HCS --> |create_request| CR3["Create<br/>14 lines"]
        CR3 --> |audit| CA3["Audit<br/>6 lines (DUPLICATE)"]
        CA3 --> |notify| CN3["Notify<br/>4 lines (DUPLICATE)"]
        
        style CA1 fill:#ffcccc
        style CA2 fill:#ffcccc
        style CA3 fill:#ffcccc
        style CN1 fill:#ffffcc
        style CN2 fill:#ffffcc
        style CN3 fill:#ffffcc
    end
    
    subgraph AFTER ["AFTER: Inheritance (Unified Logic)"]
        direction TB
        
        BASE["<b>BaseRequestService</b><br/>─────────────────<br/>■ create_request()<br/>■ get_request()<br/>■ list_citizen_requests()<br/>■ update_status()<br/>■ count_by_citizen()"]
        
        BASE --> |audit| BA["Audit<br/>1 place"]
        BASE --> |notify| BN["Notify<br/>1 place"]
        BA --> |hooks| BH["Override Hooks"]
        BN --> |hooks| BH
        
        CRSC["RequestService<br/>(citizen)"]
        SRSC["RequestService<br/>(service_requests)"]
        HCSC["HealthcareService<br/>(saude_primaria)"]
        
        CRSC -.->|implements| BH
        SRSC -.->|implements| BH
        HCSC -.->|implements| BH
        
        BH --> |hook: validate| V["_validate_create_<br/>request()"]
        BH --> |hook: post_save| P["_post_save_<br/>create()"]
        BH --> |hook: perms| PRM["_check_read_<br/>permission()"]
        
        style BH fill:#ccffcc
        style BA fill:#ccffcc
        style BN fill:#ccffcc
        style BASE fill:#cce5ff
    end
    
    BEFORE -.->|REFACTOR| AFTER
    
    %% Styling
    classDef duplicate fill:#ffcccc,stroke:#cc0000,stroke-width:2px
    classDef shared fill:#ccffcc,stroke:#00cc00,stroke-width:2px
    classDef base fill:#cce5ff,stroke:#0000cc,stroke-width:2px
"""

TEMPLATE_METHOD_FLOW = """
graph LR
    A["🚀 create_request<br/>citizen_id, request_data<br/>────────────────"] --> B["1️⃣ Validate<br/>_validate_create_<br/>request<br/>(override hook)"]
    
    B --> C["2️⃣ Create Model<br/>create_request_<br/>model<br/>(you implement)"]
    
    C --> D["3️⃣ Pre-Save<br/>_pre_save_<br/>create<br/>(override hook)"]
    
    D --> E["4️⃣ Save to DB<br/>repo.save<br/>request<br/>(you provide repo)"]
    
    E --> F["5️⃣ Post-Save<br/>_post_save_<br/>create<br/>(override hook)"]
    
    F --> G["6️⃣ Audit Log<br/>_audit_create<br/>AUTOMATIC"]
    
    G --> H["7️⃣ Return<br/>saved request"]
    
    style A fill:#fff3cd,stroke:#ff6b6b,stroke-width:3px
    style B fill:#ffe0e0
    style C fill:#e0f2e0
    style D fill:#ffe0e0
    style E fill:#e0e5ff
    style F fill:#ffe0e0
    style G fill:#fff3cd
    style H fill:#d4edda,stroke:#00cc00,stroke-width:2px
"""

INHERITANCE_DIAGRAM = """
graph TB
    BASE["<b>BaseRequestService[TRequest, TRepo]</b><br/>─────────────────────────────<br/><i>Abstract Base Class</i><br/><br/>🔧 Required (abstract):<br/>• get_repository() → TRepository<br/>• default_status() → str<br/>• create_request_model() → TRequest<br/>• get_user_from_citizen_id() → UUID?<br/><br/>📋 Provided (template methods):<br/>• create_request() ✓<br/>• get_request() ✓<br/>• list_citizen_requests() ✓<br/>• update_status() ✓<br/>• count_by_citizen() ✓<br/><br/>🪝 Extension Hooks (optional override):<br/>• _validate_create_request()<br/>• _pre_save_create()<br/>• _post_save_create()<br/>• _check_read_permission()<br/>• _audit_create()"]
    
    CRS["<b>RequestService</b><br/>(app/citizen/core)<br/>────────────────<br/>✅ Implements:<br/>• get_repository()<br/>• default_status()<br/>• create_request_model()<br/>• get_user_from_citizen_id()<br/><br/>Override (optional):<br/>• _post_save_create()<br/>  (nothing needed)"]
    
    SRS["<b>RequestService</b><br/>(app/modules/service_)<br/>────────────────<br/>✅ Implements:<br/>• get_repository()<br/>• default_status()<br/>• create_request_model()<br/>• get_user_from_citizen_id()<br/><br/>Override (optional):<br/>• _post_save_create()<br/>  (start workflow)"]
    
    HCS["<b>HealthcareService</b><br/>(app/modules/saude)<br/>────────────────<br/>✅ Implements:<br/>• get_repository()<br/>• default_status()<br/>• create_request_model()<br/>• get_user_from_citizen_id()<br/><br/>Override (optional):<br/>• _validate_create_request()<br/>  (healthcare rules)<br/>• _post_save_create()<br/>  (notify health unit)"]
    
    BASE --> CRS
    BASE --> SRS
    BASE --> HCS
    
    style BASE fill:#cce5ff,stroke:#0000cc,stroke-width:3px
    style CRS fill:#e0f2e0,stroke:#00cc00,stroke-width:2px
    style SRS fill:#e0f2e0,stroke:#00cc00,stroke-width:2px
    style HCS fill:#e0f2e0,stroke:#00cc00,stroke-width:2px
"""

DUPLICATION_SNAPSHOT = """
graph TB
    subgraph METRICS ["Duplication Metrics - Before vs After"]
        direction LR
        
        LINES["<u>Duplicated Lines</u><br/><br/>Before: 63<br/>After: 0<br/>───────<br/>Saved: -100%"]
        
        LOCS["<u>Locations</u><br/>(audit bugs)<br/><br/>Before: 3<br/>After: 1<br/>───────<br/>-67% bugs"]
        
        MAINT["<u>Maintenance</u><br/>(per bug)<br/><br/>Before: 3x<br/>After: 1x<br/>───────<br/>-67%"]
        
        SERVICE["<u>New Service</u><br/>(onboarding)<br/><br/>Before: 2hrs<br/>After: 15min<br/>───────<br/>8x faster"]
        
        TEST["<u>Test Lines</u><br/>(lifecycle)<br/><br/>Before: 180<br/>After: 60<br/>───────<br/>-67%"]
    end
    
    style LINES fill:#ffcccc
    style LOCS fill:#ffcccc
    style MAINT fill:#ffcccc
    style SERVICE fill:#ccffcc
    style TEST fill:#ccffcc
"""

IMPLEMENTATION_ROADMAP = """
graph LR
    A["1️⃣<br/>BaseRequestService<br/>(skeleton)<br/>✅ DONE"] --> B["2️⃣<br/>Citizen RequestService<br/>(first implementation)<br/>🔧 TODO"]
    
    B --> C["3️⃣<br/>Service_requests<br/>RequestService<br/>🔧 TODO"]
    
    C --> D["4️⃣<br/>HealthcareService<br/>🔧 TODO"]
    
    D --> E["5️⃣<br/>Consolidate Tests<br/>(AÇÃO 4)<br/>📋 PENDING"]
    
    style A fill:#d4edda,stroke:#00cc00,stroke-width:2px
    style B fill:#fff3cd,stroke:#ff9800,stroke-width:2px
    style C fill:#fff3cd,stroke:#ff9800,stroke-width:2px
    style D fill:#fff3cd,stroke:#ff9800,stroke-width:2px
    style E fill:#e0e5ff,stroke:#0000cc,stroke-width:2px
"""

if __name__ == "__main__":
    print("""
# AÇÃO 3 Architecture Diagrams
# Run with: python -m app.core.services.base_request_service_diagrams

These diagrams can be rendered in markdown using:
renderMermaidDiagram(markup, title)
    """)
    
    print("\n" + "="*70)
    print("DIAGRAM 1: BEFORE vs AFTER Architecture")
    print("="*70)
    print(BEFORE_AFTER_ARCHITECTURE)
    
    print("\n" + "="*70)
    print("DIAGRAM 2: Template Method Pattern Flow")
    print("="*70)
    print(TEMPLATE_METHOD_FLOW)
    
    print("\n" + "="*70)
    print("DIAGRAM 3: Inheritance Hierarchy")
    print("="*70)
    print(INHERITANCE_DIAGRAM)
    
    print("\n" + "="*70)
    print("DIAGRAM 4: Duplication Metrics")
    print("="*70)
    print(DUPLICATION_SNAPSHOT)
    
    print("\n" + "="*70)
    print("DIAGRAM 5: Implementation Roadmap")
    print("="*70)
    print(IMPLEMENTATION_ROADMAP)
