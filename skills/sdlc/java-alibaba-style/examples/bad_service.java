package com.example.order.service;

// VIOLATION: 直接使用 Logback API，未使用 SLF4J 门面
import ch.qos.logback.classic.Logger;
import ch.qos.logback.classic.LoggerContext;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;

// VIOLATION: 类注释使用 //，未使用 Javadoc /** */；缺少 @author / @date
// 订单服务
public class orderServiceimpl {  // VIOLATION: 类名应为 OrderServiceImpl（UpperCamelCase）

    // VIOLATION: 魔法值直接出现；常量命名不规范（未大写下划线）
    private static final int maxretry = 3;
    private static final long timeout = 3600l;  // VIOLATION: long 用小写 l

    // VIOLATION: 使用 new BigDecimal(double) 构造，存在精度损失
    private static final BigDecimal MIN_AMOUNT = new BigDecimal(0.01);

    // VIOLATION: SimpleDateFormat 定义为 static，线程不安全
    // VIOLATION: 大写 Y（week year）
    private static final java.text.SimpleDateFormat SDF =
        new java.text.SimpleDateFormat("YYYY-MM-dd");

    // VIOLATION: 使用 Executors 创建线程池（有 OOM 风险）
    private final ScheduledExecutorService executor =
        Executors.newScheduledThreadPool(10);

    public Order getOrder(Long orderId) {  // VIOLATION: 方法无 Javadoc 注释
        // VIOLATION: 对 RuntimeException 进行 catch，应前置判空
        try {
            if (orderId == null) {
                // VIOLATION: 主动抛 NPE
                throw new NullPointerException("orderId is null");
            }
        } catch (NullPointerException e) {
            e.printStackTrace();  // VIOLATION: 生产环境禁止 printStackTrace
        }

        // VIOLATION: POJO 属性使用基本类型 int，未用包装类型 Integer
        int status = 0;

        // VIOLATION: 字符串拼接 SQL，存在 SQL 注入风险
        String sql = "SELECT * FROM order WHERE id = " + orderId;

        // VIOLATION: 使用 == 比较 BigDecimal
        if (MIN_AMOUNT == new BigDecimal("0.01")) {
            // ...
        }

        // VIOLATION: 未指定初始大小；泛型钻石语法可用但未用 <>
        List<Order> list = new ArrayList();
        // VIOLATION: 判断空集合应使用 isEmpty()
        if (list.size() == 0) {
            return null;  // VIOLATION: 返回 null 而非空集合
        }

        // VIOLATION: foreach 中进行 remove 操作
        for (Order o : list) {
            if (o == null) {
                list.remove(o);  // VIOLATION: 应使用 Iterator.remove()
            }
        }

        // VIOLATION: 循环内使用 + 拼接字符串
        String ids = "";
        for (Order o : list) {
            ids += o.getOrderId() + ",";
        }

        return new Order();
    }

    // VIOLATION: 方法名未使用 lowerCamelCase；参数未校验
    public void Process_Order(String status) {
        // VIOLATION: switch 变量为 String 外部参数，未先判 null
        switch (status) {
            case "PAID":
                break;
            // VIOLATION: switch 缺少 default
        }

        // VIOLATION: if 无大括号（即使一行代码也必须有大括号）
        if (status.equals("PAID"))
            doSomething();

        // VIOLATION: 三目运算符自动拆箱 NPE 风险（Integer 与 int 混用）
        Integer a = 1;
        Integer b = 2;
        Integer c = null;
        int result = true ? a * b : c;  // VIOLATION: c 为 null，自动拆箱抛 NPE
    }

    public void doSomething() {
        // VIOLATION: 生产环境使用 System.out.println
        System.out.println("Processing...");

        // VIOLATION: 日志使用字符串拼接，未用占位符
        logger.info("Processing order, id: " + 123);

        // VIOLATION: ThreadLocal 未在 finally 中 remove，可能导致内存泄漏
        ThreadLocal<String> tl = new ThreadLocal<>();
        tl.set("user");
        try {
            // ...
        } catch (Exception e) {
            // VIOLATION: 吞异常（catch 块为空）
        }
    }

    // VIOLATION: POJO 类中同时存在 isDeleted() 和 getDeleted()
    public boolean isDeleted() {
        return false;
    }

    public boolean getDeleted() {
        return false;
    }
}
