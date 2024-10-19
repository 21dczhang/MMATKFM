import sys
from typing import List
from pathlib import Path
from maa.resource import Resource
from maa.tasker import Tasker, LoggingLevelEnum


def check(dirs: List[Path]) -> bool:
    resource = Resource()

    print(f"Checking {len(dirs)} directories...")

    for dir in dirs:
        if not dir.exists() or not dir.is_dir():
            print(f"{dir} does not exist or is not a directory.")
            return False

        print(f"Checking directory: {dir}")

        # 递归检查目录及其子目录中的所有文件和目录
        for path in dir.rglob('*'):
            print(f"Checking {path}...")
            result = resource.post_path(path).wait()
            status = result.status()
            
            # 如果状态检查失败，输出更多调试信息
            if not status.succeeded():
                print(f"Failed to check {path}. Status: {status}")
                
                # 如果有日志信息，输出日志
                if hasattr(result, 'logs'):
                    print(f"Logs for {path}:")
                    for log in result.logs:
                        print(log)
                
                return False

    print("All directories and files checked successfully.")
    return True


def main():
    if len(sys.argv) < 2:
        print("Usage: python check_resource.py <directory>")
        sys.exit(1)

    Tasker.set_stdout_level(LoggingLevelEnum.All)

    # 将命令行参数中的目录路径转为 Path 对象
    dirs = [Path(arg) for arg in sys.argv[1:]]
    
    # 执行检查，如果失败则退出状态码为1
    if not check(dirs):
        sys.exit(1)


if __name__ == "__main__":
    main()
