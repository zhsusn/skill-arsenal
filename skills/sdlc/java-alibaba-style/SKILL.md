---
name: java-alibaba-style
description: 当用户要求编写 Java 代码、审查 Java 代码、格式化 Java 文件，或项目包含 .java / pom.xml / build.gradle 文件时触发。强制遵循《阿里巴巴 Java 开发手册（黄山版）》编写 Java 代码。
---

# Java Alibaba Style

## 适用场景
- 编写新的 Java 类、接口、方法
- 审查现有 Java 代码的规范性
- 重构代码以符合阿里开发规范

## 强制规范

### 1. 命名规范

| 类型 | 规则 | 示例 |
|:---|:---|:---|
| 类 | UpperCamelCase（DO/PO/DTO/BO/VO/UID 除外） | `OrderServiceImpl` |
| 方法/变量 | lowerCamelCase | `getOrderById()` / `userName` |
| 常量 | UPPER_SNAKE_CASE，语义完整 | `MAX_RETRY_COUNT` |
| 包 | 全小写，单数，点间仅一个单词 | `com.alibaba.order.service` |
| 抽象类 | Abstract/Base 开头 | `AbstractOrderService` |
| 异常类 | Exception 结尾 | `OrderNotFoundException` |
| 测试类 | 类名 + Test 结尾 | `OrderServiceTest` |
| Service/DAO 实现 | Impl 后缀 | `OrderServiceImpl` |
| POJO 布尔属性 | **禁止**加 `is` 前缀 | `deleted`（而非 `isDeleted`）|

```java
// Yes
public class OrderServiceImpl implements OrderService {
    private static final int MAX_RETRY_COUNT = 3;
    private String userName;
    public OrderDTO getOrderById(Long orderId) { ... }
}

// No
public class orderServiceimpl {
    private static final int maxretry = 3;
    private String UserName;
    private boolean isDeleted;
}
```

### 2. 常量与数值处理
- 禁止魔法值直接出现，必须定义为命名常量。
- `long` / `Long` 赋值后使用大写 `L`；浮点数后缀统一大写 `D` / `F`。
- 货币金额以最小货币单位且为整型存储；禁止用 `float` / `double` 做精确计算。
- `BigDecimal` 禁止 `new BigDecimal(double)`，必须用 `String` 构造或 `BigDecimal.valueOf()`。
- `BigDecimal` 等值比较必须用 `compareTo()`，不能用 `equals()`（精度不同会误判）。

```java
// Yes
private static final Long CACHE_EXPIRED_TIME = 3600L;
private static final BigDecimal MIN_AMOUNT = new BigDecimal("0.01");
if (amount.compareTo(MIN_AMOUNT) >= 0) { ... }

// No
if (amount == 0.01) { ... }
BigDecimal d = new BigDecimal(0.1);
if (amount.equals(MIN_AMOUNT)) { ... }
```

### 3. 代码格式
- 4 空格缩进，禁止 Tab；单行不超过 120 字符。
- 左大括号前不换行，后换行；右大括号前换行，后接 else/catch/finally 则不换行。
- 运算符（`=`、`&&`、`+` 等）左右必须有一个空格。
- `if` / `for` / `while` / `switch` / `do` 与左右括号之间必须加空格；方法参数逗号后必须加空格。

```java
// Yes
public void processOrder(Long orderId, Integer status) {
    if (orderId != null && status != null) {
        // ...
    } else {
        // ...
    }
}

// No
public void processOrder(Long orderId,Integer status){
    if(orderId!=null){
        // ...
    }
}
```

### 4. OOP 规约
- 所有 POJO 类属性必须使用包装数据类型（`Integer` 而非 `int`），RPC 方法返回值和参数同理。
- 定义 DO/PO/DTO/VO 等 POJO 类时不要设定任何属性默认值。
- 覆写方法必须加 `@Override`；外部正在调用的接口不允许修改方法签名，过时须加 `@Deprecated` 并说明新接口。
- 使用常量或确定有值的对象调用 `equals`，避免 NPE：`"test".equals(param)`。
- 所有整型包装类对象之间值的比较全部使用 `equals`。
- POJO 类必须写 `toString()`；构造方法里面禁止加入任何业务逻辑。
- 禁止在 POJO 类中同时存在对应属性 `xxx` 的 `isXxx()` 和 `getXxx()` 方法。

```java
// Yes
public class OrderDTO implements Serializable {
    private static final long serialVersionUID = 1L;
    private Long orderId;
    private Integer status;
    private Boolean deleted;

    @Override
    public String toString() {
        return "OrderDTO{" + "orderId=" + orderId + '}';
    }
}

// No
public class OrderDTO {
    private long orderId;
    private int status = 0;
    public boolean isDeleted() { return deleted; }
}
```

### 5. 集合处理
- 只要覆写 `equals`，就必须覆写 `hashCode`。
- 判断集合为空使用 `isEmpty()`，而不是 `size() == 0`。
- 使用 `Collectors.toMap()` 时必须提供 `mergeFunction` 处理 key 冲突。
- `ArrayList` 的 `subList` 结果不可强转成 `ArrayList`。
- 禁止在 `foreach` 循环里进行元素的 `remove` / `add`，`remove` 请使用 `Iterator`。
- 集合初始化时指定初始值大小（尤其 `HashMap`）。

```java
// Yes
Map<String, Object> map = new HashMap<>(16);
if (map.isEmpty()) { ... }

List<OrderDTO> result = list.stream()
    .collect(Collectors.toMap(OrderDTO::getOrderId, v -> v, (v1, v2) -> v1));

Iterator<OrderDTO> iterator = list.iterator();
while (iterator.hasNext()) {
    if (iterator.next() == null) {
        iterator.remove();
    }
}

// No
for (OrderDTO dto : list) {
    if (dto == null) { list.remove(dto); }
}
Map<String, Object> map = new HashMap();
```

### 6. 并发与日期
- 线程资源必须通过线程池提供，禁止显式 `new Thread()`；线程池禁止用 `Executors`，必须用 `ThreadPoolExecutor`。
- `SimpleDateFormat` 线程不安全，JDK8 使用 `DateTimeFormatter` 替代。
- 必须回收自定义的 `ThreadLocal` 变量，尽量在 `try-finally` 中回收。
- 高并发时：能用无锁数据结构就不用锁；能锁区块就不锁整个方法；能用对象锁就不用类锁。
- 日期格式化年份统一用小写 `y`（`yyyy-MM-dd`），禁止大写 `Y`（`YYYY` 代表 week year，跨年周会出错）。
- 获取当前毫秒数用 `System.currentTimeMillis()`；禁止写死一年为 365 天，用 `LocalDate.now().lengthOfYear()`。

```java
// Yes
private static final DateTimeFormatter FORMATTER =
    DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

public void process() {
    try {
        // ...
    } finally {
        DATE_FORMAT_THREAD_LOCAL.remove();
    }
}

// No
private static final SimpleDateFormat SDF = new SimpleDateFormat("yyyy-MM-dd");
int days = 365;
```

### 7. 异常处理
- 可通过预检查规避的 `RuntimeException`（如 NPE、越界）不应该通过 `catch` 处理，应做前置判空/越界检查。
- 异常捕获后不要用来做流程控制；`catch` 时分清稳定代码和非稳定代码，禁止对大段代码 `try-catch`。
- 捕获异常是为了处理它，不要捕获了却什么都不处理；事务场景中 `catch` 后如需回滚，注意手动回滚事务。
- `finally` 块必须关闭资源对象、流对象，有异常也要 `try-catch`；不要在 `finally` 块中使用 `return`。
- 调用 RPC、二方包、或动态生成类的方法时，捕获异常使用 `Throwable` 进行拦截。

```java
// Yes
public void updateOrder(OrderDTO dto) {
    if (dto == null || dto.getOrderId() == null) {
        throw new IllegalArgumentException("Order or orderId is null");
    }
    try {
        orderDao.update(dto);
    } catch (DaoException e) {
        logger.error("Update order failed, orderId: {}, dto: {}", dto.getOrderId(), dto, e);
        throw new ServiceException("Update failed", e);
    }
}

// No
try {
    // 100行业务代码
} catch (Exception e) {
    // 空 catch，吞异常
}
```

### 8. 日志规约
- 应用中不可直接使用日志系统（Log4j、Logback）中的 API，而应依赖日志框架门面（SLF4J / JCL），推荐使用 SLF4J。
- 日志输出时，字符串变量之间的拼接使用占位符 `{}` 的方式，不用字符串拼接。
- 对于 `trace` / `debug` / `info` 级别的日志输出，必须进行日志级别的开关判断（`logger.isDebugEnabled()`）。
- 生产环境禁止使用 `System.out` 或 `System.err`，禁止使用 `e.printStackTrace()`。
- 异常信息应该包括两类信息：案发现场信息和异常堆栈信息。

```java
// Yes
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class OrderService {
    private static final Logger logger = LoggerFactory.getLogger(OrderService.class);

    public void process(Long orderId) {
        if (logger.isDebugEnabled()) {
            logger.debug("Processing order, orderId: {}, status: {}", orderId, getStatus());
        }
        try {
            // ...
        } catch (Exception e) {
            logger.error("Process order failed, orderId: {}", orderId, e);
        }
    }
}

// No
import org.apache.log4j.Logger;
logger.debug("Processing order, orderId: " + orderId);
e.printStackTrace();
```

### 9. 控制语句
- `switch` 每个 `case` 要么通过 `break` / `return` / `continue` 终止，要么注释说明继续执行到哪个 `case`；必须包含 `default` 且放在最后。
- 当 `switch` 括号内的变量类型为 `String` 且为外部参数时，必须先进行 `null` 判断。
- `if` / `else` / `for` / `while` / `do` 必须使用大括号，即使只有一行代码。
- 三目运算符中，高度注意表达式 1 和 2 在类型对齐时可能抛出自动拆箱导致的 NPE。
- 表达异常分支时，少用 `if-else`，推荐卫语句（提前 `return`），避免嵌套超过 3 层。

```java
// Yes
public void checkOrder(OrderDTO dto) {
    if (dto == null) {
        throw new IllegalArgumentException("Order is null");
    }
    if (dto.getOrderId() == null) {
        throw new IllegalArgumentException("Order ID is null");
    }
    // 正常业务逻辑
}

// No
if (condition)
    doSomething();

switch (status) {
    case "PAID":
        break;
    // 缺少 default
}
```

### 10. 字符串与资源
- 循环体内字符串的连接使用 `StringBuilder` 的 `append` 方法，禁止循环内 `+` 拼接。
- `try` 块内代码最小化；必须使用 `try-with-resources` 或 `finally` 关闭文件、socket、数据库连接等资源。
- 使用正则表达式时，利用好预编译功能（`Pattern.compile` 应定义为静态常量），不要在方法体内临时编译。

```java
// Yes
private static final Pattern PHONE_PATTERN = Pattern.compile("^1[3-9]\\d{9}$");

public String buildSql(List<Long> ids) {
    StringBuilder sql = new StringBuilder();
    sql.append("SELECT * FROM order WHERE id IN (");
    for (int i = 0; i < ids.size(); i++) {
        sql.append(ids.get(i));
        if (i < ids.size() - 1) {
            sql.append(",");
        }
    }
    sql.append(")");
    return sql.toString();
}

// No
String sql = "SELECT * FROM order WHERE id IN (";
for (Long id : ids) {
    sql += id + ",";
}
```

### 11. 安全规约（涉及 Web/API/数据库时）
- 用户输入的 SQL 参数严格使用参数绑定或 METADATA 字段值限定，禁止字符串拼接 SQL，防止 SQL 注入。
- 用户请求传入的任何参数必须做有效性验证（防止 page size 过大、恶意 order by、缓存击穿、SSRF 等）。
- 禁止向 HTML 页面输出未经安全过滤或未正确转义的用户数据（防 XSS）。
- 表单、AJAX 提交必须执行 CSRF 安全验证；URL 外部重定向传入的目标地址必须执行白名单过滤。
- 配置文件中的密码需要加密。
- 前后端交互的 JSON 数据中，所有 key 必须为 lowerCamelCase。
- 超大整数场景，服务端一律使用 `String` 返回，禁止使用 `Long`（JavaScript 精度丢失）。

```java
// Yes
@Select("SELECT * FROM order WHERE id = #{orderId}")
OrderDO getById(@Param("orderId") Long orderId);

result.put("orderId", orderId.toString());

// No
String sql = "SELECT * FROM order WHERE id = " + orderId;
result.put("order_id", orderId);
```

### 12. 注释规约
- 类、类属性、类方法的注释必须使用 Javadoc 规范（`/** */`），不得使用 `// xxx` 方式。
- 所有的类都必须添加创建者和创建日期（`@author` / `@date`）。
- 方法内部单行注释，在被注释语句上方另起一行，使用 `//` 注释。
- 所有的枚举类型字段必须要有注释，说明每个数据项的用途。
- 与其用半吊子英文来注释，不如用中文注释说清楚。

```java
// Yes
/**
 * 订单服务实现类。
 *
 * @author example
 * @date 2026/05/20
 */
@Service
public class OrderServiceImpl implements OrderService {

    /** 最大重试次数。 */
    private static final int MAX_RETRY_COUNT = 3;

    /**
     * 根据订单ID获取订单详情。
     *
     * @param orderId 订单ID
     * @return 订单详情
     * @throws OrderNotFoundException 订单不存在时抛出
     */
    @Override
    public OrderDTO getOrderById(Long orderId) {
        // 参数校验
        if (orderId == null) {
            throw new IllegalArgumentException("Order ID is null");
        }
        return orderDao.selectById(orderId);
    }
}

// No
// 订单服务类
public class OrderService {
    private int maxRetry = 3;  // 最大重试次数
    public Order getOrder(Long id) { /* ... */ }
}
```

## 速查：命名规范速查表

| 类型 | 规范 | 正例 | 反例 |
|:---|:---|:---|:---|
| 类 | UpperCamelCase | `OrderServiceImpl` | `orderServiceimpl` |
| 方法 | lowerCamelCase | `getOrderById()` | `GetOrderByID()` |
| 变量 | lowerCamelCase | `localValue` | `local_value` |
| 常量 | UPPER_SNAKE_CASE | `MAX_STOCK_COUNT` | `MAX_COUNT` |
| 包 | 全小写单数 | `com.alibaba.order` | `com.alibaba.orders` |
| 抽象类 | Abstract/Base 开头 | `AbstractOrderService` | `BaseOrderService`（不规范）|
| 异常类 | Exception 结尾 | `OrderNotFoundException` | `OrderNotFound` |
| 测试类 | 类名+Test | `OrderServiceTest` | `TestOrderService` |
| 布尔属性 | 不加 is 前缀 | `deleted` | `isDeleted` |
| Service/DAO 实现 | Impl 后缀 | `OrderServiceImpl` | `OrderServiceImplementation` |

## 一致性原则（BE CONSISTENT）

如果你正在编辑已有文件，花几分钟观察周围代码的风格。如果现有代码使用 `m_` 前缀命名成员变量，你也应该这样做。风格指南的目的是建立共同词汇，让人们专注于"说什么"而非"怎么说"。

## Gotchas

- **布尔属性命名陷阱**：POJO 布尔属性命名 `isDeleted` 会导致部分框架（如 Fastjson、Jackson）序列化/反序列化时属性名解析为 `deleted`，造成前后端字段不一致。统一使用 `deleted`，通过 `getDeleted()` / `setDeleted()` 访问。
- **BigDecimal 构造陷阱**：`new BigDecimal(0.1)` 实际存储的是 `0.10000000000000000555...`，金额计算必用 `new BigDecimal("0.1")` 或 `BigDecimal.valueOf(0.1)`。
- **BigDecimal equals vs compareTo**：`new BigDecimal("1.0").equals(new BigDecimal("1.00"))` 返回 `false`（精度不同），等值判断永远用 `compareTo() == 0`。
- **long 后缀大小写**：`3600l` 极易被误读为 `36001`，必须写 `3600L`。
- **YYYY 与 yyyy**：`YYYY` 是 week-based year，跨年时如果该周属于上一年/下一年，日期会跳变。格式化年份永远用小写 `yyyy`。
- **foreach remove 的坑**：`ConcurrentModificationException` 是 Java 集合最常见的线上故障之一，删除元素务必使用 `Iterator.remove()`。
- **toMap 的 mergeFunction**：`Collectors.toMap(keyMapper, valueMapper)` 在 key 冲突时抛 `IllegalStateException`，生产环境必须提供 `(v1, v2) -> v1` 等 merge 函数。
- **三目运算符自动拆箱 NPE**：`Integer c = null; int result = flag ? a * b : c;` 中即使 `flag` 为 true，`c` 为 null 也会在自动拆箱时抛 NPE。三目运算符中确保两侧类型一致且不涉及自动拆箱。
- **ThreadLocal 内存泄漏**：线程池场景下 `ThreadLocal` 若不在 `finally` 中 `remove()`，线程复用会导致脏数据或内存泄漏。
- **日志占位符 vs 字符串拼接**：`logger.debug("a=" + a)` 在日志级别为 info 时仍会执行字符串拼接，浪费性能；占位符 `{}` 由日志框架在真正输出时才格式化。
- **包装类型 vs 基本类型**：POJO 属性用 `int` 时，数据库返回 null 会自动装箱为 0，导致业务语义丢失（如"未设置"和"设置为0"无法区分）。RPC 参数/返回值同理。
- **修改已有文件时优先保持一致**：即使旧代码不完全符合本规范，也不要在同一次 PR 中混合风格，除非是专门的重构提交。
