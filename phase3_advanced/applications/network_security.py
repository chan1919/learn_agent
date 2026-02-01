"""
网络安全应用场景
"""

import time
from typing import Dict, List, Optional, Any, Tuple


class SecurityMonitor:
    """
    网络安全监控系统
    """
    
    def __init__(self):
        """
        初始化安全监控系统
        """
        self.alerts = []  # 安全告警
        self.rules = []  # 安全规则
        self.anomaly_detector = AnomalyDetector()
        
        # 注册内置规则
        self._register_builtin_rules()
    
    def monitor(self, network_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        监控网络数据
        
        Args:
            network_data: 网络数据
            
        Returns:
            生成的告警列表
        """
        detected_alerts = []
        
        # 应用安全规则
        for rule in self.rules:
            alert = rule.check(network_data)
            if alert:
                detected_alerts.append(alert)
        
        # 异常检测
        anomaly_alert = self.anomaly_detector.detect(network_data)
        if anomaly_alert:
            detected_alerts.append(anomaly_alert)
        
        # 存储告警
        for alert in detected_alerts:
            self.alerts.append(alert)
        
        return detected_alerts
    
    def add_rule(self, rule):
        """
        添加安全规则
        
        Args:
            rule: 安全规则对象
        """
        self.rules.append(rule)
        print(f"已添加安全规则: {rule.name}")
    
    def get_alerts(self, severity: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        获取告警
        
        Args:
            severity: 告警 severity，如果为None则获取所有告警
            
        Returns:
            告警列表
        """
        if severity:
            return [alert for alert in self.alerts if alert.get("severity") == severity]
        return self.alerts
    
    def _register_builtin_rules(self):
        """
        注册内置规则
        """
        # 注册端口扫描检测规则
        port_scan_rule = PortScanRule()
        self.add_rule(port_scan_rule)
        
        # 注册DDoS检测规则
        ddos_rule = DDoSRule()
        self.add_rule(ddos_rule)


class SecurityRule:
    """
    安全规则基类
    """
    
    def __init__(self, name: str, severity: str = "medium"):
        """
        初始化安全规则
        
        Args:
            name: 规则名称
            severity: 规则 severity，可选值: low, medium, high
        """
        self.name = name
        self.severity = severity
    
    def check(self, network_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        检查网络数据
        
        Args:
            network_data: 网络数据
            
        Returns:
            告警信息，如果没有告警返回None
        """
        raise NotImplementedError("子类必须实现check方法")


class PortScanRule(SecurityRule):
    """
    端口扫描检测规则
    """
    
    def __init__(self):
        """
        初始化端口扫描检测规则
        """
        super().__init__("端口扫描检测", "high")
        self.scan_threshold = 10  # 阈值：10秒内尝试连接超过10个不同端口
        self.ip_port_mapping = {}  # 存储IP地址和尝试连接的端口
    
    def check(self, network_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        检查是否存在端口扫描行为
        
        Args:
            network_data: 网络数据
            
        Returns:
            告警信息，如果没有告警返回None
        """
        if "source_ip" in network_data and "destination_port" in network_data:
            source_ip = network_data["source_ip"]
            dest_port = network_data["destination_port"]
            timestamp = network_data.get("timestamp", time.time())
            
            # 清理过期数据（10秒前的数据）
            if source_ip in self.ip_port_mapping:
                self.ip_port_mapping[source_ip] = [(port, t) for port, t in self.ip_port_mapping[source_ip] if timestamp - t < 10]
            else:
                self.ip_port_mapping[source_ip] = []
            
            # 添加新的端口连接记录
            self.ip_port_mapping[source_ip].append((dest_port, timestamp))
            
            # 检查是否超过阈值
            unique_ports = len(set([port for port, _ in self.ip_port_mapping[source_ip]]))
            if unique_ports > self.scan_threshold:
                return {
                    "rule": self.name,
                    "severity": self.severity,
                    "message": f"检测到端口扫描行为，源IP: {source_ip}, 尝试端口数: {unique_ports}",
                    "timestamp": timestamp,
                    "source_ip": source_ip
                }
        
        return None


class DDoSRule(SecurityRule):
    """
    DDoS检测规则
    """
    
    def __init__(self):
        """
        初始化DDoS检测规则
        """
        super().__init__("DDoS检测", "high")
        self.request_threshold = 100  # 阈值：10秒内超过100个请求
        self.target_requests = {}  # 存储目标和请求数
    
    def check(self, network_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        检查是否存在DDoS攻击
        
        Args:
            network_data: 网络数据
            
        Returns:
            告警信息，如果没有告警返回None
        """
        if "destination_ip" in network_data:
            dest_ip = network_data["destination_ip"]
            timestamp = network_data.get("timestamp", time.time())
            
            # 清理过期数据（10秒前的数据）
            if dest_ip in self.target_requests:
                self.target_requests[dest_ip] = [(t) for t in self.target_requests[dest_ip] if timestamp - t < 10]
            else:
                self.target_requests[dest_ip] = []
            
            # 添加新的请求记录
            self.target_requests[dest_ip].append(timestamp)
            
            # 检查是否超过阈值
            request_count = len(self.target_requests[dest_ip])
            if request_count > self.request_threshold:
                return {
                    "rule": self.name,
                    "severity": self.severity,
                    "message": f"检测到DDoS攻击，目标IP: {dest_ip}, 10秒内请求数: {request_count}",
                    "timestamp": timestamp,
                    "destination_ip": dest_ip
                }
        
        return None


class AnomalyDetector:
    """
    异常检测器
    """
    
    def __init__(self):
        """
        初始化异常检测器
        """
        self.baseline = {}  # 基线数据
        self.threshold = 2.0  # 异常阈值
    
    def detect(self, network_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        检测异常
        
        Args:
            network_data: 网络数据
            
        Returns:
            告警信息，如果没有异常返回None
        """
        # 简单的异常检测，实际应用中应该使用更复杂的算法
        if "bytes_transferred" in network_data:
            bytes_transferred = network_data["bytes_transferred"]
            timestamp = network_data.get("timestamp", time.time())
            
            # 更新基线
            self._update_baseline(bytes_transferred)
            
            # 检测异常
            if self.baseline.get("mean") and self.baseline.get("std"):
                z_score = abs(bytes_transferred - self.baseline["mean"]) / self.baseline["std"]
                if z_score > self.threshold:
                    return {
                        "rule": "异常检测",
                        "severity": "medium",
                        "message": f"检测到异常流量，传输字节数: {bytes_transferred}, Z-score: {z_score:.2f}",
                        "timestamp": timestamp
                    }
        
        return None
    
    def _update_baseline(self, value: float):
        """
        更新基线数据
        
        Args:
            value: 新的观测值
        """
        # 简单的移动平均和标准差计算
        if "values" not in self.baseline:
            self.baseline["values"] = []
        
        self.baseline["values"].append(value)
        
        # 只保留最近100个值
        if len(self.baseline["values"]) > 100:
            self.baseline["values"] = self.baseline["values"][-100:]
        
        # 计算均值和标准差
        if self.baseline["values"]:
            import numpy as np
            self.baseline["mean"] = np.mean(self.baseline["values"])
            self.baseline["std"] = np.std(self.baseline["values"])
