# A股全维度数据系统 (a-share-analyst)

六层数据架构的 A 股数据采集系统，为量化分析、交易决策提供统一的命令行数据接口。

## 快速开始

```bash
# 1. 克隆
git clone https://github.com/qq1009128320-dotcom/a-share-analyst.git
cd a-share-analyst

# 2. 安装依赖 (Python >= 3.10)
pip install -r requirements.txt

# 3. 直接使用
python3 a_stock.py quote 600036 000858
```

不需要额外配置。首次运行会自动使用内置默认值。编辑 `config.yaml` 可自定义股票池和数据源。

## 六层架构

| 层级 | 命令 | 数据源 | 说明 |
|------|------|--------|------|
| 行情层 | `quote` / `kline` | 腾讯财经 → mootdx 自动降级 | 实时行情、历史K线 |
| 研报层 | `research` | akshare 东方财富 | 机构研报、评级、盈利预测 |
| 信号层 | `signal` | akshare 东方财富 | 板块资金流、概念热点、个股资金 |
| 新闻层 | `news` | akshare（财联社+东财+同花顺） | 实时电报、个股新闻、综合快讯 |
| 财务层 | `finance` | mootdx + akshare | 财务摘要、资产负债表、利润表、现金流 |
| 公告层 | `announce` | akshare 巨潮 | 定期报告披露、公告查询 |

## 命令行用法

```bash
# 实时行情（支持多个股票代码）
python3 a_stock.py quote 600036 000858 300750

# K线数据 (-p: 周期, -c: 数量)
python3 a_stock.py kline 600036 -p day -c 20

# 机构研报
python3 a_stock.py research 600036

# 市场信号（资金流 + 热点概念）
python3 a_stock.py signal

# 财经新闻
python3 a_stock.py news

# 财务数据
python3 a_stock.py finance 600036

# 公司公告
python3 a_stock.py announce 600036

# 一键监控（行情 + 研报 + 信号 + 新闻）
python3 a_stock.py monitor 600036 000858
```

股票代码前缀规则：
- `60xxxx` → 上交所主板
- `68xxxx` → 科创板
- `00xxxx` / `30xxxx` → 深交所
- `8xxxxx` / `4xxxxx` → 北交所

## 配置 (config.yaml)

```yaml
watchlist:           # 默认监控股票
  - "600036"
  - "000858"

data_sources:        # 数据源优先级
  quote: ["tencent", "mootdx"]

network:
  timeout: 10        # 请求超时(秒)
  retry: 2           # 重试次数

output:
  format: "table"    # table | json | csv
  max_rows: 30
```

修改后立即生效，无需重启。

## 作为数据源被调用

```python
import sys
sys.path.insert(0, "/path/to/a-share-analyst")

from layers.quotes import TencentQuotes
from layers.research import ResearchReports
from layers.signal import SignalScanner
from layers.news import NewsFeed
from layers.finance import FinancialData
from layers.announce import Announcements

# 行情
q = TencentQuotes()
data = q.get_quotes(["600036", "000858"])

# 研报
r = ResearchReports()
reports = r.get_reports("600036")

# 信号扫描
s = SignalScanner()
hot = s.get_hot_concepts()
flow = s.get_sector_funds()
```

## 依赖

| 包 | 版本 | 用途 |
|----|------|------|
| akshare | >=1.16.0 | 东方财富/巨潮/财联社数据 |
| mootdx | >=0.12.0 | 通达信行情（腾讯财经降级备选） |
| pandas | >=2.0 | 数据处理 |
| numpy | >=1.24 | 数值计算 |
| pyyaml | (akshare 附带) | 配置文件解析 |

## 已知问题

- **WSL 环境**：腾讯财经接口偶发超时，系统会自动降级到 mootdx
- **akshare 首次运行**：可能下载缓存数据，需等待几分钟
- **交易时段**：行情数据实时性取决于数据源刷新频率

## License

MIT
