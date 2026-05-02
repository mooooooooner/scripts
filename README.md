# scripts

一个最小可用示例：
- `receiver.py`：HTTP 接口接收端，接收环境变量 JSON
- `sender.py`：读取指定环境变量并发送到接口

## 1. 启动接收端

```bash
python receiver.py --host 0.0.0.0 --port 8080
```

默认接口地址：`http://127.0.0.1:8080/env`

## 2. 发送指定环境变量

```bash
python sender.py --endpoint http://127.0.0.1:8080/env --keys PATH USERNAME TEMP
```

如果某些环境变量不存在，希望仍然发送一个默认值：

```bash
python sender.py --endpoint http://127.0.0.1:8080/env --keys PATH USERNAME NOT_EXIST_KEY --default-value N/A
```

参数说明：
- `--endpoint`：目标接口地址（必填）
- `--keys`：要发送的环境变量名列表（必填）
- `--timeout`：请求超时秒数（可选，默认 10）
- `--default-value`：环境变量不存在时使用的默认值（可选，不传则记录到 `missing_keys`）

## 3. 请求/响应数据结构

发送 JSON（示例）：

```json
{
  "hostname": "MY-PC",
  "sent_at": "2026-05-02T03:00:00.000000+00:00",
  "env_vars": {
    "PATH": "...",
    "USERNAME": "...",
    "NOT_EXIST_KEY": "N/A"
  },
  "missing_keys": [],
  "defaulted_keys": ["NOT_EXIST_KEY"]
}
```

接收端响应 JSON（示例）：

```json
{
  "status": "ok",
  "received_at": "2026-05-02T03:00:01.000000+00:00",
  "received_keys": ["PATH", "USERNAME"],
  "received_count": 2,
  "missing_keys": ["NOT_EXIST_KEY"],
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
python sender.py --endpoint http://127.0.0.1:8080/env --keys PATH USERNAME
```
