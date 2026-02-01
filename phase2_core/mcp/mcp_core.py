import os
import sys
from typing import Dict, Any, Optional, List, Tuple

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from phase2_core.architectures.llm_manager import get_llm_manager, call_llm
from .tool_interface import get_tool_registry, ToolError
from .tools import initialize_tools


class MCPError(Exception):
    """
    MCP执行异常
    """
    pass


class MCP:
    """
    Master Control Program，主控程序，负责协调LLM模型和工具的调用
    """

    def __init__(self):
        """
        初始化MCP
        """
        self.llm_manager = get_llm_manager()
        self.tool_registry = get_tool_registry()
        # 初始化工具
        initialize_tools()

    def execute_task(self, task: str, context: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
        """
        执行任务

        参数:
            task: 任务描述
            context: 任务上下文
            **kwargs: 额外参数

        返回:
            执行结果字典

        异常:
            MCPError: 如果执行失败
        """
        try:
            # 1. 分析任务
            analysis_result = self.analyze_task(task, context)

            # 2. 制定执行计划
            plan = self.create_execution_plan(analysis_result)

            # 3. 执行计划
            execution_result = self.execute_plan(plan, context)

            # 4. 处理结果
            final_result = self.process_result(execution_result, context)

            return {
                "success": True,
                "result": final_result,
                "plan": plan
            }
        except Exception as e:
            raise MCPError(f"执行任务失败: {str(e)}")

    def analyze_task(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        分析任务

        参数:
            task: 任务描述
            context: 任务上下文

        返回:
            分析结果字典
        """
        # 使用LLM分析任务
        prompt = f"""
        请分析以下任务，确定需要执行的操作类型：

        任务：{task}

        上下文：{context or '无'}

        请判断这是以下哪种类型的任务：
        1. 纯LLM任务：只需要LLM生成回答，不需要调用工具
        2. 文件操作任务：需要读写文件
        3. 命令执行任务：需要执行系统命令
        4. 混合任务：需要结合LLM和工具

        请返回一个JSON对象，包含以下字段：
        - task_type: 任务类型（'llm', 'file', 'command', 'hybrid'）
        - required_tools: 需要使用的工具列表（如果不需要工具则为空列表）
        - description: 任务描述
        """

        # 调用LLM分析任务
        response = call_llm(prompt)

        # 解析LLM响应
        import json
        try:
            analysis_result = json.loads(response)
        except json.JSONDecodeError:
            # 如果LLM返回的不是有效的JSON，默认处理为纯LLM任务
            analysis_result = {
                "task_type": "llm",
                "required_tools": [],
                "description": task
            }

        return analysis_result

    def create_execution_plan(self, analysis_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        制定执行计划

        参数:
            analysis_result: 任务分析结果

        返回:
            执行计划列表
        """
        plan = []
        task_type = analysis_result.get("task_type", "llm")
        required_tools = analysis_result.get("required_tools", [])

        if task_type == "llm":
            # 纯LLM任务
            plan.append({
                "step_type": "llm",
                "description": "使用LLM生成回答"
            })
        elif task_type == "file":
            # 文件操作任务
            for tool in required_tools:
                plan.append({
                    "step_type": "tool",
                    "tool_name": tool,
                    "description": f"执行{tool}工具"
                })
            # 最后使用LLM总结结果
            plan.append({
                "step_type": "llm",
                "description": "总结执行结果"
            })
        elif task_type == "command":
            # 命令执行任务
            for tool in required_tools:
                plan.append({
                    "step_type": "tool",
                    "tool_name": tool,
                    "description": f"执行{tool}工具"
                })
            # 最后使用LLM总结结果
            plan.append({
                "step_type": "llm",
                "description": "总结执行结果"
            })
        elif task_type == "hybrid":
            # 混合任务
            # 先执行工具操作
            for tool in required_tools:
                plan.append({
                    "step_type": "tool",
                    "tool_name": tool,
                    "description": f"执行{tool}工具"
                })
            # 然后使用LLM处理结果
            plan.append({
                "step_type": "llm",
                "description": "使用LLM处理工具执行结果"
            })

        return plan

    def execute_plan(self, plan: List[Dict[str, Any]], context: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        执行计划

        参数:
            plan: 执行计划
            context: 任务上下文

        返回:
            执行结果列表
        """
        execution_results = []
        current_context = context or {}

        for step in plan:
            step_type = step.get("step_type")

            if step_type == "llm":
                # 执行LLM步骤
                result = self._execute_llm_step(step, current_context)
            elif step_type == "tool":
                # 执行工具步骤
                result = self._execute_tool_step(step, current_context)
            else:
                raise MCPError(f"未知的步骤类型: {step_type}")

            execution_results.append(result)
            # 更新上下文
            current_context["last_result"] = result

        return execution_results

    def _execute_llm_step(self, step: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行LLM步骤

        参数:
            step: 步骤信息
            context: 上下文信息

        返回:
            执行结果
        """
        # 构建LLM提示词
        prompt = self._build_llm_prompt(step, context)

        # 调用LLM
        response = call_llm(prompt)

        return {
            "step_type": "llm",
            "description": step.get("description"),
            "result": response
        }

    def _execute_tool_step(self, step: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行工具步骤

        参数:
            step: 步骤信息
            context: 上下文信息

        返回:
            执行结果
        """
        tool_name = step.get("tool_name")
        if not tool_name:
            raise MCPError("工具步骤缺少工具名称")

        # 获取工具
        try:
            tool = self.tool_registry.get_tool(tool_name)
        except ToolError as e:
            raise MCPError(f"获取工具失败: {str(e)}")

        # 生成工具执行参数
        parameters = self._generate_tool_parameters(tool, context)

        # 执行工具
        try:
            tool_result = tool.execute(**parameters)
        except Exception as e:
            raise MCPError(f"执行工具失败: {str(e)}")

        return {
            "step_type": "tool",
            "tool_name": tool_name,
            "description": step.get("description"),
            "result": tool_result
        }

    def _build_llm_prompt(self, step: Dict[str, Any], context: Dict[str, Any]) -> str:
        """
        构建LLM提示词

        参数:
            step: 步骤信息
            context: 上下文信息

        返回:
            构建好的提示词
        """
        description = step.get("description")
        last_result = context.get("last_result")

        prompt = f"""
        请根据以下信息完成任务：

        任务：{description}

        上下文信息：
        {context or '无'}

        {f"上一步执行结果：{last_result}" if last_result else ''}

        请提供详细的回答。
        """

        return prompt

    def _generate_tool_parameters(self, tool: Any, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        生成工具执行参数

        参数:
            tool: 工具实例
            context: 上下文信息

        返回:
            工具执行参数
        """
        # 获取工具参数信息
        parameters_info = tool.get_parameters()
        required_params = [param for param, info in parameters_info.items() if info.get("required", False)]

        # 使用LLM生成参数
        prompt = f"""
        请为工具 '{tool.name}' 生成执行参数。

        工具描述：{tool.description}

        必需参数：{required_params}

        参数信息：{parameters_info}

        上下文信息：{context}

        请返回一个JSON对象，包含所有必需的参数。
        """

        # 调用LLM生成参数
        response = call_llm(prompt)

        # 解析LLM响应
        import json
        try:
            parameters = json.loads(response)
        except json.JSONDecodeError:
            raise MCPError(f"无法解析LLM生成的工具参数: {response}")

        # 验证必需参数
        for param in required_params:
            if param not in parameters:
                raise MCPError(f"缺少必需的工具参数: {param}")

        return parameters

    def process_result(self, execution_results: List[Dict[str, Any]], context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        处理执行结果

        参数:
            execution_results: 执行结果列表
            context: 任务上下文

        返回:
            处理后的结果
        """
        # 构建结果摘要
        summary_prompt = f"""
        请根据以下执行结果，生成一个详细的任务完成摘要：

        执行结果：
        {execution_results}

        上下文：
        {context or '无'}

        请提供一个清晰、详细的摘要，说明任务的执行过程和结果。
        """

        # 调用LLM生成摘要
        summary = call_llm(summary_prompt)

        return {
            "summary": summary,
            "details": execution_results
        }

    def get_available_tools(self) -> List[Dict[str, Any]]:
        """
        获取所有可用的工具

        返回:
            工具信息列表
        """
        return self.tool_registry.get_tool_info_list()


# 全局MCP实例
_mcp_instance = None


def get_mcp() -> MCP:
    """
    获取全局MCP实例

    返回:
        MCP实例
    """
    global _mcp_instance
    if _mcp_instance is None:
        _mcp_instance = MCP()
    return _mcp_instance


# 便捷函数
def execute_task(task: str, context: Optional[Dict[str, Any]] = None, **kwargs) -> Dict[str, Any]:
    """
    便捷执行任务的函数

    参数:
        task: 任务描述
        context: 任务上下文
        **kwargs: 额外参数

    返回:
        执行结果

    异常:
        MCPError: 如果执行失败
    """
    return get_mcp().execute_task(task, context, **kwargs)


def get_available_tools() -> List[Dict[str, Any]]:
    """
    获取所有可用的工具

    返回:
        工具信息列表
    """
    return get_mcp().get_available_tools()
