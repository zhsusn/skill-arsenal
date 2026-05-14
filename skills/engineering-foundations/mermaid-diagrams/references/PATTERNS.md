# Mermaid 场景化模式速查

按典型技术文档场景提供可直接复用的 Mermaid 模板与约定。

## 图表类型选择

| 场景 | 图表类型 | Mermaid 语法 |
|------|---------|-------------|
| 数据库 schema | ERD | `erDiagram` |
| API 调用 | 时序图 | `sequenceDiagram` |
| 业务流程 | 流程图 | `flowchart TD` |
| 组件架构 | 流程图 | `flowchart LR` |
| 状态转换 | 状态图 | `stateDiagram-v2` |
| 用户旅程 | 旅程图 | `journey` |
| 项目时间线 | 甘特图 | `gantt` |
| 类关系 | 类图 | `classDiagram` |

## ERD 模式（数据库设计文档）

```mermaid
erDiagram
    PATIENT {
        uuid Id PK
        string FirstName
        string LastName
        string Email UK
        string Phone
        date DateOfBirth
        timestamp CreationTime
        uuid CreatorId FK
        boolean IsDeleted
    }

    DOCTOR {
        uuid Id PK
        string FullName
        string Specialization
        string Email UK
        string Phone
    }

    APPOINTMENT {
        uuid Id PK
        uuid PatientId FK
        uuid DoctorId FK
        timestamp AppointmentDate
        string Description
        smallint Status "0=Scheduled,1=Completed,2=Cancelled"
    }

    PATIENT ||--o{ APPOINTMENT : "has"
    DOCTOR ||--o{ APPOINTMENT : "conducts"
```

### ERD 约定

| 标记 | 含义 |
|------|------|
| `PK` | 主键 |
| `FK` | 外键 |
| `UK` | 唯一键 |
| `||--o{` | 一对多 |
| `}o--o{` | 多对多 |

## 时序图模式（API 交互文档）

```mermaid
sequenceDiagram
    autonumber
    participant C as Client
    participant API as API Gateway
    participant S as AppService
    participant DB as Database

    C->>+API: POST /api/app/patients
    API->>API: Validate JWT
    API->>+S: CreateAsync(dto)
    S->>S: Validate input
    S->>+DB: Insert Patient
    DB-->>-S: Patient entity
    S-->>-API: PatientDto
    API-->>-C: 201 Created

    Note over C,DB: Error handling
    C->>+API: POST /api/app/patients (invalid)
    API->>+S: CreateAsync(dto)
    S-->>-API: ValidationException
    API-->>-C: 400 Bad Request
```

### 时序图约定

| 箭头 | 含义 |
|------|------|
| `->>` | 同步请求 |
| `-->>` | 同步响应 |
| `--)` | 异步消息 |
| `+` / `-` | 激活/取消激活 |

## 流程图模式（业务流程）

```mermaid
flowchart TD
    A[Start: New Appointment Request] --> B{Patient Exists?}
    B -->|Yes| C[Load Patient]
    B -->|No| D[Create Patient]
    D --> C
    C --> E{Doctor Available?}
    E -->|Yes| F[Create Appointment]
    E -->|No| G[Show Available Slots]
    G --> H[User Selects Slot]
    H --> F
    F --> I[Send Confirmation]
    I --> J[End]

    style A fill:#e1f5fe
    style J fill:#c8e6c9
    style B fill:#fff3e0
    style E fill:#fff3e0
```

### 流程图形状约定

| 形状 | 语法 | 用途 |
|------|------|------|
| 矩形 | `[text]` | 处理/动作 |
| 菱形 | `{text}` | 决策 |
| 圆角矩形 | `([text])` | 开始/结束 |
| 平行四边形 | `[/text/]` | 输入/输出 |
| 圆形 | `((text))` | 连接符 |

## 架构图模式（系统组件可视化）

```mermaid
flowchart LR
    subgraph Client
        UI[React App]
    end

    subgraph API["API Layer"]
        GW[API Gateway]
        AUTH[AuthServer]
    end

    subgraph Services["Application Services"]
        PS[PatientService]
        DS[DoctorService]
        AS[AppointmentService]
    end

    subgraph Data["Data Layer"]
        PG[(PostgreSQL)]
        RD[(Redis Cache)]
    end

    UI --> GW
    UI --> AUTH
    GW --> PS & DS & AS
    PS & DS & AS --> PG
    PS & DS & AS --> RD

    style PG fill:#336791,color:#fff
    style RD fill:#dc382d,color:#fff
```

## 状态图模式（实体生命周期）

```mermaid
stateDiagram-v2
    [*] --> Scheduled: Create

    Scheduled --> Confirmed: Patient Confirms
    Scheduled --> Cancelled: Cancel

    Confirmed --> InProgress: Check-in
    Confirmed --> Cancelled: Cancel
    Confirmed --> NoShow: No Check-in

    InProgress --> Completed: Finish

    Completed --> [*]
    Cancelled --> [*]
    NoShow --> [*]

    note right of Scheduled: Initial state
    note right of Completed: Triggers billing
```

## 样式指南

### 全局主题初始化

```mermaid
%%{init: {'theme': 'base', 'themeVariables': {
    'primaryColor': '#1976d2',
    'primaryTextColor': '#fff',
    'primaryBorderColor': '#1565c0',
    'lineColor': '#424242',
    'secondaryColor': '#f5f5f5',
    'tertiaryColor': '#e3f2fd'
}}}%%
```

### 样式类定义

```mermaid
classDef className fill:#color,stroke:#color
class NodeId className
```

## Quality Checklist

- [ ] 为场景选择了正确的图表类型
- [ ] 标签清晰、描述性强
- [ ] 箭头方向一致（TD=自上而下，LR=自左向右）
- [ ] ERD 中关系基数正确
- [ ] 时序图中长操作使用激活条
- [ ] 流程图中决策点明确标记
- [ ] 使用 subgraph 进行逻辑分组
- [ ] 复杂区域添加注释（`%%`）
