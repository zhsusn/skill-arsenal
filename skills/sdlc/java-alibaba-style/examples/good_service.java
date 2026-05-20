package com.example.order.service;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.Objects;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;
import java.util.regex.Pattern;

/**
 * 订单服务实现类。
 *
 * @author example
 * @date 2026/05/20
 */
@Service
public class OrderServiceImpl implements OrderService {

    private static final Logger logger = LoggerFactory.getLogger(OrderServiceImpl.class);
    private static final int MAX_RETRY_COUNT = 3;
    private static final BigDecimal MIN_ORDER_AMOUNT = new BigDecimal("0.01");
    private static final DateTimeFormatter DATE_FORMATTER =
        DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
    private static final Pattern PHONE_PATTERN = Pattern.compile("^1[3-9]\\d{9}$");

    private final ThreadPoolExecutor executor = new ThreadPoolExecutor(
        4, 8, 60L, TimeUnit.SECONDS,
        new LinkedBlockingQueue<>(100),
        new CustomThreadFactory("order-process"),
        new ThreadPoolExecutor.CallerRunsPolicy()
    );

    @Override
    @Transactional(rollbackFor = Exception.class)
    public OrderDTO createOrder(OrderCreateRequest request) {
        if (request == null) {
            throw new IllegalArgumentException("Request is null");
        }
        if (request.getUserId() == null || request.getUserId() <= 0) {
            throw new IllegalArgumentException("User ID must be positive");
        }

        // 金额校验
        if (request.getAmount() == null
            || request.getAmount().compareTo(MIN_ORDER_AMOUNT) < 0) {
            throw new BusinessException("Order amount must be at least 0.01");
        }

        OrderDO order = new OrderDO();
        order.setUserId(request.getUserId());
        order.setAmount(request.getAmount());
        order.setStatus(0);
        order.setCreateTime(LocalDateTime.now());
        order.setUpdateTime(LocalDateTime.now());

        orderDao.insert(order);

        if (logger.isDebugEnabled()) {
            logger.debug("Order created, orderId: {}, userId: {}",
                order.getOrderId(), order.getUserId());
        }

        return convertToDTO(order);
    }

    @Override
    public List<OrderDTO> getOrdersByUserId(Long userId) {
        if (userId == null || userId <= 0) {
            return new ArrayList<>();
        }

        List<OrderDO> orderList = orderDao.selectByUserId(userId);
        if (orderList == null || orderList.isEmpty()) {
            return new ArrayList<>();
        }

        List<OrderDTO> result = new ArrayList<>(orderList.size());
        for (OrderDO order : orderList) {
            result.add(convertToDTO(order));
        }

        return result;
    }

    @Override
    public boolean cancelOrder(Long orderId) {
        if (orderId == null || orderId <= 0) {
            logger.warn("Invalid orderId: {}", orderId);
            return false;
        }

        try {
            OrderDO order = orderDao.selectById(orderId);
            if (order == null) {
                throw new OrderNotFoundException(
                    "Order not found, orderId: " + orderId);
            }

            if (!Objects.equals(order.getStatus(), 0)) {
                throw new BusinessException(
                    "Order cannot be cancelled, current status: " + order.getStatus());
            }

            int updated = orderDao.updateStatus(orderId, 9);
            return updated > 0;
        } catch (OrderNotFoundException e) {
            logger.error("Cancel order failed, orderId: {}", orderId, e);
            throw e;
        } catch (Exception e) {
            logger.error("Cancel order error, orderId: {}", orderId, e);
            throw new ServiceException("Cancel order failed", e);
        }
    }

    @Override
    public void batchProcess(List<Long> orderIds) {
        if (orderIds == null || orderIds.isEmpty()) {
            return;
        }

        Iterator<Long> iterator = orderIds.iterator();
        while (iterator.hasNext()) {
            Long id = iterator.next();
            if (id == null || id <= 0) {
                iterator.remove();
            }
        }

        executor.execute(() -> {
            for (Long orderId : orderIds) {
                try {
                    cancelOrder(orderId);
                } catch (Exception e) {
                    logger.error("Batch process failed, orderId: {}", orderId, e);
                }
            }
        });
    }

    /**
     * 将 OrderDO 转换为 OrderDTO。
     *
     * @param order 数据对象
     * @return 传输对象
     */
    private OrderDTO convertToDTO(OrderDO order) {
        if (order == null) {
            return null;
        }
        OrderDTO dto = new OrderDTO();
        dto.setOrderId(order.getOrderId());
        dto.setUserId(order.getUserId());
        dto.setAmount(order.getAmount());
        dto.setStatus(order.getStatus());
        dto.setCreateTime(
            order.getCreateTime() != null
                ? order.getCreateTime().format(DATE_FORMATTER)
                : null);
        return dto;
    }
}
