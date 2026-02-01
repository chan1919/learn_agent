# 环境配置指南

## 1. Python 环境设置

### 1.1 使用 pyenv 管理 Python 版本

#### 1.1.1 检查可用的 Python 版本
```powershell
pyenv versions
```

#### 1.1.2 设置本地 Python 版本
```powershell
pyenv local 3.10.11
```

#### 1.1.3 验证 Python 版本
```powershell
python --version
# 应该输出: Python 3.10.11
```

### 1.2 使用 virtualenv 创建虚拟环境

#### 1.2.1 安装 virtualenv
```powershell
pip install virtualenv
```

#### 1.2.2 创建虚拟环境
```powershell
virtualenv venv
```

#### 1.2.3 激活虚拟环境
```powershell
# Windows PowerShell
.\venv\Scripts\Activate.ps1

# Windows CMD
.\venv\Scripts\activate.bat
```

#### 1.2.4 退出虚拟环境
```powershell
deactivate
```

## 2. 安装依赖库

### 2.1 使用 requirements.txt 安装

#### 2.1.1 安装所有依赖
```powershell
pip install -r requirements.txt
```

#### 2.1.2 升级 pip
```powershell
pip install --upgrade pip
```

### 2.2 常用库的单独安装

#### 2.2.1 核心库
```powershell
pip install numpy pandas scipy
```

#### 2.2.2 机器学习库
```powershell
pip install scikit-learn tensorflow pytorch
```

#### 2.2.3 自然语言处理库
```powershell
pip install nltk spacy transformers langchain
```

#### 2.2.4 强化学习库
```powershell
pip install stable-baselines3 gymnasium
```

#### 2.2.5 Agent 相关库
```powershell
pip install autogen crewai
```

## 3. 验证安装

### 3.1 检查已安装的库
```powershell
pip list
```

### 3.2 验证核心库功能
```powershell
python -c "import numpy; print('NumPy:', numpy.__version__)"
python -c "import pandas; print('Pandas:', pandas.__version__)"
python -c "import sklearn; print('scikit-learn:', sklearn.__version__)"
python -c "import langchain; print('LangChain:', langchain.__version__)"
```

## 4. 开发工具配置

### 4.1 IDE 推荐
- **VS Code**：轻量级，插件丰富
- **PyCharm**：专业的 Python IDE
- **Jupyter Notebook**：交互式开发和实验

### 4.2 VS Code 插件
- Python
- Jupyter
- Pylance
- Black Formatter
- Flake8

### 4.3 代码风格配置

#### 4.3.1 使用 Black 格式化代码
```powershell
# 格式化单个文件
black your_file.py

# 格式化整个目录
black your_directory/
```

#### 4.3.2 使用 Flake8 检查代码风格
```powershell
flake8 your_file.py
```

## 5. 常见问题与解决方案

### 5.1 安装失败
- **问题**：依赖冲突
  **解决方案**：使用虚拟环境隔离依赖

- **问题**：网络连接问题
  **解决方案**：使用国内镜像源
  ```powershell
  pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
  ```

- **问题**：权限不足
  **解决方案**：使用管理员权限运行 PowerShell

### 5.2 版本兼容性
- **问题**：库版本不兼容
  **解决方案**：使用 requirements.txt 中指定的版本

- **问题**：Python 版本不匹配
  **解决方案**：使用 pyenv 切换到正确的 Python 版本

### 5.3 性能问题
- **问题**：安装速度慢
  **解决方案**：使用 --no-cache-dir 选项
  ```powershell
  pip install -r requirements.txt --no-cache-dir
  ```

- **问题**：运行内存不足
  **解决方案**：减少批量大小，使用更轻量级的模型

## 6. 环境验证测试

### 6.1 运行简单测试脚本
```python
# test_environment.py
import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from langchain.llms import OpenAI

# 测试 NumPy
print("Testing NumPy...")
arr = np.array([1, 2, 3, 4, 5])
print(f"NumPy array: {arr}")

# 测试 Pandas
print("\nTesting Pandas...")
df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
print(f"Pandas DataFrame:\n{df}")

# 测试 scikit-learn
print("\nTesting scikit-learn...")
iris = load_iris()
print(f"Iris dataset shape: {iris.data.shape}")

print("\nAll tests passed! Environment is ready.")
```

### 6.2 执行测试
```powershell
python test_environment.py
```

## 7. 小结

通过本指南，你应该已经成功设置了 Python 开发环境并安装了所有必要的库。现在你可以开始：

- 创建和运行简单的 Agent 示例
- 开发更复杂的 Agent 系统
- 探索各种 Agent 架构和技术

如果在环境配置过程中遇到任何问题，请参考常见问题与解决方案部分，或查阅相关库的官方文档。