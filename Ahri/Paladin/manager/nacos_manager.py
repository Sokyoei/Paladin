import threading
import time
from typing import Callable

from loguru import logger
from nacos import NacosClient
from nacos.exception import NacosException

from Ahri.Paladin.config import settings


class NacosManager(object):

    def __init__(
        self,
        server_addresses: str,
        namespace: str | None = None,
        username: str | None = None,
        password: str | None = None,
    ):
        """初始化 Nacos 管理器。

        Args:
            server_addresses (str): Nacos 服务器地址
            namespace (str | None): 命名空间，用于隔离
            username (str | None): 用户名，用于认证
            password (str | None): 密码，用于认证
        """
        self.nacos_client = NacosClient(
            server_addresses=server_addresses, namespace=namespace, username=username, password=password
        )

        self.registered_services: dict[str, dict] = {}  # key: 服务唯一标识，value: 服务信息
        self.heartbeat_threads: dict[str, threading.Thread] = {}  # 心跳线程
        self.heartbeat_running: bool = True  # 心跳运行开关

    def get_config(self, data_id: str, group: str = "DEFAULT_GROUP", timeout_ms: int = 5000) -> str | None:
        """从 Nacos 获取配置。

        Args:
            data_id (str): 配置 ID
            group (str): 配置组。默认为 "DEFAULT_GROUP"。
            timeout_ms (int): 超时时间，单位毫秒。默认为 5000。

        Returns:
            str | None: 配置内容，失败时返回 None
        """
        try:
            logger.info(f"获取 Nacos 配置: data_id={data_id}, group={group}")
            config_content = self.nacos_client.get_config(
                data_id=data_id, group=group, timeout=timeout_ms / 1000  # SDK 接收秒为单位
            )
            if config_content:
                logger.info(f"成功获取配置: {data_id}")
                return config_content
            logger.warning(f"Nacos 配置为空: data_id={data_id}")
            return None
        except NacosException as e:
            logger.error(f"获取配置失败: {data_id}, 错误: {e!s}")
            return None

    def add_config_listener(self, data_id: str, callback: Callable[[str], None], group: str = "DEFAULT_GROUP"):
        """添加配置变更监听器。

        Args:
            data_id (str): 配置 ID
            callback (Callable[[str], None]): 配置变更时的回调函数
            group (str): 配置组。默认为 "DEFAULT_GROUP"。
        """

        def wrapper(config_content: str):
            """包装回调，增加异常处理"""
            try:
                callback(config_content)
            except Exception as e:
                logger.error(f"配置回调执行失败: {e!s}")

        try:
            self.nacos_client.add_config_watcher(data_id=data_id, group=group, cb=wrapper)
            logger.info(f"配置监听器添加成功: {data_id}")
        except NacosException as e:
            logger.error(f"添加配置监听器失败: {data_id}, 错误: {e!s}")

    def __get_service_key(self, service_name: str, ip: str, port: int) -> str:
        """生成唯一的服务键。

        Args:
            service_name (str): 服务名称
            ip (str): 服务 IP
            port (int): 服务端口

        Returns:
            str: 唯一的服务键
        """
        return f"{service_name}_{ip}_{port}"

    def register_service(
        self,
        service_name: str,
        ip: str,
        port: int,
        group_name: str = "DEFAULT_GROUP",
        cluster_name: str = "DEFAULT",
        metadata: dict | None = None,
    ) -> bool:
        """向 Nacos 注册服务并启动心跳。

        Args:
            service_name (str): 服务名称
            ip (str): 服务 IP
            port (int): 服务端口
            group_name (str): 服务组。默认为 "DEFAULT_GROUP"。
            cluster_name (str): 集群名称。默认为 "DEFAULT"。
            metadata (dict | None): 自定义元数据。默认为 None。

        Returns:
            bool: 注册结果
        """
        try:
            # 构建元数据
            service_metadata = {
                "version": "1.0.0",
                "timestamp": str(int(time.time())),
                "source": "Ahri.Paladin",
                "group": group_name,
                "cluster": cluster_name,
            }
            if metadata:
                service_metadata.update(metadata)

            # 注册服务（显式指定临时实例，必须发送心跳）
            success = self.nacos_client.add_naming_instance(
                service_name=service_name,
                ip=ip,
                port=port,
                group_name=group_name,
                cluster_name=cluster_name,
                metadata=service_metadata,
            )

            if not success:
                logger.error(f"服务注册失败: {service_name}@{ip}:{port}")
                return False

            # 记录已注册服务
            service_key = self.__get_service_key(service_name, ip, port)
            self.registered_services[service_key] = {
                "service_name": service_name,
                "ip": ip,
                "port": port,
                "group_name": group_name,
                "cluster_name": cluster_name,
                "metadata": service_metadata,
            }

            # 启动心跳线程
            self.__start_heartbeat(service_name, ip, port, group_name, cluster_name)
            logger.info(f"服务注册成功并启动心跳: {service_name}@{ip}:{port}")
            return True

        except NacosException as e:
            logger.error(f"服务注册异常: {service_name}@{ip}:{port}, 错误: {e!s}")
            return False

    def __start_heartbeat(
        self, service_name: str, ip: str, port: int, group_name: str = "DEFAULT_GROUP", cluster_name: str = "DEFAULT"
    ):
        """启动心跳线程。

        Args:
            service_name (str): 服务名称
            ip (str): 服务 IP
            port (int): 服务端口
            group_name (str): 服务组。默认为 "DEFAULT_GROUP"。
            cluster_name (str): 集群名称。默认为 "DEFAULT"。
        """
        service_key = self.__get_service_key(service_name, ip, port)

        # 避免重复启动心跳
        if service_key in self.heartbeat_threads and self.heartbeat_threads[service_key].is_alive():
            logger.warning(f"心跳线程已运行: {service_name}@{ip}:{port}")
            return

        def heartbeat_task():
            """心跳任务"""
            while self.heartbeat_running:
                try:
                    # 发送心跳
                    self.nacos_client.send_heartbeat(
                        service_name=service_name,
                        ip=ip,
                        port=port,
                        group_name=group_name,
                        cluster_name=cluster_name,
                        ephemeral=True,  # 必须和注册时一致
                    )
                    logger.debug(f"心跳发送成功: {service_name}@{ip}:{port}")
                except NacosException as e:
                    logger.error(f"心跳发送失败: {service_name}@{ip}:{port}, 错误: {e!s}")
                    # 心跳失败时尝试重新注册
                    self.__reregister_service(service_name, ip, port, group_name, cluster_name)
                time.sleep(5)  # 每 5 秒一次心跳

        # 启动守护线程（程序退出时自动终止）
        thread = threading.Thread(target=heartbeat_task, daemon=True, name=f"heartbeat-{service_key}")
        thread.start()
        self.heartbeat_threads[service_key] = thread
        logger.info(f"心跳线程启动成功: {service_name}@{ip}:{port}")

    def __stop_heartbeat(self, service_name: str, ip: str, port: int):
        """停止特定服务的心跳线程。

        Args:
            service_name (str): 服务名称
            ip (str): 服务 IP
            port (int): 服务端口
        """
        service_key = self.__get_service_key(service_name, ip, port)
        if service_key in self.heartbeat_threads:
            thread = self.heartbeat_threads[service_key]
            # 标记心跳停止（线程内循环会退出）
            self.heartbeat_running = False
            # 等待线程终止（最多等 5 秒）
            thread.join(timeout=5)
            del self.heartbeat_threads[service_key]
            logger.info(f"心跳线程已停止: {service_name}@{ip}:{port}")

    def __reregister_service(
        self, service_name: str, ip: str, port: int, group_name: str = "DEFAULT_GROUP", cluster_name: str = "DEFAULT"
    ):
        """心跳失败时重新注册服务。

        Args:
            service_name (str): 服务名称
            ip (str): 服务 IP
            port (int): 服务端口
            group_name (str): 服务组。默认为 "DEFAULT_GROUP"。
            cluster_name (str): 集群名称。默认为 "DEFAULT"。
        """
        logger.warning(f"尝试重新注册服务: {service_name}@{ip}:{port}")
        service_key = self.__get_service_key(service_name, ip, port)
        if service_key not in self.registered_services:
            logger.error(f"服务未注册，无法重新注册: {service_name}@{ip}:{port}")
            return

        service_info = self.registered_services[service_key]
        try:
            # 先注销旧实例
            self.nacos_client.remove_naming_instance(
                service_name=service_name,
                ip=ip,
                port=port,
                group_name=group_name,
                cluster_name=cluster_name,
                ephemeral=True,
            )
            # 重新注册
            self.nacos_client.add_naming_instance(
                service_name=service_name,
                ip=ip,
                port=port,
                group_name=group_name,
                cluster_name=cluster_name,
                metadata=service_info["metadata"],
                ephemeral=True,
                healthy=True,
            )
            logger.info(f"服务重新注册成功: {service_name}@{ip}:{port}")
        except NacosException as e:
            logger.error(f"服务重新注册失败: {service_name}@{ip}:{port}, 错误: {e!s}")

    def deregister_service(self, service_name: str, ip: str, port: int) -> bool:
        """注销服务。

        Args:
            service_name (str): 服务名称
            ip (str): 服务 IP
            port (int): 服务端口

        Returns:
            bool: 注销结果
        """
        try:
            service_key = self.__get_service_key(service_name, ip, port)
            # 先停止心跳
            self.__stop_heartbeat(service_name, ip, port)

            # 注销服务实例
            success = self.nacos_client.remove_naming_instance(
                service_name=service_name, ip=ip, port=port, ephemeral=True  # 必须和注册时一致
            )

            if success:
                if service_key in self.registered_services:
                    del self.registered_services[service_key]
                logger.info(f"服务注销成功: {service_name}@{ip}:{port}")
            else:
                logger.warning(f"服务注销失败: {service_name}@{ip}:{port}")
            return success

        except NacosException as e:
            logger.error(f"服务注销异常: {service_name}@{ip}:{port}, 错误: {e!s}")
            return False

    def get_service_instances(
        self, service_name: str, group_name: str = "DEFAULT_GROUP", cluster_name: str = "DEFAULT"
    ) -> list[dict]:
        """获取服务实例列表。

        Args:
            service_name (str): 服务名称
            group_name (str): 服务组。默认为 "DEFAULT_GROUP"。
            cluster_name (str): 集群名称。默认为 "DEFAULT"。

        Returns:
            list[dict]: 服务实例列表
        """
        try:
            instances = self.nacos_client.list_naming_instance(
                service_name=service_name,
                group_name=group_name,
                clusters=cluster_name,
                healthy_only=False,  # 返回所有实例（含不健康）
            )
            return instances.get("hosts", []) if instances else []
        except NacosException as e:
            logger.error(f"获取服务实例失败: {service_name}, 错误: {e!s}")
            return []

    def is_service_healthy(self, service_name: str, ip: str, port: int) -> bool:
        """检查服务实例是否健康。

        Args:
            service_name (str): 服务名称
            ip (str): 服务 IP
            port (int): 服务端口

        Returns:
            bool: 健康状态
        """
        instances = self.get_service_instances(service_name)
        for instance in instances:
            if instance.get("ip") == ip and instance.get("port") == port:
                return instance.get("healthy", False)
        logger.warning(f"未找到服务实例: {service_name}@{ip}:{port}")
        return False

    def stop_all_heartbeats(self):
        """停止所有心跳线程。"""
        self.heartbeat_running = False  # 标记心跳停止
        for service_key, thread in list(self.heartbeat_threads.items()):
            thread.join(timeout=5)
            del self.heartbeat_threads[service_key]
        logger.info("所有心跳线程已停止")

    def deregister_all_services(self):
        """注销所有已注册的服务。"""
        for service_key in list(self.registered_services.keys()):
            service_info = self.registered_services[service_key]
            self.deregister_service(service_info["service_name"], service_info["ip"], service_info["port"])
        logger.info("所有服务已注销")

    def close(self):
        """关闭 Nacos 管理器（生命周期结束时调用）。"""
        self.stop_all_heartbeats()
        self.deregister_all_services()
        logger.info("Nacos 管理器已关闭")


nacos_manager = NacosManager(
    settings.NACOS_SERVER_ADDRESSES, settings.NACOS_NAMESPACE, settings.NACOS_USERNAME, settings.NACOS_PASSWORD
)
