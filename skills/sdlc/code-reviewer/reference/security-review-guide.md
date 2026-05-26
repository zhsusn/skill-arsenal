# Security Review Guide（安全审查指南）

> 全语言通用安全审查清单。按被审查代码涉及的场景勾选。
> 本指南供 `code-reviewer` Skill 在 Phase 3 按需加载注入。

## 输入验证与清理

- [ ] 所有用户输入（URL 参数、表单、Header、Cookie、文件上传）是否经过校验？
- [ ] 是否使用了白名单校验而非黑名单？
- [ ] 特殊字符（null 字节、换行、控制字符）是否被正确处理？
- [ ] 文件上传是否限制 MIME 类型、扩展名和大小？
- [ ] 上传文件是否存储在非执行目录？是否重命名以避免覆盖？

## 认证与授权

- [ ] 敏感端点是否检查了认证状态？
- [ ] 权限校验是否在服务端执行（不依赖客户端隐藏 UI）？
- [ ] 是否有水平越权风险？（用户 A 能否访问用户 B 的资源）
- [ ] 是否有垂直越权风险？（普通用户能否访问管理员接口）
- [ ] 会话管理是否安全？（过期时间、刷新机制、注销失效）
- [ ] JWT / Token 是否正确验证签名和过期时间？
- [ ] 密码是否使用强哈希算法（bcrypt/Argon2/scrypt）？

## 注入防护

- [ ] SQL 查询是否使用参数化查询 / ORM 绑定？禁止字符串拼接 SQL。
- [ ] 命令执行是否避免将用户输入直接传入 shell？
- [ ] LDAP/XPath/XML 注入是否被防护？
- [ ] 正则表达式是否避免了 ReDoS（灾难性回溯）？

## XSS 与输出编码

- [ ] 用户生成的内容在渲染到 HTML 前是否经过编码？
- [ ] 是否使用了安全的 DOM API（textContent 而非 innerHTML）？
- [ ] JSON 输出是否正确设置了 Content-Type（application/json）？
- [ ] URL 重定向是否使用白名单，避免开放重定向？

## 敏感数据保护

- [ ] 密钥、Token、密码是否硬编码在源码中？
- [ ] 敏感配置是否通过环境变量或安全密钥管理服务提供？
- [ ] 日志中是否打印了敏感信息（密码、Token、PII）？
- [ ] 错误信息是否向用户暴露了内部实现细节（堆栈跟踪、SQL 语句）？
- [ ] 是否使用了 HTTPS 传输敏感数据？
- [ ] 静态资源（JS/CSS）是否包含敏感配置？

## 依赖与供应链

- [ ] 新增依赖是否来自可信源？
- [ ] 依赖是否有已知 CVE？（运行 `npm audit`、`pip-audit`、`cargo audit` 等）
- [ ] 依赖许可证是否与项目兼容？
- [ ] 依赖是否仍在积极维护？（最近提交时间、未处理的 security issue）

## 业务逻辑安全

- [ ] 关键操作是否有防重放机制？
- [ ] 资金/数量操作是否检查了负数、零值、精度溢出？
- [ ] 批量操作是否有限制（避免 DoS）？
- [ ] 时间敏感操作是否使用了服务端时间而非客户端时间？
- [ ] 是否有竞态条件导致的状态不一致？（库存扣减、余额变动）

## 基础设施安全

- [ ] CORS 配置是否过于宽松（避免 `*` 或反射 Origin）？
- [ ] CSP（Content Security Policy）是否配置？
- [ ] 安全响应头是否齐全（X-Content-Type-Options、X-Frame-Options 等）？
- [ ] 是否禁用了不安全的 HTTP 方法（TRACE、OPTIONS 滥用）？

## 语言/框架特定项

### Python
- [ ] 是否使用了 `pickle` / `yaml.load` 处理不可信数据？（应使用 `json` / `yaml.safe_load`）
- [ ] `eval` / `exec` 是否处理用户输入？
- [ ] 模板渲染（Jinja2）是否开启了 autoescape？

### JavaScript/TypeScript (Node)
- [ ] `child_process.exec` 是否拼接了用户输入？（使用 `execFile`）
- [ ] `new Function()` 或 `eval()` 是否使用了外部数据？
- [ ] 原型链污染防护：是否禁用了 `__proto__` / `constructor` 赋值？

### Java
- [ ] 反序列化是否使用了 `ObjectInputStream` 处理不可信数据？
- [ ] XML 解析是否禁用了外部实体（XXE）？

### Go
- [ ] `text/template` 是否用于 HTML 输出？（应使用 `html/template`）

## 审查输出标记

发现安全问题时，使用以下标记：
- 🔴 **blocking**：SQL 注入、XSS、硬编码密钥、越权访问、敏感信息泄露
- 🟠 **important**：CORS 过宽、日志泄露、输入校验不完整、依赖有 CVE
- 🔵 **suggestion**：增加 CSP、增强密码策略、添加安全响应头
