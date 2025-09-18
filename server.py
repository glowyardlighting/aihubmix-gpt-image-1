#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AIHubMix Image MCP Server
基于 AIHubMix API 的图像生成 MCP 服务器
"""

import asyncio
import json
import os
import sys
import io
import base64
from datetime import datetime
from typing import Any, Dict, List, Optional
import httpx
from dotenv import load_dotenv

class AIHubMixImageMCPServer:
    """AIHubMix 图像生成 MCP 服务器"""
    
    def __init__(self):
        self.api_key = os.getenv('AIHUBMIX_API_KEY')
        self.base_url = os.getenv('AIHUBMIX_BASE_URL', 'http://aihubmix.com')
        self.model = os.getenv('AIHUBMIX_MODEL', 'gpt-image-1')
        self.server_name = os.getenv('MCP_SERVER_NAME', 'aihubmix-image-mcp-server')
        
        # 图像保存目录
        self.image_save_dir = os.path.join(os.path.dirname(__file__), 'images')
        
        # 验证配置
        if not self.api_key:
            raise ValueError("AIHUBMIX_API_KEY 环境变量未设置")
        
        print(f"🚀 {self.server_name} 启动中...")
        print(f"📡 API 基础 URL: {self.base_url}")
        print(f"🎨 默认模型: {self.model}")
        print(f"💾 图像保存目录: {self.image_save_dir}")
    
    async def start(self):
        """启动 MCP 服务器"""
        print(f"✅ {self.server_name} 已启动，等待 MCP 请求...")
        
        # 测试 API 连接
        await self._test_connection()
        
        # 主循环 - 处理 MCP 请求
        while True:
            try:
                # 读取 MCP 请求
                request = await self._read_request()
                if not request:
                    continue
                
                # 处理请求
                response = await self._handle_request(request)
                
                # 发送响应
                await self._send_response(response)
                
            except KeyboardInterrupt:
                print(f"\n🛑 {self.server_name} 正在停止...")
                break
            except Exception as e:
                print(f"❌ 处理请求时出错: {e}")
                error_response = {
                    "jsonrpc": "2.0",
                    "id": request.get("id") if request else None,
                    "error": {
                        "code": -32603,
                        "message": f"内部错误: {str(e)}"
                    }
                }
                await self._send_response(error_response)
    
    async def _test_connection(self):
        """测试 API 连接"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.base_url}/v1/models",
                    headers={"Authorization": f"Bearer {self.api_key}"}
                )
                if response.status_code == 200:
                    models = response.json()
                    print(f"✅ API 连接成功，可用模型数量: {len(models.get('data', []))}")
                else:
                    print(f"⚠️ API 连接测试失败，状态码: {response.status_code}")
        except Exception as e:
            print(f"⚠️ API 连接测试失败: {e}")
    
    async def _read_request(self) -> Optional[Dict[str, Any]]:
        """读取 MCP 请求"""
        try:
            line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            if not line:
                return None
            return json.loads(line.strip())
        except Exception as e:
            print(f"❌ 读取请求失败: {e}")
            return None
    
    async def _send_response(self, response: Dict[str, Any]):
        """发送 MCP 响应"""
        try:
            print(json.dumps(response, ensure_ascii=False))
            sys.stdout.flush()
        except Exception as e:
            print(f"❌ 发送响应失败: {e}")
    
    async def _handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """处理 MCP 请求"""
        method = request.get("method")
        request_id = request.get("id")
        
        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {}
                    },
                    "serverInfo": {
                        "name": self.server_name,
                        "version": "1.0.0"
                    }
                }
            }
        
        elif method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "tools": [
                        {
                            "name": "generate_image",
                            "description": "使用 AIHubMix API 生成图像",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "prompt": {
                                        "type": "string",
                                        "description": "图像描述提示词"
                                    },
                                    "model": {
                                        "type": "string",
                                        "description": "使用的模型 (gpt-image-1)",
                                        "default": self.model
                                    },
                                    "size": {
                                        "type": "string",
                                        "description": "图像尺寸",
                                        "enum": ["256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"],
                                        "default": "1024x1024"
                                    },
                                    "n": {
                                        "type": "integer",
                                        "description": "生成图像数量 (1-10)",
                                        "minimum": 1,
                                        "maximum": 10,
                                        "default": 1
                                    },
                                    "filename": {
                                        "type": "string",
                                        "description": "输出文件名 (不含扩展名)",
                                        "default": "generated_image"
                                    }
                                },
                                "required": ["prompt"]
                            }
                        }
                    ]
                }
            }
        
        elif method == "tools/call":
            tool_name = request.get("params", {}).get("name")
            if tool_name == "generate_image":
                return await self._handle_generate_image(request)
            else:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32601,
                        "message": f"未知工具: {tool_name}"
                    }
                }
        
        else:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32601,
                    "message": f"未知方法: {method}"
                }
                }
    
    async def _handle_generate_image(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """处理图像生成请求"""
        request_id = request.get("id")
        params = request.get("params", {}).get("arguments", {})
        
        try:
            # 提取参数
            prompt = params.get("prompt")
            model = params.get("model", self.model)
            size = params.get("size", "1024x1024")
            n = params.get("n", 1)
            filename = params.get("filename", "generated_image")
            
            if not prompt:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32602,
                        "message": "缺少必需参数: prompt"
                    }
                }
            
            # 调用 AIHubMix API
            result = await self._generate_image_with_aihubmix(
                prompt=prompt,
                model=model,
                size=size,
                n=n,
                filename=filename
            )
            
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": result["message"]
                        }
                    ],
                    "isError": False
                }
            }
            
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32603,
                    "message": f"图像生成失败: {str(e)}"
                    }
                }
    
    async def _generate_image_with_aihubmix(
        self,
        prompt: str,
        model: str = "gpt-image-1",
        size: str = "1024x1024",
        n: int = 1,
        filename: str = "generated_image"
    ) -> Dict[str, Any]:
        """使用 AIHubMix API 生成图像"""
        
        # 构建请求数据
        request_data = {
            "model": model,
            "prompt": prompt,
            "size": size,
            "n": n
        }
        
        # 对于 gpt-image-1 模型，请求 base64 格式的响应
        if model == "gpt-image-1":
            request_data["response_format"] = "b64_json"
        
        print(f"🎨 正在生成图像...")
        print(f"   提示词: {prompt}")
        print(f"   模型: {model}")
        print(f"   尺寸: {size}")
        print(f"   数量: {n}")
        print(f"   响应格式: {'base64' if model == 'gpt-image-1' else 'URL'}")
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.base_url}/v1/images/generations",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    json=request_data
                )
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"✅ 图像生成成功!")
                    print(f"   创建时间: {result.get('created')}")
                    
                    # 处理生成的图像
                    saved_files = []
                    if result.get('data'):
                        for i, image_data in enumerate(result['data']):
                            if 'url' in image_data:
                                # 下载并保存图像
                                saved_file = await self._download_and_save_image(
                                    image_data['url'],
                                    filename,
                                    i
                                )
                                if saved_file:
                                    saved_files.append(saved_file)
                            elif 'b64_json' in image_data:
                                # 保存 base64 图像
                                saved_file = await self._save_base64_image(
                                    image_data['b64_json'],
                                    filename,
                                    i
                                )
                                if saved_file:
                                    saved_files.append(saved_file)
                    
                    message = f"成功生成 {len(result.get('data', []))} 张图像"
                    if saved_files:
                        message += f"，已保存到: {', '.join(saved_files)}"
                    
                    return {
                        "message": message,
                        "data": result,
                        "saved_files": saved_files
                    }
                
                elif response.status_code == 401:
                    raise Exception("API 密钥无效，请检查 AIHUBMIX_API_KEY")
                elif response.status_code == 402:
                    raise Exception("账户余额不足，请充值")
                elif response.status_code == 429:
                    raise Exception("请求频率过高，请稍后重试")
                else:
                    raise Exception(f"API 请求失败，状态码: {response.status_code}, 响应: {response.text}")
        
        except httpx.TimeoutException:
            raise Exception("请求超时，请检查网络连接")
        except httpx.ConnectError:
            raise Exception("无法连接到 AIHubMix API，请检查网络连接")
        except Exception as e:
            raise Exception(f"图像生成失败: {str(e)}")
    
    async def _download_and_save_image(self, url: str, filename: str, index: int = 0) -> Optional[str]:
        """下载并保存图像"""
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url)
                if response.status_code == 200:
                    # 确保保存目录存在
                    os.makedirs(self.image_save_dir, exist_ok=True)
                    
                    # 构建文件名
                    suffix = f"_{index}" if index > 0 else ""
                    file_path = os.path.join(self.image_save_dir, f"{filename}{suffix}.png")
                    
                    # 保存图片
                    with open(file_path, "wb") as f:
                        f.write(response.content)
                    
                    print(f"💾 图像已保存: {file_path}")
                    return file_path
                else:
                    print(f"❌ 下载图像失败，状态码: {response.status_code}")
                    return None
        except Exception as e:
            print(f"❌ 保存图像失败: {e}")
            return None
    
    async def _save_base64_image(self, b64_data: str, filename: str, index: int = 0) -> Optional[str]:
        """保存 base64 编码的图像"""
        try:
            import base64
            
            # 确保保存目录存在
            os.makedirs(self.image_save_dir, exist_ok=True)
            
            # 构建文件名
            suffix = f"_{index}" if index > 0 else ""
            file_path = os.path.join(self.image_save_dir, f"{filename}{suffix}.png")
            
            # 解码并保存 base64 图像
            image_data = base64.b64decode(b64_data)
            with open(file_path, "wb") as f:
                f.write(image_data)
            
            print(f"💾 图像已保存: {file_path}")
            return file_path
        except Exception as e:
            print(f"❌ 保存 base64 图像失败: {e}")
            return None

def main():
    # 设置控制台输出编码
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='xmlcharrefreplace')
    load_dotenv()
    server = AIHubMixImageMCPServer()
    asyncio.run(server.start())

if __name__ == "__main__":
    main()