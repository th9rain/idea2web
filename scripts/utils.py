"""
通用工具函数
"""

import re
import os
import sys
import json
import logging
import socket
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple


def setup_logger(name: str = "idea2web", log_file: Optional[str] = None) -> logging.Logger:
    """
    配置日志记录器

    Args:
        name: logger 名称
        log_file: 日志文件路径（可选）

    Returns:
        配置好的 logger 对象
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # 清除现有 handlers
    logger.handlers = []

    # 控制台 handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(message)s',
        datefmt='%H:%M:%S'
    )
    console_handler.setFormatter(console_format)
    logger.addHandler(console_handler)

    # 文件 handler（如果指定）
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(name)s - %(message)s'
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)

    return logger


def to_snake_case(text: str) -> str:
    """
    将字符串转换为 snake_case

    Args:
        text: 输入字符串

    Returns:
        snake_case 格式的字符串

    Examples:
        >>> to_snake_case("HelloWorld")
        'hello_world'
        >>> to_snake_case("userProfile")
        'user_profile'
    """
    # 在大写字母前添加下划线
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
    # 在小写字母和大写字母之间添加下划线
    s2 = re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1)
    return s2.lower()


def to_camel_case(text: str) -> str:
    """
    将字符串转换为 camelCase

    Args:
        text: 输入字符串（通常是 snake_case）

    Returns:
        camelCase 格式的字符串

    Examples:
        >>> to_camel_case("hello_world")
        'helloWorld'
        >>> to_camel_case("user_profile")
        'userProfile'
    """
    components = text.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def to_pascal_case(text: str) -> str:
    """
    将字符串转换为 PascalCase

    Args:
        text: 输入字符串（通常是 snake_case）

    Returns:
        PascalCase 格式的字符串

    Examples:
        >>> to_pascal_case("hello_world")
        'HelloWorld'
        >>> to_pascal_case("user_profile")
        'UserProfile'
    """
    components = text.split('_')
    return ''.join(x.title() for x in components)


def to_kebab_case(text: str) -> str:
    """
    将字符串转换为 kebab-case

    Args:
        text: 输入字符串

    Returns:
        kebab-case 格式的字符串

    Examples:
        >>> to_kebab_case("HelloWorld")
        'hello-world'
        >>> to_kebab_case("user_profile")
        'user-profile'
    """
    snake = to_snake_case(text)
    return snake.replace('_', '-')


def pluralize(word: str) -> str:
    """
    简单的英文单词复数形式转换

    Args:
        word: 单数形式的单词

    Returns:
        复数形式的单词

    Examples:
        >>> pluralize("user")
        'users'
        >>> pluralize("category")
        'categories'
        >>> pluralize("box")
        'boxes'
    """
    if word.endswith('y'):
        return word[:-1] + 'ies'
    elif word.endswith(('s', 'x', 'z', 'ch', 'sh')):
        return word + 'es'
    else:
        return word + 's'


def singularize(word: str) -> str:
    """
    将英文单词转换为单数形式（用于表名转类名）

    Args:
        word: 复数形式的单词

    Returns:
        单数形式的单词

    Examples:
        >>> singularize("users")
        'user'
        >>> singularize("categories")
        'category'
        >>> singularize("boxes")
        'box'
        >>> singularize("statuses")
        'status'
    """
    # 特殊规则：ies → y
    if word.endswith('ies') and len(word) > 3:
        return word[:-3] + 'y'  # categories → category

    # 特殊规则：ses/xes/zes → s/x/z
    if word.endswith('ses') and len(word) > 3:
        return word[:-2]  # statuses → status
    if word.endswith('xes') and len(word) > 3:
        return word[:-2]  # boxes → box
    if word.endswith('zes') and len(word) > 3:
        return word[:-2]  # quizzes → quiz

    # 特殊规则：ches/shes → ch/sh
    if word.endswith('ches') and len(word) > 4:
        return word[:-2]  # batches → batch
    if word.endswith('shes') and len(word) > 4:
        return word[:-2]  # dishes → dish

    # 一般规则：末尾 s
    if word.endswith('s') and len(word) > 1:
        return word[:-1]  # users → user

    return word


def read_json_file(file_path: str) -> Dict[str, Any]:
    """
    读取 JSON 文件

    Args:
        file_path: JSON 文件路径

    Returns:
        解析后的 JSON 数据

    Raises:
        FileNotFoundError: 文件不存在
        json.JSONDecodeError: JSON 格式错误
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"JSON 文件不存在: {file_path}")

    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def write_json_file(file_path: str, data: Dict[str, Any], indent: int = 2) -> None:
    """
    写入 JSON 文件

    Args:
        file_path: JSON 文件路径
        data: 要写入的数据
        indent: 缩进空格数
    """
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=indent, ensure_ascii=False)


def ensure_dir(directory: str) -> Path:
    """
    确保目录存在，不存在则创建

    Args:
        directory: 目录路径

    Returns:
        Path 对象
    """
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_skill_root() -> Path:
    """
    获取 skill 根目录

    Returns:
        skill 根目录的 Path 对象
    """
    # 当前文件是 scripts/utils.py，根目录是上一级
    return Path(__file__).parent.parent


def get_templates_dir() -> Path:
    """
    获取模板目录

    Returns:
        templates 目录的 Path 对象
    """
    return get_skill_root() / "templates"


def get_config_dir() -> Path:
    """
    获取配置目录

    Returns:
        config 目录的 Path 对象
    """
    return get_skill_root() / "config"


def validate_app_name(name: str) -> bool:
    """
    验证应用名称是否合法

    Args:
        name: 应用名称

    Returns:
        是否合法

    Rules:
        - 只包含字母、数字、下划线、连字符
        - 长度 1-50
        - 不以数字开头
    """
    if not name or len(name) > 50:
        return False

    if name[0].isdigit():
        return False

    pattern = r'^[a-zA-Z0-9_-]+$'
    return bool(re.match(pattern, name))


def sanitize_filename(filename: str) -> str:
    """
    清理文件名，移除不安全字符

    Args:
        filename: 原始文件名

    Returns:
        清理后的文件名
    """
    # 移除或替换不安全字符
    unsafe_chars = '<>:"/\\|?*'
    for char in unsafe_chars:
        filename = filename.replace(char, '_')

    # 移除开头和结尾的空格和点号
    filename = filename.strip('. ')

    return filename


def format_file_size(size_bytes: int) -> str:
    """
    格式化文件大小

    Args:
        size_bytes: 文件大小（字节）

    Returns:
        可读的文件大小字符串

    Examples:
        >>> format_file_size(1024)
        '1.0 KB'
        >>> format_file_size(1048576)
        '1.0 MB'
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    截断文本

    Args:
        text: 原始文本
        max_length: 最大长度
        suffix: 截断后缀

    Returns:
        截断后的文本
    """
    if len(text) <= max_length:
        return text

    return text[:max_length - len(suffix)] + suffix


def is_port_available(port: int, host: str = "127.0.0.1") -> bool:
    """
    检查端口是否可用

    Args:
        port: 端口号
        host: 主机地址，默认为 127.0.0.1

    Returns:
        是否可用
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((host, port))
            return result != 0
    except Exception:
        return False


def find_available_port(
    start_port: int,
    max_attempts: int = 50,
    host: str = "127.0.0.1"
) -> int:
    """
    在端口范围内找到可用端口

    Args:
        start_port: 起始端口
        max_attempts: 最大尝试次数
        host: 主机地址

    Returns:
        可用的端口号

    Raises:
        RuntimeError: 无法找到可用端口
    """
    for port in range(start_port, start_port + max_attempts):
        if is_port_available(port, host):
            return port

    raise RuntimeError(
        f"无法在 {start_port}-{start_port + max_attempts} 范围内找到可用端口"
    )


def allocate_ports(
    backend_start: int = 8000,
    frontend_start: int = 5173
) -> Tuple[int, int]:
    """
    为前后端分配可用端口

    Args:
        backend_start: 后端起始端口
        frontend_start: 前端起始端口

    Returns:
        (backend_port, frontend_port) 元组
    """
    backend_port = find_available_port(backend_start, max_attempts=100)
    logger.debug(f"后端端口: {backend_port}")

    # 前端端口可能与后端在同一范围，但我们会尝试从前端起始端口开始
    # 如果前端端口已被占用，我们尝试其他端口
    frontend_port = find_available_port(frontend_start, max_attempts=100)
    logger.debug(f"前端端口: {frontend_port}")

    # 确保前后端端口不同
    while frontend_port == backend_port:
        frontend_port = find_available_port(frontend_port + 1, max_attempts=10)

    return backend_port, frontend_port


def get_used_ports() -> List[int]:
    """
    获取当前系统常用的被占用端口（idea2web 可用范围）

    Returns:
        被占用且在 3000-9999 范围内的端口列表
    """
    used_ports = []

    # 常见的开发服务器端口范围
    common_ranges = [
        (3000, 3010),   # 常见前端开发服务器
        (5173, 5180),   # Vite 默认范围
        (8000, 8010),   # 常见后端开发服务器端口
    ]

    for start, end in common_ranges:
        for port in range(start, end):
            if not is_port_available(port):
                used_ports.append(port)

    return sorted(used_ports)
