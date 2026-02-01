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
